from django.urls import path
from task_manager.labels import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='labels'),
    path('create/', views.LabelCreateFormView.as_view(), name='labels_create'),
    path('<int:id>/update/', views.LabelUpdateFormView.as_view(), name='labels_update'),
    path('<int:id>/delete/', views.LabelDeleteFormView.as_view(), name='labels_delete'),
]
