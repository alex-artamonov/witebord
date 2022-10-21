from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.base import ContextMixin
from django.db.models import Count

import ads.models as ads
import users.models as um
from ads.forms import ReplyForm


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
    replies = ads.Reply.objects.filter(parent_ad_id=ad.pk)
    # context = {'ad': ad, 'replies': replies}
    ad = get_object_or_404(ads.Ad, pk=ad_id)
    # return render(request, 'ads/ad_detail.html', context)
    user = request.user
    new_reply = None

    if request.method == 'POST':
        # A comment was posted
        reply_form = ReplyForm(data=request.POST)
        if reply_form.is_valid():            
            # Create Comment object but don't save to database yet          
            new_reply = reply_form.save(commit=False)
            new_reply.author = user
            # Assign the current post to the comment
            new_reply.parent_ad = ad
            # Save the comment to the database
            new_reply.save()
            # return redirect('/post_reply')
    else:
        reply_form = ReplyForm()                   
    return render(request,
                  'ads/ad_detail.html',
                  {'ad': ad,
                  'user': user,
                  'replies': replies,
                  'new_reply': new_reply,
                  'reply_form': reply_form})


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