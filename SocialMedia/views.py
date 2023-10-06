from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm,PostForm
from .models import Profile,Post,LikePost
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
import random


@login_required(login_url='login')
def follow_profile(request, profile_id):
    profile_to_follow = Profile.objects.get(pk=profile_id)
    current_profile = request.user.profile
    if request.method == "POST":
        action = request.POST['follow']
        if action == 'follow':
            current_profile.follows.add(profile_to_follow)
    current_profile.save() 
    return redirect('index')  # Redirect back to the index page after following/unfollowing



@login_required(login_url='login')
def index(request):
    form = PostForm(request.POST or None, request.FILES or None)
    
    if request.method == "POST":
        if form.is_valid():
            post_form = form.save(commit=False)
            post_form.user = request.user
            post_form.save()
            return redirect("/")

    profiles_not_following = Profile.objects.exclude(user__profile__in=request.user.profile.follows.all())
    followed_posts = Post.objects.filter(user__profile__in=request.user.profile.follows.all()).order_by("-created_at")

    # Shuffle the list of profiles and select the first 4
    shuffled_profiles = list(profiles_not_following)
    random.shuffle(shuffled_profiles)
    random_profiles = shuffled_profiles[:4]

    context = {
        'form': form,
        'posts': followed_posts,
        'random_profiles': random_profiles,  # Pass the random profiles to the template
    }

    return render(request, 'index.html', context)



@login_required(login_url='login')
def settings(request):
  profile_user = Profile.objects.get(user=request.user)
  form = ProfileForm(request.POST or None,request.FILES or None,instance=profile_user)
  if request.method=="POST":
      if form.is_valid():
          form.save()
          return redirect('settings')
  return render(request,'setting.html',{"form":form,"profile_user":profile_user})

@login_required(login_url='login')
def search(request):
    if 'q' in request.GET:
        query = request.GET['q']
        if query:
            results = Profile.objects.filter(
                Q(user__username__icontains=query) # Search by username      
            )
            context = {
                'query': query,
                'results': results,
            }
            return render(request, 'search.html', context)
    return render(request, 'search.html')
      
      
@login_required(login_url="login") 
def profile(request,pk):
  if request.user.is_authenticated:
      profile = Profile.objects.get(id=pk)
      
      if request.method == "POST":
         action = request.POST['follow']
         current_profile = request.user.profile

         if action == "unfollow":
            current_profile.follows.remove(profile)
         elif action == "follow":
            current_profile.follows.add(profile)
         current_profile.save()
         return redirect("profile",pk=profile.id)
      
         
      context = {
          'profile':profile,
      }
      return render(request,"profile.html",context)
  else:
      messages.success(request,("You Must Be Logged In To View This Page..."))
      return redirect("/")
  
@login_required(login_url='login')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get("post_id")

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id,username=username).first()
    
    if like_filter == None:
        new_like =LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')
    
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password == password1:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username is taken")
                return redirect("register")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                #Log in the user and redirect to settings
                user = auth.authenticate(username=username,password=password)
                auth.login(request,user)
                #Log in the user and redirect to settings
                return redirect("settings")
        else:
            messages.error(request, "Passwords do not match")
            return redirect('register')
    return render(request, "signup.html")

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password =request.POST['password']

        user = auth.authenticate(username=username,password=password)


        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            messages.error(request,"Credentials Invalid")
            return redirect("login")
    return render(request,'signin.html')




@login_required(login_url='login')
def delete(request, post_id):
    # Retrieve the post based on the post_id
    post = get_object_or_404(Post, id=post_id)

    # Check if the logged-in user is the owner of the post
    if request.user == post.user:
        # Delete the post
        post.delete()
        # Redirect to the index page or any other appropriate page
        return redirect('/')
    else:

        return redirect('/')
