from django.urls import path
from task_manager.statuses import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='statuses'),
    path('create/', views.StatusCreateFormView.as_view(), name='statuses_create'),
    path('<int:id>/update/', views.StatusUpdateFormView.as_view(), name='statuses_update'),
    path('<int:id>/delete/', views.StatusDeleteFormView.as_view(), name='statuses_delete'),
]
