from apps.api.blog.views import ArticleViewSet
from rest_framework.routers import DefaultRouter

urlpatterns = []

router = DefaultRouter()
router.register('article', ArticleViewSet, basename='article')

urlpatterns += router.urls