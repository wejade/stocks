from django.shortcuts import render,render_to_response
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import Http404
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.http import HttpResponse,HttpResponseNotFound

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from .models import company,Stock
from .forms  import searchform

import pdb

CACHE_TTL 	=	getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@cache_page(CACHE_TTL)
def Company(request):
	form 	=searchform()
	data	=	company.objects.order_by('Name')
	paginator=Paginator(data, 30)
	page=request.GET.get('page',1)
	try:
		data1=paginator.page(page)
	except PageNotAnInteger:
		data1=paginator.page(1)
	except EmptyPage:
		data1=paginator.page(paginator.num_pages)
	
	return render(request, 'list-company.html',{"data":data1,"form":form})
	
	

def search(request):
	if(request.method=='POST'):
		form=searchform(request.POST)
		if(form.is_valid()):
			id=request.POST['symbol']
			data=company.objects.filter(Symbol=id)
			form=searchform()
			return render(request, 'list-company.html',{"data":data,"form":form})


@cache_page(CACHE_TTL)
def prices(request,id):
	
	data=Stock.objects.filter(symbol=id)
	if not data:
		return HttpResponseNotFound('<h1>Prices not found</h1>')
	else:
		fig = Figure()
		canvas 	= 	FigureCanvas(fig)
		axes1 	= 	fig.add_subplot(2,2,1)
		axes2 	=	fig.add_subplot(2,2,2)
		axes3	=	fig.add_subplot(2,2,3)
		axes4 	=	fig.add_subplot(2,2,4)
		l=[]
		for stock in data:
			l.append(stock.openp)
		
		ls=np.array(l)
		axes1.plot(ls)
		
		l=[]
		for stock in data:
			l.append(stock.closep)
		ls=np.array(l)
		axes2.plot(ls)
		l=[]
		for stock in data:
			l.append(stock.low)
		ls=np.array(l)
		axes3.plot(ls)
		l=[]
		for stock in data:
			l.append(stock.high)
		ls=np.array(l)
		axes4.plot(ls)
		
		axes2.set_title('closep prices')
		axes3.set_title('Low prices')
		axes4.set_title('High prices')

		
		response=HttpResponse(content_type='image/png')
		canvas.print_png(response)
		return response
	
def index(request):
	t="title"
	return render(request, 'index.html',{"t":t})