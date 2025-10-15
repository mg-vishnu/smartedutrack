from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from accounts import views  
from .views import PasswordResetRequestView, PasswordResetConfirmView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path('create-teacher-parent/', views.CreateTeacherParentView.as_view(), name='create-teacher-parent'),
    path("login/", csrf_exempt(views.SessionLoginView.as_view()), name="session-login"),
    path("logout/", views.SessionLogoutView.as_view(), name="session-logout"),
     path("password-reset/", PasswordResetRequestView.as_view(), name="password-reset-request"),
    path("password-reset-confirm/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path('gettoken/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(),name='token_Verify'),
]


