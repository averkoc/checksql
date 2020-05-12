""" This program checks user submitted answer-file to sql-exercises
    The user file contains sql-statements and other text """

import sqlite3
import re
from sqlite3 import Error
from enum import Enum
import json


myLang = 'English' # StatementChecker constructor will modify this
messages = [] # Language dependent texts are loaded into this by set_translations function

def set_translations(myLang):
    if not myLang == 'English':
        langfile = str(myLang) + '.json'
        with open(langfile, 'r', encoding='utf-8') as fp:
            global messages
            messages = json.load(fp)


def _(i, s ):
    if not myLang == 'English':
        return (messages[str(i)])
    else:
        return s


# Enumerations for different test results
class PassLevel(Enum):
    NOTRUN = 0
    ERROR = 1
    EXECUTED = 2
    ROWCOLUMNMATCH = 3
    CONTENTMATCH = 4
    ORDERMATCH = 5


class CompareTestResult:
    def __init__(self, statement):
        self.statement = statement
        self.errormsg = ''
        self.passlevel = PassLevel.NOTRUN
        self.sampleRow = ''
        self.correctSampleRow = ''



    def getfeedback(self, index):
        feedback = _(1, "-- Your {}. SQL-statement:\n").format(index + 1) + ''.join(self.statement)

        if self.passlevel == PassLevel.NOTRUN:
            feedback = feedback + _(2, '\n-- Statement was not executed')

        if self.passlevel == PassLevel.ERROR:
            feedback = feedback + _(3, '\n-- Gave the following error message:') + self.errormsg

        if self.passlevel == PassLevel.EXECUTED:
            feedback = feedback + _(4, "n-- Run without errors but didn't meet requirements")

        if self.passlevel == PassLevel.ROWCOLUMNMATCH:
            feedback = feedback + _(5,
                                    "\n-- Produced correct number of rows and columns but contents didn't match with correct answer")

        if self.passlevel == PassLevel.CONTENTMATCH:
            feedback = feedback + _(6, "\n-- Produced correct result!")

        if self.passlevel in (PassLevel.EXECUTED, PassLevel.ROWCOLUMNMATCH, PassLevel.CONTENTMATCH, PassLevel.ORDERMATCH):
            feedback = feedback + _(7, '\n-- Sample rows from your query and model answer\n--') + json.dumps(
                self.sampleRow, ensure_ascii=False)
            feedback = feedback + '\n--' + json.dumps(self.correctSampleRow, ensure_ascii=False)

        return feedback


class StatementChecker:
    def __init__(self, lang):
        global myLang
        myLang = lang
        set_translations(myLang)

    def compareSQL(self,statement: str, refstatement: str, db: str) -> CompareTestResult:
        compareResult = CompareTestResult(statement)

        conn = sqlite3.connect(db)
        c = conn.cursor()
        try:
            c.execute(statement)
            rows1 = c.fetchall()
            compareResult.passlevel = PassLevel.EXECUTED

            if len(rows1) > 0:
                compareResult.sampleRow = rows1[0]

            c.execute(refstatement)
            rows2 = c.fetchall()
            if len(rows2) > 0:
                compareResult.correctSampleRow = rows2[0]

            columns1 = 0 if len(rows1) == 0 else len(rows1[0])
            columns2 = 0 if len(rows2) == 0 else len(rows2[0])

            # Does number of rows and columns match with reference statement result
            if (len(rows1), columns1) == (len(rows2), columns2):
                compareResult.passlevel = PassLevel.ROWCOLUMNMATCH

                # Contents match test
                # Temp tables needed because possible 'order by' allowed only in the end of stmt
                c.execute('drop table if exists  temp1;')
                c.execute('drop table if exists  temp2')
                c.execute('create table temp1 as ' + statement)
                c.execute('create table temp2 as ' + refstatement)
                c.execute('select * from temp1 except select * from temp2;')
                rows = c.fetchall()
                if len(rows) == 0:
                    compareResult.passlevel = PassLevel.CONTENTMATCH

            if len(rows1) > 0:
                compareResult.samplerow = rows1[0]

        except Error as e:
            compareResult.passlevel = PassLevel.ERROR
            compareResult.errormsg = e.__str__()
            pass

        return compareResult
