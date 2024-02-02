from django.contrib import admin

from .models import Question, Choice
from .forms import QuestionForm, ChoiceAddForm, ChoiceInlineFormset
# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = Choice
    can_delete = False
    max_num = Choice.MAX_CHOICES_COUNT
    min_num = Choice.MAX_CHOICES_COUNT
    form = ChoiceAddForm
    formset = ChoiceInlineFormset

class QuestionAdmin(admin.ModelAdmin):
    model = Question
    inlines = (ChoiceInline, )
    list_display = ['qus_txt', 'is_published']
    list_filter = ['is_published']
    # search_fields = ['qus_txt', 'choices__choice_text']
    actions = None
    form = QuestionForm

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.pk is not None and obj.is_published is True:
            return False
        return True

admin.site.register(Question, QuestionAdmin)