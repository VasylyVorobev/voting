import logging
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework import status
from .models import Question, Choice
from . import serializers

logger = logging.getLogger(__name__)


class PollsViewSet(ModelViewSet):

    swagger_tags = ['Polls crud']

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return serializers.CreateUpdatePollsSerializer
        return serializers.QuestionSerializer

    def get_queryset(self):
        return Question.objects.prefetch_related('choice_set')

    @swagger_auto_schema(tags=swagger_tags)
    def list(self, request, *args, **kwargs):
        """
        API for list of poll

        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=swagger_tags)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        Choice.objects.filter(question=instance).delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(tags=swagger_tags)
    def create(self, request, *args, **kwargs):
        """
        API for create poll

        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=swagger_tags)
    def update(self, request, *args, **kwargs):
        """
        API for update poll

        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=swagger_tags)
    def retrieve(self, request, *args, **kwargs):
        """
        API for retrieve poll
        """
        return super().retrieve(request, *args, **kwargs)


class VotingView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.VotingSerializer
    swagger_tags = ['Voting']

    def get_queryset(self):
        return Choice.objects.select_related('question')

    @swagger_auto_schema(tags=swagger_tags)
    def post(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data: dict = serializer.save()
        return Response(response_data, status.HTTP_200_OK)
