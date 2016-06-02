from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.mail import send_mail
from .models import Sample
from django.conf import settings
from django.template.defaulttags import register
from .forms import ContactForm, SignUpForm, SearchForm, UploadFileForm
from .models import Sample, SignUp
from django.utils.encoding import smart_str
from django.contrib.staticfiles import finders
from zipfile import ZipFile

import re
import copy
import itertools
import StringIO

import os, sys
import zipfile
import StringIO
import csv
import json
import subprocess
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

@register.filter
def get_reflectance(dictionary, key):
  for item in dictionary:
    if item.get("data_id") == key:
      reflectancedict = sorted(item.get("reflectance").iteritems())
      stringlist = []
      for key,value in reflectancedict:
        stringlist.append(str(key) + ":" +  str(value) + ",\n")
      return ''.join(stringlist)
  return None

def meta(request):
  if request.method == 'POST':
    if 'meta' in request.POST:
      selections = request.POST.getlist('selection')
      samples = Sample.objects.filter(data_id__in=selections)
    samples
    dictionaries = [ obj.as_dict() for obj in samples]
    return render_to_response('meta.html', {"metaResults": samples,"reflectancedict":dictionaries,}, context_instance=RequestContext(request))

def search(request):
  form_class = SearchForm
  results = Sample.objects.all()

  if request.method == 'POST':
    form = form_class(data=request.POST)

	#	if form.is_valid():
    mName =  request.POST.get('mineral_name')
    mClass = request.POST.get('mineral_class')
    mDataId = request.POST.get('mineral_Id')
    mOrigin = request.POST.get('database_of_origin')

    if mName:
      results = results.filter(name__icontains=mName)
    if mClass:
      results = results.filter(sample_class__icontains=mClass)
    if mDataId:
      results = results.filter(data_id__icontains=mDataId)
    if mOrigin:
      if mOrigin != 'Any':
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
      json_string = json.dumps(dictionaries)

      return render_to_response('graph.html', {"graphResults": samples,"graphJSON":json_string,}, context_instance=RequestContext(request))

    elif 'export' in request.POST:
      selections = request.POST.getlist('selection')
      samples = Sample.objects.filter(data_id__in=selections)
      dictionaries = [obj.as_dict() for obj in samples]
      reflectanceDict = {}
      for item in dictionaries:
        sortedList = sorted(item["reflectance"].iteritems())
        stringlist = []
        for key,value in sortedList:
          stringlist.append(str(key) + ":" +  str(value) + ",")

        reflectanceDict[item["data_id"]] =  ''.join(stringlist)

      files = []
      names = []
      count = 0
      for s in samples:
        # Create the HttpResponse object with the appropriate CSV header
        file = StringIO.StringIO()
        writer = csv.writer(file)
        names.append(smart_str(s.data_id))

        # Make sure whatever text reader you open this csv file with is set to Unicode (UTF-8)
        writer.writerow([smart_str("Database of Origin"), smart_str(s.origin),])
        writer.writerow([smart_str("Locality"), smart_str(s.locality),])
        writer.writerow([smart_str("Sample Description"), smart_str(s.sample_desc),])
        writer.writerow([smart_str("Date Accessed"), smart_str(s.date_accessed),])
        writer.writerow([])
        writer.writerow([smart_str("Data ID"), smart_str(s.data_id),])
        writer.writerow([smart_str("Sample ID"), smart_str(s.sample_id),])
        writer.writerow([smart_str("Mineral Name"), smart_str(s.name),])
        writer.writerow([smart_str("Sample Type"), smart_str(s.sample_type),])
        writer.writerow([smart_str("Mineral Class"), smart_str(s.sample_class),])
        writer.writerow([smart_str("Grain Size"), smart_str(s.grain_size),])
        writer.writerow([smart_str("Viewing Geometry"), smart_str(s.view_geom),])
        writer.writerow([smart_str("Resolution"), smart_str(s.resolution),])
        writer.writerow([smart_str("Reflectance Range"), smart_str(s.refl_range),])
        writer.writerow([smart_str("Formula"), smart_str(s.formula),])
        writer.writerow([smart_str("Composition"), smart_str(s.composition),])
        writer.writerow([])
        writer.writerow([])
        writer.writerow([])
        writer.writerow([smart_str("Wavelength"), smart_str("Reflectance"),])
        refl = reflectanceDict[s.data_id].split(',')
        count = count + 1
        for r in range(0,len(refl)-1):
          line = refl[r].split(':')
          writer.writerow([line[0], line[1],])
        file.seek(0)
        files.append(file)
      zipped_file = StringIO.StringIO()
      with zipfile.ZipFile(zipped_file, 'w') as zip:
        for i, file in enumerate(files):
          file.seek(0)
          zip.writestr(names[i]+".csv".format(i), file.read())
      zipped_file.seek(0)

      response = HttpResponse(zipped_file, content_type='application/octet-stream')
      response['Content-Disposition'] = 'attachment; filename=zippy.zip'

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


@login_required(login_url='/admin/login/')
def upload_file(request):
  if request.method == 'POST':
    form = UploadFileForm(request.POST, request.FILES)
    mclass = request.POST.get('sample_class')
    if not mclass:
      mclass = "NULL"
    mtype = request.POST.get('sample_type')
    if not mtype:
      mtype = "NULL"
    print mclass
    print mtype
    if form.is_valid():
      process_file(request.FILES['file'], mclass, mtype)
      return HttpResponseRedirect('/admin/mars/sample')
  else:
    form = UploadFileForm()
  return render(request, 'upload.html', {'form': form})

