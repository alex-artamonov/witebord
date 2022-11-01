from django.urls import path

import ads.views as av

app_name = "ads"


urlpatterns = [
    path("ads", av.AdsListView.as_view(), name="home"),
    path("ads/<int:pk>", av.ad_detail, name="ad_detail"),
    # path('ads/<int:pk>', av.AdDetailView.as_view(), name='ad_detail'),
    path("guilds", av.GuildsListView.as_view(), name="guilds_list"),
    path("guilds/<int:pk>", av.GuildDetailView.as_view(), name="guild_detail"),
    path("rules", av.RulesView.as_view(), name="rules"),
    path("ads/<int:ad_id>/new_reply", av.ad_detail, name="post_reply"),
    path("ads/create", av.AdCreateView.as_view(), name="create_ad"),
    path("ads/<int:pk>/update", av.AdUpdateView.as_view(), name="update_ad"),
    path("ads/<int:pk>/delete", av.AdDeleteView.as_view(), name="delete_ad"),
    # path("ads/my_ads", av.AdsRepliesUpdateView.as_view(), name="ads_replies_list_view"),
    path("ads/my_ads", av.ads_replies_list_view, name="ads_replies_list_view"),
    path("ads/my_ads/reply/<int:pk>/delete", av.ads_replies_list_view, name="ads_reply_delete"),
]
