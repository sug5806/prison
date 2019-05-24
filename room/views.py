from django.shortcuts import render
from .models import Media
import math
# Create your views here.

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

