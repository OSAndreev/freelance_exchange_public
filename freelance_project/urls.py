"""freelance_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from freelance_app.views import *
from freelance_app import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', start_page, name='start_page'),
    path('login/', views.MyprojectLoginView.as_view(), name='login_page'),
    path('register/', views.RegisterUserView.as_view(), name='register_page'),
    #path('orders/all', OrderListView.as_view()),
    #path('orders/<int:pk>', OrderRetrieveView.as_view()),
    path('customer/create_order', create_order, name='create_order'),
    path('create_user/', create_user, name='create_user'),
    path('freelancer/main_page', freelancer_main_page, name='freelancer_main_page'),
    path('customer/customer_main_page', customer_main_page, name='customer_main_page'),
    path('orders/add', add_order, name='add_order'),
    path('orders/all', OrderViewAll.as_view(), name='all_orders'),
    path('orders/update/<int:pk>', OrderUpdateView.as_view(), name='update_order'),
    re_path(r'customer/customer_main_page/order_responses/(?P<order_id>\w+)/$', order_responses, name="order_responses"),
    re_path(r'customer/customer_main_page/order_responses/.*?/(?P<pk>\w+)/$', assign_to_order),
    re_path(r'customer/customer_main_page/order_responses/.*?/(?P<pk>\w+)/remove$', remove_from_order),
    # Все нижние Никитины
    path('freelancer/main_page/chose/<int:pk>', update_offers),
    path('freelancer/main_page/my_works', freelancer_my_works, name='my_works'),
    path('freelancer/main_page/refuse/<int:pk>', refuse_offer),
    path('freelancer/main_page/my_works/save_answer/<int:pk>', freelancer_my_works),
    path('customer/customer_main_page/accept/<int:pk>', accept_order),
    path('customer/customer_main_page/rate/<int:pk>', customer_main_page),
    path('customer/customer_main_page/reject/<int:pk>', refuse_order),
    #новое
    path('customer/customer_main_page/balance', my_balance, name='my_balance_customer'),
    path('freelancer/main_page/balance', my_balance, name='my_balance_freelancer'),
    path('customer/customer_main_page/deal_history', show_deal_history),
    path('freelancer/main_page/deal_history', show_deal_history),
    path('customer/customer_main_page/delete_order/<int:pk>', delete_order)

]
