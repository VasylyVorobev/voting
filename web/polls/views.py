import logging
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status

from . import services
from . import serializers

logger = logging.getLogger(__name__)


class CreatePollsView(CreateModelMixin, GenericViewSet):
    serializer_class = serializers.CreatePollsSerializer
