from django.urls import path
from . import views

app_name = 'note'

urlpatterns = [
    path('', views.TransactionList.as_view(), name='transaction_list'),
    path('detail/<int:pk>/', views.TransactionDetail.as_view(), name='detail'),
    path('history_create/<int:pk>/', views.HistoryCreate.as_view(), name='history_create'),
    path('history_delete/<int:pk>/', views.HistoryDelete.as_view(), name='history_delete'),
    path('transaction_create/', views.TransactionCreate.as_view(), name='transaction_create'),
    path('transaction_update/<int:pk>/', views.TransactionUpdate.as_view(), name='transaction_update'),
    path('dashboard/', views.DashBoard.as_view(), name='dashboard'),
]
