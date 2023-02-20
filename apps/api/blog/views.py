from rest_framework import permissions, viewsets, status
from apps.blog.models import Article, Tag
from rest_framework.response import Response
from apps.api.blog.serializers import ArticleWriteSerializer, ArticleReadSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleReadSerializer
    queryset = Article.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return ArticleWriteSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [permission() for permission in [permissions.IsAdminUser]]
        return [permission() for permission in [permissions.AllowAny]]

    def get_queryset(self):
        queryset = Article.objects.all()

        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(categories=category)

        user = self.request.query_params.get('user')
        if user:
            queryset = queryset.filter(user=user)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tags = []
        for tag_name in serializer.validated_data.get('tags'):
            tag = Tag.objects.filter(name=tag_name).first()
            if not tag:
                tag = Tag.objects.create(name=tag_name)
            tags.append(tag)

        article = serializer.save(user=self.request.user, tags=tags)

        read_serializer = self.serializer_class(article, context={"request": request})

        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        tags = []
        for tag_name in serializer.validated_data.get('tags'):
            tag = Tag.objects.filter(name=tag_name).first()
            if not tag:
                tag = Tag.objects.create(name=tag_name)
            tags.append(tag)

        article = serializer.save(user=self.request.user, tags=tags)

        read_serializer = self.serializer_class(article, context={"request": request})

        return Response(read_serializer.data, status=status.HTTP_201_CREATED)