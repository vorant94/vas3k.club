from uuid import uuid4

from django.db import models

from users.models.user import User


class Muted(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    user_from = models.ForeignKey(User, related_name="muted_from", db_index=True, on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name="muted_to", on_delete=models.CASCADE)

    class Meta:
        db_table = "muted"
        unique_together = [["user_from", "user_to"]]

    @classmethod
    def mute(cls, user_from, user_to):
        return cls.objects.get_or_create(
            user_from=user_from,
            user_to=user_to,
        )

    @classmethod
    def unmute(cls, user_from, user_to):
        return cls.objects.filter(
            user_from=user_from,
            user_to=user_to,
        ).delete()