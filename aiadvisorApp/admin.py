from django.contrib import admin
from aiadvisorApp.models import Conversation, Message

# Register your models here.
admin.site.register([Conversation, Message])
