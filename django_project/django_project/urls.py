from django.contrib import admin
from django.urls import path
from recipe import views

urlpatterns = [
    path('demo/',views.demo,name='demo'),
    path('login/', views.login, name='login'),
    path('',views.users_list, name='users_list'),
    
    path('manage/', views.manage_users, name='manage_users'),
    path('most-viewed/', views.most_viewed, name='most_viewed'),
    path('recipe_detail/', views.recipe_detail, name='recipe_detail'),
    path('user_details/', views.userlist , name='userlist'),
    path('logout/', views.logout_view, name='logout'),

]
