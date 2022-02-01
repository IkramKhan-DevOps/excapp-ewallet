
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from src.accounts.decorators import identification_required, student_required
User = get_user_model()

student_decorators = [login_required, identification_required, student_required]
student_nocache_decorators = [login_required, identification_required, student_required, never_cache]

"""  VIEWS ================================================================================= """


@method_decorator(student_decorators, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'student/dashboard.html'
