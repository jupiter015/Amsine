from multiselectfield import MultiSelectField

from django.core.validators import MinLengthValidator
from django.db import models
from HomePage.models import UserMeta, LanguageMeta

# Create your models here.
class UserProfile(models.Model):
    interests_choices = (('travelling', 'Travelling'), ('reading', 'Reading'), ('gaming', 'Gaming'),)
    userMeta = models.ForeignKey(UserMeta, on_delete=models.CASCADE, related_name='user_profiles')
    bio = models.CharField(max_length=80)
    language_learning = models.ManyToManyField(LanguageMeta, related_name='learning_profiles', blank=True)
    native_language = models.ForeignKey(LanguageMeta, related_name='native_profiles', blank=True, null=True, on_delete=models.SET_NULL)
    interests = MultiSelectField(choices=interests_choices, max_choices=3, validators=[MinLengthValidator(1)])
    last_language_used = models.ForeignKey(LanguageMeta, on_delete=models.SET_NULL, null=True, blank=True, related_name='last_used_profiles')

    def __str__(self):
        return str(self.userMeta.uuid)

class UserEconomy(models.Model):
    userMeta = models.ForeignKey(UserMeta, on_delete=models.CASCADE)
    amount_of_coins = models.IntegerField(default=0)
    amount_of_exp = models.IntegerField(default=0)

    def __str__(self):
        return str(self.userMeta.uuid)