from django.db import models


# Create your models here.

class Media(models.Model):
    name = models.CharField(max_length=500, verbose_name="건물 종류")
    media = models.FileField(upload_to='videos/', null=True, verbose_name="미디어파일")
    select = models.CharField(max_length=50, default="", verbose_name="매매종류")
    price_str = models.CharField(max_length=5, default="", verbose_name="가격")
    price_real = models.BigIntegerField(default=0)
    address = models.CharField(max_length=200, default="", verbose_name="주소")
    address_detail = models.CharField(max_length=100, default="", verbose_name="상세주소")
    space = models.CharField(max_length=10, default="", verbose_name="공간 면적")
    description = models.TextField(verbose_name="설명")
    const_date = models.CharField(max_length=100, verbose_name='준공년월')
    construction_firm = models.CharField(max_length=20, verbose_name='건설사')
    low_high = models.CharField(max_length=10, verbose_name='저/고층')
    household = models.PositiveSmallIntegerField(verbose_name='세대수')

    def __str__(self):
        return f'{self.name}, {self.select}, {self.price_real}'
