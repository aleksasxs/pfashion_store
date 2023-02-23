from django.shortcuts import render
from django.views import generic
from apps.main.models import Page
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


class PageView(generic.DetailView):
    model = Page
    template_name = 'main/page.html'
    queryset = Page.objects.all()

    def set_breadcrumbs(self):
        self.page = Page.objects.get(slug=self.kwargs['slug'])
        breadcrumbs = {'current': self.page.name}
        return breadcrumbs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'breadcrumbs': self.set_breadcrumbs()})
        return context
