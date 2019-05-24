from django.db import models

<<<<<<< HEAD

# temp model name
class NaverUser(models.Model):
    # user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user')
    address = models.CharField(max_length=100)
=======
# Create your models here.

from django.db import models

# Create your models here.

class Media(models.Model):
    name = models.CharField(max_length=500)
    media = models.FileField(upload_to='videos/', null=True, verbose_name="")
    select = models.CharField(max_length=50, default="")
    price_str = models.CharField(max_length=5, default="")
    price_real = models.BigIntegerField(default=0)
    address = models.CharField(max_length=200, default="")
    description = models.TextField()


    def __str__(self):
        return self.name + ", " + self.select + ", " + str(self.price_real)

>>>>>>> upstream/develop
