from django.conf import settings

from .models import Question, Choice


class PollsService:
    @staticmethod
    def create_question(question: str) -> Question:
        return Question.objects.create(title=question)

    @staticmethod
    def bulk_create_choice(choices: list, question: Question) -> None:
        bulk_list: list = [
            Choice(title=choice, question=question) for choice in choices
        ]
        return Choice.objects.bulk_create(bulk_list)
