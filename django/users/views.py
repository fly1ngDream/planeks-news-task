from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import Group
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render


from .forms import CustomUserCreateForm
from .tokens import account_activation_token
from users.models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'signup.djhtml'
    success_message = 'Account was successfully created!'


    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            ordinary_users_group = Group.objects.get(name='ordinary_users')
            ordinary_users_group.user_set.add(user)

            form.instance.is_active = False
            current_site = get_current_site(self.request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.djhtml', {
                'user': user,
                'domain': current_site.domain,
                'pk': user.pk,
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(self.request, 'acc_active.djhtml')
        return super().form_valid(form)


def activate(request, pk, token):
    try:
        user = CustomUser.objects.get(pk=pk)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'acc_active_done.djhtml')
    else:
        return HttpResponse('Activation link is invalid!')
