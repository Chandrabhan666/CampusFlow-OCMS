from django.db import models


# Derived analytics are computed from live OCMS tables and cached in Redis.
class DashboardSnapshot(models.Model):
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
