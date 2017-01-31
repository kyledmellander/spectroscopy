from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import finders
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.template.defaulttags import register
from django.utils.encoding import smart_str

from .forms import SearchForm, UploadFileForm
from .models import Sample,SampleType
from zipfile import ZipFile

import re
import copy
import itertools

import os, sys
#import unicodedata
import zipfile
import csv
import json
import subprocess
import operator
import StringIO
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
      prevSelectedList = request.POST.getlist("prev_selected")
      selections = list(set(selections + prevSelectedList))
      samples = Sample.objects.filter(data_id__in=selections)
    dictionaries = [ obj.as_dict() for obj in samples]
    return render(request, 'meta.html', {"metaResults": samples,"reflectancedict":dictionaries,})

def results(request):
    allSamples = Sample.objects.order_by('data_id')
    searchResultIDList = []
    searchResults = Sample.objects.none()
    selectedSpectra = Sample.objects.none()

    if request.method == 'POST':
        # If using a previous search, get the saved results
        if (request.POST.get("page_selected", False)):
            searchResultIDList = request.POST.getlist("search_results", [])
            print("SEARCHRESULTLIST: ", searchResultIDList)

            # Get any results selected via the form
            selections = request.POST.getlist('selection')

            # Get any results selected previously
            prevSelections = request.POST.getlist('prev_selected')


            # Join previously selected with newly selected
            selections = list(set(selections + prevSelections))
            selectedSpectra = allSamples.filter(data_id__in=selections)
            searchResults = allSamples.filter()
        else:
            SearchFormSet = formset_factory(SearchForm)
            search_formset = SearchFormSet(request.POST)
            for search_form in search_formset:
                if search_form.is_valid():
                    mName =  search_form.cleaned_data.get('mineral_name')
                    mClass = search_form.cleaned_data.get('mineral_class')
                    mDataId = search_form.cleaned_data.get('mineral_Id')
                    mOrigin = search_form.cleaned_data.get('database_of_origin')
                    anyData = search_form.cleaned_data.get('any_data')
                    xMin = search_form.cleaned_data.get('min_included_range')
                    xMax = search_form.cleaned_data.get('max_included_range')

                    # Remove 'Any' from choice field
                    if mOrigin == 'Any':
                        mOrigin = None

                    formResults = allSamples.filter()

                    if mName:
                        formResults = formResults.filter(name__icontains=mName)
                    if mClass:
                        formResults = formResults.filter(sample_class__icontains=mClass)
                    if mDataId:
                        formResults = formResults.filter(data_id__icontains=mDataId)
                    if mOrigin:
                        formResults = formResults.filter(origin__icontains=mOrigin)
                    if not anyData:
                        if (xMax < 300000):
                            formResults = formResults.filter(refl_range__1__lte=xMax)
                        if (xMin > 0):
                            formResults = formResults.filter(refl_range__0__gte=xMin)
                    else:
                        formResults = formResults.filter( (Q(refl_range__1__lte=xMax) & Q(refl_range__1__gte=xMin))
                                                        | (Q(refl_range__0__lte=xMax) & Q(refl_range__0__gte=xMin))
                                                        | (Q(refl_range__0__lte=xMin) & Q(refl_range__1__gte=xMax)))
                    searchResults = searchResults | formResults

            for result in searchResults:
                searchResultIDList.append(result.data_id.strip())


        # Create a new string of selected Spectra
        selectedList = []
        for spectra in selectedSpectra:
            selectedList.append(spectra.data_id.strip())

        #Keep a string of the selected dataIds
        selectedString = ','.join(selectedList)

        # Send the paginated results
        paginator = Paginator(searchResults, 50)
        pageSelected = int(request.POST.get("page_selected", 1))
        page_results = paginator.page(pageSelected)
        page_choices = range( max(1,pageSelected-3), min(pageSelected+4,paginator.num_pages+1))

        page_ids=[]
        for sample in page_results.object_list:
            page_ids.append(sample.data_id.strip())
        print(page_ids)
        return render (request, 'results.html', {"page_ids": page_ids, "selected_ids":selectedList, "page_choices": page_choices, "page_results": page_results, "search_results": searchResultIDList})

