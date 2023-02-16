from rest_framework import generics, permissions, viewsets
from apps.blog.models import Article
from apps.api.blog.serializers import ArticleSerializer


class ArticleListView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.all()

        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(categories=category)

        user = self.request.query_params.get('user')
        if user:
            queryset = queryset.filter(user=user)

        return queryset


class ArticleDetailView(generics.RetrieveAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

class ArticleCreateView(generics.CreateAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ArticleUpdateView(generics.UpdateAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [permissions.IsAdminUser]

class ArticleDeleteView(generics.DestroyAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [permissions.IsAdminUser]



# class ArticleViewSet(viewsets.ModelViewSet):
#     serializer_class = ArticleSerializer
#     queryset = Article.objects.all()
#
#     def get_permissions(self):
#         if self.action in ['create', 'update', 'destroy']:
#             return [permission() for permission in [permissions.IsAdminUser]]
#         return [permission() for permission in [permissions.AllowAny]]