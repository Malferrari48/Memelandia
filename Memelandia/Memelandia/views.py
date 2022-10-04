from django.db.models import Count
from django.shortcuts import render
from taggit.models import Tag

from users.models import Profile, User
from meme.models import Meme

def homepage(request):
    friends = []
    if not request.user.is_anonymous:
        friends = Profile.objects.get(user=request.user).friends.all()
        memesOriginalNotFriends = Meme.objects.filter(userOriginal__profile__is_private=True).exclude(userOriginal__profile__in = friends)
        memesAmici = Meme.objects.filter(user__profile__in = friends).annotate(like_count=Count('likes')).order_by('-like_count')
        if memesAmici.count() < 10:
            memes = Meme.objects.exclude(user__profile__in = friends).exclude(user__profile__is_private=True).annotate(like_count=Count('likes')).order_by('-like_count')[:(10-memesAmici.count())]
        memes.difference(memesOriginalNotFriends)
    else:
        memesAmici = []
        memes = Meme.objects.annotate(like_count=Count('likes')).order_by('-like_count').exclude(user__profile__is_private=True).exclude(userOriginal__profile__is_private=True)
    return render(request,template_name="homepage.html",context={"memesAmici": memesAmici[:10], "memes":memes, "friends":friends, "tags_usati":Meme.tags.most_common()[:15]})

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        utenti = User.objects.filter(username__icontains=searched)
        friends = Profile.objects.get(user=request.user).friends.all()
        tags = Tag.objects.filter(slug__icontains=searched)
        return render(request,'search.html',{'searched':searched, 'utenti':utenti, 'tags':tags, 'friends':friends})
    else:
        return render(request,'search.html',{})