def search(request):
    SearchFormSet = formset_factory(SearchForm)
    dataBaseChoices = [c.strip() for c in Sample.objects.all().values_list('origin', flat=True).distinct()]
    dataBaseChoices = [(c.lower(), c) for c in dataBaseChoices]
    dataBaseChoices = sorted(dataBaseChoices)
    dataBaseChoices.insert(0, ('Any','Any'))
    print(dataBaseChoices)
    return render(request, 'search.html', {
        'search_formset': SearchFormSet, 'database_choices': dataBaseChoices,
        })


def graph(request):
  if request.method == 'POST':
    if 'graphForm' in request.POST:
      selections = request.POST.getlist('selection')

      prevSelectedList = request.POST.getlist("prev_selected")
      selections = list(set(selections + prevSelectedList))


      samples = Sample.objects.filter(data_id__in=selections)
      dictionaries = [ obj.as_dict() for obj in samples]
      for obj in dictionaries:
        for key in obj["reflectance"].keys():
          if (obj["reflectance"][key] == "NULL"):
            del obj["reflectance"][key]
      json_string = json.dumps(dictionaries)

      return render(request, 'graph.html', {"graphResults": samples,"graphJSON":json_string})

    elif 'export' in request.POST:
      selections = request.POST.getlist('selection')
      prevSelectedList = request.POST.getlist("prev_selected")
      selections = list(set(selections + prevSelectedList))

      samples = Sample.objects.filter(data_id__in=selections)
      dictionaries = [obj.as_dict() for obj in samples]
      reflectanceDict = {}
      for item in dictionaries:
        sortedList = sorted(item["reflectance"].iteritems(), key = lambda x:float(x[0]))
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
        writer.writerow([smart_str("Date Added"), smart_str(s.date_added),])
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


