from django.contrib import admin
from .models import (
    Skill, Project,
    ServicePackage, PackageFeature,
    Tag, BlogPost, Comment,
    OrderInquiry, PageView,
)

admin.site.site_header  = '🖥 DevPortfolio Admin'
admin.site.site_title   = 'DevPortfolio'
admin.site.index_title  = 'Панель управління'


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display  = ('name', 'category', 'level')
    list_editable = ('level',)
    list_filter   = ('category',)


class PackageFeatureInline(admin.TabularInline):
    model = PackageFeature
    extra = 3


@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display  = ('name', 'tier', 'price', 'delivery_days', 'revisions', 'is_popular')
    list_editable = ('is_popular',)
    inlines       = [PackageFeatureInline]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ('title', 'category', 'is_featured', 'views_count', 'created_at')
    list_editable = ('is_featured',)
    list_filter   = ('category',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display        = ('title', 'published', 'views', 'created_at')
    list_editable       = ('published',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal   = ('tags',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ('name', 'post', 'approved', 'created_at')
    list_editable = ('approved',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(OrderInquiry)
class OrderInquiryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'package', 'status', 'created_at')
    list_editable = ('status',)
    list_filter   = ('status',)


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display  = ('path', 'ip_address', 'created_at')
    list_filter   = ('path',)
    readonly_fields = ('path', 'ip_address', 'created_at')
