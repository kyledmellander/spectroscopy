from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.mail import send_mail
from django.conf import settings
from django.template.defaulttags import register
from .forms import ContactForm, SignUpForm, SearchForm, UploadFileForm
from .models import Sample, SignUp
from django.utils.encoding import smart_str
from django.contrib.staticfiles import finders
from zipfile import ZipFile
from django.contrib.auth import logout

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
import operator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages

# Create your views here.

def logout_view(request):
  logout(request)
  return redirect('/')

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
  #results = Sample.objects.order_by('data_id')
  results = Sample.objects.extra(select={'lower_name': 'lower(name)'}).order_by('lower_name', 'data_id')
  #results = results.extra(select={'name_is_null': 'name IS NULL'}).order_by('name_is_null')

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

    #results = results.sort(key=lambda x: x.name.lower())
    #ordered = sorted(results, key=operator.attrgetter('name').lower())
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
        sortedList = sorted(item["reflectance"].iteritems(), key=lambda(x,y):float(x))
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
        names.append(smart_str(s.data_id.strip()))

        # Make sure whatever text reader you open this csv file with is set to Unicode (UTF-8)
        writer.writerow([smart_str("Database of Origin"), smart_str(s.origin),])
        writer.writerow([smart_str("Sample Description"), smart_str(s.sample_desc),])
        writer.writerow([smart_str("Date Accessed"), smart_str(s.date_accessed),])
        writer.writerow([])
        writer.writerow([smart_str("Data ID"), smart_str(s.data_id),])
        writer.writerow([smart_str("Sample ID"), smart_str(s.sample_id),])
        writer.writerow([smart_str("Mineral Name"), smart_str(s.name),])
        writer.writerow([smart_str("Locality"), smart_str(s.locality),])
        writer.writerow([smart_str("Grain Size"), smart_str(s.grain_size),])
        writer.writerow([smart_str("Viewing Geometry"), smart_str(s.view_geom),])
        writer.writerow([smart_str("Resolution"), smart_str(s.resolution),])
        writer.writerow([smart_str("Formula"), smart_str(s.formula),])
        writer.writerow([smart_str("Composition"), smart_str(s.composition),])
        writer.writerow([])
        writer.writerow([smart_str("Wavelength"),])
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
      response['Content-Disposition'] = 'attachment; filename=spectra.zip'

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
      mclass = ""
    mtype = request.POST.get('sample_type')
    if not mtype:
      mtype = ""
    print mclass
    print mtype
    if form.is_valid():
      error_msg, warning_msgs, overwrite = process_file(request.FILES['file'], mclass, mtype)
      if error_msg != '':
        messages.error(request, 'ERROR: ' + error_msg)
      else:
        messages.success(request, 'Success!')
        if len(warning_msgs) != 0:
          for warning_msg in warning_msgs:
            messages.warning(request, 'WARNING: ' + warning_msg)
        if len(overwrite) != 0:
          messages.warning(request, 'WARNING: The following data IDs were overwritten. If this was not the intended behavior, please check for non-unique data IDs. ' + ', '.join(overwrite))
      #return HttpResponseRedirect('/admin/mars/sample')
      return HttpResponseRedirect('/upload/')
  else:
    form = UploadFileForm()
  return render(request, 'upload.html', {'form': form})

def hasNumbers(inputString):
  result = bool(re.search(r'\d', inputString))
  return result

