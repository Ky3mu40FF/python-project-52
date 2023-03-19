from django.urls import path
from task_manager.users import views

urlpatterns = [
    path('', views.UsersListView.as_view(), name='users'),
    path('create/', views.UserCreationFormView.as_view(), name='users_create'),
    path('<int:pk>/update/', views.UserUpdateFormView.as_view(), name='users_update'),
    path('<int:pk>/delete/', views.UserDeleteFormView.as_view(), name='users_delete'),
    path('login/', views.UserAuthenticationFormView.as_view(), name='login'),
    path('logout/', views.UserLogOutView.as_view(), name='logout'),
]
