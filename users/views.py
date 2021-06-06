from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetView,
    PasswordResetConfirmView, PasswordChangeView, PasswordChangeDoneView)
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView, CreateView
from django.utils.translation import gettext as _

from .forms import (RegistrationForm, ContactForm,
    ContactLogForm, FrontAuthenticationForm, FrontPasswordResetForm,
    FrontSetPasswordForm, FrontPasswordChangeForm, ProfileChangeForm,
    ProfileDeleteForm)
from .models import User, Profile

class GetMixin:

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'submitted' in request.GET:
            context['submitted'] = request.GET['submitted']
        return self.render_to_response(context)

def registration_message( username, password ):
    #TODO have some info in settings
    message = _("""
        Hello %(username)s! \n
        We have received your registration to %(site_name)s.\n
        You can login at following link: \n
        %(login)s \n
        Use the username that you chose: %(username)s
        This is the password: %(password)s (change it!).
        After login you can manage your profile.
        Thanks.
        The staff of %(site_name)s \n
        Useful links:
        Privacy agreement: %(privacy)s
        Change password: %(change_pwd)s
        """) % {'username': username, 'site_name': settings.WEBSITE_NAME,
        'login': str(settings.BASE_URL) + reverse('front_login'),
        'password': password,
        'privacy': str(settings.BASE_URL) + reverse('docs:page_list') + 'privacy/',
        'change_pwd': str(settings.BASE_URL) + reverse('password_change')}
    return message

