import logging
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework import status
from .models import Question, Choice
from . import services
from . import serializers

logger = logging.getLogger(__name__)


class PollsViewSet(UpdateModelMixin, RetrieveModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet):

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return serializers.CreateUpdatePollsSerializer
        return serializers.QuestionSerializer

    def get_queryset(self):
        return Question.objects.prefetch_related('choice_set')
