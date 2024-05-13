from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.label


class TaggedItemManager(models.Manager):
    def get_tags_for(self, object_type, object_id):
        contenttype = ContentType.objects.get_for_model(object_type) 
        
        return TaggedItem.objects \
                .select_related('tag') \
                .filter(
                    content_type=contenttype,
                    object_id=object_id
                )


# When you don't know that forign key references to what
# It depends on multiple relation (table) it can be any of it
# there we can use genericforeignkey
class TaggedItem(models.Model):
    objects = TaggedItemManager()
    # What tag is assigned to which item
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # Type of item can be (product, video, article)
    # Here Content type is define by django present in installed app
    # it helps to distinguish between multiple items
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()