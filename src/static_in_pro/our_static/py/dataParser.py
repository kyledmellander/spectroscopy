import csv
import sys
import numpy as np

csvFile = sys.argv[1]

def get_column(A, colNum):
    return A[:,colNum]

dataArray = []
sampArray = []
nameArray = []
grainArray = []
vGeoArray = []
resArray = []
rangArray = []
formArray = []
compArray = []
wavelens = []  #matrix of num_data_point rows by 1+num_samples columns
#reflectance = []


with open(csvFile, 'rb') as cf:
    reader = csv.reader(cf)
    origin = reader.next()[1]
    print(origin)
    collection = reader.next()[1]
    desc = reader.next()[1]
    access = reader.next()[1]
    reader.next()

    data = reader.next()
    i = 2
    while i < len(data):
        #dataArray[j] = data[i]
        dataArray.append(data[i])
        i+=1


    samp = reader.next()
    i = 2
    while i < len(samp):
        sampArray.append(samp[i])
        i+=1

    name = reader.next()
    i = 2
    while i < len(name):
        nameArray.append(name[i])
        i+=1

    scale = "nanometers"
    size = reader.next()
    if "??" or "micron" in size[0]:
        scale = "microns"
    i = 2
    while i < len(size):
        if "??" or "micron" in size[i]:
            temp = size[i].split()
            temp1 = temp[0]
            if "<" in temp1:
                temp1 = temp1.replace("<", "")
                temp1 = float(temp1)*1000
                temp1 = "<" + str(temp1)
            elif "-" in temp1:
                temp2 = temp1.split("-")
                temp1 = str(float(temp2[0])*1000) + "-" + str(float(temp2[1])*1000)
            grainArray.append(temp1)
        else:
            grainArray.append(size[i])
        i+=1
    scale = "nanometers"

    vg = reader.next()
    i = 2
    while i < len(vg):
        if vg[i] != "":
            token = vg[i].split('/')
            vGeoArray.append(token)
        else:
            #empty case - don't put in database
            vGeoArray.append(vg[i])
        i+=1

    res = reader.next()
    i = 2
    while i < len(res):
        if res[i] != "":
            tempArray = []
            temp1 = res[i].split('-')
            tempArray.append(temp1[0])
            tempArray.append(temp1[1])
            resArray.append(tempArray)
        else:
            #empty case- don't put in database
            resArray.append(res[i])
        i+=1

    rang = reader.next()
    i = 2
    if "??" or "micron" in rang[0]:
        scale = "microns"
    while i < len(rang):
        if rang[i] != "":
            temp1 = []
            if scale == "microns":
                temp = rang[i].split('-')
                temp1.append(str(float(temp[0])*1000))
                temp1.append(str(float(temp[1])*1000))
            else:
                temp = rang[i].split('-')
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
        compArray.append(comp[i])
        i+=1

    reader.next()
    reader.next()
    reader.next()
    reader.next()
    reader.next()

    factor = 1
    wl = reader.next()
    if "microns" or "??" in wl:
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

f = open('marsdb.sql', 'w')
insert = "INSERT INTO mars_sample (data_id, sample_id, date_accessed, origin, name, grain_size, view_geom)"

for i in range(len(dataArray)):
    line = insert + " VALUES ('" + dataArray[i] + "', '" \
    + sampArray[i] + "', '" + access + "', '" + origin + "', '" \
    + nameArray[i] + "', '" + grainArray[i] + "', '{" + str(vGeoArray[i][0]) \
    + ', ' + str(vGeoArray[i][1]) + "}');"
    f.write(line + '\n')

f.close()
