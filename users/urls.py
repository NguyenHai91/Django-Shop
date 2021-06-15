from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import GetUserView, RegisterView, MyTokenObtainPairView

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('register/', RegisterView.as_view()),
    path('get_user/', GetUserView.as_view()),
]
