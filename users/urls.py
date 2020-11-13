from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (FrontLoginView, FrontLogoutView, FrontPasswordResetView,
    TemplateResetView, FrontPasswordResetConfirmView, TemplateResetDoneView,
    TemplateAccountView, FrontPasswordChangeView, FrontPasswordChangeDoneView,
    ProfileChangeView, ProfileDeleteView, TemplateDeletedView,
    RegistrationFormView)

#app_name = 'account'
urlpatterns = [
    path(_('profile/'), TemplateAccountView.as_view(),
        name='profile'),
    path(_('profile/<uuid:pk>/change'), ProfileChangeView.as_view(),
        name='profile_change'),
    path(_('profile/<uuid:pk>/delete'), ProfileDeleteView.as_view(),
        name='profile_delete'),
    path(_('profile/deleted'), TemplateDeletedView.as_view(),
        name='profile_deleted'),
    path(_('registration/'), RegistrationFormView.as_view(),
        name='registration'),
    path(_('login/'), FrontLoginView.as_view(),
        name='front_login'),
    path(_('logout/'), FrontLogoutView.as_view(),
        name='front_logout'),
    path(_('password_reset/'), FrontPasswordResetView.as_view(),
        name='front_password_reset'),
    path(_('password_reset/done/'), TemplateResetView.as_view(),
        name='password_reset_done'),
    path(_('reset/<uidb64>/<token>/'), FrontPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    path(_('reset/done/'), TemplateResetDoneView.as_view(),
        name='password_reset_complete'),
    path(_('password_change/'), FrontPasswordChangeView.as_view(),
        name='password_change'),
    path(_('password_change_done/'), FrontPasswordChangeDoneView.as_view(),
        name='password_change_done'),
    ]
