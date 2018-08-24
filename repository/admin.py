from django.contrib import admin
from .models import *
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'add_date', 'classify', 'article_type_id',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('uid','bid','create_time','reply',)


class StatusAdmin(admin.ModelAdmin):
    list_display = ('uid','aid','status')


admin.site.register(User)
admin.site.register(UserFans)
admin.site.register(PersonalBlog)
admin.site.register(BlogArticle, ArticleAdmin)
admin.site.register(BlogArticleDetail)
admin.site.register(ArticleTag)
admin.site.register(ArticleClassify)
admin.site.register(ArticleComment, CommentAdmin)
admin.site.register(ArticleStatus, StatusAdmin)
admin.site.register(TagsToArticle)
admin.site.register(Trouble)


