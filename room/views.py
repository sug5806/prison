from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import NaverUser
import requests
# from .forms import AddressForm


# Create your views here.
class NaverAPI(CreateView):
    model = NaverUser
    fields = ['address']
    template_name = "naver_api/index.html"
    success_url = '/'
    def post(self, request):
    # def map(self, search):
    #     result = search()
    #     form = AddressForm()
        address = request.POSTtgit.get('address')

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

        # output results

        jb_address = road_req.json()["results"]["juso"][0]['jibunAddr']
        rd_address = road_req.json()["results"]["juso"][0]['roadAddr']
        coord_lat = naver_req.json()["addresses"][0]["x"]
        coord_long = naver_req.json()["addresses"][0]["y"]

        return render(request, self.template_name, {'form': form, 'coord_lat': coord_lat,
                                                    'coord_long': coord_long, 'jb_address': jb_address,
                                                    'rd_address': rd_address})
