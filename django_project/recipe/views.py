#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>BACKEND VIEWS>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import get_user_model
from .models import Recipe
User = get_user_model()

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> API VIEWS>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import  HTTP_200_OK, HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND,HTTP_403_FORBIDDEN,HTTP_400_BAD_REQUEST
from django.http import JsonResponse
from .models import User,Recipe

# direct actions 
def demo(request):
    return render(request, 'recipe/demo.html')

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid() and form.get_user().is_admin:
            user = form.get_user()
            auth_login(request, user)
            return redirect('/all_user')
        elif form.is_valid():
            messages.error(request, "You are not authorized to login Only admin can login here.")
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'recipe/login.html', {'form': form})
@login_required
def admin_logout(request):
    logout(request)
    return redirect('/adminlogin/') 


@never_cache
@login_required
def users_list(request):
    search_query = request.GET.get("q", "").strip()

    users = User.objects.filter(is_admin=False)

    if search_query:
        users = users.filter(name__icontains=search_query)

    paginator = Paginator(users, 5)  
    page_number = request.GET.get("page")
    users_page = paginator.get_page(page_number)

    return render(request, 'recipe/user_list.html', {
        'users': users_page,
        'search_query': search_query
    })
@login_required
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id, is_admin=False)
    user.is_active = not user.is_active
    user.save()
    return redirect('users_list')

@login_required
def toggle_user_manage(request, user_id):
    user = get_object_or_404(User, id=user_id, is_admin=False)
    user.is_active = not user.is_active
    user.save()
    return redirect(request.META.get("HTTP_REFERER", "manage_users"))


@login_required
def admin_user_recipes(request, user_id):
    user = get_object_or_404(User, id=user_id, is_admin=False)
    recipes_qs = Recipe.objects.filter(shef=user).order_by("-id")

    paginator = Paginator(recipes_qs, 2)  
    page_number = request.GET.get("page")
    recipes_page = paginator.get_page(page_number)

    return render(
        request,
        "recipe/user_details.html",
        {
            "user": user,
            "recipes": recipes_page,
        }
    )

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    next_url = request.GET.get("next")

    return render(
        request,
        "recipe/recipe_view.html",
        {
            "recipe": recipe,
            "next_url": next_url
        }
    )


@never_cache
@login_required
def manage_users(request):
    search_query = request.GET.get("q", "").strip()

    users = User.objects.filter(is_active=False)

    if search_query:
        users = users.filter(email__icontains=search_query)

    paginator = Paginator(users, 5)
    page_number = request.GET.get("page")
    users_page = paginator.get_page(page_number)

    return render(request, "recipe/manage_user.html", {
        "users": users_page,
        "search_query": search_query
    })


@login_required
def most_viewed(request):
    search_query = request.GET.get("q", "").strip()
    recipes = Recipe.objects.all().order_by('-views')
    if search_query:
        recipes = recipes.filter(title__icontains=search_query)
    paginator = Paginator(recipes, 5)
    page_number = request.GET.get("page")
    recipes_page = paginator.get_page(page_number)

    return render(request, "recipe/mostview.html", {
        "recipes": recipes_page,
        "search_query": search_query
    })




# api actions

@api_view(['POST'])
@permission_classes((AllowAny,))

def Signup(request):
        email  = request.data.get("email")
        password = request.data.get("password")
        name = request.data.get("name")
        if not name or not email or not password:
            return Response({'message':'All fields are required'})
        if len(password) < 8:
            return Response(
                {"message": "Password must be at least 8 characters long"},
                status=HTTP_400_BAD_REQUEST
        )
        if User.objects.filter(email=email).exists():
            return  JsonResponse({'message':'Email already exist'})
        user = User.objects.create_user(email=email,password=password)
        user.name = name
        user.save()
        return JsonResponse({'message':'user created successsfully'} ,status = 200)    
    
    #api login
    
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def api_login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if not email or not password:
        return Response(
            {'error': 'Please provide both email and password'},
            status=HTTP_400_BAD_REQUEST
        )
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid email or password'},
            status=HTTP_401_UNAUTHORIZED
        )
    if not user.is_active:
        return Response(
            {'error': 'Your account is blocked. Please contact admin.'},
            status=HTTP_403_FORBIDDEN
        )
    if not check_password(password, user.password):
        return Response(
            {'error': 'Invalid email or password'},
            status=HTTP_401_UNAUTHORIZED
        )
    token, _ = Token.objects.get_or_create(user=user)
    return Response(
        {'token': token.key},status=HTTP_200_OK)
    
    
    

# profile view
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def userProfile(request):
    user=request.user
    profile_data={
        'name':user.name,
        'email':user.email,
        # 'password':user.password,
    }
    return Response(profile_data , status=HTTP_200_OK)

# profile password change
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def chnage_password(request):
    user=request.user
    old_password=request.data.get("old_password")
    new_password=request.data.get("new_password")
    if not user.check_password(old_password):
        return Response({"message":"Old password is incorret"}, status=HTTP_400_BAD_REQUEST)
    user.set_password(new_password)
    user.save()
    return Response({"message":"Password changed successfully"},status=HTTP_200_OK)

# add recipe (user)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_recipe(request):
    user=request.user
    title=request.data.get("title")
    ingredients=request.data.get("ingredients")
    steps=request.data.get("steps")
    time=request.data.get("time")
    difficulty=request.data.get("difficulty")
    image=request.FILES.get("image")
    user_recipe=Recipe.objects.create(
        title=title,
        shef=user,
        ingredients=ingredients,
        steps=steps,
        time=time,
        difficulty=difficulty,
        image=image
    )
    return Response({"message":"Recipe added Succeffully"},status=HTTP_200_OK)

