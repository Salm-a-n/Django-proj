from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.urls import path
from recipe import views

urlpatterns = [
    path('',views.demo,name='demo'),
    path('adminlogin/', views.admin_login, name='admin_login'),
    path('all_user',views.users_list, name='users_list'),
    path('all_user/<int:user_id>/toggle/', views.toggle_user_status, name='toggle_user'),
    path('all_user/<int:user_id>/manage/', views.toggle_user_manage, name='toggle_user_manage'),
    
    path('all_user/<int:user_id>/recipes/', views.admin_user_recipes, name='user_recipes'),
    path('recipe_detail/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    
    path('manage/', views.manage_users, name='manage_users'),
    path('most-viewed/', views.most_viewed, name='most_viewed'),
    path('adminlogout/', views.admin_logout, name='admin_logout'),
    
#   api endpoints 
#  general 
    path('signup/', views.Signup, name='signup'),
    path('api/login/',views.api_login, name='api_login'),
    path('api/profile/',views.userProfile, name='profile'),
    path('api/change_pass/',views.chnage_password, name='change_pass'),
    # user area 
    path('api/add_recipe/',views.add_recipe, name='add_recipe'),
    path('api/user_recipes/',views.user_recipes, name='user_recipes'),
    path('api/user_recipes/<int:recipe_id>/',views.user_recipe_detail, name='user_recipe_detail'),
    path('api/user_recipes/<int:recipe_id>/edit/', views.edit_user_recipe, name='edit_user_recipe'),
    path('api/delete_user_recipe/<int:recipe_id>/',views.delete_user_recipe, name='delete_user_recipe'),
    path('api/search_user_recipes/', views.search_user_recipes,name='search_user_recipes'),
    path('api/userlogout/',views.user_logout_view,name='user_logout_view'),
    # full recipes
    path('api/full_recipes/',views.full_recipes, name='full_recipes'),
    path('api/full_recipes/<int:recipe_id>/', views.uvRecipes, name='uvRecipes'),
    path("api/search_recipes_public/", views.search_recipes_public, name='search_recipes_public'),
]

# SERVE IMAGES IN DEVELOPMENT
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
