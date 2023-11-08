from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
   path('accounts/profile/', profile, name='profile'),
   path('accounts/register/', RegistrateUser.as_view(), name='register_user'),
   path('accounts/login/', BBLoginView.as_view(), name='login'),
   path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
   path('<str:page>/', other_page, name='other'),
   path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
   path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
   path('accounts/password/change/', BBPasswordChangeView.as_view(), name='password_change'),
   path('accounts/profile/', profile, name='profile'),
   path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
   path('', index, name='index'),
   path('', ViewPolls.as_view(), name='view_polls'),
   path('polls/create', CreatePoll.as_view(), name='poll_create'),
   path('home/', PollHome.as_view(), name='poll_home')
   # path('accounts/home/', home, name='home'),
   # path('accounts/create/', create, name='create'),
   # path('accounts/vote/<poll_id>/', vote, name='vote'),
   # path('accounts/results/<poll_id>/', results, name='results'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
