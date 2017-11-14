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
from shoeshowroom.forms import addprod, addship
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from collections import namedtuple
#from .models import product

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

def read_file(filename):
	db,cur=connect()
	with open(filename, 'rb') as f:
   	    photo = f.read()
   	    return photo


def insert_blob(file1,file2,file3):
	db,cur=connect()
	# read file
	data1=read_file(filename)
	data2=read_file(filename)
	data3=read_file(filename)
 
	# prepare update query and data
	query = "insert into product(img1,img2,img3) values(%s,%s,%s)"
 
	args = (data1,data2,data3)
	db=MySQLdb.connect(host="localhost",user="root",passwd="phoddiyabe",db="reqs")
	cur=db.cursor()
	cur.execute(query, args)
	db.commit()
	cur.close()
	db.close()


@login_required
def orderdetails(request,pk,username):
	db,cur=connect()
	p=int(pk)
	userx=get_object_or_404(User,username=username)
	current_user = request.user
	if(current_user==userx):
		pass
	else:
		return HttpResponseNotFound('<h1>No Page Here</h1>')
	query="SELECT * FROM orderrel WHERE order_id='%s'"%(p)
	cur.execute(query)
	every=cur.fetchall()
	all_products=giveallprods()
	list1=[[i[0],i[2],i[3],i[4]] for i in every]
	#print list1
	#list1=[[i.productid,i.size,i.quantity,i.relid] for i in every if i.userid==userx.username]
	product_quan=[]
	for i in list1:
		for j in all_products:
			if(i[3]==j.myid):
				product_quan.append([j,i[2],i[1],i[3]])
	return render(request,"shoeshowroom/orderdetails.html",{'product_quan':product_quan,'user':userx})

@login_required
def cart(request,username):
	db,cur=connect()
	userx=get_object_or_404(User,username=username)
	current_user = request.user
	if(current_user==userx):
		pass
	else:
		return HttpResponseNotFound('<h1>No Page Here</h1>')
	query="SELECT * FROM relation"
	cur.execute(query);
	every=cur.fetchall();
	#print every
	#every=relation.objects.all()
	all_products=giveallprods()
	list1=[[i[0],i[2],i[3],i[4]] for i in every if i[1]==userx.username]
	#print list1
	#list1=[[i.productid,i.size,i.quantity,i.relid] for i in every if i.userid==userx.username]
	product_quan=[]
	for i in list1:
		for j in all_products:
			if(i[3]==j.myid):
				product_quan.append([j,i[2],i[1],i[3]])
	tpr=0
	dvc=0
	tc=0
	for i in product_quan:
		tpr=tpr+i[0].price*i[1];
	if tpr<600 and tpr>0:
		dvc=49
	tc=dvc+tpr
	if tpr>0:
		return render(request,"shoeshowroom/cart.html",{'product_quan':product_quan,'tpr':tpr,'dvc':dvc,'tc':tc,'user':userx})
	else:
		return render(request,"shoeshowroom/emptycart.html",{})


@login_required
def myorder(request,username):
	db,cur=connect()
	userx=get_object_or_404(User,username=username)
	current_user = request.user
	if(current_user==userx):
		pass
	else:
		return HttpResponseNotFound('<h1>No Page Here</h1>')
	query="SELECT DISTINCT order_id from orderrel where userid='%s'"%(userx.username)
	cur.execute(query)
	every=cur.fetchall()

	orders=[]
	for i in every:
		query="SELECT * FROM orderx where order_id='%s'"%(i[0])
		cur.execute(query)
		orders.append(cur.fetchall()[0])
	le=len(orders)
	f=0
	if(le==0):
		f=1
	return render(request,"shoeshowroom/orders.html",{'orders':orders,'f':f})

def tquery(request):
	db,cur=connect()
	if request.method=="POST":
		namex=request.POST['name']
		emailx=request.POST['email']
		queryx=request.POST['query']
		#queryentry=querysub(name=namex,email=emailx,query=queryx)
		#queryentry.save()
		query="INSERT INTO querysub(name,email,query) values('%s','%s','%s')"%(namex,emailx,queryx)
		cur.execute(query);
		db.commit();
		query="SELECT * FROM querysub"
		cur.execute(query);
		queries=cur.fetchall();
		#queries=querysub.objects.all()
		return render(request,'shoeshowroom/query.html',{'queries':queries})
	else:
		return render(request,'shoeshowroom/tquery.html',{})

