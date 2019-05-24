from django.db import models


# temp model name
class NaverUser(models.Model):
    # user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user')
    address = models.CharField(max_length=100)
