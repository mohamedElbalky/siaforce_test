
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from app.custom_jwt import MyTokenObtainPairView
from app .views import register_user_view

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api-auth/', include('rest_framework.urls')),
    
    path('api/user/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('api/user/register/', register_user_view, name='register'),
    
    path('api/', include('app.urls')),
]
