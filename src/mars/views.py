from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.mail import send_mail

from .forms import ContactForm, SignUpForm
from .models import Sample, SignUp

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
	return render(request,"home.html",context)

def contact(request):
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
          try:
            send_mail(
                request.POST.get('subject', ''),
                request.POST.get('message', ''),
                request.POST.get('your_email', ''),
                ['digren@students.wwu.edu'],
            )
            return HttpResponseRedirect('sent/')
          except Exception, err:
            return HttpResponse(str(err))

    return render(request, 'contact.html', {
        'form': form_class,
    })

def sent(request):
	context = RequestContext(request)
	return render(request, 'sent.html', context_instance=context)

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
