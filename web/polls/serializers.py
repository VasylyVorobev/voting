from django.utils.translation import gettext as _
from rest_framework import serializers
from .models import Question, Choice
from .services import PollsService

error_messages: dict = {
    'questions_number': _("the number of responses must be at least 2")
}


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ('id', 'title', )


class QuestionSerializer(serializers.ModelSerializer):
    choice_set = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ('title', 'choice_set')


class CreateUpdatePollsSerializer(serializers.Serializer):
    question = serializers.CharField()
    choice = serializers.ListSerializer(child=serializers.CharField())

    def validate_choice(self, choice) -> list:
        if len(choice) < 2:
            raise serializers.ValidationError(error_messages['questions_number'])
        return choice

    def create(self, validated_data) -> dict:
        question = PollsService.create_question(validated_data['question'])
        PollsService.bulk_create_choice(validated_data['choice'], question)
        return validated_data

    def update(self, instance: Question, validated_data: dict) -> dict:
        instance.title = validated_data['question']
        instance.save(update_fields=('title', ))
        PollsService.bulk_create_choice(validated_data['choice'], question=instance, delete_old=True)
        return validated_data
