from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model


User = get_user_model()


class Question(models.Model):
    title = models.CharField(_('Question text'), max_length=250)
    created = models.DateTimeField(_('Date published'), auto_now_add=True)
    objects = models.Manager()

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _("Questions")

    def __str__(self):
        return self.title


class Choice(models.Model):
    question = models.ForeignKey(
        Question, related_name='choice_set', on_delete=models.CASCADE, verbose_name=_('Question')
    )
    user_response = models.ManyToManyField(User, blank=True, null=True)
    title = models.CharField(_('Choice'), max_length=150)
    objects = models.Manager()

    class Meta:
        verbose_name = _('Choice')
        verbose_name_plural = _("Choice")

    def __str__(self):
        return self.title