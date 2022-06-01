from django.urls import path
from .import views


urlpatterns=[
path('',views.singIn),
path('postsign',views.postsign),
path('post_create',views.post_create),
path('Download',views.Download),
path('DownloadPdf',views.DownloadPdf),
path('DuplicatesValues',views.DuplicatesValues)

]