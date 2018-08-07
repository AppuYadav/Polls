from django.contrib import admin
from .models import Question, Choice, Country, City
from django.contrib.auth.models import Group

# Register your models here.

admin.site.site_header = 'Admin Polls Dashboard'

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldssets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        ]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    inlines = [ChoiceInline]

class CountryAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Question, QuestionAdmin)


admin.site.register(Choice)
admin.site.register(Country, CountryAdmin)
admin.site.register(City)
admin.site.unregister(Group)
