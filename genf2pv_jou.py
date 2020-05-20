#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Generates a export to ensight-gold format journal for fluent data files in a directory.

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

arglen = (len(sys.argv)-1)

# default values:
dryrun = False
journalName = "f2pv.jou"
suffix = ".dat"
prefix = ""
targetfolder=  os.getcwd()  
exportfolder = ""
exportname = "f2pv_export"
variables = "x-velocity"
cellBased = "yes"
writeBinary = "yes"
mustReadCase = False
caseSuffix = ".case"

for (i,eachArg) in enumerate(sys.argv):
    if "--dry" == eachArg or "-d" == eachArg:
        dryrun = True
        print("Performing dry run!")

    if "--ascii" == eachArg or "-a" == eachArg:
        writeBinary = "no"
        print("Setting to ascii export!")

    if "--prefix" == eachArg or "-p" == eachArg:
        if arglen > i and not sys.argv[i+1].startswith("-"): 
            prefix = sys.argv[i+1]
            print("Looking for files with prefix: ", prefix)
        else:
            raise Exception("No prefix given!")

    if "--suffix" == eachArg or "-s" ==eachArg:
        if arglen > i and (not sys.argv[i+1].startswith("-")): 
            suffix = sys.argv[i+1]
            print("Looking for files with suffix: ", suffix)
        else:
            raise Exception("No suffix given!")

    if "--targetFolder" == eachArg or "-t" == eachArg:
        # target fluent data file folder
        if arglen > i and (not sys.argv[i+1].startswith("-")) and os.path.exists(sys.argv[i+1]): 
            print("Using target folder: ", sys.argv[i+1])
            targetfolder = sys.argv[i+1]
        else:
            raise Exception("--targetFolder: A parameter is missing or a non-existing path was given.")

    if "--nodeValues" == eachArg or "-nv" == eachArg:
        cellBased = "no"
        print("Setting export to node values!")

    if "--exportFolder" == eachArg or "-f" == eachArg:
        # export folder target (no check if exist ...)
        print(sys.argv[i+1])
        if arglen > i and (not sys.argv[i+1].startswith("-")): 
            print("Using export folder: ", sys.argv[i+1])
            exportfolder = sys.argv[i+1]
        else:
            raise Exception("--exportFolder: A parameter is missing or a non-existing path was given.")

    if "--exportName" == eachArg or "-n" == eachArg:
        #target export filename
        if arglen > i and (not sys.argv[i+1].startswith("-")): 
            print("Export filename: ", sys.argv[i+1])
            exportname = sys.argv[i+1]
        else:
            raise Exception("No additional parameter given to exportname argument")

    if "--journalName" == eachArg or "-j" == eachArg:
        if arglen > i: 
            journalName = sys.argv[i+1]
            print("Journal Name: ",  journalName)
        else:
            raise Exception("No variables given")

    if "--variables" == eachArg or "-v" == eachArg:
        if arglen > i and (not sys.argv[i+1].startswith("-")): 
            variables = sys.argv[i+1]
            print("Using variables: ",  variables)
        else:
            raise Exception("No variables given")

    if "--readCase" == eachArg or "-rc" == eachArg:
        # read dat files musst have case (moving mesh etc.)
        mustReadCase = True
        print("Setting export to node values!")

    if "--caseSuffix" == eachArg or "-cs" ==eachArg:
        if arglen > i and (not sys.argv[i+1].startswith("-")): 
            caseSuffix = sys.argv[i+1]
            print("Looking for case files with suffix: ", caseSuffix)
        else:
            raise Exception("No case suffix given!")


if os.path.isfile(journalName):
    print("Journale file allready exists remove?")
    answer = input("y/N: ")
    if answer == "" or answer == "N":
        print("Aborting.")
        exit()
    elif answer == "y":
        if dryrun == False:
            os.remove(journalName)
    else:
        raise Exception("Invalid input aborting ...")


str2 = "ok\n"
str3 = "\n"

onlyfiles = [f for f in listdir(targetfolder) if isfile(join(targetfolder, f))]
writeOutput = False

for fn in onlyfiles:
    if fn.endswith(suffix) and fn.startswith(prefix):
        if mustReadCase == True and any(fn.replace(suffix, caseSuffix) in f for f in onlyfiles):
            str01 = "/read-case-data/"
            writeOutput = True
        elif mustReadCase == False:
            str01 = "/read-data/"
            writeOutput = True
        else:
            writeOutput = False

        if writeOutput == True:
            str1 = "/file"+str01+fn+"\n"
            str4 = "/file/export/ensight-gold \""+ exportfolder + "/" + exportname+"_%f\" " + variables + " () "+ writeBinary +" * () () "+ cellBased +" \n"

            if dryrun == True:
                print(str1)
                print(str2)
                print(str3)
                print(str4)
                print(str3)
            else:
                with open(journalName, 'a') as file:
                    file.write(str1)
                    file.write(str2)
                    file.write(str3)
                    file.write(str4)
                    file.write(str3)
