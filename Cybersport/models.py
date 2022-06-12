from django.db import models


class Category(models.Model):
    class Meta:
        db_table = 'category'

    name = models.CharField(max_length=100)

    def __repr__(self):
        return f"Category(name='{self.name}')"


class New(models.Model):
    class Meta:
        db_table = 'new'
        ordering = ['-date']

    title = models.CharField(max_length=300)
    text = models.CharField(max_length=5000)
    slug = models.CharField(max_length=100)
    date = models.DateTimeField()
    image_url = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField()

    def __repr__(self):
        return f"New(title='{self.title}')"



