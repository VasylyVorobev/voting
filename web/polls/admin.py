from django.contrib import admin
from .models import Question, Choice, ClientConfigure


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 0


@admin.register(Question)
class QuestionModelsAdmin(admin.ModelAdmin):
    inlines = (ChoiceInLine, )


@admin.register(Choice)
class ChoiceModelsAdmin(admin.ModelAdmin):
    pass


@admin.register(ClientConfigure)
class ClientConfigureModelsAdmin(admin.ModelAdmin):
    pass
