from django.urls import path

from app.user.views import SuperAdminSetupView, UserLogin, UserLogout, UserDetailAPI, \
    UserSetupView, UserListFilterAPI

urlpatterns = [
    # Authentication
    path('login/', UserLogin.as_view(), name='user-login'),
    path('logout/', UserLogout.as_view(), name='user-logout'),

    # Setup
    path('super-admin-setup/', SuperAdminSetupView.as_view(), name='super-admin-setup'),
    path('user-sign-up/', UserSetupView.as_view(), name='user-setup'),

    # Superadmin views
    path('<int:pk>', UserDetailAPI.as_view(), name='user-detail'),
    path('list-filter', UserListFilterAPI.as_view(), name='user-list-filter')

]
