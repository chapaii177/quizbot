from django.contrib import admin
from quester.models import Player, Question, Answer

class AnswerInline(admin.StackedInline):
    model = Answer

class PlayerAdmin(admin.ModelAdmin):
    pass

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    pass

class AnswerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Player, PlayerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)

