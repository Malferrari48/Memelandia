from django import http
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from django.views.generic import ListView,CreateView,DetailView
from django.contrib.auth.models import User
from meme.forms import CommentForm

from users.models import Profile
from .models import Comment, Meme

class MemeList(ListView):
    model = Meme
    template_name = "meme/bacheca.html"

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        profile_user = Profile.objects.get(user=user)
        if self.request.user.is_anonymous:
            profile_attuale = None
        else: 
            profile_attuale = Profile.objects.get(user=self.request.user)
        if profile_user.is_private == False or profile_user == profile_attuale or (profile_user.is_private and (profile_attuale in profile_user.friends.all())):
            return Meme.objects.filter(user=user).order_by('-created_at')
        else:
            return []

    def get_username_field(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Profile.objects.filter(user=user)


class addMemeView(LoginRequiredMixin, CreateView):
    model = Meme
    fields = ('title','tags','picture')
    template_name = "meme/creazione_meme.html"
    login_url = '/users/login/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.userOriginal = self.request.user
        obj.save()        
        form.save_m2m()
        return http.HttpResponseRedirect("bacheca/"+str(obj.user.username))

class MemeDetailView(DetailView):
    model = Meme
    template_name = "meme/meme_detail.html"

    def get_object(self):
        meme = get_object_or_404(Meme, pk=self.kwargs.get('pk'))
        profile_user = Profile.objects.get(user=meme.user)
        profile_userOriginal = Profile.objects.get(user = meme.userOriginal)
        if self.request.user.is_anonymous:
            profile_attuale = None
        else: 
            profile_attuale = Profile.objects.get(user=self.request.user)
        if profile_user.is_private == False or profile_user == profile_attuale or (profile_user.is_private and (profile_attuale in profile_user.friends.all())):
            return meme
        else:
            return None

class addCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "meme/add_comment.html"
    login_url = '/users/login/'

    def get_success_URL(self):
        return reverse('meme:meme_detail')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.meme = get_object_or_404(Meme, pk = self.kwargs['pk'])
        profile_attuale = Profile.objects.get(user=obj.user)
        profile_meme = Profile.objects.get(user=obj.meme.user)
        if not(profile_meme.is_private == False or profile_meme == profile_attuale or (profile_meme.is_private and (profile_attuale in profile_meme.friends.all()))):
            return http.HttpResponseRedirect(obj.get_absolute_url())
        obj.save()        
        return http.HttpResponseRedirect("/meme/meme_detail/"+str(obj.meme.pk))

def checkLike(meme,user):
    is_dislike = False

    for dislike in meme.dislikes.all():
        if dislike == user:
            is_dislike = True
            break

    if is_dislike:
        meme.dislikes.remove(user)

    is_like = False

    for like in meme.likes.all():
        if like == user:
            is_like = True
            break
    
    if not is_like:
        meme.likes.add(user)

    if is_like:
        meme.likes.remove(user)

class Like(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        meme = Meme.objects.get(pk=pk)

        profile_attuale = Profile.objects.get(user=self.request.user)
        profile_meme = Profile.objects.get(user=meme.user)

        if not (profile_meme.is_private == False or profile_meme == profile_attuale or (profile_meme.is_private and (profile_attuale in profile_meme.friends.all()))):
            return http.HttpResponseRedirect("/")

        checkLike(meme,request.user)

        next = request.POST.get('next','/')
        return http.HttpResponseRedirect(next)

def checkDislike(meme,user):
    is_like = False

    for like in meme.likes.all():
        if like == user:
            is_like = True
            break
        
    if is_like:
        meme.likes.remove(user)
        
    is_dislike = False

    for dislike in meme.dislikes.all():
        if dislike == user:
            is_dislike = True
            break
    
    if not is_dislike:
        meme.dislikes.add(user)

    if is_dislike:
        meme.dislikes.remove(user)

class DisLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        meme = Meme.objects.get(pk=pk)

        profile_attuale = Profile.objects.get(user=self.request.user)
        profile_meme = Profile.objects.get(user=meme.user)

        if not (profile_meme.is_private == False or profile_meme == profile_attuale or (profile_meme.is_private and (profile_attuale in profile_meme.friends.all()))):
            return http.HttpResponseRedirect("/")

        checkDislike(meme,request.user)

        next = request.POST.get('next','/')
        return http.HttpResponseRedirect(next)

class TagIndexView(ListView):
    model = Meme
    template_name = "meme/tagged.html"

    def get_queryset(self):
        return Meme.objects.filter(tags__slug__iexact=self.kwargs.get('tag_slug')).order_by('-created_at')
        
class Forward(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        meme = Meme.objects.get(pk=pk)

        profile_attuale = Profile.objects.get(user=self.request.user)
        profile_meme = Profile.objects.get(user=meme.user)

        if not (profile_meme.is_private == False or profile_meme == profile_attuale):
            return http.HttpResponseRedirect("/")

        meme_forward = meme
        meme_forward.pk = None
        meme_forward.user = self.request.user
        meme_forward.userOriginal = Meme.objects.get(pk=pk).userOriginal
        meme_forward.save()

        return http.HttpResponseRedirect("/meme/bacheca/"+str(self.request.user))