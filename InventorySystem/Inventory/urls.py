from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = "invent"

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),

    # User paths
    path('registration/', views.registration, name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='inventorySystem/login.html'), name='login'),
    path('account/', auth_views.LoginView.as_view(template_name='inventorySystem/account.html'), name='account'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('invent:login')), name='logout'),

    #Forgotten password path
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password/password_reset_complete.html'), name='password_reset_complete'),

    # Product paths
    path('list/', views.inventory_list, name='list'),
    path('add/', views.add_product, name='add_new_product'),
    path('update/<int:pk>', views.update_product, name='update_product'),
    path('delete/<int:pk>', views.delete_product, name='delete_product'),
    path('info/<int:pk>', views.product_info, name='product_info'),
]
