import os
import sys
import argparse

from checkfile import SQLFileChecker


class CheckSQLFiles:
    def __init__(self, directory, modelfile,lang):
        self.direcotry = directory
        self.modelfile = modelfile
        self.filechecker = SQLFileChecker(modelfile,lang)

    def _update_csv(self, summary):
        with open('submits4.csv', 'a', encoding='utf-8') as of:
            of.write(summary + '\n')

    def process(self):
        files = os.listdir()
        sqlfiles = [f for f in files if f.endswith('.sql')]
        for f in sqlfiles:
            summary:str = self.filechecker.test(f)
            self._update_csv(summary)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="The program checks .sql files in the given directory by comparing each file contents to the reference file. It writes feedback about each file  to github."
       "The feedback language can be selected by [en|fi|se] option."
        "The program also creates a summary file (summary.csv) that contains a short summary about"
        " each file and a link to full feedback in github")


    group = parser.add_mutually_exclusive_group()
    group.add_argument("-en", action="store_true",help='Feedback in English (default)')
    group.add_argument("-fi", action="store_true",help='Feedback in Finnish')
    group.add_argument("-se", action="store_true",help='Feedback in Swedish')


    parser.add_argument("path", type=str, help="path to a directory that contains student answer files")
    parser.add_argument("reference", type=str, help="file that contains correct sql-statements")
    args = parser.parse_args()

    print(args.path,args.reference)

    lang = 'Finnish' if args.fi\
            else 'Swedish' if args.se\
            else 'English'

    print(lang)

    modelfile = args.reference
    path = args.path

    # Add more fine grained and informative checks before advancing
    # separate checks and messages for path and referencefile
    # maybe also check that the directory contains sql-files
    if os.path.exists(path) and os.path.isfile(modelfile):
        a = CheckSQLFiles(path, modelfile,lang)
        a.process()
        print('\nModel file used for tests:', modelfile)
    else:
        print("Non-existent student directory or modelfile")
