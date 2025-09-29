from django.urls import path
from .views import CreateCheckoutSession,stripe_webhook

urlpatterns = [
    path("create_checkout_session/", CreateCheckoutSession.as_view()),
   path("stripe_webhook/",stripe_webhook),
]