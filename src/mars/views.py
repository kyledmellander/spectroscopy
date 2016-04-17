from django.shortcuts import render, render_to_response
from .forms import ContactForm, SignUpForm
from .models import Sample
from django.template import RequestContext

# Create your views here.
def home(request):
	title = "Welcome"
	if request.user.is_authenticated():
		title = "Hello again, %s" %(request.user)
	form = SignUpForm(request.POST or None)

	context = {
		"template_title": title,
		"form": form,
	}

	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		print(instance)

		context = {
			"template_title": "Thank You"
		}
	return render(request,"base.html",context)

def contact(request):
	form = ContactForm(request.POST or None)
	context = {
		"form":form,
	}
	return render(request,"forms.html",context)

def search(request):
	request_params = request.GET.get('mineral')
	try:
		query = int(query)
	except ValueError:
		query = None
		results = None
	if query:
		results = Sample.objects.get(name=query)
	context = RequestContext(request)
	return render_to_response('results.html', {"results": results,}, context_instance=context)
	
