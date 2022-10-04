from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/users/login/')
def home(request):
    return render(request, 'chat/home.html')

@login_required(login_url='/users/login/')
def room(request, room):
    room_details = Room.objects.get(name=room)
    return render(request, 'chat/room.html', {
        'username': request.user.username,
        'room': room,
        'room_details': room_details
    })

@login_required(login_url='/users/login/')
def fallimento(request):
    return render(request, 'chat/fallimento.html')

@login_required(login_url='/users/login/')
def checkview(request):
    room_name = request.POST['room_name']
    username = request.user.username

    if Room.objects.filter(name=room_name).exists():
        room = Room.objects.get(name=room_name)
        if room.utenteCreatore == request.user or room.utenteSecondo == request.user:
            return redirect('/chat/'+room_name+'/?username='+username)
        elif room.utenteSecondo is None:
            room.utenteSecondo = request.user
            room.save()
            return redirect('/chat/'+room_name+'/?username='+username)
        else:
            return redirect("/chat/fallimento")
    else:
        new_room = Room.objects.create(name=room_name,utenteCreatore=request.user)
        new_room.save()
        return redirect('/chat/'+room_name+'/?username='+username)

@login_required(login_url='/users/login/')
def send(request):
    message = request.POST['message']
    username = request.user.username
    room_id = Room.objects.get(id=request.POST['room_id'])

    if room_id.utenteSecondo == request.user or room_id.utenteCreatore == request.user:
        new_message = Message.objects.create(value=message, user=username, room=room_id)
        new_message.save()
        return redirect("/chat/fallimento")
    return redirect("/chat/fallimento")

@login_required(login_url='/users/login/')
def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    if room_details.utenteSecondo == request.user or room_details.utenteCreatore == request.user:
        messages = Message.objects.filter(room=room_details)
        return JsonResponse({"messages":list(messages.values())})
    else:
        return redirect("/chat/fallimento")