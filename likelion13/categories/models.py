from django.db import models
from accounts.models import User
from posts.models import BaseModel

# Create your models here.

class Category(BaseModel):
    categoryId = models.AutoField(primary_key = True)
    categoryTitle = models.CharField(max_length = 30)

    def __str__(self):
        return self.categoryTitle

#카테고리와 연결
class CategoryLink(BaseModel):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name = "categorylink") #post와 연결
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = "categorylink", null=True, blank=True)

    def __str__(self):
        return f"{self.post.title} - {self.category.categoryTitle}"
