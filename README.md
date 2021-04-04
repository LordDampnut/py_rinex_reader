# py_rinex_reader

A crude RINEX file reader. By no means the work of a professional but mearly a student giving his best.
This programm was tested with the included RINEX file (version 3.02) but i want to test other (newer) 
vesions too. It wont catch errors yet but that could change in the near future. 

# How to use

This programm was written in python 3.7.

simply run the "run.py" file to run the program with the provided example file.

run.py [ARGUMENT]

Arguments: 

* -h or --help to display the help menu

* [RINEX INPUT FILE]


## Major issue

Due to missing values in the rinex file and the problem of finding out how to know which values are missing, the lines containing missing values will not be in the output file.
The SV will be logged but the "codes" tag will be empty even though some values are present in the input file.

Image 1: ![](https://i.imgur.com/4Srtmd2.png)

(1) In the input file there should be 12 values for 'Gxx' satellites but the first two SVs only show 8. 

Image 2: ![](https://i.imgur.com/F3voTjU.png)

(2) The missing Values are not stored, the SVN however is.

This would not be a problem if the only values missing were at the end of a line. Unfortunately there are many lines with missing values in between which makes it hard for me to programm a filter that knows which value corresponds wo which code.




# ToDo
* ~JSON output file~
* CLI input arguments
  * ~define inout file~
  * define ~output filename~
  * define number of epochs to be converted?
* GUI with some sort of interaction
    * Load different RINEX file?
    * DIsplay metadata of choosen file?
    
* ~Use of dictionaries~
* ~JSON dump~
* Clean up header reading code  
