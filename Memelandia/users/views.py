from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.models import FriendRequest, Profile

from .forms import UpdateUserForm, UpdateProfileForm


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "user_create.html"
    success_url = reverse_lazy("users:login")


@login_required(login_url='/users/login/')
def profile_update(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return render(request, template_name='users/profile.html', context={'user':request.user,'profile':request.user.profile})
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/modify_profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required(login_url='/users/login/')
def profile(request):
    return render(request, template_name='users/profile.html', context={'user':request.user,'profile':request.user.profile})

@login_required(login_url='/users/login/')
def send_friend_request(request, userID):
    from_user = Profile.objects.get(user=request.user)
    to_user = Profile.objects.get(user=userID)

    if from_user != to_user and from_user not in to_user.friends.all():
        friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
        
    if created:
        return render(request,template_name="users/risultato_positivo.html")
    else:
        return render(request,template_name="users/risultato_negativo.html")


@login_required(login_url='/users/login/')
def accept_friend_request(request, requestID):
    friend_request = FriendRequest.objects.get(id=requestID)
    if friend_request.to_user == Profile.objects.get(user=request.user):
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return render(request,template_name="users/risultato_accettato.html")
    else:
        return render(request,template_name="users/risultato_non_accettato.html")

@login_required(login_url='/users/login/')
def listRequestsSend(request):
    return render(request,template_name="users/friends_request.html",context={"not_friends":Profile.objects.all().exclude(friends__in=request.user.profile.friends.all()).exclude(user=request.user)})

@login_required(login_url='/users/login/')
def listRequestsAccept(request):
    return render(request,template_name="users/accept_friends_request.html",
    context={"all_friend_requests":FriendRequest.objects.all()})

@login_required(login_url='/users/login/')
def listFriends(request):
    return render(request,template_name="users/friends_list.html",context={"friends":Profile.objects.get(user=request.user).friends.all()})