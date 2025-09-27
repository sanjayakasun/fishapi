from django.contrib import admin
from .models import FishSpecies, ChatSession, ChatMessage


@admin.register(FishSpecies)
class FishSpeciesAdmin(admin.ModelAdmin):
    list_display = ['vernacular_name', 'scientific_name', 'family', 'threat_status']
    list_filter = ['family', 'threat_status']
    search_fields = ['vernacular_name', 'scientific_name', 'family']


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'role', 'content_preview', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['content']
    readonly_fields = ['created_at']

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Content Preview"
