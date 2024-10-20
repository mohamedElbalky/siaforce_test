from django.urls import path


from .views import get_credentials

urlpatterns = [
    path('credentials/', get_credentials, name='get_credentials'),
]