from django.urls import path
from .views import purchase_subscription
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path(
        '<slug:category_slug>/',
        views.product_list,
        name='product_list_by_category',
    ),
    path(
        '<int:id>/<slug:slug>/',
        views.product_detail,
        name='product_detail',
    ),
    path('purchase_subscription/', purchase_subscription, name='purchase_subscription'),
]