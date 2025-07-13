from django.urls import path
from .views import *

urlpatterns = [
    path('', ad_list, name='ad_list'),
    path('ad/create/', ad_create, name='ad_create'),
    path('ad/<int:pk>/edit/', ad_edit, name='ad_edit'),
    path('ad/<int:pk>/delete/', ad_delete, name='ad_delete'),
    path('proposals/', proposal_list, name='proposal_list'),
    path('proposal/create/', proposal_create, name='proposal_create'),
    path('proposal/<int:pk>/<str:status>/', proposal_update_status, name='proposal_update_status'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]