def process_file(file, mineral_class, mineral_type):
    dataArray = [] # Array of IDs
    sampArray = [] # Sample IDs
    nameArray = [] # Mineral Names
    collArray = [] # Collection localities
    grainArray = [] # Grain sizes
    vGeoArray = [] # Viewing Geometries
    resArray = [] # Resolutions
    formArray = [] # Formulas
    compArray = [] # Compositions

    error_messages = ''
    warning_messages = []
    overwritten = []

    try:
        paramFile = file.read()
        reader = csv.reader(file)

        # HEADER Section
        origin = None
        desc = None
        access = None
        header_line = reader.next()
        while header_line[0] != '':

            # Database of origin
            if 'database' in header_line[0].lower():
                origin = header_line[1]

            # Spreadsheet Description
            elif 'description' in header_line[0].lower():
                desc = header_line[1]

            # Date of original database access (YEAR-MONTH-DAY)
            elif 'accessed' in header_line[0].lower():
                access = header_line[1]

            else:
                warning_messages.append("\"" + header_line[0] + "\" does not contain a known key. Row ignored.")

            header_line = reader.next()
        
        # Check for mandatory header fields
        if origin == None:
            warning_messages.append("Database of origin not provided.")
        if access == None:
            warning_messages.append("Date accessed not provided.")

        # METADATA Section
        dataIDs = reader.next() # Data ID must come first
        if 'data id' not in dataIDs[0].lower():
            error_messages += 'Data ID must come first in metadata section. Check that there is only one (1) blank row between each section.'
            return error_messages, warning_messages, overwritten

        start = 1
        while dataIDs[start] == '':
            start += 1

        c = start
        while c < len(dataIDs):
            dataArray.append(dataIDs[c])
            c+=1

        # Rest of the metadata
        meta_line = reader.next()
        while meta_line[0] != '':
            c = start

            # Sample ID
            if 'sample id' in meta_line[0].lower():
                while c < len(meta_line):
                    sampArray.append(meta_line[c])
                    c+=1

            # Mineral name
            elif 'name' in meta_line[0].lower():
                while c < len(meta_line):
                    nameArray.append(meta_line[c])
                    c+=1

            # Collection Locality
            elif 'locality' in meta_line[0].lower():
                while c < len(meta_line):
                    collArray.append(meta_line[c])
                    c+=1

            # Grain size
            elif 'grain size' in meta_line[0].lower():
                while c < len(meta_line):
                    grainArray.append(meta_line[c])
                    c+=1

            # Viewing geometry
            elif 'viewing geometry' in meta_line[0].lower():
                while c < len(meta_line):
                    vGeoArray.append(meta_line[c])
                    c+=1

            # Resolution
            elif 'resolution' in meta_line[0].lower():
                while c < len(meta_line):
                    resArray.append(meta_line[c])
                    c+=1

            # Formula
            elif 'formula' in meta_line[0].lower():
                while c < len(meta_line):
                    formArray.append(meta_line[c])
                    c+=1

            # Composition
            elif 'composition' in meta_line[0].lower():
                while c < len(meta_line):
                    compArray.append(meta_line[c])
                    c+=1
            
            # New metadata fields here

            else:
                warning_messages.append("\"" + meta_line[0] + "\" does not contain a known key. Row ignored.")

            meta_line = reader.next()

        # REFLECTANCE Section
        line = reader.next()

        if line[0] == '':
            error_messages += 'Check that there is only one (1) blank row between each section.'
            return error_messages, warning_messages, overwritten

        # Figure out units
        if "microns" in line[0] or "um" in line[0]:
            factor = 1000
        else:
            factor = 1

        wl = reader.next()

        row_len = len(dataIDs)
        c = start

        dataPoints = []
        for d in range(row_len - c):
            dataPoints.append({})

        for row in reader:
            if hasNumbers(row[0]) == True:
                for column in xrange(c,row_len):
                    if row[column] == '':
                      continue

                    if float(row[column]) > 1.0:
                        dataPoints[column-c][str(float(row[0]) * factor)] = str(float(row[column]) / 100.)

                    # Check for invalid datapoints #
                    elif float(row[column]) < 0.0:
                        continue

                    else:
                        dataPoints[column-c][str(float(row[0]) * factor)] = row[column]

    except Exception, e:
        print str(e)

    size = len(dataArray)

    # Pad arrays to catch any missing values at end
    sampArray += [''] * (size - len(sampArray))
    nameArray += [''] * (size - len(nameArray))
    collArray += [''] * (size - len(collArray))
    grainArray += [''] * (size - len(grainArray))
    vGeoArray += [''] * (size - len(vGeoArray))
    resArray += [''] * (size - len(resArray))
    formArray += [''] * (size - len(formArray))
    compArray += [''] * (size - len(compArray))
    
    for i in range(size):
        dataId = dataArray[i]
        sampId = sampArray[i]
        name = nameArray[i]
        collection = collArray[i]
        gr = grainArray[i]
        vGeo= vGeoArray[i]
        res = resArray[i]

        low = min([float(w) for w in dataPoints[i]])
        high = max([float(w) for w in dataPoints[i]])
        tempRan = [int(round(low, -2)), int(round(high, -2))]

        form = formArray[i]
        comp = compArray[i]

        # Check to see if Data ID already exists #
        if Sample.objects.filter(data_id=dataId).exists():
          overwritten.append(dataId)

        sample = Sample.create(dataId, sampId, access, origin, collection, name, desc, mineral_type, mineral_class,'', gr, vGeo, res, tempRan, form, comp, dataPoints[i])
        sample.save()

    return error_messages, warning_messages, overwritten
