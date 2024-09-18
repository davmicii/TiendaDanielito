# app/core/user/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL
from crum import get_current_request


class User(AbstractUser):
    image = models.ImageField(upload_to='users/%Y/%m/%d/', null=True, blank=True)

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/user/user.svg')

    def tojson(self):
        item = model_to_dict(self, exclude=['password', 'user_permissions', 'last_login'])
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%Y-%m-%d %H:%M:%S')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d %H:%M:%S')
        item['image'] = self.get_image()
        item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        return item

    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if 'group_id' not in request.session:
                    request.session['group_id'] = groups[0].id
        except:
            pass