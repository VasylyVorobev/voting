from django.utils.translation import gettext as _
from rest_framework import serializers
from .models import Question, Choice
from .services import PollsService

error_messages: dict = {
    'questions_number': _("The number of responses must be at least 2"),
    'choice_exists': _('There is no such choice')
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


class VotingSerializer(serializers.Serializer):
    choice_id = serializers.IntegerField()

    def validate_choice_id(self, choice_id) -> int:
        if not PollsService.is_choice_exists(choice_id):
            raise serializers.ValidationError(error_messages['choice_exists'])
        return choice_id

    def save(self, **kwargs):
        user = self.context['request'].user
        PollsService.add_user_choice(self.validated_data['choice_id'], user)
        return self.validated_data
