from django.urls import path
from .views import OrderAPIView,OrderItemAPIView

urlpatterns = [
    path('order/', OrderAPIView.as_view()),                # POST créer commande
    path('order/<int:order_id>/', OrderAPIView.as_view()), # GET commande
    path('orderitem/<int:order_id>/', OrderItemAPIView.as_view()),  # GET items de la commande

]