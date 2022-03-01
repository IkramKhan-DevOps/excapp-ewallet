from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import (
    TemplateView,
    ListView, DetailView)

from src.accounts.models import User
from src.portals.admins.filters import UserFilter
from src.portals.admins.models import Withdrawal, Transaction, TopUp

admin_decorators = [login_required, user_passes_test(lambda u: u.is_superuser)]
admin_nocache_decorators = [login_required, user_passes_test(lambda u: u.is_superuser), never_cache]


"""  INIT ------------------------------------------------------------------------- """


@method_decorator(admin_decorators, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'admins/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context


@method_decorator(admin_decorators, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'admins/user_list.html'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        filter_object = UserFilter(self.request.GET, queryset=User.objects.all())
        context['filter_form'] = filter_object.form

        paginator = Paginator(filter_object.qs, 50)
        page_number = self.request.GET.get('page')
        page_object = paginator.get_page(page_number)

        context['object_list'] = page_object
        return context


"""  WITHDRAWALS ------------------------------------------------------------------- """


@method_decorator(admin_decorators, name='dispatch')
class WithdrawalListView(ListView):
    queryset = Withdrawal.objects.all()


@method_decorator(admin_decorators, name='dispatch')
class WithdrawalDetailView(DetailView):
    model = Withdrawal


@method_decorator(admin_decorators, name='dispatch')
class WithdrawalInvoiceView(DetailView):
    model = Withdrawal
    template_name = 'customer/invoice/withdrawal_invoice.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Withdrawal.objects.all(), pk=self.kwargs['pk'])


"""  TRANSACTION ------------------------------------------------------------------- """


@method_decorator(admin_decorators, name='dispatch')
class TransactionListView(ListView):
    queryset = Transaction.objects.all()


@method_decorator(admin_decorators, name='dispatch')
class TransactionDetailView(DetailView):
    model = Transaction


@method_decorator(admin_decorators, name='dispatch')
class TransactionInvoiceView(DetailView):
    template_name = 'customer/invoice/transaction_invoice.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Transaction.objects.all().filter(status='com'), pk=self.kwargs['pk']
        )


"""  TOP UP ------------------------------------------------------------------- """


@method_decorator(admin_decorators, name='dispatch')
class TopUpListView(ListView):
    queryset = TopUp.objects.all()


@method_decorator(admin_decorators, name='dispatch')
class TopUpDetailView(DetailView):
    model = TopUp


@method_decorator(admin_decorators, name='dispatch')
class TopUpInvoiceView(DetailView):
    template_name = 'customer/invoice/topup_invoice.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            TopUp.objects.filter(status='com'), pk=self.kwargs['pk']
        )
