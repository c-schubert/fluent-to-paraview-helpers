#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Conversion script for Enight-Gold ANSYS Fluent exports of several timesteps
# to be readable by paraview
# must have been exportet with:
# filename-%f
# make sure all .dat files have been finally converted - else there may be a wrong order generated

# todo: add input timestamp type


# MIT License

# Copyright (c) 2020 Christian Schubert

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import os
from os import listdir
from os.path import isfile, join
from shutil import copyfile
import re


################## FUNCTIONS ########################

def readFileContentToString(casefile):
    with open(casefile, 'r') as fp:
        casecontent = fp.read()
    return casecontent

def overwritecasecontent(casefile, newcasecontent,dryrun):
    print("Writing new case content:")
    if dryrun == True:
        print(newcasecontent)
    else: 
        with open(casefile, 'w') as fp:
            fp.write(newcasecontent)

def appendToFile(casefile, additionalcasecontent, dryrun):
    print("Writing case content:")
    if dryrun == True:
        print(additionalcasecontent)
    else: 
        with open(casefile, 'a') as fp:
            fp.write(additionalcasecontent)


def replaceGeomOfCase(casefile, newgeomfile, dryrun):
    print("Replacing geom reference in case ", casefile)

    casecontent = readFileContentToString(casefile)
    newcasecontent =  re.sub("model: \S+\.geo","model: " + newgeomfile,casecontent)
    overwritecasecontent(casefile, newcasecontent,dryrun)


def replaceNumberOfFileWithStars(casefile, dryrun):
    print("Replacing file numbering in ", casefile," with stars")

    casecontent = readFileContentToString(casefile)
    newcasecontent =  re.sub("\d{8}\.(scl\d+|vel|geo|xml)",r"********.\1",casecontent)
    overwritecasecontent(casefile, newcasecontent,dryrun)

def replaceFileNamesInCase(casefile, replacestr, withstr, dryrun):
    print("Replacing filename in case ", casefile)

    casecontent = readFileContentToString(casefile)
    newcasecontent =  casecontent.replace(replacestr,withstr)

    overwritecasecontent(casefile, newcasecontent,dryrun)

def removeScriptEntry(casefile,dryrun):
    casecontent = readFileContentToString(casefile)
    lb2casecontent = casecontent.splitlines()

    newcasecontent = ""
    for l in lb2casecontent:
        if not ("SCRIPTS" in l or l.startswith("metadata:")):
            newcasecontent += l + "\n"
    
    overwritecasecontent(casefile, newcasecontent,dryrun)

################## DEFAULTS ########################
dryrun = False
mesh_is_const = True
targetfolder = os.getcwd()  
nodeValues = False
trans_case_name = "encase_trans.case"


################## START ########################

arglen = (len(sys.argv)-1)

for (i,eachArg) in enumerate(sys.argv):
    if "--dry" == eachArg or "-d" == eachArg:
        dryrun = True
        print("Performing dry run!")
    if "--keepMesh" == eachArg or "-k" == eachArg:
        mesh_is_const = False
        print("Meshes may change over time. Keeping all .geo files!")
    if "--folder" == eachArg or "-f" == eachArg:
        if arglen > i and (not sys.argv[i+1].startswith("-")) and os.path.exists(sys.argv[i+1]): 
            targetfolder = sys.argv[i+1]
            print("Using folder: ", targetfolder)
        else:
            raise Exception("File a parameter is missing or a wrong path was given.")



onlyfiles = [f for f in listdir(targetfolder) if isfile(join(targetfolder, f))]


times = []              #float values
timestamps=[]           # string values

for fn in onlyfiles:
    if fn.endswith(".encas"):
        if dryrun:
            print("Renaming case ", fn , "\t to ", fn.replace(".encas", ".case"))
        else:
            print("Renaming case ", fn , "\t to ", fn.replace(".encas", ".case"))
            os.rename(join(targetfolder,fn), join(targetfolder,fn.replace(".encas", ".case")))

# read again 
onlyfiles = [f for f in listdir(targetfolder) if isfile(join(targetfolder, f))]

#get timestampes
for fn in onlyfiles:
    if fn.endswith(".geo"):
        m = re.search("\d{3}.\d{6}", fn).group(0)
        times.append(float(m))
        timestamps.append(m)

print("Found times: ", times)

for (i,ts) in enumerate(timestamps):
    print(str(i), " Timestamp: ", ts)
    for fn in onlyfiles:
        if ts in fn:
            nfn = fn.replace(ts, "{0:d}".format(i).zfill(8))

            if dryrun != True:
                print("rename file ", fn, "\t to ", nfn)
                os.rename(join(targetfolder,fn),join(targetfolder,nfn)) # rename files
                if fn.endswith(".case") or fn.endswith(".encas"):
                    replaceFileNamesInCase(join(targetfolder,nfn), str(ts),  "{0:d}".format(i).zfill(8), dryrun)
            else:
                print("rename file ", fn, "\t to ", nfn)
                if fn.endswith(".case") or fn.endswith(".encas"):
                    replaceFileNamesInCase(join(targetfolder,fn), str(ts),  "{0:d}".format(i).zfill(8), dryrun)


# read again 
onlyfiles = [f for f in listdir(targetfolder) if isfile(join(targetfolder, f))]

# # copy frist geo & remove other -> maybe change geo in other cases files? 

for fn in onlyfiles:
    if "casegeom.geo" in fn:
        print("Removing old all .geo file ", fn)
        if dryrun != True:
            os.remove(join(targetfolder,fn))
    if trans_case_name in fn: 
        print("Removing old trans case file ", fn)
        if dryrun != True:
            os.remove(join(targetfolder,fn))

copyGeoFile = False
copyCaseFile = False
for fn in onlyfiles:
    if mesh_is_const == True and copyGeoFile == False and fn.endswith(".geo"):
        print("Copy file ", fn, " to ", "casegeom.geo")
        if dryrun != True:
            copyfile(join(targetfolder,fn), join(targetfolder,"casegeom.geo"))
        copyGeoFile = True

    if mesh_is_const == True and (fn.endswith(".case") or fn.endswith(".encas")) :
            replaceGeomOfCase(join(targetfolder,fn), "casegeom.geo", dryrun )

    if copyCaseFile == False and fn.endswith(".case"):
        print("Copy file ", fn, " to ", trans_case_name)
        if dryrun != True:
            copyfile(join(targetfolder,fn), join(targetfolder,trans_case_name))
        copyCaseFile = True

    if mesh_is_const == True and fn.endswith(".geo"):
        print("Removing unecessary .geo file ", fn)
        if dryrun == False:
            os.remove(join(targetfolder,fn))


if dryrun == False:
    replaceNumberOfFileWithStars(join(targetfolder,trans_case_name),dryrun)


appstr = "TIME\n" +  "time set: 1\n" + "number of steps: " + str(len(times)) + "\n" + "filename start number: 0 \n" + "filename increment: 1 \n" + "time values: " + " ".join(str(x) for x in times) + "\n"

appendToFile(join(targetfolder,trans_case_name),appstr, dryrun)

removeScriptEntry(join(targetfolder,trans_case_name), dryrun)