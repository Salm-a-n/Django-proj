from django.shortcuts import render, redirect
def login(request):
    return render(request, 'recipe/login.html')
def demo(request):
    return render(request, 'recipe/demo.html')





def users_list(request):
    return render(request, "recipe/dashboard.html")

def manage_users(request):
    return render(request, "recipe/manage_user.html")

def most_viewed(request):
    return render(request, "recipe/mostview.html")

def recipe_detail(request):
    return render(request, "recipe/recipe_view.html")

def logout_view(request):
    return redirect("users_list")
def userlist (request):
    return render(request,'recipe/user_details.html')


