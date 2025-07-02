from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.search import index
from django.utils import timezone
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.models import ParentalKey, ParentalManyToManyField
from wagtail.snippets.models import register_snippet
from django import forms
from taggit.models import TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager

class BlogIndexPage(Page):
    description = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("description")]
    
    
class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey("BlogPage",related_name="tagged_items", on_delete=models.CASCADE)
    
    
class BlogPage(Page):
    date = models.DateField("Post date", default=timezone.now)
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)
    authors = ParentalManyToManyField("blog.Author", blank=True)
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)


    content_panels = Page.content_panels + [FieldPanel("date"),
                                            FieldPanel("authors", widget=forms.CheckboxSelectMultiple),
                                            FieldPanel("intro"),
                                            FieldPanel("body"),
                                            InlinePanel("image_gallery", label="Image Gallery"),
                                            FieldPanel("tags"),
                                            ]
    
    
class BlogPageImageGallery(Orderable):
    page = ParentalKey("BlogPage", related_name="image_gallery", on_delete=models.CASCADE)
    image = models.ForeignKey("wagtailimages.Image", related_name="+", on_delete=models.CASCADE)
    caption = models.CharField(max_length=255, blank=True)
    
    panels = [FieldPanel("image"), FieldPanel("caption")]
    
    
@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey("wagtailimages.Image", related_name="+", on_delete=models.CASCADE)
    
    panels = [FieldPanel("name"), FieldPanel("author_image")]
    
    def __str__(self):
        return self.name
    
    
class TagIndexPage(Page):
    pass