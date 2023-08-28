from typing import Any, Dict
from django.conf import settings
from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from django.views.generic import (
    DetailView,
    ListView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
)

from django.db.models import Count, Exists, OuterRef
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.postgres.search import SearchVector

import ads.models as ads
import users.models as um
from .forms import ReplyForm
import ads.forms as af


class AdCreateView(CreateView):
    form_class = af.AdForm
    template_name = "ads/ad_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AdUpdateView(UpdateView):
    form_class = af.AdForm
    template_name = "ads/ad_form.html"

    def get_object(self, **kwargs):
        pk = self.kwargs.get("pk")
        obj = ads.Ad.objects.get(pk=pk)
        if obj.author != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj


class AdDeleteView(DeleteView):
    success_url = reverse_lazy("ads:home")

    def get_object(self, **kwargs):
        pk = self.kwargs.get("pk")
        obj = ads.Ad.objects.get(pk=pk)
        if obj.author != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj


def index(request):
    ads_list = ads.Ad.objects.all()
    output = "<br><hr>".join(
        [f"<h3>{ad.title}:</h3><p>{ad.content}</p>" for ad in ads_list]
    )
    context = {"ads_list": ads_list}
    return render(request, "ads/ads.html", context)


class AdDetailView(DetailView):
    model = ads.Ad
    context_object_name = "ad"

    def get_context_data(self, **kwargs):
        # xxx will be available in the template as the related objects
        context = super().get_context_data(**kwargs)
        # AnotherModel.objects.filter(var=self.get_object())
        context["replies"] = ads.Reply.objects.filter(
            parent_ad=self.get_object()
        ).select_related("author")

        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user
        replies = ads.Reply.objects.filter(
            parent_ad_id=self.get_object()
        ).select_related("author")
        new_reply = None
        reply_form = ads.ReplyForm(data=request.POST)
        if reply_form.is_valid():
            # Create Comment object but don't save to database yet
            new_reply = reply_form.save(commit=False)
            new_reply.author = user
            # Assign the current post to the comment
            new_reply.parent_ad = self.get_object()
            # Save the comment to the database
            new_reply.save()
            # return redirect('/post_reply')
        return render(
            request,
            "ads/ad_detail.html",
            {
                "ad": self.get_object(),
                "user": user,
                "replies": replies,
                "new_reply": new_reply,
                "reply_form": reply_form,
                "guilds": ads.Guild.objects.annotate(cnt=Count("user")),
                "users": um.User.objects.all(),
            },
        )


def ad_detail(request, pk):
    ad = ads.Ad.objects.get(pk=pk)
    replies = ads.Reply.objects.filter(parent_ad_id=ad.pk).select_related("author")
    user = request.user
    new_reply = None

    if request.method == "POST":
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
            messages.success(request, "Отклик успешно добавлен.")
        else:
            messages.error(request, "Произошла ошибка.")
    else:
        reply_form = ReplyForm()
    return render(
        request,
        "ads/ad_detail.html",
        {
            "ad": ad,
            "user": user,
            "replies": replies,
            "new_reply": new_reply,
            "reply_form": reply_form,
        },
    )


class AdsListView(ListView):
    context_object_name = "ads_list"
    paginate_by = 6
    

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        search_form = af.SearchForm()
        context = super().get_context_data(**kwargs)
        context['search_form'] = search_form
        return context

    def get_queryset(self):
        author_id = self.request.GET.get("author_id", None)
        if author_id:
            return ads.Ad.objects.filter(author__id=author_id)
        elif 'query' in self.request.GET:
            print('hi from query')
            search_form = af.SearchForm(self.request.GET)        
            if search_form.is_valid():
                vector = SearchVector('title', 'content')
                query = search_form.cleaned_data['query']
                # query = 'test'
                results = ads.Ad.objects.all().annotate(search=vector).filter(search=query)
            return results
            
            # return ads.Ad.objects.filter(title__icontains='test')
        else:
            return ads.Ad.objects.all()
    #     search_form = af.SearchForm()
    # # query = 'django'
    #     query = None
    #     results = []
    #     if 'query' in request.GET:
            


class MyAdsListView(LoginRequiredMixin, ListView):
    context_object_name = "ads_list"
    paginate_by = 6

    def get_queryset(self):
        return ads.Ad.objects.filter(author=self.request.user)


class GuildsListView(ListView):
    model = ads.Guild
    context_object_name = "guilds_list"


class GuildDetailView(DetailView):
    model = ads.Guild
    context_object_name = "guild"


def rules(request):
    return render(request, "ads/rules.html")


class RulesView(TemplateView):
    template_name = "ads/rules.html"


def profile(request):
    if request.method == "POST":
        print(request)
    return render(request, "ads/rules.html")


@login_required
def ads_replies_list_view(request):
    user = request.user

    to_reply = ads.Reply.objects.exclude(accepted=False).filter(
        parent_ad_id=OuterRef("pk")
    )
    ads_list = ads.Ad.objects.filter(
        Exists(to_reply),
        author=user,
    )
    print(ads_list.query)
    if request.method == "POST":
        reply = ads.Reply.objects.get(pk=int(request.POST["reply_id"]))
        reply.accepted = bool(int(request.POST["btnAction"]))
        reply.save()
        messages.info(request, "Отклик был изменен")

    return render(request, "ads/my_ad_list.html", {"ads_list": ads_list})


class AdsRepliesUpdateView(UpdateView):
    queryset = ads.Ad.objects.exclude(reply__accepted=False)
    template_name = "ads/my_ad_list.html"

    def get_queryset(self):
        return ads.Ad.objects.exclude(reply__accepted=False)

def search(request):
    search_form = af.SearchForm()
    # query = 'django'
    query = None
    results = []
    if 'query' in request.GET:
        search_form = af.SearchForm(request.GET)        
        if search_form.is_valid():
            vector = SearchVector('title', 'content')
            query = search_form.cleaned_data['query']
            # query = 'test'
            results = ads.Ad.objects.all().annotate(search=vector).filter(search=query)
    return render(request, 'ads/ad_search.html',                   
                  {'search_form': search_form,
                   'query': query,
                   'results': results,
                   'test': 'TEST',}
                  )
def search(request):
    search_form = af.SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        search_form = af.SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            search_vector = SearchVector('title', 'content')
            # search_query = SearchQuery(query)
            results = ads.Ad.objects.all().annotate(
                search=search_vector,
                # rank=SearchRank(search_vector, search_query)
                # ).filter(search=search_query).order_by('-rank')
                ).filter(search=query)
    return render(request, 'ads/ad_search.html',
                  {'search_form': search_form,
                      'query': query,
                      'results': results})




    # return render(request ,"ads/ad_search.html")
