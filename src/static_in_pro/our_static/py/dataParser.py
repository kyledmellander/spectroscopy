import csv
import sys
import json
import re
import copy
import itertools
import numpy as np
#import psycopg2

#Takes in the csv file
csvFile = sys.argv[1]

# Grab Sample_Class (e.g. Magnetite, Sulfate)
path = sys.argv[1]
if "Magnetites" in path:
    sample_cl = "Magnetite"
elif "Oxides" in path:
    sample_cl= "Oxide"
elif "Sulfates" in path:
    sample_cl = "Sulfate"
else: sample_cl = 'NULL'

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
A = np.array([])


with open(csvFile, 'rU') as cf:
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
        #print id_num[0]
        #idStringArray.append(id_num[0])
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
    #print idStringArray
    while k < sizeIdArray:
        newId = str(idStringArray[k]) + "_" + str(finalIdArray[k]).zfill(2)
        #print newId
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
        if vg[i] != "" and vg[i].find("unknown") == -1 and vg[i].find("?") == -1: #Question mark check: make more robust? Will there be some ?'s and some data?
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
                    #if isinstance(temp1[0], float):
                    if hasNumbers(temp1[0]) == True:
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
    #print wl

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
            if hasNumbers(row[0]) == True:
                currDict[row[0]] = row[i] * factor

        dataPts.append(currDict)
        i += 1

#----Database Things Happen Here----
conn = None

#Need to fill in with correct information
conn = psycopg2.connect("dbname = 'spectrodb' user = 'myprojectuser' host = localhost password = 'password'")
cur = conn.cursor()

size = len(dataArray)
for i in range(size):
    dataId = dataArray[i]
    sampId = sampArray[i]
    name = nameArray[i]
    gr = grainArray[i]

    tempVG = vGeoArray[i]
    for j in range(len(tempVG)):
        if tempVG[j] == None:
            tempVG[j] = 'NULL'
    vg = '{' + str(tempVG[0]).strip() + ', ' + str(tempVG[1]).strip() + ', ' + str(tempVG[2]).strip() + ', ' + str(tempVG[3]).strip() + '}'

    tempRes = resArray[i]
    for j in range(len(tempRes)):
        if tempRes[j] == None:
            tempRes[j] = 'NULL'
    res = '{' + str(tempRes[0]).strip() + ', ' + str(tempRes[1]).strip() + ', ' + str(tempRes[2]).strip() + ', ' + str(tempRes[3]).strip() + '}'

    tempRan = rangArray[i]
    if len(tempRan) == 0:
        tempRan = ['NULL', 'NULL']
    for j in range(len(tempRan)):
        if tempRan[j] == None:
            tempRan[j] = 'NULL'
    ran = '{' + str(tempRan[0]).strip() + ', ' + str(tempRan[1]).strip() + '}'

    form = formArray[i]
    comp = compArray[i]
    print dataPts[i]
    reflect = json.dumps(dataPts[i])
    # query = "INSERT INTO mars_sample (DATA_ID, SAMPLE_ID, DATE_ACCESSED, ORIGIN, LOCALITY, NAME, SAMPLE_DESC, GRAIN_SIZE, VIEW_GEOM, RESOLUTION, REFL_RANGE, FORMULA, COMPOSITION, REFLECTANCE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    # data = (dataId, sampId, access, origin, collection, name, desc, gr, vg, res, ran, form, comp, reflect)
    query = "UPDATE mars_sample SET SAMPLE_CLASS = %s WHERE DATA_ID = %s"
    data = (sample_cl, dataId)
    cur.execute(query, data)

conn.commit()
conn.close()

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
