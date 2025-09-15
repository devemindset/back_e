from django.urls import path
from .views import ProductListAPIView,ProductDetailAPIView,ProductCategoryDetailAPIView


urlpatterns = [
      path('product_list/', ProductListAPIView.as_view()),
      path('detail/<slug:slug>/', ProductDetailAPIView.as_view(), name='product-detail'),
      path('product_categories/<slug:slug>/', ProductCategoryDetailAPIView.as_view(), name='product-category-detail'),
]
