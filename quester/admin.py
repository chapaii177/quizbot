from django.contrib import admin
from quester.models import Player, Question, Answer, News

class PlayerAdmin(admin.ModelAdmin):
    readonly_fields = ['name','score','status','status_news']
    list_display = ['name', 'score', 'status', 'status_news']
    pass

class AnswerInline(admin.StackedInline):
    model = Answer

@admin.display(description='Question')
def question_short_name(obj):
    return obj.__str__()

class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ['answer_count','answer_users','task_id']
    inlines = [AnswerInline]
    list_display = [question_short_name, 'date', 'answer_count', 'prizes_count']
    pass

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['questions','answer_text']
    pass

@admin.display(description='Title')
def news_short_name(obj):
    return obj.__str__()

class NewsAdmin(admin.ModelAdmin):
    readonly_fields = ['task_id',]
    list_display = [news_short_name, 'date']
    pass

admin.site.register(Player, PlayerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(News, NewsAdmin)

