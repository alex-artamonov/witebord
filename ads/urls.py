from django.urls import path

import ads.views as av

app_name = 'ads'



urlpatterns = [
    # path('ads', av.index, name='ads'),
    path('ads', av.AdsListView.as_view(), name='home'),
    path('ads/<int:pk>', av.ad_detail, name='ad_detail'),
    # path('ads/<int:pk>', av.AdDetailView.as_view(), name='ad_detail'),
    path('guilds', av.GuildsListView.as_view(), name='guilds_list'),
    path('guilds/<int:pk>', av.GuildDetailView.as_view(), name='guild_detail'),
    path('accounts/<int:pk>', av.UserProfileView.as_view(), name='user_profile'),
    path('rules', av.RulesView.as_view(), name='rules' ),
    path('accounts/profile/<int:pk>', av.UserProfileView.as_view()),
    path('ads/<int:ad_id>/new_reply', av.ad_detail, name='post_reply'),
    path('ads/create', av.AdCreateView.as_view(), name='create_ad'),
    path('ads/<int:pk>/update', av.AdUpdateView.as_view(), name='update_ad'),
    path('ads/<int:pk>/delete', av.AdDeleteView.as_view(), name='delete_ad'),
    #  path('rules', av.rules, name='rules' ),
]