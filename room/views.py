from django.shortcuts import render
from django.views.generic.edit import CreateView
import requests
# from .forms import AddressForm # AddressForm : {class} 주소 입력창의 form

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import Q

from .models import Media
import math


# Create your views here.
@receiver(pre_save, sender=Media)
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


def search(request):
    cb_list = request.GET.getlist('cb', None)
    search_key = request.GET.get('search_key', None)

    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)

    search_p = None
    obj_list = None

    if not (search_key or cb_list or min_price or max_price):
        obj_list = Media.objects.all()

        return render(request, 'room/search_list.html',
                      {
                          'object_list': obj_list,
                      }
                      )

    # 최소, 최대가격 조건이 둘 중 하나 또는 둘다 있는경우
    if min_price or max_price:
        dic = {'만': 1, '억': 10000, }

        # 최소 가격 조건만 있는 경우
        if min_price and not max_price:
            price_min_num = int(min_price[:-1])
            price_min_str = dic[min_price[-1]]
            min_price = price_min_num * price_min_str
            search_p = Q(price_real__gte=min_price)

            obj_list = Media.objects.filter(search_p)

        # 최대 가격 조건만 있는 경우
        elif max_price and not min_price:
            price_max_num = int(max_price[:-1])
            price_max_str = dic[max_price[-1]]
            max_price = price_max_str * price_max_num
            search_p = Q(price_real__lte=max_price)

            obj_list = Media.objects.filter(search_p)

        # 둘다 있는 경우
        else:
            price_min_num = int(min_price[:-1])
            price_min_str = dic[min_price[-1]]
            min_price = price_min_num * price_min_str

            price_max_num = int(max_price[:-1])
            price_max_str = dic[max_price[-1]]
            max_price = price_max_str * price_max_num

            search_p = Q(price_real__gte=min_price) & Q(price_real__lte=max_price)
            obj_list = Media.objects.filter(search_p)

    # 검색어와 가격 조건이 둘다 있는 경우
    if search_key and search_p:
        search_p = Q(address__icontains=search_key) | Q(name__icontains=search_key)
        obj_list = obj_list & Media.objects.filter(search_p)
    # 둘중 하나만 있는 경우
    else:
        # 검색어만 있는 경우
        if search_key or not obj_list:
            search_p = Q(address__icontains=search_key) | Q(name__icontains=search_key)
            obj_list = Media.objects.filter(search_p)

        # 가격 조건만 있는 경우는 이미 위에서 obj_list를 만듬

    if cb_list:
        temp_p = search_p & Q(select__icontains=cb_list[0]) if search_key else Q(select__icontains=cb_list[0])
        length = len(cb_list)
        if length >= 2:
            for i in range(1, length):
                temp_p &= Q(select__icontains=cb_list[i])

        if not obj_list:
            obj_list = Media.objects.filter(temp_p)

        else:
            obj_list = obj_list & Media.objects.filter(temp_p)

    return render(request, 'room/search_list.html',
                  {
                      'object_list': obj_list,
                  }
                  )


def detail(request, pk):
    if request.method == "GET":
        document = Media.objects.get(pk=pk)
        vdo = str(document.media)[-3:-1]
        address = document.address
        # full_address = 도로명 주소 + 상세 주소
        # 예)성수동 상원길 63 쌍용아파트 107동 101호 = 상원길 63 + 쌍용아파트 107동 101호

        # naver geocoding API - setting
        naver_url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query=" + address
        custom_headers = {
            "X-NCP-APIGW-API-KEY-ID": 'b4wnbq4cd7',
            "X-NCP-APIGW-API-KEY": "8o4ERGCLrQgfFb9qoXRmJELLQBI6N3kHxUjELMXX"
        }
        # road address API - setting
        confmkey = "U01TX0FVVEgyMDE5MDUyMzAwNDAwMzEwODc0Nzc="
        road_url = "http://www.juso.go.kr/addrlink/addrLinkApi.do?keyword=" + address + "&confmKey=" + confmkey + "&resultType=json"

        # requests of both API
        naver_req = requests.get(naver_url, headers=custom_headers)
        road_req = requests.get(road_url)
        jb_address = road_req.json()["results"]["juso"][0]['jibunAddr']
        rd_address = road_req.json()["results"]["juso"][0]['roadAddr']
        coord_lat = naver_req.json()["addresses"][0]["x"]
        coord_long = naver_req.json()["addresses"][0]["y"]
        return render(request, 'room/media_detail.html', {'object': document,
                                                          'extension': vdo,
                                                          'address': address, 'coord_lat': coord_lat,
                                                          'coord_long': coord_long, 'jb_address': jb_address,
                                                          'rd_address': rd_address})

