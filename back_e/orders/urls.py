from django.urls import path
from .views import OrderAPIView,OrderItemAPIView

urlpatterns = [
    path('create_order/', OrderAPIView.as_view()),                # POST créer commande
    path('<int:order_id>/', OrderAPIView.as_view()), # GET commande
    path('orderitem/<int:order_id>/', OrderItemAPIView.as_view()),  # GET items de la commande

]