from django.urls import path
from .views import CreateCheckoutSession

urlpatterns = [
    path("create_checkout_session/", CreateCheckoutSession.as_view()),
   
]