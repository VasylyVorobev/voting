from typing import Union
from django.db.models import F
from django.utils.translation import gettext as _
from rest_framework import serializers
from .models import Question, Choice
from .services import PollsService


error_messages: dict = {
    'questions_number': _("The number of responses must be at least 2"),
    'choice_exists': _('There is no such choice'),
    'choice_belong_poll': _('The choice does not belong to the poll')
}


class ChoiceSerializer(serializers.ModelSerializer):
    percent = serializers.SerializerMethodField()

    class Meta:
        model = Choice
        fields = ('id', 'title', 'votes', 'percent')

    def get_percent(self, instance: Choice) -> Union[float, int]:
        question = instance.question
        choices = question.choice_set.values_list('votes', flat=True)
        count_votes = sum([i for i in choices])
        return round(instance.votes / count_votes * 100, 2) if count_votes > 0 else 0


class QuestionSerializer(serializers.ModelSerializer):
    choice_set = ChoiceSerializer(many=True)
    result_vote = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('id', 'title', 'choice_set', 'result_vote')

    def get_result_vote(self, instance: Question) -> int:

        return sum(instance.choice_set.values_list('votes', flat=True))


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
        if not PollsService.is_choice_belong_poll(choice_id, self.context['view'].kwargs.get('pk')):
            raise serializers.ValidationError(error_messages['choice_belong_poll'])
        return choice_id

    def save(self, **kwargs):
        choice = PollsService.get_choice(self.validated_data['choice_id'])
        choice.votes = F('votes') + 1
        choice.save(update_fields=('votes', ))
        return self.validated_data
