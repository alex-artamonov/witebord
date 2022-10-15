from django.shortcuts import render, HttpResponse
import ads.models as ads

# Create your views here.


def index(request):
    ads_list = ads.Ad.objects.all()
    output = '<br><hr>'.join([f'<h3>{ad.title}:</h3><p>{ad.content}</p>' for ad in ads_list])
    # return HttpResponse(output)
    context = {'ads_list': ads_list}
    return render(request, 'ads/ads.html', context)