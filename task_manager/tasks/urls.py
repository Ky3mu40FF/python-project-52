from django.urls import path
from task_manager.tasks import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='tasks'),
    path('create/', views.TaskCreateFormView.as_view(), name='tasks_create'),
    path('<int:id>/update/', views.TaskUpdateFormView.as_view(), name='tasks_update'),
    path('<int:id>/delete/', views.TaskDeleteFormView.as_view(), name='tasks_delete'),
    path('<int:id>/', views.TaskDetailsView.as_view(), name='tasks_details'),
]