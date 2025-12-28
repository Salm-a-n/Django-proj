from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
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
    path("api/user_recipes/<int:recipe_id>/edit/", views.edit_user_recipe, name='edit_user_recipe'),
    path("api/delete_user_recipe/<int:recipe_id>/",views.delete_user_recipe, name='delete_user_recipe'),
    path("api/search_user_recipes/", views.search_user_recipes,name='search_user_recipes'),
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
