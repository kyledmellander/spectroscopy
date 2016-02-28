import csv
import sys
import json
import re
import numpy as np
import psycopg2

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
wavelens = []  #matrix of num_data_point rows by 1+num_samples columns
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
        if vg[i] != "":
            token = vg[i].split('/')
            vGeoArray.append(int(token[0]))
            vGeoArray.append(int(token[1]))
        else:
            #empty case - don't put in database
            vGeoArray.append(vg[i])
        i+=1

    # Resolution
    res = reader.next()
    i = 2
    if ("um" or "micron") in res[0]:
        scale = "microns"
    else:
        scale = "nanometers"
    while i < len(res):
        if res[i] != "":
            tempArray = []
            temp1 = res[i].split('-')
            first = temp1[0].split('@')
            last = temp1[1].split('@')
            if last[1].find("nm") != -1:
                lt = last[1].split("n")
                scale = "nanometers"
            else:
                lt = last[1].split("u")
                scale = "microns"
            if scale == "microns":
                tempArray.append(str(float(first[0])*1000))
                tempArray.append(str(float(first[1])*1000))
                tempArray.append(str(float(last[0])*1000))
                tempArray.append(str(float(lt[0])*1000))
            else:
                tempArray.append(first[0])
                tempArray.append(first[1])
                tempArray.append(last[0])
                tempArray.append(lt[0])

            resArray.append(tempArray)
        else:
            #empty case- don't put in database
            resArray.append(res[i])
        i+=1

    # Range
    rang = reader.next()
    i = 2
    print rang[0]
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
                    temp1.append(str(float(temp[0])*1000))
                    temp1.append(str(float(ty[0])*1000))
                else:
                    temp1.append(str(float(temp[0])*1000))
                    temp1.append(str(float(temp[1])*1000))
            else:
                temp = rang[i].split('-')
                if temp[1].find("nm") != -1:
                    ty = temp[1].split("n")
                    temp1.append(temp[0])
                    temp1.append(ty[0])
                else:
                    temp1.append(temp[0])
                    temp1.append(temp[1])
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
        print str(comp[i]) + "\n"
        compArray.append(comp[i])
        i+=1

    line = reader.next()
    print line
    while ("Wavelength" not in line[0]):
        print line
        line = reader.next()

    # reader.next()
    # reader.next()
    # reader.next()
    # reader.next()

    factor = 1
    wl = reader.next()
    print "wl: " + str(wl)
    if ("microns" or "um") in wl:
        factor = 1000
    for row in reader:
        #print row
        #w = reader.next()
        i = 0
        tempArray = []
        tempArray.append(str(float(row[0])*factor))
        i = 2
        while i < len(row):
            tempArray.append(str(float(row[i])*factor))
            i+=1
        wavelens.append(tempArray)
        #print tempArray
    A = np.array(wavelens)

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
