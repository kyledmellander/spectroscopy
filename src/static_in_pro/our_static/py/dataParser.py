import csv
import sys
import json
import re
import copy
import numpy as np
#import psycopg2

#Takes in the csv file
csvFile = sys.argv[1]

def hasNumbers(inputString):
    return bool(re.search(r'/d', inputString))

def get_column(A, colNum):
    return A[:,colNum]

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
A = np.array([])


with open(csvFile, 'rb') as cf:
    reader = csv.reader(cf)
    origin = reader.next()[1]
    collection = reader.next()[1]
    desc = reader.next()[1]
    access = reader.next()[1]
    reader.next()

    # Data ID
    data = reader.next()
    i = 2
    while i < len(data):
        #dataArray[j] = data[i]
        dataArray.append(data[i])
        i+=1

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
                    #temp1 = str(float(temp2[0])*1000) + "-" + str(float(temp2[1])*1000)
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
                #grainArray.append(size[i])
                temp = size[i].split()
                temp1 = temp[0]
                if "<" in temp1:
                    temp1 = temp1.replace("<", "")
                    if temp1.find("nm") != -1:
                        temp2 = temp1.split("n")
                        arr.append(temp2[0])
                    else:
                        arr.append(temp1)
                    #temp1 = "<" + str(temp1)
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
        geoArray = [None] * 4
        if vg[i] != "" and vg[i].find("unknown") == -1:
            token = vg[i].split('/')
            if token[0].find("|") != -1:
                sl = token[0].split("|")
                geoArray[0] = sl[0]
                geoArray[1] = sl[1]
            else:
                geoArray[0] = token[0]
            if len(token) > 1:
                if token[1].find("|") != -1:
                    sr = token[1].split("|")
                    if geoArray[1] != None:
                        geoArray[2] = sr[0]
                        geoArray[3] = sr[1]
                    else:
                        geoArray[1] = sr[0]
                        geoArray[2] = sr[1]
                else:
                    geoArray[1] = token[1]
            vGeoArray.append(geoArray)
        else:
            #empty case - don't put in database
            vGeoArray.append(geoArray)
        i+=1

    # Resolution
    res = reader.next()
    i = 2
    if ("um" or "micron") in res[0]:
        scale = "microns"
    else:
        scale = "nanometers"
    while i < len(res):
        tempArray = [None] * 4
        if res[i] != "" and res[i].find("unknown") == -1:
            if res[i].find("/") != -1:
                slash = res[i].split('/')
                if scale == "microns":
                    tempArray[0] = float(slash[0]*1000)
                else:
                    tempArray[0] = float(slash[0])
                dash = slash[1].split('-')
                if len(dash) > 1:
                    if scale == "microns":
                        tempArray[1] = float(dash[0]*1000)
                        tempArray[2] = float(dash[1]*1000)
                    else:
                        tempArray[1] = float(dash[0])
                        tempArray[2] = float(dash[1])
            else:
                temp1 = res[i].split('-')
                if len(temp1) > 1:
                    first = temp1[0].split('@')
                    if len(first) > 1:
                        last = temp1[1].split('@') #Assuming 2@3500-7@3500
                        if last[1].find("nm") != -1:
                            lt = last[1].split("n")
                            scale = "nanometers"
                        else:
                            lt = last[1].split("u")
                            scale = "microns"
                        if scale == "microns":
                            tempArray[0] = float(first[0])*1000
                            tempArray[1] = float(first[1])*1000
                            tempArray[2] = float(last[0])*1000
                            tempArray[3] = float(last[1])*1000
                        else:
                            tempArray[0] = float(first[0])
                            tempArray[1] = float(first[1])
                            tempArray[2] = float(last[0])
                            tempArray[3] = float(last[1])
                    else:
                        if scale == "microns":
                            tempArray[0] = float(first[0])*1000
                            tempArray[1] = float(temp1[1])*1000
                        else:
                            tempArray[0] = float(first[0])
                            tempArray[1] = float(temp1[1])
                else:
                    if isinstance(temp1[0], float):
                        if scale == "microns":
                            tempArray[0] = float(temp1[0])*1000
                        else:
                            tempArray[0] = float(temp1[0])
            resArray.append(tempArray)
        else:
            #empty case- don't put in database
            resArray.append(tempArray)
        i+=1

    # Range
    rang = reader.next()
    i = 2
    #print rang[0]
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
                    temp1.append(float(temp[0])*1000)
                    temp1.append(float(ty[0])*1000)
                else:
                    temp1.append(float(temp[0])*1000)
                    temp1.append(float(temp[1])*1000)
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
    print wl

    row_len = len(wl)

    waveDataPt = {}
    for row in reader:
        #print row
        if isinstance(row[0], float):
            #row_len = len(row)
            waveDataPt[str(row[0])] = None

    print row_len

    i = 2
    while i < row_len:
        print i
        cf.seek(20)
        currDict = copy.deepcopy(waveDataPt)
        for row in reader:
            if isinstance(row[0], float):
                currDict[str(row[0])] = str(float(row[i])*factor)

        dataPts.append(currDict)
        i += 1

# #----Database Things Happen Here----
# conn = None
#
# #Need to fill in with correct information
# conn = psycopg2.connect("dbname = 'spectrodb' user = 'myprojectuser' host = localhost password = 'password'")
# cur = conn.cursor()
#
# wave = get_column(A, 0)
# size = len(dataArray)
# for i in size:
#     dataId = dataArray[i]
#     sampId = sampArray[i]
#     name = nameArray[i]
#     gr = grainArray[i]
#     vg = vGeoArray[i]
#     res = resArray[i]
#     ran = rangArray[i]
#     form = formArray[i]
#     comp = compArray[i]
#     reflect = get_column(A, i+1)
#     query = "INSERT INTO samples (DATA_ID, SAMPLE_ID, DATE_ADDED, ORIGIN, LOCALITY, NAME, SAMPLE_DESC, GRAIN_SIZE, VIEW_GEOM, RESOLUTION, RANGE, FORMULA, COMPOSITION, WAVE_LENGTH, REFLECTANCE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
#     data = (dataId, sampId, access, origin, collection, name, desc, gr, vg, res, ran, form, comp, wave, reflect)
#     cursor.execute(query, data)
#
# conn.commit()
# conn.close()

# f = open('marsdb.sql', 'w')
# insert = "INSERT INTO mars_sample (data_id, sample_id, date_accessed, origin, name, grain_size, view_geom)"
#
# for i in range(len(dataArray)):
#     line = insert + " VALUES ('" + dataArray[i] + "', '" \
#     + sampArray[i] + "', '" + access + "', '" + origin + "', '" \
#     + nameArray[i] + "', '" + grainArray[i] + "', '{" + str(vGeoArray[i][0]) \
#     + ', ' + str(vGeoArray[i][1]) + "}');"
#     f.write(line + '\n')
#
# f.close()
