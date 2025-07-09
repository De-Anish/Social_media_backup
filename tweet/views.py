from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Tweet, Follower, UserProfile, Like, Comment
from .forms import tweetform, UserProfileForm
import random
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import JsonResponse

# Create your views here.
def index(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    suggestions = []
    recent_activities = []
    # Example: populate with latest 5 users (replace with your real activity logic)
    for user in User.objects.order_by('-date_joined')[:5]:
        recent_activities.append({
            'user': user,
            'timestamp': user.date_joined,
            'percentage': 100,  # Placeholder for activity bar
        })
    if request.user.is_authenticated:
        following_ids = Follower.objects.filter(user=request.user).values_list('follows_id', flat=True)
        suggestions = User.objects.exclude(id__in=following_ids).exclude(id=request.user.id)
        suggestions = list(suggestions)
        random.shuffle(suggestions)
        suggestions = suggestions[:3]
        # Handle follow POST
        if request.method == 'POST' and 'follow_user_id' in request.POST:
            follow_user_id = request.POST.get('follow_user_id')
            to_follow = get_object_or_404(User, id=follow_user_id)
            if not Follower.objects.filter(user=request.user, follows=to_follow).exists() and to_follow != request.user:
                Follower.objects.create(user=request.user, follows=to_follow)
            return redirect('index')
    # Add is_liked_by_user property for each tweet
    for tweet in tweets:
        tweet.is_liked_by_user = False
        if request.user.is_authenticated:
            tweet.is_liked_by_user = tweet.likes.filter(user=request.user).exists()
    return render(request, 'tweet/index.html', {'tweets': tweets, 'suggestions': suggestions, 'recent_activities': recent_activities})

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    # Add is_liked_by_user property for each tweet
    for tweet in tweets:
        tweet.is_liked_by_user = False
        if request.user.is_authenticated:
            tweet.is_liked_by_user = tweet.likes.filter(user=request.user).exists()
    return render(request, 'tweet/tweet_list.html', {'tweets': tweets})

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = tweetform(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('index')  # or 'tweet_list' if that's your homepage
    else:
        form = tweetform()
    return render(request, 'tweet/tweetform.html', {'form': form})

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        form = tweetform(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('index')
    else:
        form = tweetform(instance=tweet)
    return render(request, 'tweet/tweetform.html', {'form': form})

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        tweet.delete()
        return redirect('index')
    return render(request, 'tweet/tweet_confirm_delete.html', {'tweet': tweet})

@login_required
@require_POST
def follow_user(request):
    follow_user_id = request.POST.get('follow_user_id')
    to_follow = get_object_or_404(User, id=follow_user_id)
    if not Follower.objects.filter(user=request.user, follows=to_follow).exists() and to_follow != request.user:
        Follower.objects.create(user=request.user, follows=to_follow)
    return redirect('index')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'tweet/signup.html', {'form': form})

# Custom login view to always pass form
class CustomLoginView(LoginView):
    template_name = 'tweet/login.html'
    authentication_form = AuthenticationForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.get_form()
        return context

# In urls.py, use: path('login/', CustomLoginView.as_view(), name='login'),

@login_required
def profile_view(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    return render(request, 'tweet/profile.html', {'profile_user': user, 'profile': profile})

@login_required
def profile_edit_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    initial = {'username': request.user.username}
    if request.method == 'POST' and 'remove_photo' in request.POST:
        profile.profile_photo.delete(save=True)
        return redirect('profile_edit')
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        new_username = request.POST.get('username', '').strip()
        username_error = None
        if new_username and new_username != request.user.username:
            if User.objects.filter(username=new_username).exclude(pk=request.user.pk).exists():
                username_error = 'This username is already taken.'
            elif len(new_username) < 3:
                username_error = 'Username must be at least 3 characters.'
            else:
                request.user.username = new_username
                request.user.save()
        if form.is_valid() and not username_error:
            form.save()
            return redirect('profile')
        else:
            if username_error:
                form.add_error(None, username_error)
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'tweet/profile_edit.html', {'form': form, 'profile': profile})

@login_required
def search(request):
    query = request.GET.get('q', '').strip()
    user_results = []
    if query:
        user_results = User.objects.filter(Q(username__icontains=query))
    return render(request, 'tweet/search_results.html', {
        'query': query,
        'user_results': user_results,
    })

@login_required
@require_POST
def like_tweet_ajax(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
    liked = True
    if not created:
        like.delete()
        liked = False
    like_count = tweet.likes.count()
    return JsonResponse({'liked': liked, 'like_count': like_count})

@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
    if not created:
        like.delete()  # Unlike if already liked
    referer = request.META.get('HTTP_REFERER', '/')
    anchor = f'#tweet-{tweet_id}'
    if referer:
        if '#' in referer:
            referer = referer.split('#')[0]
        return redirect(referer + anchor)
    return redirect(anchor)

def add_comment(request, tweet_id):
    if not request.user.is_authenticated:
        return redirect('login')
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if request.method == 'POST':
        text = request.POST.get('comment', '').strip()
        if text:
            Comment.objects.create(user=request.user, tweet=tweet, text=text)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def my_posts(request):
    tweets = Tweet.objects.filter(user=request.user).order_by('-created_at')
    recent_activities = []
    for user in User.objects.order_by('-date_joined')[:5]:
        recent_activities.append({
            'user': user,
            'timestamp': user.date_joined,
            'percentage': 100,
        })
    for tweet in tweets:
        tweet.is_liked_by_user = False
        if request.user.is_authenticated:
            tweet.is_liked_by_user = tweet.likes.filter(user=request.user).exists()
    return render(request, 'tweet/index.html', {'tweets': tweets, 'my_posts': True, 'recent_activities': recent_activities})

      