#def handle_loaded_file(f):
#  file = '/tmp/somefile.csv'
#  with open(file, 'wb+') as dest:
#    for chunk in f.chunks():
#      dest.write(chunk)
#    process_file(file)

def hasNumbers(inputString):
  result = bool(re.search(r'\d', inputString))
  return result

def process_file(file, mineral_class, mineral_type):
    dataArray = [] #Array of IDs
    sampArray = [] #Sample IDs
    nameArray = [] #names
    grainArray = []
    vGeoArray = []
    resArray = []
    rangArray = []
    formArray = []
    compArray = []

    try:
        paramFile = file.read()
        reader = csv.reader(file)
        origin = reader.next()[1]
        collection = reader.next()[1]
        desc = reader.next()[1]
        access = reader.next()[1]
        reader.next()

        # Data ID
        data = reader.next()
        if data[1] != '':
          i =1
        else:
          i = 2
        idArray = []
        idStringArray = []
        while i < len(data):
          id_num = data[i].rsplit("_", 1)
          if len(id_num) > 1:
            idStringArray.append(id_num[0])
            num = int(id_num[1])
            idArray.append(num)
            i+=1

        j = 1
        sizeIdArray = len(idArray)
        finalIdArray = []
        finalIdArray.append(idArray[0])
        while j < sizeIdArray:
          if idArray[j] == idArray[j-1]:
            newNum = idArray[j] + 1
            idArray[j] = newNum
            finalIdArray.append(newNum)
          else:
            finalIdArray.append(idArray[j])
            j += 1

        k = 0
        while k < sizeIdArray:
          newId = str(idStringArray[k]) + "_" + str(finalIdArray[k]).zfill(2)
          dataArray.append(newId)
          k += 1

        # Sample ID
        samp = reader.next()
        i = 2
        while i < len(samp):
          sampArray.append(samp[i])
          i+=1

        # Mineral name
        name = reader.next()
        i = 2
        while i < len(name):
          nameArray.append(name[i])
          i+=1

        scale = "nanometers"
        size = reader.next()
        if ("um" or "micron") in size[0]:
          scale = "microns"
        i = 2

        #Get grain size
        while i < len(size):
          grainArray.append(size[i])
          i+=1

        scale = "nanometers"

        # Viewing Geometry
        vg = reader.next()
        i = 2
        while i < len(vg):
          vGeoArray.append(vg[i])
          i+=1

        # Resolution
        res = reader.next()
        i = 2

        while i < len(res):
          resArray.append(res[i])
          i+=1

        # Range
        rang = reader.next()
        i = 2
        if "um" in rang[0] or "micron" in rang[0]:
          factor = 1000
        else:
          factor = 1
        while i < len(rang):
          if rang[i] != "":
            temp1 = []
            if scale == "microns":
              temp = rang[i].split('-')
              if temp[1].find("um") != -1:
                ty = temp[1].split("u")
                temp1.append(float(temp[0]) * factor)
                temp1.append(float(ty[0]) * factor)
              else:
                temp1.append(float(temp[0]) * factor)
                temp1.append(float(temp[1]) * factor)
            else:
              temp = rang[i].split('-')
              if temp[1].find("nm") != -1:
                ty = temp[1].split("n")
                temp1.append(float(temp[0]))
                temp1.append(float(ty[0]))
              else:
                temp1.append(float(temp[0]))
                temp1.append(float(temp[1]))
            rangArray.append(temp1)
          else:
            #empty case - don't put in database
            rangArray.append(rang[i])
          i+=1
        scale = "nanometers"

        formula = reader.next()
        i = 2
        while i < len(formula):
          formArray.append(formula[i])
          i+=1

        comp = reader.next()
        i = 2
        while i < len(comp):
          compArray.append(comp[i])
          i+=1

        line = reader.next()
        while ("Wavelength" not in line[0]):
          line = reader.next()

        if ("microns" or "um") in line:
          factor = 1000
        else:
          factor = 1

        wl = reader.next()

        row_len = len(wl)

        dataPoints = [{}] * (row_len - 2)
        for row in reader:
          if hasNumbers(row[0]) == True:
            for column in xrange(2,row_len):
              if float(row[column]) > 1.0:
                dataPoints[column-2][str(float(row[0]) * factor)] = str(float(row[column]) / 100.)

              # Check for invalid datapoints #
              elif float(row[column]) < 0.0:
                continue

              else:
                dataPoints[column-2][str(float(row[0]) * factor)] = row[column]

    except Exception, e:
      print str(e)

    size = len(dataArray)
    
    for i in range(size):
        dataId = dataArray[i]
        sampId = sampArray[i]
        name = nameArray[i]
        gr = grainArray[i]
        vGeo= vGeoArray[i]
        res = resArray[i]

        low = min([float(w) for w in dataPoints[i]])
        high = max([float(w) for w in dataPoints[i]])
        tempRan = [int(round(low, -2)), int(round(high, -2))]
        # for j in range(len(tempRan)):
        #     if tempRan[j] == None:
        #         tempRan[j] = 'NULL'

        form = formArray[i]
        comp = compArray[i]

        sample = Sample.create(dataId, sampId, access, origin, collection, name, desc, mineral_type, mineral_class, gr, vGeo, res, tempRan, form, comp, dataPoints[i])
        sample.save()
