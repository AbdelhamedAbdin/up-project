from django.urls import path
from . import views


app_name = 'accounts'


urlpatterns = [
    path('profile/<slug:slug>/', views.userProfile, name="profile"),
    path('register/', views.register, name="register"),
    path('login/', views.Login.as_view(), name='login'),
    path('login/?message=user-already-activated/', views.Login.as_view(), name='login_success'),
    path('page-not-found/', views.page_not_found, name='index_404'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path("activate/<uidb64>/<token>/", views.Verification.as_view(), name="activate"),
    path("change-password/", views.PasswordChangeView.as_view(), name="change_password")
]
