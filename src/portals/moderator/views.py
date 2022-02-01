from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import (
    TemplateView
)

from src.accounts.decorators import moderator_required, identification_required

moderator_decorators = [moderator_required, identification_required]
moderator_nocache_decorators = [moderator_required, identification_required, never_cache]


@method_decorator(moderator_decorators, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'moderator/dashboard.html'

