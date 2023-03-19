from django.urls import path
from task_manager.labels import views

urlpatterns = [
    path('', views.LabelsListView.as_view(), name='labels'),
    path('create/', views.LabelCreateFormView.as_view(), name='labels_create'),
    path('<int:pk>/update/', views.LabelUpdateFormView.as_view(), name='labels_update'),
    path('<int:pk>/delete/', views.LabelDeleteFormView.as_view(), name='labels_delete'),
]
