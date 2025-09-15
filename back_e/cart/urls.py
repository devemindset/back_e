from django.urls import path
from .views import CartAPIView,CartItemAPIView

urlpatterns = [
    path('create_cart/', CartAPIView.as_view()),                  # POST créer panier
    path('create_cartitem/', CartItemAPIView.as_view()),          # POST ajouter item
    path('<str:session_id>/', CartAPIView.as_view()),    # GET panier
    # path('cartitem/<int:cart_id>/', CartItemAPIView.as_view()),  # GET items du panier
    path('cartitem/<int:cart_item_id>/', CartItemAPIView.as_view()),  # DELETE items du panier

]
