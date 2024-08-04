"""
URL configuration for assetshare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from asset import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # home
    path('', views.home, name="home"),

    # additem
    path('requestpost/', views.requestpost, name="requestpost"),
    path('viewpostrequest/', views.view_request_post, name="view_request_post"),
    path('approve_item/<int:item_id>/', views.approve_item, name='approve_item'),

    # request item
    path('request_item/<int:item_id>/', views.request_item, name='request_item'),
    path('viewinterestrequest/', views.view_request_item, name="view_request_item"),
    path('approve_request/<int:interest_id>/', views.approve_request, name='approve_request'),

    #approved
    path('view_interests/', views.view_interests, name='view_interests'),
    path('approve_interest/<int:interest_id>/', views.approve_interest, name='approve_interest'),

    #finance
    path('view_interests_finance/', views.view_interests_finance, name='view_interests_finance'),
    path('approve_interest_finance/<int:interest_id>/', views.approve_interest_finance, name='approve_interest_finance'),
    path('reject_interest_finance/<int:interest_id>/', views.reject_interest_finance, name='reject_interest_finance'),

    path('display/', views.displaysent, name='displaysent'),
    path('displayreceived/', views.displayreceived, name='displayreceived'),

    #auth
    path('login',views.loginuser,name='login'),
    path('logout',views.logoutuser,name='logout'),

    path('search-products/', views.search_products, name='search_products'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
