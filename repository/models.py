from django.db import models
import django.utils.timezone as timezone


class User(models.Model):
    username = models.CharField(max_length=20, verbose_name='用户名', unique=True)
    nickname = models.CharField(verbose_name='昵称', max_length=32, null=True, blank=True)
    pwd = models.CharField(max_length=32, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱', unique=True)
    img = models.ImageField(verbose_name='头像', upload_to='static/user_img', null=True)
    fans = models.ManyToManyField(to='User',
                                  through='UserFans',
                                  related_name='f',
                                  through_fields=('user', 'follower'),
                                  verbose_name='粉丝')

    class Meta:
        db_table = 'User'
        verbose_name_plural = '用户信息'

    def __str__(self):
        return self.username


class PersonalBlog(models.Model):
    title = models.CharField(max_length=32, verbose_name='博客标题')
    site = models.CharField(max_length=32, verbose_name='博客后缀', unique=True)
    theme = models.CharField(max_length=32, verbose_name='博客主题')
    summary = models.CharField(max_length=128, verbose_name='基本介绍')
    pb = models.OneToOneField('User', related_name='pb')

    class Meta:
        db_table = 'PersonalBlog'
        verbose_name_plural = '个人博客'

    def __str__(self):
        return self.pb.username


class UserFans(models.Model):
    """
    互粉关系表
    """
    user = models.ForeignKey(verbose_name='博主', to='User', to_field='id', related_name='users')
    follower = models.ForeignKey(verbose_name='粉丝', to='User', to_field='id', related_name='followers')

    class Meta:
        unique_together = [
            ('user', 'follower'),
        ]
        verbose_name_plural = '互粉关系'


class ArticleClassify(models.Model):
    classify = models.CharField(max_length=32, verbose_name='文章分类')
    blog = models.ForeignKey('PersonalBlog', on_delete=models.CASCADE, verbose_name='所属博客')

    class Meta:
        db_table = 'ArticleClassify'
        verbose_name_plural = '文章分类'

    def __str__(self):
        return self.classify


class ArticleTag(models.Model):
    tag = models.CharField(max_length=32, verbose_name='文章标签')
    blog = models.ForeignKey('PersonalBlog', on_delete=models.CASCADE, verbose_name='所属博客')

    class Meta:
        db_table = 'ArticleTag'
        verbose_name_plural = '文章标签'

    def __str__(self):
        return self.tag


class BlogArticle(models.Model):
    title = models.CharField(max_length=128, verbose_name='文章标题')
    summary = models.CharField(max_length=255, verbose_name='文章简介')
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    add_date = models.DateTimeField('保存日期', default=timezone.now)
    mod_date = models.DateTimeField('最后修改日期', auto_now=True)
    blog = models.ForeignKey('PersonalBlog', verbose_name='所属博客')
    classify = models.ForeignKey('ArticleClassify', verbose_name='个人分类', null=True)
    tags = models.ManyToManyField(to="ArticleTag",
                                  through='TagsToArticle',
                                  through_fields=('article', 'tag'),
                                  verbose_name='文章标签')
    type_choices = [
        (1, 'Python'),
        (2, 'Linux'),
        (3, ' OpenStack'),
        (4, ' GoLang'),
    ]
    article_type_id = models.IntegerField(choices=type_choices, default=None, verbose_name='文章种类')

    class Meta:
        db_table = 'BlogArticle'
        verbose_name_plural = '博客文章'

    def __str__(self):
        return self.title


class BlogArticleDetail(models.Model):
    content = models.TextField('文章内容')
    bid = models.OneToOneField('BlogArticle',verbose_name='所属文章',to_field='id',on_delete=models.CASCADE)

    class Meta:
        db_table = 'BlogArticleDetail'
        verbose_name_plural = '文章内容'

    def __str__(self):
        return self.bid.title


class TagsToArticle(models.Model):
    article = models.ForeignKey('BlogArticle', verbose_name='文章')
    tag = models.ForeignKey('ArticleTag', verbose_name='标签')

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]
        db_table = 'TagsToArticle'
        verbose_name_plural = '文章对应标签'


class ArticleStatus(models.Model):
    choices = {
        (0, '赞'),
        (1, '踩'),
    }
    aid = models.ForeignKey('BlogArticle', on_delete=models.CASCADE, verbose_name='文章')
    uid = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='赞踩用户')
    status = models.BooleanField(choices=choices, verbose_name='赞踩状态')

    class Meta:
        db_table = 'ArticleStatus'
        verbose_name_plural = '赞踩文章状态'
        unique_together = [('aid', 'uid'), ]

    def __str__(self):
        return self.aid.title


class ArticleComment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    bid = models.ForeignKey('BlogArticle', on_delete=models.CASCADE, verbose_name='评价的文章')
    uid = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='评价人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    reply = models.ForeignKey(verbose_name='回复评论', to='self', related_name='back', null=True, blank=True,)

    class Meta:
        db_table = 'ArticleComment'
        verbose_name_plural = '文章评论'

    def __str__(self):
        return self.bid.title


class Trouble(models.Model):
    title = models.CharField(max_length=32)
    detail = models.TextField()
    user = models.ForeignKey('User', related_name='u',)
    status_choices = {
        (1, '未处理'),
        (2, '处理中'),
        (3, '已处理'),
    }
    status = models.IntegerField(choices=status_choices, default=1)
    create_time = models.DateTimeField(default=timezone.now)
    handler = models.ForeignKey('User', related_name='h',null=True,blank=True)
    solution = models.TextField(null=True, blank=True)
    solve_time = models.DateTimeField(null=True,blank=True)
    evaluate_choices = {
        (1, '不是很舒服'),
        (2, '可还行'),
        (3, '舒服舒服'),
        (4, 'nice')
    }
    evaluate = models.IntegerField(choices=evaluate_choices, null=True, blank=True, default=2)

    class Meta:
        db_table = 'Trouble'
        verbose_name_plural = '报障表'

