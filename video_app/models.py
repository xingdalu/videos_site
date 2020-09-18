from django.db import models
from faker import Factory
from django.contrib.auth.admin import User


class UserProfile(models.Model):
    belong_to = models.OneToOneField(to=User, related_name='profile', on_delete=models.CASCADE)
    profile_image = models.FileField(upload_to='profile_image')
    nickname = models.CharField(null=True, blank=True, max_length=100, default='xingxing')
    choice_list = (
        ('author', 'author'),
        ('normal', 'normal')
    )
    choice = models.CharField(choices=choice_list, max_length=10, default='normal')

    def __str__(self):
        return self.belong_to.username


# Create your models here.
class Video(models.Model):
    title = models.CharField(null=True, blank=True, max_length=50)
    content = models.TextField(null=True, blank=True)
    url_image = models.URLField(null=True, blank=True)
    cover = models.FileField(upload_to='cover_image', null=True)
    editor_choice = models.BooleanField(default=False)
    owner = models.ForeignKey(to=UserProfile, related_name='videos', default=1, on_delete=models.CASCADE)
    mode_choice = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# fake = Factory.create()
# with open(r'D:/web开发/Django/root/video_site/video_app/image_url.txt', 'r') as f:
#     for url in f.readlines():
#         if url:
#             v = Video(
#                 title=fake.text(max_nb_chars=90),
#                 content=fake.text(max_nb_chars=3000),
#                 url_image=url,
#                 editor_choice=fake.pybool()
#                 )
#             v.save()


class Ticket(models.Model):
    voter = models.ForeignKey(to=UserProfile, related_name='voted_tickets', on_delete=models.CASCADE)
    video = models.ForeignKey(to=Video, related_name='tickets', on_delete=models.CASCADE)
    voted_choices = (
        ('like', 'like'),
        ('dislike', 'dislike'),
        ('normal', 'normal')
    )
    choice = models.CharField(choices=voted_choices, max_length=10)

    def __str__(self):
        return str(self.id)
