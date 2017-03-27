"""meinberlin URL Configuration."""

from allauth import urls as allauth_urls
from ckeditor_uploader import views as ck_views
from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.i18n import javascript_catalog
from rest_framework import routers
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls

from adhocracy4.comments.api import CommentViewSet
from adhocracy4.ratings.api import RatingViewSet

from apps.budgeting import urls as budgeting_urls
from apps.dashboard import urls as dashboard_urls
from apps.documents import urls as paragraph_urls
from apps.documents.api import DocumentViewSet
from apps.embed import urls as embed_urls
from apps.ideas import urls as ideas_urls
from apps.projects import urls as projects_urls

js_info_dict = {
    'packages': ('adhocracy4.comments',),
}

router = routers.DefaultRouter()
router.register(r'ratings', RatingViewSet, base_name='ratings')
router.register(r'comments', CommentViewSet, base_name='comments')
router.register(r'documents', DocumentViewSet, base_name='documents')


urlpatterns = [
    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^dashboard/', include(dashboard_urls)),
    url(r'^embed/', include(embed_urls)),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^accounts/', include(allauth_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^projects/', include(projects_urls)),

    url(r'^ideas/', include(ideas_urls)),
    url(r'^paragraphs/', include(paragraph_urls)),
    url(r'^budgeting/', include(budgeting_urls)),

    url(r'^api/', include(router.urls)),

    url(r'^upload/',
        login_required(ck_views.upload), name='ckeditor_upload'),
    url(r'^browse/',
        never_cache(login_required(ck_views.browse)), name='ckeditor_browse'),

    url(r'^jsi18n/$', javascript_catalog,
        js_info_dict, name='javascript-catalog'),
    url(r'', include(wagtail_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media locally
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
