from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.mail import send_mail

from .models import Sample

from .forms import ContactForm, SignUpForm, SearchForm, GraphForm
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

def about(request):
	context = RequestContext(request)
	return render(request, 'about.html', context_instance=context)

def search(request):
	form_class = SearchForm
	results = Sample.objects.all()

	if request.method == 'POST':
		form = form_class(data=request.POST)

	#	if form.is_valid():
		mName =  request.POST.get('mineral_name')
		mClass = request.POST.get('mineral_class')
		mOrigin = request.POST.get('database_of_origin')

		if mName:
			results = results.filter(name=mName)
		if mClass:
			results = results.filter(sample_class=mClass)
		if mOrigin:
			results = results.filter(origin=mOrigin)

                toGraph = GraphForm(queryset=results, fields=('name',
                                                              'sample_class',
                                                              'origin'))

                return render(request, 'tograph.html', {
                        'form': toGraph,
                 })
		#return render_to_response('tograph.html', {"results": results,}, context_instance=RequestContext(request))

	else:
		return render(request, 'search.html', {
			'form': form_class,
		})

def graph(request):
	if request.method == 'POST':
		selections = request.POST.getlist('graphing')
		print selections
    return render_to_response('graph.html', {"graphResults": selections,}, context_instance=RequestContext(request))
