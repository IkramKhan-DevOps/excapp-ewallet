from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import (
    TemplateView, ListView, DetailView, UpdateView,
    CreateView
)

from src.accounts.models import User
from src.portals.admins.filters import UserFilter
from src.portals.admins.models import Withdrawal, Transaction, TopUp, Ticket

admin_decorators = [login_required, user_passes_test(lambda u: u.is_superuser)]
admin_nocache_decorators = [login_required, user_passes_test(lambda u: u.is_superuser), never_cache]


"""  INIT ------------------------------------------------------------------------- """


@method_decorator(admin_decorators, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'admins/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        # TODO:: statistics implementation required ----------------------------------------------------------
        transaction_statistics = Transaction.objects.filter(status='com').aggregate(Sum('total'), Count('pk'))
        top_up_statistics = TopUp.objects.filter(status='com').aggregate(Sum('total'), Count('pk'))
        withdrawal_statistics = Withdrawal.objects.filter(status='com').aggregate(Sum('total'), Count('pk'))

        context['total_transactions_amount'] = Transaction.objects.filter(status='com').count()
        context['total_transactions_count'] = Transaction.objects.filter(status='com').count()
        context['total_top_up_amount'] = TopUp.objects.filter(status='com').count()
        context['total_top_up_count'] = TopUp.objects.filter(status='com').count()
        context['total_withdrawal_amount'] = Withdrawal.objects.filter(status='com').count()
        context['total_withdrawal_count'] = Withdrawal.objects.filter(status='com').count()
        # ----------------------------------------------------------------------------------------------------

        context['transactions_list'] = Transaction.objects.filter()[:10]
        context['top_up_list'] = TopUp.objects.all()[:10]
        context['withdrawal_list'] = Withdrawal.objects.all()[:10]
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


@method_decorator(admin_decorators, name='dispatch')
class UserDetailView(DetailView):
    model = User
    template_name = 'admins/user_detail.html'

    def get_context_data(self, **kwargs):

        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs['pk'])

        context['top_up'] = TopUp.objects.filter(wallet__user=user)
        context['transaction'] = Transaction.objects.filter(
            Q(sender_wallet__user=user) | Q(receiver_wallet__user=user)
        )
        context['withdrawal'] = Withdrawal.objects.filter(wallet__user=user)
        return context


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = [
        'profile_image', 'first_name', 'last_name', 'username',
        'email', 'gender', 'about', 'address', 'phone_number', 'is_customer', 'is_active'
    ]
    template_name = 'admins/user_form.html'

    def get_success_url(self):
        return reverse('admins-portal:user-detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required, name='dispatch')
class UserPasswordResetView(View):

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = AdminPasswordChangeForm(user=user)
        return render(request, 'admins/user_password_reset.html', {'form': form})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = AdminPasswordChangeForm(data=request.POST, user=user)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, f"{user.get_full_name()}'s password changed successfully.")
        return render(request, 'admins/user_password_reset.html', {'form': form})


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


""" -------------------------------------------------------------------------- """


@method_decorator(admin_decorators, name='dispatch')
class TicketListView(ListView):
    paginate_by = 25
    queryset = Ticket.objects.all()


@method_decorator(admin_decorators, name='dispatch')
class TicketDetailView(DetailView):
    model = Ticket


@method_decorator(admin_decorators, name='dispatch')
class TicketStatusChangeView(View):

    def get(self, request, pk,  *args, **kwargs):
        ticket = Ticket.objects.get(pk=pk)
        if ticket.is_completed:
            messages.success(request, f"ID {ticket.pk} has re-opened and case has been marked as unresolved")
            ticket.is_completed = False
        else:
            messages.success(request, f"ID {ticket.pk} has been closed and case has been marked as resolved")
            ticket.is_completed = True
        ticket.save()
        return redirect('admin-portal:ticket-detail', ticket.pk)
