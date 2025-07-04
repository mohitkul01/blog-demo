# microblog/models.py
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel  # Import FieldPanel
from blog.models import BlogIndexPage


class HomePage(Page):
    body = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # Fetch live BlogIndexPage children
        context['blog_indices'] = BlogIndexPage.objects.child_of(self).live()
        return context