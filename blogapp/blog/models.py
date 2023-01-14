from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.


class BaseModel(models.Model):   
    uid= models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    created_at=models.DateField(auto_now_add=True,auto_now=False)
    updated_at=models.DateField(auto_now=True,auto_now_add=False)

    class Meta:
        abstract=True

class Blog(BaseModel):

    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog')
    title=models.CharField(max_length=100)
    description=models.TextField()
    main_image=models.ImageField(upload_to='blog_images/')

    def __str__(self):
        return self.title

class Comment(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='comment')
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='comment')
    body=models.TextField()

    def __str__(self):
        return "comment on blog-" + str(self.blog)







