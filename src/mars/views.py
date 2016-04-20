from django.shortcuts import render, render_to_response
from .models import Sample
from django.template import RequestContext

# Create your views here.
def home(request):
	title = "Welcome"
	
	return render(request,"base.html",context)

def contact(request):
	form = ContactForm(request.POST or None)
	context = {
		"form":form,
	}
	return render(request,"forms.html",context)

def search(request):
	query = request.GET.get('mineral')
	try:
		query = query
	except ValueError:
		query = None
		results = None
	if query:
		results = Sample.objects.filter(name=query)
	context = RequestContext(request)
	return render_to_response('results.html', {"results": results,}, context_instance=context)
