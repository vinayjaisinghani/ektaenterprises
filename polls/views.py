from django.shortcuts import render, render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, Template,RequestContext
import datetime
import hashlib
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.context_processors import csrf
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseNotFound  
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from base64 import b64encode
from shoeshowroom.forms import addprod
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from collections import namedtuple
from django.template import RequestContext
import datetime

import MySQLdb;
def connect():
	db=MySQLdb.connect(host="localhost",user="root",passwd="phoddiyabe",db="reqs")
	cur=db.cursor()
	return db,cur
# Create your views here.


def giveimages(p):
	db,cur=connect()
	pq = """ SELECT img1,img2,img3 FROM product WHERE myid='%d' """%(p)
	cur.execute(pq)
	data = cur.fetchone()
	images=[data[0],data[1],data[2]]
	for i in range(len(images)):
		images[i]=b64encode(images[i])
	return images

def getprods(l):
	db,cur=connect()
	images=giveimages(l[0]);
	l2=[]
	for i in l:
		l2.append(i)
	l2[6]=images[0]
	l2[7]=images[1]
	l2[8]=images[2]
	row = namedtuple('row', ['myid', 'floater', 'company','modelname','gender','price','img1','img2','img3','size','neck_height','outer_material','occasion','weight','pack_of','availability'])
	return row._make(l2)


def giveallprods():
	db,cur=connect()
	query="SELECT * FROM product";
	cur.execute(query)
	all_products=cur.fetchall()
	p=[]
	for i in range(len(all_products)):
		p.append(getprods(all_products[i]))
	return p

def giveprod(p):
	db,cur=connect()
	query="SELECT * FROM product WHERE myid='%d' "%(p)
	cur.execute(query)
	productx=cur.fetchall()[0]
	productx=getprods(productx)
	return productx




@login_required
@csrf_protect
@csrf_exempt
def payment(request,username):
	db,cur=connect()
	# Amount Calculaion
	userx=get_object_or_404(User,username=username)
	current_user = request.user
	if(current_user==userx):
		pass
	else:
		return HttpResponseNotFound('<h1>No Page Here</h1>')


	query="SELECT * FROM relation"
	cur.execute(query);
	every=cur.fetchall();

	all_products=giveallprods()

	list1=[i[4] for i in every if i[1]==userx.username]
	list_of_products=[i for i in all_products if i.myid in list1]
	quantity_product=[]
	for i in list_of_products:
		for j in every:
			if(i.myid==j[4] and userx.username==j[1]):
				quantity_product.append(j[3])
				break
	product_quan=[[list_of_products[i],quantity_product[i]] for i in range(len(list_of_products))]
	tpr=0
	dvc=0
	tc=0
	for i in product_quan:
		tpr=tpr+i[0].price*i[1];
	if tpr<200:
		dvc=49
	tc=dvc+tpr
	amount=int(tc)
	MERCHANT_KEY = "zkHhZ9b8"
	key="zkHhZ9b8"
	SALT = "DfbyayHWeu"
	PAYU_BASE_URL = "https://secure.payu.in/_payment"
	action = ''
	posted={}
	posted['email']=str(userx.email).upper()
	for i in request.POST:
		posted[i]=request.POST[i]

	hash_object = hashlib.sha256(b'randint(0,20)')
	txnid=hash_object.hexdigest()[0:20]
	hashh = ''
	posted['txnid']=txnid
	posted['amount']=amount
	posted['firstname']=str(userx.first_name).upper()
	posted['lastname']=str(userx.last_name).upper()
	hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
	posted['key']=key
	posted['surl']="https://127.0.0.1:8000/Failure"
	posted['furl']="127.0.0.1:8000/Failure"
	hash_string=''
	hashVarsSeq=hashSequence.split('|')
	for i in hashVarsSeq:
		try:
			hash_string+=str(posted[i])
		except Exception:
			hash_string+=''
		hash_string+='|'
	hash_string+=SALT
	print "woo",hash_string,"woo"
	hashh=hashlib.sha512(hash_string).hexdigest().lower()
	print "hii",hashh
	action =PAYU_BASE_URL
	query="SELECT productid,quantity FROM relation where userid='%s'"%(userx.username)
	cur.execute(query)
	every=cur.fetchall()
	if(len(every)==0):
		return redirect('home')
	flag=0
	for i in every:
		query="SELECT availability from product where myid='%s'"%(i[0])
		cur.execute(query)
		u=int(cur.fetchall()[0][0])
		if(u<i[1]):
			flag=1
			query="DELETE FROM relation where userid='%s' and productid='%s'"%(userx.username,i[0])
			cur.execute(query)
			db.commit()
	if flag:
		return HttpResponseNotFound('<h1>Seems Like Certain Items Had Changes In Availability. Items That Had More Quantity Than Availability In Your Cart Have Been Deleted.</h1>')
	if(posted.get("key")!=None and posted.get("txnid")!=None and posted.get("productinfo")!=None and posted.get("firstname")!=None and posted.get("email")!=None):

		datex=datetime.datetime.now()
		date=str(datex.day)+"/"+str(datex.month)+"/"+str(datex.year)
		addr=posted['address1']+"; "+posted['address2']+"; "+posted['city']+"; "+posted['state']+"; "+posted['country']+"; "+posted['zipcode']
		query="INSERT INTO orderx(order_date,shipping_address,amount,payment_left,shipping_status,reached) VALUES('%s','%s','%s','%s','%s','%s')"%(date,addr,amount,amount,0,0)
		cur.execute(query)
		db.commit()
		query="SELECT * FROM orderx ORDER BY order_id DESC LIMIT 1"
		cur.execute(query)
		siz=cur.fetchall()[0]
		siz=siz[0]
		query="SELECT * FROM relation WHERE userid='%s'"%(userx.username)
		cur.execute(query)
		everyx=cur.fetchall()
		for i in everyx:
			query="INSERT INTO orderrel VALUES('%s','%s','%s','%s','%s')"%(siz,i[1],i[2],i[3],i[4])
			cur.execute(query)
			db.commit()
			query="UPDATE product SET availability=availability-'%d' where myid='%s'"%(int(i[3]),i[4])
			cur.execute(query)
			db.commit()
		query="DELETE FROM relation WHERE userid='%s'"%(userx.username)
		cur.execute(query)
		db.commit()

		return render_to_response('polls/current_datetime.html',{'user':userx,"posted":posted,"hashh":hashh,"MERCHANT_KEY":MERCHANT_KEY,"txnid":txnid,"hash_string":hash_string,"action":"https://secure.payu.in/_payment" })
	else:
		return render_to_response('polls/current_datetime.html',{'user':userx,"posted":posted,"hashh":hashh,"MERCHANT_KEY":MERCHANT_KEY,"txnid":txnid,"hash_string":hash_string,"action":"." })

