from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from src.accounts.forms import UserProfileForm


@method_decorator(login_required, name='dispatch')
class CrossAuthView(View):

    def get(self, request):

        if not request.user.is_completed:
            return redirect('accounts:identification-check')

        if request.user.is_superuser:
            return redirect('admin-portal:dashboard')
        elif request.user.is_student:

            # CREATE PROFILE IF NOT EXISTS
            request.user.get_student_profile()
            return redirect('student-portal:dashboard')

        elif request.user.is_parent:
            return redirect('parent-portal:dashboard')
        else:
            return redirect('moderator-portal:dashboard')


@method_decorator(login_required, name='dispatch')
class IdentificationCheckView(View):

    def get(self, request):

        # IS USER ALREADY IDENTIFIED
        if request.user.is_completed: return redirect('accounts:cross-auth-view')
        return render(request, 'accounts/identification-check.html')

    def post(self, request):

        # IF USER ALREADY IDENTIFIED
        if request.user.is_completed: return redirect('accounts:cross-auth-view')

        user_type = request.POST.get('user_type', None)

        # IF USER HAS TYPE
        if user_type is not None:
            user = request.user

            # IF USER HAS CORRECT TYPE
            if user_type == 's' or user_type == 'm' or user_type == 'p':
                if user_type == 's':
                    messages.success(request, "You are identified as Student")
                    user.is_student = True
                elif user_type == 'm':
                    messages.success(request, "You are identified as Moderator")
                    user.is_moderator = True
                else:
                    messages.success(request, "You are identified as Parent")
                    user.is_parent = True
                user.is_completed = True
                user.save()
                return redirect('accounts:cross-auth-view')
            else:
                messages.error(request, "Please provide correct user type")
        else:
            messages.error(request, "Please provide user type")

        return render(request, 'accounts/identification-check.html')


@method_decorator(login_required, name='dispatch')
class UserUpdateView(View):

    def get(self, request):
        form = UserProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, template_name='accounts/user_update_form.html', context=context)

    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            messages.success(request, "Your profile updated successfully")
            form.save(commit=True)
        context = {'form': form}
        return render(request, template_name='accounts/user_update_form.html', context=context)
