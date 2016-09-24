import os, sys, time
from PIL import Image

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify


from tourism_configs.settings import BASE_DIR
# Create your models here.

class PostManager (models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager,self).filter(draft=False).filter(published_date__lte=timezone.now())

def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,
            null=True,
            blank=True,
            height_field="height_field",
            width_field="width_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = PostManager()

    class Meta:
        ordering = ["-published_date","-updated"]

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Post, self).save()
        if self.image:
            size = (300, 300)
            image_path = str(self.image.path)
            im = Image.open(image_path)
            im.thumbnail(medium_size)
            original_image_full_path = os.path.join(BASE_DIR, self.image.path)
            os.remove(original_image_full_path)

            im.save(original_image_full_path)
            super(Post, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse("post:detail", kwargs={"slug":self.slug})

    def publish(self):
        self.published_date = timezone.now()
        self.save()



def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)
