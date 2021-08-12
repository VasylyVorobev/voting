from django.utils.translation import gettext as _
from rest_framework import serializers
from .services import PollsService

error_messages = {
    'questions_number': _("the number of responses must be at least 2")
}


class CreatePollsSerializer(serializers.Serializer):
    question = serializers.CharField()
    choice = serializers.ListSerializer(child=serializers.CharField())

    def validate_choice(self, choice):
        if len(choice) < 2:
            raise serializers.ValidationError(error_messages['questions_number'])
        return choice

    def save(self, **kwargs):
        question = PollsService.create_question(self.validated_data['question'])
        PollsService.bulk_create_choice(self.validated_data['choice'], question)
        return self.validated_data
