from django.db import models


class Notifications(models.Model):
    user = models.ForeignKey(to='auth_user.User', related_name='notifications', on_delete=models.CASCADE, blank=True,
                             null=True)
    title = models.CharField(max_length=255)
    message = models.TextField()
    lida = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.id, self.title)

    class Meta:
        ordering = ('-created_at',)
