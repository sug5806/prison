from django.shortcuts import render
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Media
import math
# Create your views here.


@receiver(pre_save, sender = Media)
def pre_save(sender, instance, **kwagrs):
    dic = {'만': 1, '억': 10000, }
    price = instance.price_str
    price_n = int(price[:-1])
    price_s = dic[price[-1]]

    instance.price_real = price_n * price_s


def showmedia(request):

    page = int(request.GET.get('page', 1))
    paginated_by = 5
    rooms = Media.objects.all()

    total_count = len(rooms)
    start_index = paginated_by * (page - 1)
    end_index = paginated_by * page
    rooms = rooms[start_index:end_index]
    rng = range(1, math.ceil(total_count / paginated_by) + 1)

    context = {
        'object_list': rooms,
        'range': rng,

    }


    return render(request, 'room/media_list.html', context)

