from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
	#url(r'^accounts/login/$', auth_views.login, {'template_name': 'Election_Portal/login.html'},name='login'),
	url(r'^filter/$',views.filter,name='filter'),
	url(r'^$',views.home,name='home'),
	url(r'^home/$',views.home,name='home'),
	url(r'^details/(?P<pk>\d+)/$',views.details,name='details'),
	url(r'^orderdetails/(?P<pk>\d+)/(?P<username>[\w.@+-]+)/$',views.orderdetails,name='orderdetails'),
	url(r'^cart/(?P<username>[\w.@+-]+)/$',views.cart,name='cart'),
	url(r'^myorder/(?P<username>[\w.@+-]+)/$',views.myorder,name='myorder'),
	url(r'^add_to_cart/(?P<pk>\d+)/(?P<username>[\w.@+-]+)/(?P<sz>\d+)/$',views.add_to_cart,name='add_to_cart'),
	url(r'^remove_from_cart/(?P<pk>\d+)/(?P<username>[\w.@+-]+)/(?P<sz>\d+)/$',views.remove_from_cart,name='remove_from_cart'),
	#url(r'^payment/(?P<username>[\w.@+-]+)/$',views.payment,name='payment'),
	url(r'^men_sec/',views.men_sec,name='men_sec'),
	url(r'^women_sec/',views.women_sec,name='women_sec'),
	url(r'^kids_sec/',views.kids_sec,name='kids_sec'),
	url(r'^query/',views.query,name='query'),
	url(r'^tquery/',views.tquery,name='tquery'),
	url(r'^queryadmin/',views.queryadmin,name='queryadmin'),
	url(r'^querydetails/(?P<pk>\d+)/$',views.querydetails,name='querydetails'),
	url(r'^useradmin/',views.useradmin,name='useradmin'),
	url(r'^userdetails/(?P<usern>[\w.@+-]+)/$',views.userdetails,name='userdetails'),
	url(r'^myadmin/$',views.myadmin,name='myadmin'),
	url(r'^addpic/(?P<pk>\d+)/$',views.addpic,name='addpic'),
	url(r'^prodadmin/$',views.prodadmin,name='prodadmin'),
	url(r'^proddetails/(?P<pk>\d+)/$',views.proddetails,name='proddetails'),
	url(r'^addnew/$',views.addnew,name='addnew'),
	url(r'^changeq/(?P<pk>\d+)/(?P<username>[\w.@+-]+)/(?P<sz>\d+)/$',views.changeq,name='changeq'),
	url(r'^orderadmin/$',views.orderadmin,name='orderadmin'),
	url(r'^orderdetailsadmin/(?P<pk>\d+)/$',views.orderdetailsadmin,name='orderdetailsadmin'),
	url(r'^addship/(?P<pk>\d+)/$',views.addship,name='addship'),
	url(r'^shipperadmin/$',views.shipperadmin,name='shipperadmin'),
	url(r'^addnewshipper/$',views.addnewshipper,name='addnewshipper'),
	url(r'^shipperdetails/(?P<pk>\d+)/$',views.shipperdetails,name='shipperdetails'),
	url(r'^reachedstatus/(?P<pk>\d+)/$',views.reachedstatus,name='reachedstatus'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)