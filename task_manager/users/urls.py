from django.urls import path
from task_manager.users import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='users'),
    path('create/', views.UserCreationFormView.as_view(), name='users_create'),
    path('<int:id>/update/', views.UserChangeFormView.as_view(), name='users_update'),
    path('<int:id>/delete/', views.UserDeleteFormView.as_view(), name='users_delete'),
    path('login/', views.UserAuthenticationFormView.as_view(), name='users_login'),
    path('logout/', views.UserLogOutView.as_view(), name='users_logout'),
]
