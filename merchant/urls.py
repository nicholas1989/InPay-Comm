from django.urls import path
from .import views

app_name = 'merchant'

urlpatterns = [
    path('', views.MerchantView.as_view(), name='merchant'),
    path('create/', views.ProductCreateView.as_view(), name='product-create'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<pk>/update/', views.ProductUpdateView.as_view(), name='product-update'),
    path('products/<pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),  
]