@csrf_protect
@csrf_exempt
def success(request):
	c = {}
    	c.update(csrf(request))
	status=request.POST["status"]
	firstname=request.POST["firstname"]
	amount=request.POST["amount"]
	txnid=request.POST["txnid"]
	posted_hash=request.POST["hash"]
	key=request.POST["key"]
	productinfo=request.POST["productinfo"]
	email=request.POST["email"]
	salt="DfbyayHWeu"
	try:
		additionalCharges=request.POST["additionalCharges"]
		retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	except Exception:
		retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	hashh=hashlib.sha512(retHashSeq).hexdigest().lower()
	if(hashh !=posted_hash):
		print "Invalid Transaction. Please try again"
	else:
		print "Thank You. Your order status is ", status
		print "Your Transaction ID for this transaction is ",txnid
		print "We have received a payment of Rs. ", amount ,". Your order will soon be shipped."
	return render_to_response('sucess.html',RequestContext(request,{"txnid":txnid,"status":status,"amount":amount}))


@csrf_protect
@csrf_exempt
def failure(request):
	c = {}
    	c.update(csrf(request))
	status=request.POST["status"]
	firstname=request.POST["firstname"]
	amount=request.POST["amount"]
	txnid=request.POST["txnid"]
	posted_hash=request.POST["hash"]
	key=request.POST["key"]
	productinfo=request.POST["productinfo"]
	email=request.POST["email"]
	salt="DfbyayHWeu"
	try:
		additionalCharges=request.POST["additionalCharges"]
		retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	except Exception:
		retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	hashh=hashlib.sha512(retHashSeq).hexdigest().lower()
	if(hashh !=posted_hash):
		print "Invalid Transaction. Please try again"
	else:
		print "Thank You. Your order status is ", status
		print "Your Transaction ID for this transaction is ",txnid
		print "We have received a payment of Rs. ", amount ,". Your order will soon be shipped."
 	return render_to_response("Failure.html",RequestContext(request,c))

	
