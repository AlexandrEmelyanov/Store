from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('order-create/', views.OrderCreateView.as_view(), name='order_create'),
    path('', views.OrderListView.as_view(), name='orders_list'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order'),
    path('order-canceled/', views.CanceledTemplateView.as_view(), name='order_canceled'),
    path('order-success/', views.SuccessTemplateView.as_view(), name='order_success'),
]
