from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

User = get_user_model()


def user_photo_upload_to(instance, filename: str) -> str:
    extension = filename.split('.')[-1]
    return f'users/{instance.id}/photo.{extension}'


class UserProfile(models.Model):
    """Модель пользователя."""

    user = models.OneToOneField(to=User, related_name='profile', on_delete=models.CASCADE, verbose_name='пользователь')
    name = models.CharField(max_length=64, blank=True)
    photo = models.ImageField(
        default='users/default/photo.png',
        blank=True,
        upload_to=user_photo_upload_to,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg']), ],
        verbose_name='фото',
    )

    class Meta:
        db_table = 'users_user_profile'
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'профили пользователей'

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.set_default_name()
        super(UserProfile, self).save(*args, **kwargs)

    def set_default_name(self):
        if not self.name:
            self.name = self.user.username
