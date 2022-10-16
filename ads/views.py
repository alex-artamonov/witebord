from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.generic import DetailView
import ads.models as ads


# Create your views here.


def index(request):
    ads_list = ads.Ad.objects.all()
    output = '<br><hr>'.join([f'<h3>{ad.title}:</h3><p>{ad.content}</p>' for ad in ads_list])
    # return HttpResponse(output)
    context = {'ads_list': ads_list}
    s = render(request, 'ads/ads.html', context)
    print(s)
    return s


def ad_detail(request, ad_id):
    # ad = ads.Ad.objects.get(pk=pk)
    ad = ads.Ad.objects.get(pk=ad_id)
    context = {'ad': ad}
    ad = get_object_or_404(ads.Ad, pk=ad_id)
    return render(request, 'ads/ad_detail.html', context)

class GuildDetailView(DetailView):
    model = ads.Guild
    template_name = 'ads/ad_detail.html'
    context_object_name = 'guild'
