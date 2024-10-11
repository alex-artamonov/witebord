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
from django.views.generic.base import ContextMixin
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from requests import session
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponse
import ads.models as ads
import users.models as um
from ads.forms import ReplyForm
import ads.forms as af

from django.contrib.auth import get_user_model
# Create your views here.

# class CustomContextMixin(ContextMixin):
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['guilds'] = ads.Guild.objects.annotate(cnt=Count('user'))
#         # context['users'] = um.User.objects.all()
#         return context


class AdCreateView(LoginRequiredMixin, CreateView):
    # model = ads.Ad
    form_class = af.AdForm
    template_name = "ads/ad_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, UpdateView):
    form_class = af.AdForm
    template_name = "ads/ad_form.html"

    def get_object(self, **kwargs):
        pk = self.kwargs.get("pk")
        obj = ads.Ad.objects.get(pk=pk)
        if obj.author != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj


class AdDeleteView(LoginRequiredMixin, DeleteView):
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
    # return HttpResponse(output)
    context = {"ads_list": ads_list}
    return render(request, "ads/ads.html", context)


class AdDetailView(DetailView):
    model = ads.Ad
    context_object_name = "ad"

    # def __init__(request, *args, **kwargs) -> None:
    #     super().__init__()
    #     ses = session()
    #     print('hello', ses.get() )
    #     # user = request.user

    def get_context_data(self, **kwargs):
        # xxx will be available in the template as the related objects
        context = super().get_context_data(**kwargs)
        # AnotherModel.objects.filter(var=self.get_object())
        context["replies"] = ads.Reply.objects.filter(
            parent_ad=self.get_object()
        ).select_related("author")

        return context

    # @login_required(login_url='settings.LOGIN_URL')
    def post(self, request, *args, **kwargs):
        user = self.request.user
        replies = ads.Reply.objects.filter(
            parent_ad_id=self.get_object()
        ).select_related("author")
        new_reply = None
        reply_form = ReplyForm(data=request.POST)
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


@login_required(login_url=settings.LOGIN_URL)
def ad_detail(request, pk):
    ad = ads.Ad.objects.get(pk=pk)
    # ad = get_object_or_404(ads.Ad, pk=pk)
    replies = ads.Reply.objects.filter(parent_ad_id=ad.pk).select_related("author")
    # context = {'ad': ad, 'replies': replies}
    # return render(request, 'ads/ad_detail.html', context)
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
            # return redirect('/post_reply')
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


class AdsListView(ListView, LoginRequiredMixin):
    model = ads.Ad
    context_object_name = "ads_list"
    paginate_by = 6


class GuildsListView(LoginRequiredMixin, ListView):
    model = ads.Guild
    context_object_name = "guilds_list"


class GuildDetailView(LoginRequiredMixin, DetailView):
    model = ads.Guild
    context_object_name = "guild"


class UserProfileView(LoginRequiredMixin, DetailView):
    model = um.User
    context_object_name = "user"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['guilds'] = ads.Guild.objects.all()
    #     return context


def rules(request):
    return render(request, "ads/rules.html")


class RulesView(TemplateView):
    template_name = "ads/rules.html"
    # context_object_name = 'user'


def profile(request):
    if request.method == "POST":
        print(request)
    # return HttpResponse("hi from profile view")
    return render(request, "ads/rules.html")


# def ad_search(request):
#     form = af.SearchForm()
#     query = None
#     results = []
#     if 'query' in request.GET:
#         form = af.SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             results = ads.Ad.objects.annotate(search=SearchVector(
#                 'title', 'content')).filter(search=query)
#     return render(request, 'ads/search.html',
#                   {'form': form,
#                    'query': query,
#                    'results': results})


def ad_search(request):
    form = af.SearchForm()
    query_name = "query"
    results = []
    if query_name in request.GET:
        query_text = request.GET[query_name]
        results = ads.Ad.objects.annotate(
            search=SearchVector("title", "content")
        ).filter(search=query_text)
    return render(
        request,
        "ads/search.html",
        {"form": form, "query": query_text, "results": results},
    )


    