from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from taggit.managers import TaggableManager

from PIL import Image

from users.models import Profile

class Meme(models.Model):
    user = models.ForeignKey(User,related_name='memes',on_delete=models.CASCADE)
    userOriginal = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_original",blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=30,default='Memino')
    picture= models.ImageField(default='default.jpg', upload_to="memes/")
    title_html = models.CharField(max_length=30,default='Memino', editable = False)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    dislikes = models.ManyToManyField(User, blank=True, related_name="dislikes")
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.picture.path)

        if img.height > 300 or img.width > 300:
            new_img = (300, 300)
            img.thumbnail(new_img)
            img.save(self.picture.path)

        if Profile.objects.get(user=self.user).is_private:
            self.is_private = True

    def get_absolute_url(self):
        return reverse("homepage")

class Comment(models.Model): 
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField() 
    created = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ('created',) 

    def save(self, *args, **kwargs):
        super().save()

    def __str__(self): 
        return 'Comment by {} on {}'.format(self.user.username, self.post) 

    def get_absolute_url(self):
        return reverse_lazy("homepage")