# user recipes api
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_recipes(request):
    user = request.user
    recipes = Recipe.objects.filter(shef=user)
    recipe_list = []
    for recipe in recipes:
        recipe_list.append({
            'id': recipe.id,
            'title': recipe.title,
            # 'ingredients': recipe.ingredients,
            # 'steps': recipe.steps,
            'time': recipe.time,
            # 'difficulty': recipe.difficulty,
            "image": request.build_absolute_uri(recipe.image.url) if recipe.image else None,
            'views': recipe.views
        })
    return Response({'recipes': recipe_list}, status=HTTP_200_OK)

# usre own recipes
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_recipe_detail(request, recipe_id):
    user = request.user
    try:
        recipe = Recipe.objects.get(id=recipe_id, shef=user)
    except Recipe.DoesNotExist:
        return Response({"error": "Recipe not found"}, status=HTTP_404_NOT_FOUND)

    data = {
        "id": recipe.id,
        "title": recipe.title,
        "ingredients": recipe.ingredients,
        "steps": recipe.steps,
        "time": recipe.time,
        "difficulty": recipe.difficulty,
        "image": recipe.image.url if recipe.image else None,
        "views": recipe.views,
        "created_at": recipe.created_at,
    }
    return Response(data, status=HTTP_200_OK)

# user recipe edit 
@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def edit_user_recipe(request, recipe_id):
    user = request.user
    try:
        recipe = Recipe.objects.get(id=recipe_id, shef=user)
    except Recipe.DoesNotExist:
        return Response({"error": "Recipe not found"}, status=HTTP_404_NOT_FOUND)
    
    recipe.title = request.data.get("title", recipe.title)
    recipe.ingredients = request.data.get("ingredients", recipe.ingredients)
    recipe.steps = request.data.get("steps", recipe.steps)
    recipe.time = request.data.get("time", recipe.time)
    recipe.difficulty = request.data.get("difficulty", recipe.difficulty)
    if "image" in request.FILES:
        recipe.image = request.FILES["image"]

    recipe.save()

    return Response({"message": "Recipe updated successfully"}, status=HTTP_200_OK)

#public recipe api (all recipes)
@api_view(["GET"])
@permission_classes([AllowAny])
def full_recipes(request):
    recipes=Recipe.objects.all()
    recipe_list=[]
    for recipe in recipes:
        recipe_list.append({
            'id': recipe.id,
            'title': recipe.title,
            'shef': recipe.shef.name,
            'time': recipe.time,
           'image': request.build_absolute_uri(recipe.image.url) if recipe.image else None,# to genetare the path 
            'views': recipe.views
        })
    return Response({'recipes':recipe_list},status=HTTP_200_OK)

# public view recipe(individual api)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def uvRecipes(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        return Response({"error": "Recipe not found"}, status=HTTP_404_NOT_FOUND)

    user = request.user
    if user != recipe.shef:
        recipe.views += 1
        recipe.save()

    recipe_data = {
        'id': recipe.id,
        'title': recipe.title,
        'shef': recipe.shef.name, 
        'ingredients': recipe.ingredients,
        'steps': recipe.steps,
        'time': recipe.time,
        'difficulty': recipe.difficulty,
        'image': recipe.image.url if recipe.image else None,
        'views': recipe.views,
        'created_at': recipe.created_at
    }
    return Response(recipe_data, status=HTTP_200_OK)


#all user serach 
@api_view(["GET"])
@permission_classes([AllowAny])
def search_recipes_public(request):
    title_query = request.GET.get("title", None)
    if not title_query:
        return Response({"error": "PLease enter something"}, status=400)
    recipes = Recipe.objects.filter(title__icontains=title_query)
    if not recipes.exists(): 
        return Response({"error": "No recipes found"}, status=404)


    recipe_list = []
    for recipe in recipes:
        recipe_list.append({
            "id": recipe.id,
            "title": recipe.title,
            "shef": recipe.shef.name,
            "time": recipe.time,
             'image': request.build_absolute_uri(recipe.image.url) if recipe.image else None,
            "views": recipe.views,
        })

    return Response({"recipes": recipe_list}, status=HTTP_200_OK)

# shef/ user search in my list
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_user_recipes(request):
    user = request.user
    title_query = request.GET.get("title", "")
    if not title_query:
        return Response({"error": "Enter a recipe name "}, status=400)
    recipes = Recipe.objects.filter(shef=user, title__icontains=title_query)
    if not recipes.exists():
        return Response({"error": "No recipes found"}, status=404)

    recipe_list = []
    for recipe in recipes:
        recipe_list.append({
            "id": recipe.id,
            "title": recipe.title,
            "time": recipe.time,
            'image': request.build_absolute_uri(recipe.image.url) if recipe.image else None,
            "views": recipe.views,
        })

    return Response({"recipes": recipe_list}, status=HTTP_200_OK)

#deleting the ecipe

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user_recipe(request, recipe_id):
    user = request.user
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        return Response({"error": "Recipe not found"}, status=HTTP_404_NOT_FOUND)
    if recipe.shef != user:
        return Response({"error": "You are not allowed to delete this recipe"}, status=HTTP_403_FORBIDDEN)
    recipe.delete()
    return Response({"message": "Recipe deleted successfully"}, status=HTTP_200_OK)

# api logout
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_logout_view(request):
    request.user.auth_token.delete()
    return Response(
        {"message": "Logged out successfully"},
        status=HTTP_200_OK
    )
