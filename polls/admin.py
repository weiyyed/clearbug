from django.conf.urls import url
from django.contrib import admin
from .models import Choice, Question

#
# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3
#
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ('question_text', 'pub_date', 'was_published_recently')
#     fieldsets = [
#         (None,               {'fields': ['question_text']}),
#         ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
#     ]
#     inlines = [ChoiceInline]
#     list_filter = ['pub_date','question_text']
#     search_fields = ['question_text','pub_date']
#
# admin.site.register(Question, QuestionAdmin)

# #图片评论实例
# class ProductiveAuthorsFilter(admin.SimpleListFilter):
#     parameter_name = 'is_productive'
#     title = 'Productive author'
#     YES, NO = 1, 0
#     # Number of comments for an author to be considered a productive one
#     THRESHOLD = 100
#
#     def lookups(self, request, model_admin):
#         return (
#             (self.YES, 'yes'),
#             (self.NO, 'no'),
#         )
#
#     def queryset(self, request, queryset):
#
#         qs = queryset.annotate(Count('comments'))
#
#         # Note the syntax. This way we avoid touching the queryset if our
#
#         # filter is not used at all.
#
#         if self.value() == self.YES:
#             return qs.filter(comments__count__gte=self.THRESHOLD)
#
#         if self.value() == self.NO:
#             return qs.filter(comments__count__lt=self.THRESHOLD)
#
#         return queryset
# class PictureAdmin(admin.ModelAdmin):
#     list_display_fields = ('photo', 'animal_kind', 'author', 'is_promoted',)
#     list_filters = [..., ProductiveAuthorsFilter]
#     list_fields = ['object_link', 'mail_link',]
#     # 推广动作
#     actions = ['promote', ]
#     def promote(self, request, queryset):
#         queryset.update(is_promoted=True)
#         self.message_user(request, 'The posts are promoted')
#     promote.short_description = 'Promote the pictures'
#     search_fields = ('title', 'author__name', 'comments__text',)
#     # “在站点查看”
#     list_fields = [..., 'object_link']
#     def object_link(self, item):
#         url = item.get_absolute_url()
#         return u'<a href={url}>open</a>'.format(url=url)
#     object_link.short_description = 'View on site'
#     object_link.allow_tags = True
#     # 对象自定义action
#     def mail_link(self, obj):
#         dest = reverse('admin:myapp_pictures_mail_author',
#
#                        kwargs={'pk': obj.pk})
#
#         return '<a href="{url}">{title}</a>'.format(url=dest, title='send mail')
#
#     mail_link.short_description = 'Show some love'
#
#     mail_link.allow_tags = True
#
#     def get_urls(self):
#         urls = [
#
#             url('^(?P<pk>\d+)/sendaletter/?$',
#
#                 self.admin_site.admin_view(self.mail_view),
#
#                 name='myapp_pictures_mail_author'),
#
#         ]
#
#         return urls + super(PictureAdmin, self).get_urls()
#
#     def mail_view(self, request, *args, **kwargs):
#         obj = get_object_or_404(Picture, pk=kwargs['pk'])
#
#         send_mail('Feel the granny\'s love', 'Hey, she loves your pet!',
#
#                   'granny@yoursite.com', [obj.author.email])
#
#         self.message_user(request, 'The letter is on its way')
#
#         return redirect(reverse('admin:myapp_picture_changelist'))
#
# admin.site.register(Picture, PictureAdmin)
#
# class Author2Admin(admin.ModelAdmin):
#     list_display_fields = ('name', 'email',)
#
# admin.site.register(Author2, Author2Admin)
# class CommentAdmin(admin.ModelAdmin):
#     list_display_fields = ('picture', 'author',)


