from django.contrib import admin

# Register your models here.

from . import models

class PersonAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Person, PersonAdmin)

class LinkAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Link, LinkAdmin)

class MessageAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Message, MessageAdmin)

class RelayAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Relay, RelayAdmin)

class GameAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Game, GameAdmin)
