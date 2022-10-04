from django.test import TestCase
from django.urls import reverse
from .models import User

class ProfileFriendsTest(TestCase):
    def setUp(self):
        self.acredentials = {
            "username": "test1",
            "password": "test1",
        }
        self.auser = User.objects.create_user(
            **self.acredentials,
        )

        self.bcredentials = {
            "username": "test2",
            "password": "test2",
        }
        self.buser = User.objects.create(
            **self.bcredentials,
        )

        self.ccredentials = {
            "username": "test3",
            "password": "test3",
        }
        self.cuser = User.objects.create(
            **self.ccredentials,
        )
        
    def test_friends(self):
        self.assertFalse(self.auser.profile in self.buser.profile.friends.all())

        # auser non può accettare la sua stessa richiesta di amicizia indirizzata a cuser
        self.client.login(**self.acredentials)
        res = self.client.get(reverse('users:send_friend_request', args=[self.cuser.profile.pk]))
        self.assertEqual(res.status_code, 200)
        res = self.client.get(reverse('users:accept_friend_request', args=[1]))
        self.assertEqual(res.status_code, 200)
        res = self.client.get(reverse('users:friends_list'))
        self.assertNotContains(res, self.cuser.username)
        self.assertFalse(self.auser.profile in self.auser.profile.friends.all())
        self.assertFalse(self.cuser.profile in self.auser.profile.friends.all())

        # Neanche buser può accettare la richiesta di amicizia indirizzata a cuser
        self.client.force_login(self.buser, backend=None)
        res = self.client.get(reverse('users:accept_friend_request', args=[1]))
        self.assertEqual(res.status_code, 200)
        self.assertFalse(self.auser.profile in self.buser.profile.friends.all())

        # Un AnonymousUser non può accettare la richiesta
        self.client.logout()
        res = self.client.get(reverse('users:accept_friend_request', args=[1]))
        self.assertEqual(res.status_code, 302)  

        # cuser accetta e diventa amico di auser 
        self.client.force_login(self.cuser, backend=None)
        res = self.client.get(reverse('users:accept_friend_request', args=[1]))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(self.auser.profile in self.cuser.profile.friends.all())    