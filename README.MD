## Python program to check files that contain SQL-statements

This is a working prototype but contains some hard-coded values.  
See the output of help option below:  

C:\Python\sqlite>python checkfiles.py -h
usage: checkfiles.py [-h] [-en | -fi | -se] path reference

The program checks .sql files in the given directory by comparing each file contents to
the reference file. It writes feedback about each file to github.The feedback language
can be selected by [en|fi|se] option.The program also creates a summary file
(summary.csv) that contains a short summary about each file and a link to full feedback
in github

positional arguments:
  path        path to a directory that contains student answer files
  reference   file that contains correct sql-statements

optional arguments:
  -h, --help  show this help message and exit
  -en         Feedback in English (default)
  -fi         Feedback in Finnish
  -se         Feedback in Swedish

C:\Python\sqlite>


