from django.contrib import admin
from home.models import Setting, ContactMessage, FAQ


# Register your models here.
class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'phone', 'create_at', 'status']

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'email', 'message', 'creat_at']
    readonly_fields = ('name', 'subject', 'email', 'message', 'ip',)
    list_filter = ['status']

class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'ordernumber', 'status']
    list_filter = ['status']

admin.site.register(Setting, SettingAdmin)
admin.site.register(ContactMessage,ContactMessageAdmin)
admin.site.register(FAQ, FAQAdmin)
