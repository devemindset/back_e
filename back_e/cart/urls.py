from django.urls import path
from .views import CartAPIView,CartItemAPIView

urlpatterns = [
    path('cart/', CartAPIView.as_view()),                  # POST créer panier
    path('cart/<int:cart_id>/', CartAPIView.as_view()),    # GET panier
    path('cartitem/', CartItemAPIView.as_view()),          # POST ajouter item
    path('cartitem/<int:cart_id>/', CartItemAPIView.as_view()),  # GET items du panier

]
