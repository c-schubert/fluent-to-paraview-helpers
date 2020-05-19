#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Conveniece layer script for the testing of gentrans_encase.py

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
import shutil

# define paths
testfilespath = "./test/testfiles/"
testfilesrestorepath = "./test/testfiles_restore/"

clean = False

arglen = (len(sys.argv)-1)

for (i,eachArg) in enumerate(sys.argv):
    if "--clean" == eachArg or "-c" == eachArg:
        clean = True
        print("Performing clean test run!")
    if "--testFolder" == eachArg or "-tf" == eachArg:
        if arglen > i and (not sys.argv[i+1].startswith("-")) and os.path.exists(sys.argv[i+1]): 
            testfilespath = sys.argv[i+1]
            print("Using test folder: ", testfilespath)
        else:
            raise Exception("File a parameter is missing or a wrong path was given.")
    if "--restoreFolder" == eachArg or "-rf" == eachArg:
        if arglen > i and (not sys.argv[i+1].startswith("-")) and os.path.exists(sys.argv[i+1]): 
            testfilesrestorepath = sys.argv[i+1]
            print("Using restore folder: ", testfilesrestorepath)
        else:
            raise Exception("File a parameter is missing or a wrong path was given.")


# -----------------------------------------------------------------------------

print("Starting testrun!")


if clean == True:
    print("Removing old testfiles!")

    abspath1 = os.path.abspath(testfilespath)
    onlyfiles1 = [f for f in listdir(abspath1) if isfile(join(abspath1, f))]


    for f in onlyfiles1:
        print("Removing file: ", join(abspath1, f), " from testfolder")
        os.remove(join(abspath1, f))


    abspath2 = os.path.abspath(testfilesrestorepath)
    onlyfiles2 = [f for f in listdir(abspath2) if isfile(join(abspath2, f))]

    print("Copying clean testfiles!")

    for f in onlyfiles2:
        print("Copy file: ",join(abspath2,f), " to testfolder ", abspath2)
        shutil.copy(join(abspath2,f), abspath1)


print("Running test!")

os.system("python gentrans_encase.py -f \""+ abspath1 +"\" > gentransout.txt")


print("Finished testrun!")