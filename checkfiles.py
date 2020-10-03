import os
import argparse

from checkfile import SQLFileChecker


class CheckSQLFiles:
    """
    This is the main class of submissions checker program
    """
    def __init__(self, directory, model_file, feedback_lang,summaryfile,testrun):
        self.direcotry = directory
        self.modelfile = model_file
        self.filechecker = SQLFileChecker(modelfile, feedback_lang)
        self.summaryfile = summaryfile


    def _update_csv(self,summary):
        with open(self.summaryfile, 'a', encoding='utf-8') as out_file:
            out_file.write(summary + '\n')

    def process(self,path,testrun):
        files = os.listdir(path)
        sqlfiles = [f for f in files if f.endswith('.sql')]
        for sql_file in sqlfiles:
            print('\nChecking file:' + sql_file + '\n')
            summary: str = self.filechecker.test(path + '\\' + sql_file,testrun)
            self._update_csv(summary)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='The program checks .sql files in the given directory by comparing each file'
                    ' contents to the reference file.'
                    'It writes feedback about each file  to github.'
                    'The feedback language can be selected by [en|fi|se] option.'
                    'The program also creates a summary file (summary.csv) that contains a short'
                    ' summary about'
                    ' each file and a link to full feedback in github.'
                    ' Due to the fact that there may well be student sql-files that dont comply with the formatting requirements,'
                    ' e.g. missing email, the default execution is test run ')

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-en", action="store_true", help='Feedback in English (default)')
    group.add_argument("-fi", action="store_true", help='Feedback in Finnish')
    group.add_argument("-se", action="store_true", help='Feedback in Swedish')

    parser.add_argument("path", type=str, help="path to a directory that contains student answer files")
    parser.add_argument("reference", type=str, help="file that contains correct sql-statements")
    parser.add_argument("-sf", type=str, default='summary.csv', help="SF is the file where the program writes summary (default summary.csv)")
    parser.add_argument("-tr", type=int,default=1, help="If TR is 1 (default) doesn't post to gist, 0 normal execution")
    args = parser.parse_args()

    print(args.path, args.reference,args.sf)

    lang = 'Finnish' if args.fi \
        else 'Swedish' if args.se \
        else 'English'

    print(lang)

    modelfile = args.reference
    path = args.path

    # Add more fine grained and informative checks before advancing
    # separate checks and messages for path and referencefile
    # maybe also check that the directory contains sql-files
    if os.path.exists(path) and os.path.isfile(modelfile):
        a = CheckSQLFiles(path, modelfile, lang,args.sf,args.tr)
        a.process(path,args.tr)
        print('\nModel file used for tests:', modelfile)
    else:
        print("Non-existent student directory or modelfile")
