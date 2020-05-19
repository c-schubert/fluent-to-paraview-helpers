# Export (transient) ANSYS Fluent Data to Paraview with Ensight-Gold Format
This is a collection of some convenience Python (ver. 3) scripts for the conversion of ANSYS Fluent data files to the Ensight-Gold (a Paraview readable) format. 
There are to main functionalities:

  - Generation of export journal with "gen2pv_jou.py"
  - Generation of transient Ensight-Gold case file from the exported data


_Warning: I am not an expert in Python nor can I guarantee the working of these scripts for every case or every fluent version. You may feel free to fork or make pull request for possible enhancements._

## Export Journal Generation
In this section we describe the automatic generation of an export journal file via the Python script "genf2pv_jou.py". 
This may be used as a convenience tool for the generation of an export journal for many ANSYS Fluent data files to the Encase-Gold format. 

The following parameters may be used:

flag | flag (short)  | default value | description
--- | --- | --- | ---
--ascii | -a | no | writes encase cases in ascii (binary = default)
--casesuffix | -cs | ".case" | may be important if "--readCase" is set
--dry | -d | false | performes a dry run 
--exportFolder | -f | empty (fluent working dir) | folder to export fluent data files in (may be relative to fluent working dir) 
--journalName | -j | "f2pv.jou" | generated journal filename 
-- exportName | -n | "f2pv_export" | prefix of exported cases 
-- nodeValues | -nv | no | write node values (cell values = default) 
--prefix | -p | "" | prefix of data files (may be used as filter)  
--readCase | -rc | false | dat file only will be exported, if case file of same name exists
--suffix | -s | ".dat" | suffix of data files |
--targetFolder | -t | python working dir | folder with fluent data files 
--variables | -v | "x-velocity" | Fluent variables to be exported, i.e.: "x-velocity y-velocity ..." 

Example call:

```
python genf2pv_jou.py -t "D:\\examplefolder\\myfolder" -s ".dat.h5" -p "esr_" -f "./pv_export" -n "flu_export" -j "f2pv_export.jou" -v "x-velocity y-velocity z-velocity temperature"
```

This will generate a the "f2pv_export.jou" journal file, which, when run with Fluent, will export all ".dat.h5" files (for all the given variables) in "D:\\examplefolder\\myfolder" to cell centred Ensight-Gold format.
 
  - in case that "--readCase" parameter is given no case must be read before running the journal
  - otherwise the case with the constant mesh must be read before loading the generated journal file

## Generating a transient a Encase-Gold Case from exported Data
When exporting large amounts of ANSYS Fluent data files, it is likely that this will be probably transient data files, sadly there is no such thing as native transient file export in ANSYS Fluent.
Therefore the following script "gentrans_encase.py" will generate such a transient case from the exported Ensight-Gold data files (which can be generated using the previously described script).

_Warning: dryrun (parameter "--dry") is not 100% functional yet_

_Before running this script, make shure that the exported data files are located in a separate directory_

This script (if set/used wisely) will: 
  - rename all encas to case (due to Paraview convenctions)
  - delete unecessary .geo files
  - generate transient .case file, which will import all exportet timesteps in Paraview

The following parameters may be used:

flag | flag (short)  | default value | description
--- | --- | --- | ---
--dry | -d | false | performes a dry run 
--keepMesh | -k | false | keeps "*.geo" files of all cases (should only be set for moving or refining meshes) 
--folder | -f | working dir | folder all single Encase-Gold case files are located


Example call:
```
python gentrans_encase.py -f "D:\\examplefolder\\myfolder\\pv_export"
```

## Testing

If you like to modify or test modifications to the code of "gentrans_encase.py" the script "runtest.py" may be used. 

This script will run: 
  - gentrans_encase.py on a folder of testfiles
  - wipe all content of this testfiles folder and restore the testfiles from another folder (Parameter: "-c"), if necessary


flag | flag (short)  | default value | description
--- | --- | --- | ---
--clean | -c | false | restores testfiles in testfolder from restorefolder
--testFolder | -tf | "./test/testfiles" | path containing ensight-gold testfiles
--restoreFolder | -rf | "./test/testfiles_restore"  | folder for restoring ensight-gold testfiles


```
python runtest.py -c -tf "D:\\examplefolder\\myfolder\\test\\testfiles" -rf "D:\\examplefolder\\myfolder\\test\\testfiles_restore"
```