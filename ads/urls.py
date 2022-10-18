from django.urls import path

import ads.views as av

urlpatterns = [
    path('ads', av.index, name='ads'),
    path('ads/<int:ad_id>', av.ad_detail, name='ad_detail'),
    path('guilds', av.GuildsListView.as_view(), name='guilds_list'),
    path('guilds/<int:pk>', av.GuildDetailView.as_view(), name='guild_detail'),
    path('accounts/<int:pk>', av.UserProfileView.as_view(), name='user_profile'),
    path('rules', av.rules, name='rules' ),
]