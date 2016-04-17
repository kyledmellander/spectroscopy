from django.shortcuts import render, render_to_response
from .forms import ContactForm, SignUpForm
from .models import Sample

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
	request_params = request.GET['mineral']
	t = loader.get_template('templates/results.html')
	c = Context({ 'query': request_params,})
	return HttpResponse(t.render(c))
