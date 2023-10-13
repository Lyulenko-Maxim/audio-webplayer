from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class PlayerStatement(models.Model):
    REPEAT_CHOICES = [
        ('off', 'Выключено'),
        ('track', 'Повторить текущий трек'),
        ('context', 'Повторить контекст/плейлист'),
    ]
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name='пользователь')
    is_playing = models.BooleanField(default=False, verbose_name='воспроизводится')
    current_audio_url = models.URLField(blank=True)
    repeat_state = models.CharField(max_length=10, choices=REPEAT_CHOICES, default='off')
    shuffle_state = models.BooleanField(default=False)
    volume = models.FloatField(default=1.0)
    current_position = models.FloatField(default=0.0, )
