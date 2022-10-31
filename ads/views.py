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
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.core.mail import send_mail
import random
from django.contrib import messages

import ads.models as ads
import users.models as um
from .forms import ReplyForm
import ads.forms as af

# Create your views here.

# class CustomContextMixin(ContextMixin):
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['guilds'] = ads.Guild.objects.annotate(cnt=Count('user'))
#         # context['users'] = um.User.objects.all()
#         return context


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
    # return HttpResponse(output)
    context = {"ads_list": ads_list}
    return render(request, "ads/ads.html", context)


class AdDetailView(DetailView):
    model = ads.Ad
    context_object_name = "ad"

    # def dispatch(self, request, *args, **kwargs):

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


# @login_required(login_url=settings.LOGIN_URL)
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
    model = ads.Ad
    context_object_name = "ads_list"
    paginate_by = 6


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
    # context_object_name = 'user'


def profile(request):
    if request.method == "POST":
        print(request)
    # return HttpResponse("hi from profile view")
    return render(request, "ads/rules.html")


@login_required
def ads_replies_list_view(request):
    user = request.user
    # replies = ads.Reply.objects.exclude(accepted=Falsedir
    ads_list = ads.Ad.objects.filter(author=user)


    return render(request, "ads/my_ad_list.html", {'ads_list': ads_list})

