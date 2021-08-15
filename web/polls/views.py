import logging
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from .models import Question, Choice
from . import services
from . import serializers

logger = logging.getLogger(__name__)


class PollsViewSet(mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return serializers.CreateUpdatePollsSerializer
        return serializers.QuestionSerializer

    def get_queryset(self):
        return Question.objects.prefetch_related('choice_set')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        Choice.objects.filter(question=instance).delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