def query(request):
	db,cur=connect()
	query="SELECT * FROM querysub"
	cur.execute(query);
	queries=cur.fetchall();
	#queries=querysub.objects.all()
	return render(request,'shoeshowroom/query.html',{'queries':queries})

def men_sec(request):
	db,cur=connect()
	all_products=giveallprods()
	list1=[i for i in all_products if i.gender=='m']
	all_products=list1
	return render(request,'shoeshowroom/filtered.html',{'all_products':all_products})

def women_sec(request):
	db,cur=connect()
	all_products=giveallprods()
	list1=[i for i in all_products if i.gender=='f']
	all_products=list1
	return render(request,'shoeshowroom/filtered.html',{'all_products':all_products})

def kids_sec(request):
	db,cur=connect()
	all_products=giveallprods()
	list1=[i for i in all_products if i.gender=='k']
	all_products=list1
	return render(request,'shoeshowroom/filtered.html',{'all_products':all_products})


def filter(request):
	db,cur=connect()
	if request.method=="POST":
		fgender=request.POST.getlist('gender')
		fcollection=request.POST.getlist('collection')
		fsize=request.POST.getlist('size')
		minval=request.POST.get('minval')
		maxval=request.POST.get('maxval')
		all_products=giveallprods()
		if len(fgender)>0:
			list1=[i for i in all_products if i.gender in fgender]
			all_products=list1
		if len(fcollection)>0:
			list1=[i for i in all_products if i.floater in fcollection]
			all_products=list1
		if len(fsize)>0:
			alpha=[int(i) for i in fsize]
			print alpha
			list1=[]
			for i in all_products:
				if (i.size in alpha):
					list1.append(i)
			all_products=list1
		if minval:
			mi=int(minval)
			list1=[i for i in all_products if i.price>=mi]
			all_products=list1
		if maxval:
			ma=int(maxval)
			if(ma!=4000):
				list1=[i for i in all_products if i.price<=ma]
				all_products=list1
		word=request.POST['wordqu']
		if(len(word)):
			temp=[]
			flag=0
			for i in all_products:
				u=0
				for j in i:
					k1=j
					k2=word
					k1=str(k1)
					k2=str(k2)
					if(k1.upper()==k2.upper()):
						u=1
						flag=1
						temp.append(i)
				if(u==0):
					fl=i.floater
					fl=fl.split('_')
					k1=fl[0]
					k2=word
					k1=str(k1)
					k2=str(word)
					k3=fl[1]
					k3=str(k3)
					if(k1.upper()==k2.upper()):
						flag=1
						temp.append(i)
					elif(k3.upper()==k2.upper()):
						flag=1
						temp.append(i)


			if(flag):
				all_products=temp

		return render(request,'shoeshowroom/filtered.html',{'all_products':all_products})
	else:
		return render(request, 'shoeshowroom/filter.html',{})

def home(request):
	db,cur=connect()
	list_of_products=giveallprods()
	return render(request, 'shoeshowroom/home.html', {'list_of_products':list_of_products})

def details(request,pk):
	db,cur=connect()
	p=int(pk)
	productx=giveprod(p)
	return render(request,"shoeshowroom/details.html",{'productx':productx})




@login_required
def add_to_cart(request,pk,username,sz):
	db,cur=connect()
	userx=get_object_or_404(User,username=username)
	p=int(pk)
	productx=giveprod(p)
	siz=int(sz)
	current_user = request.user
	if(current_user==userx):
		pass
	else:
		return HttpResponseNotFound('<h1>No Page Here</h1>')
	query="SELECT * FROM relation"
	cur.execute(query)
	every=cur.fetchall()
	#every=relation.objects.all()
	#rel_temp=relation(userid=userx.username,productid=productx.myid,size=6,quantity=1)
	for i in every:
		if(i[1]==userx.username and i[4]==productx.myid):

			query="UPDATE relation SET quantity=quantity+1 where userid='%s' and productid='%d' "%(username,i[4])
			cur.execute(query);
			db.commit();
			return HttpResponseRedirect(reverse('cart',args=(userx.username,)))

	query="INSERT INTO relation(userid,size,quantity,productid) VALUES('%s','%d','%d','%d')"%(userx.username,siz,1,productx.myid)
	cur.execute(query);
	db.commit();
	#cartentry=relation(userid=userx.username,productid=productx.myid,size=10,quantity=1)
	#cartentry.save()
	return HttpResponseRedirect(reverse('cart',args=(userx.username,)))


