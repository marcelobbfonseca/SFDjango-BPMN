from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from .views import (DashboardView, _PasswordChangeView, _PasswordChangeDoneView, _PasswordResetView,
    _PasswordResetDoneView, _PasswordResetConfirmView, _PasswordResetCompleteView,
    CreateUser, UserCreated, UsersView, UpdateUser, UsersView, GroupsView, CreateGroup, GroupUpdate)


urlpatterns = [
    path('entrar/', LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path('sair/', LogoutView.as_view(template_name='accounts/logout.html'), name="logout"),
    path('painel/', DashboardView.as_view(), name='dashboard'),
    path('alterar-senha/', _PasswordChangeView.as_view(), name='edit_password'),
    path('alterar-senha/senha-alterada-com-sucesso', _PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('nova-senha/', _PasswordResetView.as_view(), name='password_reset'),
    path('nova-senha/nova-senha-solicitada', _PasswordResetDoneView.as_view()),
    path('confirmar-nova-senha/<uidb64>/<token>', _PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('confirmar-nova-senha/<uidb64>/senha-redefinida-com-sucesso', _PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('novo-usuario/', CreateUser.as_view(), name='new_user'),
    path('novo-usuario/usuario-inserido-com-sucesso', UserCreated.as_view()),
    path('atualizar-usuario/<int:pk>/', UpdateUser, name='update_user'),
    path('usuarios/', UsersView.as_view(), name='users'),
    path('grupos/', GroupsView.as_view(), name='groups'),
    path('novo_grupo/', CreateGroup.as_view(), name='new_group'),
    path('atualizar_grupo/<int:pk>/', GroupUpdate.as_view(), name='update_group'),
 ]
