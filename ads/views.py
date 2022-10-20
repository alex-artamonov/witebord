from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.base import ContextMixin
from django.db.models import Count

import ads.models as ads
import users.models as um


# Create your views here.

class CustomContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['guilds'] = ads.Guild.objects.annotate(cnt=Count('user'))
        context['users'] = um.User.objects.all()
        return context


def index(request):
    ads_list = ads.Ad.objects.all()
    output = '<br><hr>'.join([f'<h3>{ad.title}:</h3><p>{ad.content}</p>' for ad in ads_list])
    # return HttpResponse(output)
    context = {'ads_list': ads_list}
    return render(request, 'ads/ads.html', context)


def ad_detail(request, ad_id):
    # ad = ads.Ad.objects.get(pk=pk)
    ad = ads.Ad.objects.get(pk=ad_id)
    context = {'ad': ad}
    ad = get_object_or_404(ads.Ad, pk=ad_id)
    return render(request, 'ads/ad_detail.html', context)


class AdsListView(CustomContextMixin, ListView):
    model = ads.Ad
    template_name = 'ads/ads.html'
    context_object_name = 'ads_list'


class GuildsListView(CustomContextMixin, ListView):
    model = ads.Guild
    template_name = 'ads/guilds_list.html'
    context_object_name = 'guilds_list'


class GuildDetailView(CustomContextMixin, DetailView):
    model = ads.Guild
    template_name = 'ads/guild.html'
    context_object_name = 'guild'

class UserProfileView(CustomContextMixin, DetailView):
    model = um.User
    template_name = 'ads/profile.html'
    context_object_name = 'user'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['guilds'] = ads.Guild.objects.all()
    #     return context


def rules(request):
    return render(request,'ads/rules.html')

class RulesView(CustomContextMixin, TemplateView):
    template_name = 'ads/rules.html'
    # context_object_name = 'user'


def profile(request):
    if request.method == 'POST':
        print(request)
    # return HttpResponse("hi from profile view")
    return render(request, 'ads/rules.html')