from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.mail import send_mail
from .models import Sample
from django.conf import settings

from .forms import ContactForm, SignUpForm, SearchForm, UploadFileForm
from .models import Sample, SignUp
from django.utils.encoding import smart_str

import csv
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.

# def home(request):
# 	title = "Welcome"
# 	if request.user.is_authenticated():
# 		title = "Hello again, %s" %(request.user)
# 	form = SignUpForm(request.POST or None)
#
# 	context = {
# 		"template_title": title,
# 		"form": form,
# 	}
#
# 	if form.is_valid():
# 		instance = form.save(commit=False)
# 		instance.save()
# 		print(instance)
#
# 		context = {
# 			"template_title": "Thank You"
# 		}
# 	return render(request,"home.html",context)

# def contact(request):
#     form_class = ContactForm
#
#     if request.method == 'POST':
#         form = form_class(data=request.POST)
#
#         if form.is_valid():
#           try:
#             send_mail(
#                 request.POST.get('subject', ''),
#                 request.POST.get('message', ''),
#                 request.POST.get('your_email', ''),
#                 ['digren@students.wwu.edu'],
#             )
#             return HttpResponseRedirect('sent/')
#           except Exception, err:
#             return HttpResponse(str(err))
#
#     return render(request, 'contact.html', {
#         'form': form_class,
#     })

# def sent(request):
# 	context = RequestContext(request)
# 	return render(request, 'sent.html', context_instance=context)
#
# def about(request):
# 	context = RequestContext(request)
# 	return render(request, 'about.html', context_instance=context)

def meta(request):
	if request.method == 'POST':
		if 'meta' in request.POST:
			selections = request.POST.getlist('selection')
	        samples = Sample.objects.filter(data_id__in=selections)

		return render_to_response('meta.html', {"metaResults": samples,}, context_instance=RequestContext(request))

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
		  results = results.filter(name__icontains=mName)
		if mClass:
			results = results.filter(sample_class__icontains=mClass)
		if mOrigin:
			results = results.filter(origin__icontains=mOrigin)

		return render_to_response('results.html', {"results": results,}, context_instance=RequestContext(request))

	else:
		return render(request, 'search.html', {
			'form': form_class,
		})

def graph(request):
  if request.method == 'POST':
    if 'graphForm' in request.POST:
      selections = request.POST.getlist('selection')
      samples = Sample.objects.filter(data_id__in=selections)
      dictionaries = [ obj.as_dict() for obj in samples]
      for obj in dictionaries:
        for key in obj["reflectance"].keys():
          if (obj["reflectance"][key] == "NULL"):
            del obj["reflectance"][key]
         
      
      json_string = json.dumps(dictionaries);
      
      return render_to_response('graph.html', {"graphResults": samples,"graphJSON":json_string,}, context_instance=RequestContext(request))

    elif 'export' in request.POST:
      selections = request.POST.getlist('selection')
      samples = Sample.objects.filter(data_id__in=selections)

      # Create the HttpResponse object with the appropriate CSV header
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="metadatafile.csv"'

      # Make sure whatever text reader you open this csv file with is set to Unicode (UTF-8)
      writer = csv.writer(response)
      writer.writerow([
        smart_str("Data ID"),
        smart_str("Sample ID"),
        smart_str("Date Accessed"),
        smart_str("Database of Origin"),
        smart_str("Locality"),
        smart_str("Mineral Name"),
        smart_str("Sample Description"),
        smart_str("Sample Type"),
        smart_str("Mineral Class"),
        smart_str("Grain Size"),
        smart_str("Viewing Geometry"),
        smart_str("Resolution"),
        smart_str("Reflectance Range"),
        smart_str("Formula"),
        smart_str("Composition"),
        smart_str("Wavelength v Reflectance"),])
      for s in samples:
        writer.writerow([
          smart_str(s.data_id),
          smart_str(s.sample_id),
          smart_str(s.date_accessed),
          smart_str(s.origin),
          smart_str(s.locality),
          smart_str(s.name),
          smart_str(s.sample_desc),
          smart_str(s.sample_type),
          smart_str(s.sample_class),
          smart_str(s.grain_size),
          smart_str(s.view_geom),
          smart_str(s.resolution),
          smart_str(s.refl_range),
          smart_str(s.formula),
          smart_str(s.composition),
          smart_str(s.reflectance),])

      return response

#def my_view(request):
 # username = request.POST['username']
  #password = request.POST['password']
 # user = authenticate(username=username, password=password)
 # if user is not None:
 #   if user.is_active:
 #     login(request, user)
 #     return redirect('%s?next=%s') % (settings.LOGIN_URL, request.path))
 #   else:
 #     print("The password is valid, but the account has been disabled!")
 # else:
 #   print("The user and password were incorrect.")


@login_required
def upload_file(request):
  if request.method == 'POST':
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      handle_uploaded_file(request.FILES['file'])
      return HttpResponseRedirect('/success/url/')
  else:
    form = UploadFileForm()
  return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(f):
  filepath = '/tmp/somefile.txt'
  with open(filepath, 'wb+') as dest:
    for chunk in f.chunks():
      dest.write(chunk)
    process_file(filepath)

def process_file(filepath):
  subprocess.Popen(["python","../static_in_pro/our_static/py/dataParser.py","filepath"], close_fds=True)



  
