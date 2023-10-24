from django.db import models


class TransactionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_raise=False)

    def delete(self):
        self.update(is_deleted=True)
        return super().delete()


class TransactionRaiseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_raise=True)

    def delete(self):
        self.update(is_deleted=True)
        return super().delete()
