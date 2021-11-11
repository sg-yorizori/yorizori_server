from django.urls import path
from .views import RegistrationAPI, LoginAPI, UserAPI, UserView, ProfileUpdateAPI, ProfileCreateAPI, ProfileAPI
from knox import views as knox_views

app_name = 'users'
urlpatterns = [
    path('', UserView.as_view()),  # User에 관한 API를 처리하는 view로 Request를 넘김
    path('<int:profile_id>', UserView.as_view()),

    path("register/", RegistrationAPI.as_view()),
    path("login/", LoginAPI.as_view()),
    path("logout/", knox_views.LogoutView.as_view(), name='knox_logout'),

    path("user/", UserAPI.as_view()),
    path("profile/", ProfileAPI.as_view()),
    path("profile/create", ProfileCreateAPI.as_view()),
    path('profile/update/<int:user_id>', ProfileUpdateAPI.as_view()),

]
