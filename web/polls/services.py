from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Question, Choice


User = get_user_model()


class PollsService:
    @staticmethod
    def create_question(question: str) -> Question:
        return Question.objects.create(title=question)

    @staticmethod
    def bulk_create_choice(choices: list, question: Question, delete_old: bool = None) -> None:
        if delete_old:
            question.choice_set.all().delete()
        bulk_list: list = [
            Choice(title=choice, question=question) for choice in choices
        ]
        return Choice.objects.bulk_create(bulk_list)

    @staticmethod
    def is_choice_exists(choice_id: int) -> bool:
        return Choice.objects.filter(id=choice_id).exists()

    @staticmethod
    def add_user_choice(choice_id: int, user: User) -> None:
        choice = Choice.objects.get(id=choice_id)
        choice.user_response.add(user)

    @staticmethod
    def get_choice(choice_id: int) -> Choice:
        return Choice.objects.get(id=choice_id)

    @staticmethod
    def is_choice_belong_poll(choice_id: int, question_id: int):
        return Choice.objects.filter(id=choice_id, question_id=question_id).exists()
