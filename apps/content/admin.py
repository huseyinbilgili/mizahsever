from django.contrib import admin

from apps.content.models import Comment, Content, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    class Meta:
        model = Tag
        fields = "__all__"


@admin.register(Content)
class VideoAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("status",)

    class Meta:
        fields = "__all__"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    class Meta:
        fields = "__all__"
