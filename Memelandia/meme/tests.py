from django.test import TestCase

from meme.views import checkDislike, checkLike
from .models import User, Meme

class LikeTest(TestCase):
    def setUp(self):
        self.acredentials = {
            "username": "testA",
            "password": "testA",
        }
        self.auser = User.objects.create_user(
            **self.acredentials,
        )

        self.bcredentials = {
            "username": "testB",
            "password": "testB",
        }
        self.buser = User.objects.create(
            **self.bcredentials,
        )

        self.meme = Meme.objects.create(**{"user": self.auser})
        self.meme.save()

    def test_like(self):
        # auser mette like al meme
        checkLike(self.meme,self.auser)
        self.assertEquals(self.meme.likes.count(),1)

        # auser rimette like al meme e si azzera il conteggio
        checkLike(self.meme,self.auser)
        self.assertEquals(self.meme.likes.count(),0)

        # auser rimette like al meme
        checkLike(self.meme,self.auser)
        self.assertEquals(self.meme.likes.count(),1)

        # auser mette dislike al meme: il contatore dei
        # like torna a zero e va a 1 quello dei dislike
        checkDislike(self.meme,self.auser)
        self.assertEquals(self.meme.likes.count(),0)
        self.assertEquals(self.meme.dislikes.count(), 1)

        # auser mette due volte dislike e il contatore ritorna a 1
        checkDislike(self.meme,self.auser)
        checkDislike(self.meme,self.auser)
        self.assertEquals(self.meme.dislikes.count(),1)
        
        # auser mette like al meme: il contatore dei
        # dislike torna a zero e va a 1 quello dei like
        checkLike(self.meme,self.auser)
        self.assertEquals(self.meme.dislikes.count(), 0)
        self.assertEquals(self.meme.likes.count(),1)

        # buser mette like al meme: il contatore dei like
        # va a 2 mentre quello dei dislike 0
        checkLike(self.meme,self.buser)
        self.assertEquals(self.meme.likes.count(),2)
        self.assertEquals(self.meme.dislikes.count(), 0)

        # buser mette dislike al meme: il contatore dei like
        # torna a 1 mentre quello di dislike diventa 1
        checkDislike(self.meme,self.buser)
        self.assertEquals(self.meme.likes.count(),1)
        self.assertEquals(self.meme.dislikes.count(), 1)