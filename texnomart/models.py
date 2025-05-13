from django.db import models
from django.utils.text import slugify
# Create your models here.

class Category(models.Model):
    """THIS is category model Beginning"""
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, null=True,blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = 'Categories'
        
class Product(models.Model):
    """This model is for products
    Category is FOREIGNKEY"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='images/products/', null=True, blank=True)
    price = models.DecimalField(max_digits=14,decimal_places=2)
    quantity = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.description} - {self.category}"
    

    
    
    
    