import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings

from .models import (
    Project, Skill, ServicePackage,
    BlogPost, Tag, Comment,
    PageView, OrderInquiry
)


def track(request):
    PageView.objects.create(
        path=request.path,
        ip_address=request.META.get('REMOTE_ADDR'),
    )


def home(request):
    track(request)
    return render(request, 'portfolio/home.html', {
        'featured_projects': Project.objects.filter(is_featured=True)[:3],
        'skills':            Skill.objects.all(),
        'recent_posts':      BlogPost.objects.filter(published=True)[:2],
    })


def about(request):
    track(request)
    skills_grouped = {}
    for skill in Skill.objects.all():
        cat = skill.get_category_display()
        skills_grouped.setdefault(cat, []).append(skill)
    return render(request, 'portfolio/about.html', {
        'skills_grouped': skills_grouped,
    })


def projects(request):
    track(request)
    category = request.GET.get('cat', '')
    qs = Project.objects.all()
    if category:
        qs = qs.filter(category=category)
    return render(request, 'portfolio/projects.html', {
        'projects':        qs,
        'categories':      Project.CATEGORY_CHOICES,
        'active_category': category,
    })


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.increment_views()
    track(request)
    related = Project.objects.filter(category=project.category).exclude(pk=pk)[:3]
    return render(request, 'portfolio/project_detail.html', {
        'project': project,
        'related': related,
    })


def pricing(request):
    track(request)
    if request.method == 'POST':
        OrderInquiry.objects.create(
            name=request.POST.get('name', ''),
            email=request.POST.get('email', ''),
            package_id=request.POST.get('package_id') or None,
            project_type=request.POST.get('project_type', ''),
            budget=request.POST.get('budget') or None,
            message=request.POST.get('message', ''),
        )
        return redirect('pricing_success')
    return render(request, 'portfolio/pricing.html', {
        'packages': ServicePackage.objects.prefetch_related('features').all(),
    })


def pricing_success(request):
    return render(request, 'portfolio/pricing_success.html')


def calculate_price(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=405)
    data  = json.loads(request.body)
    base  = {'landing': 300, 'business': 800, 'webapp': 1500, 'api': 600, 'bot': 400}.get(data.get('type', 'landing'), 300)
    extra = 0
    if data.get('admin'):   extra += 200
    if data.get('auth'):    extra += 150
    if data.get('payment'): extra += 300
    if data.get('api_int'): extra += 250
    pages = int(data.get('pages', 1))
    total = (base + extra) * (1 + (pages - 1) * 0.12)
    return JsonResponse({'total': round(total), 'days': max(3, round(total / 80))})



def blog_list(request):
    track(request)
    tag_slug   = request.GET.get('tag', '')
    posts      = BlogPost.objects.filter(published=True)
    tags       = Tag.objects.annotate(cnt=Count('blogpost')).filter(cnt__gt=0)
    active_tag = None
    if tag_slug:
        active_tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=active_tag)
    return render(request, 'portfolio/blog_list.html', {
        'posts': posts, 'tags': tags, 'active_tag': active_tag,
    })


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    post.views += 1
    post.save(update_fields=['views'])
    track(request)
    if request.method == 'POST':
        Comment.objects.create(
            post=post,
            name=request.POST.get('name', ''),
            email=request.POST.get('email', ''),
            text=request.POST.get('text', ''),
        )
        return redirect('blog_detail', slug=slug)
    return render(request, 'portfolio/blog_detail.html', {
        'post':     post,
        'comments': post.comments.filter(approved=True),
    })



def contact(request):
    track(request)
    sent = False
    if request.method == 'POST':
        name    = request.POST.get('name', '')
        email   = request.POST.get('email', '')
        message = request.POST.get('message', '')

        sent = True
    return render(request, 'portfolio/contact.html', {'sent': sent})


# ══ АНАЛІТИКА (тільки для адміна) ════════════════
def analytics(request):
    if not request.user.is_staff:
        return redirect('home')
    now       = timezone.now()
    ago_30    = now - timedelta(days=30)
    ago_6m    = now - timedelta(days=180)

    by_month  = (
        OrderInquiry.objects
        .filter(created_at__gte=ago_6m)
        .annotate(month=TruncMonth('created_at'))
        .values('month').annotate(cnt=Count('id')).order_by('month')
    )
    return render(request, 'portfolio/analytics.html', {
        'total_views':   PageView.objects.count(),
        'views_30d':     PageView.objects.filter(created_at__gte=ago_30).count(),
        'total_orders':  OrderInquiry.objects.count(),
        'new_orders':    OrderInquiry.objects.filter(status='new').count(),
        'top_pages':     PageView.objects.values('path').annotate(cnt=Count('id')).order_by('-cnt')[:5],
        'top_projects':  Project.objects.order_by('-views_count')[:5],
        'chart_labels':  json.dumps([i['month'].strftime('%b %Y') for i in by_month]),
        'chart_data':    json.dumps([i['cnt'] for i in by_month]),
    })