@login_required
def remove_from_cart(request,pk,username,sz):
	db,cur=connect()
	#rel=get_object_or_404(relation,pk=pk)
	#every=relation.objects.all()
	userx=get_object_or_404(User,username=username)
	current_user = request.user
	if(current_user==userx):
		pass
	else:
		return HttpResponseNotFound('<h1>No Page Here</h1>')
	p= int(pk)
	query="DELETE FROM relation WHERE productid='%d' and userid='%s' and size='%d' " %(p,userx.username,int(sz))
	cur.execute(query);
	db.commit();
	return HttpResponseRedirect(reverse('cart',args=(userx.username,)))




@login_required
@user_passes_test(lambda u: u.is_superuser)
def queryadmin(request):
	db,cur=connect()
	query="SELECT * FROM querysub"
	cur.execute(query);
	queries=cur.fetchall();
	return render(request,"shoeshowroom/queryadmin.html",{'queries':queries})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def querydetails(request,pk):
	db,cur=connect()
	p= int(pk)
	if request.method=="POST":
		dele=request.POST.getlist('del')
		answerx=request.POST['answer']
		if(answerx):
			query="UPDATE querysub SET answer='%s' where queryid='%d' "%(answerx,p)
			cur.execute(query);
			db.commit();
		if(len(dele)):
			query="DELETE FROM querysub WHERE querysub.queryid='%d'"%(p)
			cur.execute(query);
			db.commit();
		query="SELECT * FROM querysub"
		cur.execute(query);
		queries=cur.fetchall();
		return render(request,"shoeshowroom/queryadmin.html",{'queries':queries})
	query="SELECT * FROM querysub WHERE querysub.queryid='%d' "%(p)
	cur.execute(query);
	queries=cur.fetchall();
	query=queries[0]
	return render(request,"shoeshowroom/partquery.html",{'query':query})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def useradmin(request):
	db,cur=connect()
	query="""SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name","auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user" """
	users = User.objects.raw(query)
	return render(request,"shoeshowroom/useradmin.html",{'users':users})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def userdetails(request,usern):
	db,cur=connect()
	usernm=str(usern)
	query="""SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name","auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user" """
	users = User.objects.raw(query)
	for i in users:
		p=str(i.username)
		if(p==usernm):
			usr=i
			break
	if request.method=="POST":
		dele=request.POST.getlist('del')
		mkadmin=request.POST.getlist('admin')
		passx=request.POST['pass']
		u = User.objects.get(username=usernm)
		if(len(passx)):
			if((u.username=="vinayjaisinghani" or u.username=="sushiljaisinghani") and (request.user!="vinayjaisinghani" and request.user!="sushiljaisinghani")):
				return HttpResponseNotFound('<h1>Can not change password of maker</h1>')
			u.set_password(passx)
			u.save()
		if(len(dele)):
			if(u.username=="vinayjaisinghani" or u.username=="sushiljaisinghani"):
				return HttpResponseNotFound('<h1>Can not delete maker</h1>')
			u.delete()
			query="""SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name","auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user" """
			users = User.objects.raw(query)
		if(len(mkadmin)):
			u.is_superuser=1
			u.save()
		return render(request,"shoeshowroom/useradmin.html",{'users':users})	
	return render(request,"shoeshowroom/userdetails.html",{'userx':usr})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def myadmin(request):
	db,cur=connect()
	return render(request,"shoeshowroom/myadmin.html",{})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def orderadmin(request):
	db,cur=connect()
	query="SELECT * FROM orderx";
	cur.execute(query);
	orders=cur.fetchall()
	return render(request,"shoeshowroom/orderadmin.html",{'orders':orders})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def addship(request,pk):
	db,cur=connect()
	p=int(pk)
	query="SELECT * FROM shipper"
	cur.execute(query)
	every=cur.fetchall()
	if request.method=="POST":
		sid=request.POST.get('shipper')
		sid=int(sid)
		query="UPDATE orderx SET shipping_status='%s' where order_id='%s'"%(sid,p)
		cur.execute(query)
		db.commit()
		query="INSERT into shipment values('%s','%s')"%(sid,p)
		cur.execute(query)
		db.commit()
		return redirect('myadmin')
	return render(request,"shoeshowroom/addship.html",{'shippers':every})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def shipperadmin(request):
	db,cur=connect()
	query="SELECT * FROM shipper";
	cur.execute(query);
	shippers=cur.fetchall()
	return render(request,"shoeshowroom/shipperadmin.html",{'shippers':shippers})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def addnewshipper(request):
	db,cur=connect()
	if request.method=="POST":
		company = request.POST['company']
		phone = request.POST['phone']
		email = request.POST['email']

		query="INSERT INTO shipper(company_name,phone_number,email) values ('%s','%s','%s')"%(company,phone,email)
		cur.execute(query)
		db.commit()
		return redirect('myadmin')

	return render(request,"shoeshowroom/addnewshipper.html",{})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def shipperdetails(request,pk):
	db,cur=connect()
	p=int(pk)
	query="SELECT * from shipper where shipper_id='%s'"%(p)
	cur.execute(query)
	every=cur.fetchall()[0]
	return render(request,"shoeshowroom/shipperdetails.html",{'shipper':every})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def orderdetailsadmin(request,pk):
	db,cur=connect()
	p=int(pk)
	query="SELECT * FROM orderrel WHERE order_id='%s'"%(p)
	cur.execute(query)
	every=cur.fetchall()
	all_products=giveallprods()
	list1=[[i[0],i[2],i[3],i[4]] for i in every]
	#print list1
	#list1=[[i.productid,i.size,i.quantity,i.relid] for i in every if i.userid==userx.username]
	product_quan=[]
	for i in list1:
		for j in all_products:
			if(i[3]==j.myid):
				product_quan.append([j,i[2],i[1],i[3]])
	return render(request,"shoeshowroom/orderdetailsadmin.html",{'product_quan':product_quan})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def prodadmin(request):
	db,cur=connect()
	query="SELECT * FROM product";
	cur.execute(query);
	list_of_products=cur.fetchall()
	return render(request,"shoeshowroom/prodadmin.html",{'products':list_of_products})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def proddetails(request,pk):
	db,cur=connect()
	p=int(pk)
	productx=giveprod(p)
	if request.method=="POST":
		dele=request.POST.getlist('del')
		price=(request.POST['price'])
		availability=(request.POST['availability'])

		if(price):
			price=int(price)
			if(price<=50):
				price=50
			query="UPDATE product SET price='%d' where myid='%d' "%(int(price),p)
			cur.execute(query)
			db.commit()
		if(availability):
			availability=int(availability)
			if(availability<0):
				availability=0
			query="UPDATE product SET availability='%d' where myid='%d' "%(int(availability),p)
			cur.execute(query)
			db.commit()
		if(len(dele)):
			query="DELETE FROM product WHERE myid='%d' "%(p)
			cur.execute(query)
			db.commit()
			query="DELETE FROM relation where productid='%s'"%(p)
			cur.execute(query)
			db.commit()
		return redirect('prodadmin')
	return render(request,"shoeshowroom/proddetails.html",{'productx':productx})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def addnew(request):
	db,cur=connect()
	if request.method=="POST":


		floater=request.POST.get('floater')
		floater=str(floater)

		gender=request.POST.get('gender')
		gender=str(gender)

		form = addprod(request.POST)
		if form.is_valid():
			company = form.cleaned_data.get('company')
			modelname = form.cleaned_data.get('modelname')
			price = form.cleaned_data.get('price')
			if(price<=50):
				price=50
			outer_material = form.cleaned_data.get('outer_material')
			occasion = form.cleaned_data.get('occasion')
			weight = form.cleaned_data.get('weight')
			pack_of = form.cleaned_data.get('pack_of')
			if(pack_of<=0):
				pack_of=1
			availability=form.cleaned_data.get('availability')
			if(availability<=0):
				availability=0
			size=form.cleaned_data.get('size')
			if(size<=4):
				size=4
			if(size>=10):
				size=10
			neck_height=form.cleaned_data.get('neck_height')
			query="INSERT INTO product(floater,company,modelname,gender,price,img1,img2,img3,size,neck_height,outer_material,occasion,weight,pack_of,availability) VALUES('%s','%s','%s','%s', '%d','%s','%s','%s','%d','%s','%s','%s','%s','%s','%s') "%(floater,company,modelname,gender,price,"","","",size,neck_height,outer_material,occasion,weight,pack_of,availability)
			cur.execute(query)
			db.commit()
			query="SELECT * FROM product ORDER BY myid DESC LIMIT 1"
			cur.execute(query)
			pid=cur.fetchall()[0]
			pid=pid[0]
			pid=str(pid)
			return HttpResponseRedirect(reverse('addpic',args=(pid,)))

	form=addprod
	return render(request,"shoeshowroom/addnew.html",{'form':form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def addpic(request,pk):
	db,cur=connect()
	p=int(pk)
	if request.method=="POST" and request.FILES['myfile1'] and request.FILES['myfile2'] and request.FILES['myfile2']:
		myfile1 = request.FILES['myfile1']
		fs = FileSystemStorage()
		filename1 = fs.save(myfile1.name, myfile1)
		uploaded_file_url1 = fs.url(filename1)
		uploaded_file_url1="C:\Users\Vinay Jaisinghani\Desktop\ektaenterprises"+uploaded_file_url1
		data1=read_file(uploaded_file_url1)
		myfile2 = request.FILES['myfile2']
		fs = FileSystemStorage()
		filename2 = fs.save(myfile2.name, myfile2)
		uploaded_file_url2 = fs.url(filename2)
		uploaded_file_url2="C:\Users\Vinay Jaisinghani\Desktop\ektaenterprises"+uploaded_file_url2
		data2=read_file(uploaded_file_url2)
		myfile3 = request.FILES['myfile3']
		fs = FileSystemStorage()
		filename3 = fs.save(myfile3.name, myfile3)
		uploaded_file_url3 = fs.url(filename3)
		uploaded_file_url3="C:\Users\Vinay Jaisinghani\Desktop\ektaenterprises"+uploaded_file_url3
		data3=read_file(uploaded_file_url3)
		query="UPDATE product SET img1=%s, img2=%s, img3=%s WHERE myid=%s "
		args=(data1,data2,data3,p)
		cur.execute(query,args)
		db.commit()
		return redirect('prodadmin')
	return render(request,"shoeshowroom/test.html",{'id':p})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def reachedstatus(request,pk):
	db,cur=connect()
	p=int(pk)
	query="UPDATE orderx SET reached='%s', payment_left='%s' where order_id='%s'"%(1,0,p)
	cur.execute(query)
	db.commit()
	return redirect('orderadmin')

@login_required
def changeq(request,pk,username,sz):
	db,cur=connect()
	userx=get_object_or_404(User,username=username)
	current_user = request.user
	if(current_user==userx):
		pass
	else:
		return HttpResponseNotFound('<h1>No Page Here</h1>')
	p=int(pk)
	un=str(username)
	s=int(sz)
	if request.method=="POST":
		quant=request.POST['quant']
		quant=int(quant)
		if(quant<=0):
			query="DELETE FROM relation WHERE userid='%s' and productid='%s'"%(un,p)
			cur.execute(query)
			db.commit()
			return HttpResponseRedirect(reverse('cart',args=(userx.username,)))
		query="UPDATE relation SET quantity='%d' where userid='%s' and productid='%d' and size='%d' "%(quant,un,p,s)
		cur.execute(query)
		db.commit()
		return HttpResponseRedirect(reverse('cart',args=(userx.username,)))
	return render(request,"shoeshowroom/changeq.html",{})






	
