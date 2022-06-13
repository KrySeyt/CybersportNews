from django.db import models


class Category(models.Model):
    class Meta:
        db_table = 'category'
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'

    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Category(name='{self.name}')"


class New(models.Model):
    class Meta:
        db_table = 'new'
        ordering = ['-date']

    title = models.CharField(max_length=300)
    text = models.CharField(max_length=5000)
    slug = models.CharField(max_length=300)
    date = models.DateTimeField()
    image_url = models.CharField(max_length=300, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField()

    def __repr__(self):
        return f"New(title='{self.title}')"