class RegistrationFormView(GetMixin, FormView):
    form_class = RegistrationForm
    template_name = 'users/registration.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        password = User.objects.make_random_password()
        user.password = make_password(password)
        user.save()
        subject = _('Access credentials to %(acro)s') % {'acro': settings.WEBSITE_ACRO}
        body = registration_message(user.username, password)
        mailto = [ user.email, ]
        email = EmailMessage(subject, body, settings.SERVER_EMAIL, mailto)
        email.send()
        return super(RegistrationFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('registration') + '?submitted=True'

class ContactFormView(GetMixin, FormView):
    form_class = ContactForm
    template_name = 'users/message.html'

    def get_initial(self):
        initial = super(ContactFormView, self).get_initial()
        if 'subject' in self.request.GET:
            initial.update({'subject': self.request.GET['subject']})
        return initial

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return ContactLogForm
        return super(ContactFormView, self).get_form_class()

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return 'users/message_log.html'
        return super(ContactFormView, self).get_template_names()

    def form_valid(self, form):
        message = form.save(commit=False)
        if self.request.user.is_authenticated:
            message.user = self.request.user
            message.email = self.request.user.email
            if 'recipient' in self.request.GET:
                try:
                    recip = User.objects.get(username=self.request.GET['recipient'])
                    message.recipient = recip.email
                except:
                    pass
        message.save()
        if not message.recipient:
            message.recipient = settings.DEFAULT_RECIPIENT
        subject = message.subject
        msg = '%(body)s\n\n%(from)s: %(full)s (%(email)s)' % {
            'body': message.body, 'from': _('From'),
            'full': message.get_full_name(), 'email': message.get_email()}
        mailto = [message.recipient, ]
        email = EmailMessage(subject, msg, settings.SERVER_EMAIL,
            mailto)
        if message.attachment:
            email.attach_file(message.attachment.path)
        email.send()
        return super(ContactFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('contacts') + '?submitted=True'

class FrontLoginView(LoginView):
    template_name = 'users/front_login.html'
    form_class = FrontAuthenticationForm

    def get_redirect_url(self):
        """Avoid going from login to logout and other ambiguous situations"""
        redirect_to = super(FrontLoginView, self).get_redirect_url()
        if redirect_to == reverse('front_logout'):
            return reverse('profile')
        elif redirect_to == reverse('password_reset_done'):
            return reverse('profile')
        elif redirect_to == reverse('profile_deleted'):
            return reverse('profile')
        elif redirect_to == reverse('registration'):
            return reverse('profile')
        elif not redirect_to:
            return reverse('profile')
        return redirect_to

class FrontLogoutView(LogoutView):
    template_name = 'users/front_logout.html'

class FrontPasswordResetView(PasswordResetView):
    template_name = 'users/reset_password.html'
    form_class = FrontPasswordResetForm

class TemplateResetView(TemplateView):
    template_name = 'users/reset_password_done.html'

class FrontPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/reset_password_confirm.html'
    form_class = FrontSetPasswordForm

class TemplateResetDoneView(TemplateView):
    template_name = 'users/reset_done.html'

class TemplateAccountView(LoginRequiredMixin, GetMixin, TemplateView):
    template_name = 'users/account.html'

class FrontPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/password_change.html'
    form_class = FrontPasswordChangeForm

class FrontPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'

class ProfileChangeView(LoginRequiredMixin, FormView):
    form_class = ProfileChangeForm
    template_name = 'users/profile_change.html'

    def get(self, request, *args, **kwargs):
        if request.user.uuid != kwargs['pk']:
            raise Http404(_("User is not authorized to manage this profile"))
        return super(ProfileChangeView, self).get(request, *args, **kwargs)

    def get_initial(self):
        initial = super(ProfileChangeView, self).get_initial()
        usr = self.request.user
        initial.update({'first_name': usr.first_name,
            'last_name': usr.last_name,
            'email': usr.email,
            'avatar': usr.profile.avatar,
            'bio': usr.profile.bio,
            'yes_spam': usr.profile.yes_spam,
            'city_name': usr.profile.city_name,
            'lat': usr.profile.location.coords[1],
            'long': usr.profile.location.coords[0],
            'zoom': usr.profile.zoom,
            })
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile
        if profile.location.coords[0]:
            city_long = profile.location.coords[0]
            city_lat = profile.location.coords[1]
            city_zoom = profile.zoom
        else:
            city_long = settings.CITY_LONG
            city_lat = settings.CITY_LAT
            city_zoom = settings.CITY_ZOOM
        context['map_data'] = {
            'on_map_click': True,
            'on_map_zoom': True,
            'city_lat': city_lat,
            'city_long': city_long,
            'city_zoom': city_zoom,
            'mapbox_token': settings.MAPBOX_TOKEN
            }
        return context

    def form_valid(self, form):
        user = User.objects.get(uuid = self.request.user.uuid )
        profile = user.profile
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        profile.avatar = form.cleaned_data['avatar']
        profile.bio = form.cleaned_data['bio']
        profile.yes_spam = form.cleaned_data['yes_spam']
        profile.city_name = form.cleaned_data['city_name']
        profile.lat = form.cleaned_data['lat']
        profile.long = form.cleaned_data['long']
        profile.zoom = form.cleaned_data['zoom']
        user.save()
        profile.save()
        return super(ProfileChangeView, self).form_valid(form)

    def get_success_url(self):
        return (reverse('profile') +
            f'?submitted={self.request.user.get_full_name()}')

class ProfileDeleteView(LoginRequiredMixin, FormView):
    form_class = ProfileDeleteForm
    template_name = 'users/profile_delete.html'

    def get(self, request, *args, **kwargs):
        if request.user.uuid != kwargs['pk']:
            raise Http404(_("User is not authorized to manage this profile"))
        return super(ProfileDeleteView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        user = User.objects.get(uuid = self.request.user.uuid )
        user.is_active = False
        user.first_name = ''
        user.last_name = ''
        user.email = ''
        user.save()
        profile = Profile.objects.get(pk = user.uuid)
        profile.delete()
        return super(ProfileDeleteView, self).form_valid(form)

    def get_success_url(self):
        return reverse('profile_deleted')

class TemplateDeletedView(TemplateView):
    template_name = 'users/profile_deleted.html'
