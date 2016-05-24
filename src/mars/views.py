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

import re
import copy
import itertools

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
     
      
      for s in samples:
        # Create the HttpResponse object with the appropriate CSV header
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % s.data_id
        writer = csv.writer(response)
      
        # Make sure whatever text reader you open this csv file with is set to Unicode (UTF-8)
        writer.writerow([smart_str("Data ID"), smart_str(s.data_id),])
        writer.writerow([smart_str("Sample ID"), smart_str(s.sample_id),])
        writer.writerow([smart_str("Date Accessed"), smart_str(s.date_accessed),])
        writer.writerow([smart_str("Database of Origin"), smart_str(s.origin),])
        writer.writerow([smart_str("Locality"), smart_str(s.locality),])
        writer.writerow([smart_str("Mineral Name"), smart_str(s.name),])
        writer.writerow([smart_str("Sample Description"), smart_str(s.sample_desc),])
        writer.writerow([smart_str("Sample Type"), smart_str(s.sample_type),])
        writer.writerow([smart_str("Mineral Class"), smart_str(s.sample_class),])
        writer.writerow([smart_str("Grain Size"), smart_str(s.grain_size),])
        writer.writerow([smart_str("Viewing Geometry"), smart_str(s.view_geom),])
        writer.writerow([smart_str("Resolution"), smart_str(s.resolution),])
        writer.writerow([smart_str("Reflectance Range"), smart_str(s.refl_range),])
        writer.writerow([smart_str("Formula"), smart_str(s.formula),])
        writer.writerow([smart_str("Composition"), smart_str(s.composition),])
        writer.writerow([smart_str("Wavelength"), smart_str("Reflectance"),])
        refl = reflectanceDict[s.data_id].split(',')
        for r in range(0,len(refl)-1):
          line = refl[r].split(':')
          writer.writerow([line[0], line[1],])
      

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
    if form.is_valid():
      handle_uploaded_file(request.FILES['file'])
      return HttpResponseRedirect('/admin/')
  else:
    form = UploadFileForm()
  return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(f):
  filepath = '/tmp/somefile.csv'
  with open(filepath, 'wb+') as dest:
    for chunk in f.chunks():
      dest.write(chunk)
    process_file(filepath)

def process_file(filepath):
    #result = finders.find('py/dataParser.py')
    #subprocess.Popen(['python', str(result), filepath], shell=True, close_fds=True)
    def hasNumbers(inputString):
        return bool(re.search(r'\d', inputString))

    dataArray = [] #Array of IDs
    sampArray = [] #Sample IDs
    nameArray = [] #names
    grainArray = []
    vGeoArray = []
    resArray = []
    rangArray = []
    formArray = []
    compArray = []
    dataPts = []  #matrix of num_data_point rows by 1+num_samples columns
    #reflectance = []
    #A = np.array([])

    try:
        with open(filepath, 'rU') as cf:
            reader = csv.reader(cf)
            origin = reader.next()[1]
            collection = reader.next()[1]
            desc = reader.next()[1]
            access = reader.next()[1]
            reader.next()

            # Data ID
            data = reader.next()
            if data[1] != None:
                i =1
            else:
                i = 2
            #i = 2
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

            while i < len(size):
                arr = []
                if hasNumbers(size[i]) == False:
                    grainArray.append(size[i])
                else:
                    if ("um" or "micron") in size[i]:
                        temp = size[i].split()
                        temp1 = temp[0]
                        if "<" in temp1:
                            temp2 = temp1.replace("<", "")
                            if temp2.find("um") != -1:
                                temp3 = temp2.split("u")
                                arr.append(str(float(temp3[0])*1000))
                            else:
                                temp3 = float(temp2)*1000
                                arr.append(temp3)
                        elif "-" in temp1:
                            temp2 = temp1.split("-")
                            temp3 = str(float(temp2[0])*1000)
                            arr.append(temp3)

                            if temp2[1].find("um") != -1:
                                temp5 = temp2[1].split("u")
                                temp4 = str(float(temp5[0])*1000)
                            else:
                                temp4 = str(float(temp2[1])*1000)
                            arr.append(temp4)
                        else:
                            arr.append(temp1)
                    else:
                        temp = size[i].split()
                        temp1 = temp[0]
                        if "<" in temp1:
                            temp1 = temp1.replace("<", "")
                            if temp1.find("nm") != -1:
                                temp2 = temp1.split("n")
                                arr.append(temp2[0])
                            else:
                                arr.append(temp1)
                        elif "-" in temp1:
                            temp2 = temp1.split("-")
                            arr.append(temp2[0])
                            if temp2[1].find("nm") != -1:
                                temp3 = temp2[1].split("n")
                                arr.append(temp3[0])
                            else:
                                arr.append(temp2[1])
                        else:
                            arr.append(temp1)
                    grainArray.append(arr)
                i+=1
            scale = "nanometers"

            # Viewing Geometry
            vg = reader.next()
            i = 2
            while i < len(vg):
                vGeoArray.append(vg[i])
                i+=1

            # Range
            rang = reader.next()
            i = 2
            if ("um" or "micron") in rang[0]:
                scale = "microns"
            else:
                scale = "nanometers"
            while i < len(rang):
                if rang[i] != "":
                    temp1 = []
                    if scale == "microns":
                        temp = rang[i].split('-')
                        if temp[1].find("um") != -1:
                            ty = temp[1].split("u")
                            temp1.append(float(temp[0]) * 1000)
                            temp1.append(float(ty[0]) * 1000)
                        else:
                            temp1.append(float(temp[0]) * 1000)
                            temp1.append(float(temp[1]) * 1000)
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

            waveDataPt = {}
            for row in reader:
                if hasNumbers(row[0]) == True:
                    waveDataPt[row[0]] = 'NULL'

            i = 2
            while i < row_len:
                cf.seek(20)
                currDict = copy.deepcopy(waveDataPt)

                for row in itertools.islice(reader, 21, len(currDict)):
                    if hasNumbers(row[0]) == True and row[i] != '':
                        if float(row[i]) > 1.0:
                            row[i] = float(row[i]) / 100.
                        currDict[row[0]] = row[i]

                dataPts.append(currDict)
                i += 1
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

        if vGeo == '':
            vGeo = 'NULL'

        if res == '':
            res = 'NULL'

        tempRan = rangArray[i]
        if len(tempRan) == 0:
            tempRan = ['NULL', 'NULL']
        for j in range(len(tempRan)):
            if tempRan[j] == None:
                tempRan[j] = 'NULL'

        #finalDataPts = copy.deepcopy(dataPts)

        # for j in range(len(dataPts)):
        #     for key in dataPts[j]:
        #         if dataPts[j][key] == "NULL":
        #             del finalDataPts[j][key]

        form = formArray[i]
        comp = compArray[i]
        reflect = json.dumps(dataPts[i])

        sample = Sample.create(dataId, sampleId, access, origin, 'NULL', name, desc, 'NULL', 'NULL', gr, vGeo, res, tempRan, form, comp, reflect)
        sample.save()
