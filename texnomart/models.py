from django.db import models, transaction
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User
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
    

class Korzinka(models.Model):
    """Korzinka savatcha modeli"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='korzinka')
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    
    class Meta:
        verbose_name_plural = "Korzinka Items"
        indexes = [
            models.Index(fields=['user', 'product']),
            models.Index(fields=['created_at']),
        ]
        constraints = [
            UniqueConstraint(fields=['user', 'product'], name='unique_user_product')
        ]

    def __str__(self):
        return f"{self.user.username}'s cart - {self.product.name} x {self.quantity}"

    def save(self, *args, **kwargs):
        """
        Quantity hamda total costni hisoblash uchun
        """
        self.total_price = self.product.price * self.quantity
        #transacction ni oldim internetdan
        # Use a transaction to ensure atomicity (either both updates happen or neither happens)
        with transaction.atomic():
            super().save(*args, **kwargs)  # oldin saqla

            # Update pr quanitty
            product = Product.objects.select_for_update().get(pk=self.product.pk)
            if product.quantity >= self.quantity:
                product.quantity -= self.quantity
                product.save()
            else:
                raise ValueError(f"Not enough stock of {product.name}. Available: {product.quantity}, requested: {self.quantity}")
   
     
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')    
    comment = models.TextField()
    image=models.ImageField(upload_to='images/comments/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} - {self.product} - {self.comment}"

    