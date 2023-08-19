from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import PasswordChangingForm
from django.views import View
from .forms import SignupForm
from item.models import Category, Item


class index(View):
    template_name = 'core/index.html'
    def get(self, request):
        categories = Category.objects.all()
        items = Item.objects.filter(is_sold=False)[0:6]
        
        return render(request, self.template_name, {
            'categories': categories,
            'items': items,
        })


class RegisterView(View):
    template_name = 'core/signup.html'
    def get(self, request):
        form = SignupForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
        return render(request, self.template_name, {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('/login/')

@login_required
def profile(request):
    return render(request, 'core/profile.html')


class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('core:password_success')


def password_success(request):
    return render(request, "core/password_change_success.html")