@login_required(login_url='/admin/login/')
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            for uploadedFile in request.FILES.getlist('files'):
                error_msg, warning_msgs, conflictingIds, conflictingSamples = process_file(uploadedFile)
                if error_msg != '':
                    messages.error(request, 'ERROR: ' + error_msg)
                else:
                    messages.success(request, 'Success!')
                    if len(warning_msgs) != 0:
                        for warning_msg in warning_msgs:
                            messages.warning(request, 'WARNING: ' + warning_msg)
                    elif len(conflictingIds) != 0:
                        messages.warning(request, 'WARNING: The following data IDs conflict. Please either change the new samples, or remove the conflicting samples from the database. ' + ', '.join(conflictingIds))
        #return HttpResponseRedirect('/admin/mars/sample')
        return HttpResponseRedirect('/upload/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def hasNumbers(inputString):
    result = bool(re.search(r'\d', inputString))
    return result

def process_file(file):
    print(file)
    dataArray = [] # Array of IDs
    sampArray = [] # Sample IDs
    nameArray = [] # Mineral Names
    collArray = [] # Collection localities
    grainArray = [] # Grain sizes
    vGeoArray = [] # Viewing Geometries
    resArray = [] # Resolutions
    formArray = [] # Formulas
    compArray = [] # Compositions
    classArray = [] # Sample Class
    subClassArray = [] # Sample Subclass
    sampleTypeArray = [] #Sample Type: e.g. Mineral, Coating, Volatile, ...
    mineralTypeArray = [] # Mineral Type: e.g. Tectosilicate
    dataPoints = [] # Samples graph data

    error_messages = ''
    warning_messages = []
    conflictingIds = []
    conflictingSamples = []

    try:
        paramFile = file.read()
        reader = csv.reader(file)

        # HEADER Section
        origin = None
        desc = None
        header_line = reader.next()
        while len(header_line) > 0 and header_line[0] != '':

            # Database of origin
            if 'database' in header_line[0].lower():
                for col in header_line[1:]:
                    if col != '':
                        origin = col

            # Spreadsheet Description
            elif 'description' in header_line[0].lower():
                for col in header_line[1:]:
                    if col != '':
                      desc = col

            else:
                warning_messages.append("\"" + header_line[0] + "\" does not contain a known key. Row ignored.")

            header_line = reader.next()

        # Check for mandatory header fields
        if origin == None:
            warning_messages.append("Database of origin not provided.")

        # METADATA Section
        dataIDs = reader.next() # Data ID must come first
        if 'data id' not in dataIDs[0].lower():
            error_messages += 'Data ID must come first in metadata section. Check that there is only one (1) blank row between each section.'
            return error_messages, warning_messages, conflictingIds, conflictingSamples

        start = 1
        while dataIDs[start] == '':
            start += 1

        c = start
        while c < len(dataIDs):
            dataArray.append(dataIDs[c].replace(" ",""))
            c+=1

        # Rest of the metadata
        meta_line = reader.next()
        while len(meta_line) > 0 and meta_line[0] != '':
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

            # Class
            elif 'class' in meta_line[0].lower():
                while c < len(meta_line):
                    classArray.append(meta_line[c])
                    c+=1

            # SubClass
            elif 'Sub class' in meta_line[0].lower():
                while c < len(meta_line):
                    subClassArray.append(meta_line[c])
                    c+=1

            # Mineral Type
            elif 'mineral type' in meta_line[0].lower():
                while c < len(meta_line):
                    mineralTypeArray.append(meta_line[c])
                    c+=1

            # Sample Type
            elif 'sample type' in meta_line[0].lower():
                while c < len(meta_line):
                    sampleTypeArray.append(meta_line[c])
                    c+=1

            # New metadata fields here

            else:
                warning_messages.append("\"" + meta_line[0] + "\" does not contain a known key. Row ignored.")

            meta_line = reader.next()

        # REFLECTANCE Section
        line = reader.next()

        if line[0] == '':
            error_messages += 'Check that there is only one (1) blank row between each section.'
            return error_messages, warning_messages, conflictingIds, conflictingSamples

        # Figure out units
        if "microns" in line[0] or "um" in line[0]:
            factor = 1000
        else:
            factor = 1

        wl = reader.next()

        row_len = len(dataIDs)
        c = start

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

    except (Exception, e):
        error_messages += str(e)

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
    mineralTypeArray += [''] * (size - len(mineralTypeArray))
    classArray += [''] * (size - len(classArray))
    subClassArray += [''] * (size - len(subClassArray))
    sampleTypeArray += [''] * (size - len(sampleTypeArray))

    for i in range(size):
        dataId = dataArray[i]
        sampId = sampArray[i]
        name = nameArray[i]
        collection = collArray[i]
        gr = grainArray[i]
        vGeo= vGeoArray[i]
        res = resArray[i]
        mineralType = mineralTypeArray[i]
        sampleClass = classArray[i]
        subClass = subClassArray[i]
        sampleType = SampleType()
        # Get or Create the sample type
        if(sampleTypeArray[i]):
            sampleType = SampleType(typeOfSample=sampleTypeArray[i])
            sampleType.save()

        low = min([float(w) for w in dataPoints[i]])
        high = max([float(w) for w in dataPoints[i]])
        tempRan = [int(round(low, 0)), int(round(high, 0))]

        form = formArray[i]
        comp = compArray[i]


        sample = Sample(
            data_id=dataId.strip(),
            sample_id=sampId.strip(),
            origin=origin.strip(),
            locality=collection.strip(),
            name=name.strip(),
            sample_desc=desc.strip(),
            mineral_type=mineralType.strip(),
            sample_class=sampleClass.strip(),
            sub_class=subClass.strip(),
            grain_size=gr.strip(),
            view_geom=vGeo.strip(),
            resolution=res.strip(),
            refl_range=tempRan,
            formula=form.strip(),
            composition=comp.strip(),
            reflectance=dataPoints[i],
            sample_type=sampleType)
        # Check to see if Data ID already exists #
        if Sample.objects.filter(data_id=dataId).exists():
            conflictingIds.append(dataId)
            conflictingSamples.append(sample)
        else:
            sample.save()

    return error_messages, warning_messages, conflictingIds, conflictingSamples
