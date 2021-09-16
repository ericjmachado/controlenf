import itertools
import uuid
from datetime import datetime
from typing import Union, Iterator, Tuple

from django.contrib.admin.utils import NestedObjects
from django.db import models, router, transaction
from django.db.models import QuerySet, Q
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError


class UUIDPkFieldMixin(models.Model):
    id = models.UUIDField(
        primary_key=True,
        verbose_name=_("uuid"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    class Meta:
        abstract = True

    @property
    def get_pk(self):
        return str(self.id)


class TimeManagerMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    modified_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


class UniqueTogetherManagerMixin(models.Model):
    class Meta:
        abstract = True

    class UniqueTogether:
        value = ()
        message = {}
        except_has = ()

    @staticmethod
    def __depth__(t):
        depths = [
            UniqueTogetherManagerMixin.__depth__(item)
            for item in t
            if isinstance(item, tuple)
        ]
        if len(depths) > 0:
            return 1 + max(depths)
        return 1

    def save(self, *args, **kwargs):
        if bool(self.UniqueTogether.value):
            unique = self.UniqueTogether.value
            message = (
                self.UniqueTogether.message
                if hasattr(self.UniqueTogether, "message")
                else None
            )
            except_has = (
                self.UniqueTogether.except_has
                if hasattr(self.UniqueTogether, "except_has")
                else None
            )
            Klass = self.__class__
            args_to_check = []

            if self.__depth__(unique) > 1:
                pass
            else:
                for param in unique:
                    args_to_check.append(Q(**{param: getattr(self, param)}))
            qs = Klass.objects_without_deleted.filter(
                ~Q(pk=self.get_pk), Q(deleted_at__isnull=True), *args_to_check
            )
            if except_has:
                for param in except_has:
                    key, value = None, None
                    if isinstance(param, (tuple, list)):
                        key, value = param
                    if isinstance(param, str):
                        key = param
                    if getattr(self, key) and getattr(self, key) == value:
                        qs = Klass.objects_without_deleted.none()
                        break
            if qs.exists():
                if not message:
                    message = {
                        "error": "Os campos %s devem ser únicos" % ", ".join(unique)
                    }
                raise ValidationError(message)
        return super(UniqueTogetherManagerMixin, self).save(*args, **kwargs)


class ParanoiaQuerySet(QuerySet):
    """
    Prevents objects from being hard-deleted. Instead, sets the
    ``date_deleted``, effectively soft-deleting the object.
    """

    def delete(self, *args, **kwargs):
        for obj in self:
            obj.deleted_at = datetime.now()
            obj.save()

    def restore(self, *args, **kwargs):
        for obj in self:
            obj.deleted_at = None
            obj.save()


class ParanoiaManager(models.Manager):
    """
    Only exposes objects that have NOT been soft-deleted.
    """

    def get_queryset(self):
        return ParanoiaQuerySet(self.model, using=self._db).filter(
            deleted_at__isnull=True
        )


class ParanoiaMixin(models.Model):
    class Meta:
        abstract = True

    deleted_at = models.DateTimeField(null=True, blank=True)
    objects = models.Manager()
    objects_without_deleted = ParanoiaManager()

    def related_objects(
            self, flatten=True
    ) -> Union[Iterator, Tuple[models.Model], Tuple]:
        """Return a generator to the objects that would be deleted if we delete "obj" (excluding obj)"""
        collector = NestedObjects(using=router.db_for_write(self))
        collector.collect([self])

        def flatten(elem):
            if isinstance(elem, list):
                return itertools.chain.from_iterable(map(flatten, elem))
            elif self != elem:
                return (elem,)
            return ()

        return flatten(collector.nested())

    def delete(self, **kwargs):
        if (
                hasattr(self, "request")
                and self.request.path.startswith("/admin/")
                and not kwargs.get("soft_delete", False)
        ):
            super(ParanoiaMixin, self).delete(**kwargs)
        else:
            with transaction.atomic():
                for related in self.related_objects():
                    if isinstance(related, ParanoiaMixin):
                        related.delete(cascade=True, **kwargs)

            self.deleted_at = datetime.now()
            self.save()

    def restore(self, **kwargs):
        with transaction.atomic():
            for related in self.related_objects():
                related.restore(cascade=True)

        self.deleted_at = None
        self.save()


class ControlModel(
    TimeManagerMixin,
    UUIDPkFieldMixin,
    ParanoiaMixin,
    UniqueTogetherManagerMixin,
    models.Model,
):
    class Meta:
        abstract = True

    @property
    def exists(self):
        Klass = self.__class__
        return Klass.objects_without_deleted.filter(id=self.pk).exists()
