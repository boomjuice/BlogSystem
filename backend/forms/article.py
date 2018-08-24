from django.forms import fields
from django.forms import widgets
from repository.models import *
from django import forms


class ArticleForm(forms.Form):
    title = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '文章标题'})
    )
    summary = fields.CharField(
        widget=widgets.Textarea(attrs={'class': 'form-control', 'placeholder': '文章简介', 'rows': '3'})
    )
    content = fields.CharField(
        widget=widgets.Textarea(attrs={'id': 'editor'})
    )
    article_type_id = fields.IntegerField(
        widget=widgets.RadioSelect(choices=BlogArticle.type_choices)
    )
    classify_id = fields.ChoiceField(
        choices=[],
        widget=widgets.RadioSelect
    )
    tags = fields.MultipleChoiceField(
        required=False,
        choices=[],
        widget=widgets.CheckboxSelectMultiple
    )

    def __init__(self, request, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        blog_id = request.session['user']['pb__id']
        self.fields['classify_id'].choices = ArticleClassify.objects.filter(blog_id=blog_id).values_list('id',
                                                                                                        'classify')
        self.fields['tags'].choices = ArticleTag.objects.filter(blog_id=blog_id).values_list('id', 'tag')
