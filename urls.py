
from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RegistrationView,PasswordView,ChangeProfileForAdminView,DisplayCountryView,DisplayStateView,ResetPasswordRequestToken,ResetPasswordConfirm,ChangePasswordView,employee_csvupload_ViewSet

router = DefaultRouter()
router.register(r'register', RegistrationView, basename='registrations')
router.register(r'empcsvupload', employee_csvupload_ViewSet, basename='empcsvupload')
router.register(r'changeprofile', ChangeProfileForAdminView, basename='ChangeProfileForAdminView')
router.register(r'country', DisplayCountryView, basename='DisplayCountryView')
router.register(r'state', DisplayStateView, basename='DisplayStateView')

urlpatterns = [
    path('', include(router.urls)),
    path('set-password', PasswordView.as_view(), name="PasswordView"),
    path('recovery', ResetPasswordRequestToken.as_view(), name="recovery"),
    path('resetpassword', ResetPasswordConfirm.as_view(), name="resetpassword"),
    path('changepassword', ChangePasswordView.as_view(), name="changepassword")
    
]
