"""mydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from core.views import ShowHelloWorld
from core.rest.views import TranslationViewSet, UserProfileViewSet, UserViewSet, CurrentUserView, MyTokenObtainPairView, ConfigurationsViewSet, \
    QuestionsViewSet, GroupQuestionsViewSet

from housearch.rest.views import TerritorialCoverageViewSet, TerritorialUnitViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'configurations', ConfigurationsViewSet)
router.register(r'translations', TranslationViewSet)
router.register(r'questions', QuestionsViewSet)
router.register(r'groups-questions', GroupQuestionsViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'territorial-coverage', TerritorialCoverageViewSet)
router.register(r'territorial-unit', TerritorialUnitViewSet)


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    url(r'^{}admin/'.format(settings.ADMIN_URL_PREFIX), admin.site.urls),
    url(r'^$', ShowHelloWorld.as_view()),
    url(r'^_nested_admin/', include('nested_admin.urls')),
    path('api/', include(router.urls)),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/me/', CurrentUserView.as_view(), name='current_user_view'),
    path('sentry-debug/', trigger_error),
    path('tinymce/', include('tinymce.urls')),
    path('', include('drfpasswordless.urls')),
]
urlpatterns += static(settings.STATIC_URL_PATTERN,
                      document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL_PATTERN,
                      document_root=settings.MEDIA_ROOT)
