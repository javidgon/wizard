from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class UserToken(models.Model):
    app_label = '{{ project.name }}'

    user = models.ForeignKey(User)
    token = models.CharField(max_length=20)

    def __unicode__(self):
        return '{}, {}'.format(user.username, token)

    def to_dict(self):
        return {
            'user': self.user,
            'token': self.token
        }
