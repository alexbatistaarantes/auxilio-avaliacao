from django.contrib import admin

from .models import *

# Adicionando modelos para edição no site admin
admin.site.register(Assignment)
admin.site.register(Field)
admin.site.register(Submission)
admin.site.register(Answer)
admin.site.register(AnswerGroup)
