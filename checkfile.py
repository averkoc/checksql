""" This program checks user submitted answer-file to sql-exercises
    The user file contains sql-statements and other text """

import re
from checkstatement import CompareTestResult
from checkstatement import StatementChecker
import requests
import json

# git
class SQLFileChecker:
    def __init__(self, modelfile,lang):
        self.modelfile = modelfile
        self.results:CompareTestResult = []
        self.lang = lang
        self.email = None
        self.filename = None

    def _findstatements(self,filename):
        with open(self.filename) as inputfile:
            text = inputfile.read()
        statements = re.findall('select[^;]*;', text)
        return statements

    def test(self,filename):
        try:
            self.filename = filename
            self.results.clear()
            with open(filename) as myFile:
                text = myFile.read()
                match = re.search('email:[\s]*([\w\.]+@[\w]+.[\w]+)',text)
                self.email = match.group(1)


            statements =  self._findstatements(self.filename)
            model_statements = self._findstatements(self.modelfile)


            if statements:
                statementChecker = StatementChecker(self.lang)
                contents = ''
                for idx, statement in enumerate(statements):
                    result = statementChecker.compareSQL(statement, model_statements[idx], "harjoitukset.sqlite")
                    self.results.append(result)
                    print(result.getfeedback(idx))
                    contents = contents + '\n\n' + result.getfeedback(idx)

                    print('Feedback langugage was',self.lang)
                with open('Result.SQL','w', encoding='utf-8') as of:
                    of.write('-- email:' + self.email + '\n' + contents)

            tests = ''
            for idx,item in enumerate(self.results):
                tests = tests + str(item.passlevel.value) + ','

            gisturl = self.postgist('Result.SQL')
            value = self.email + ',' + self.filename + ',' + gisturl + ',' + tests
            return (value)



        except OSError as e:
            print(e)
            exit(1)

        except AttributeError as e:
            print(f'The file {self.filename}  doesn\'t contain student\'s email')
            exit(1)

    def postgist(self,filename):
        """
        Note: Keep API-TOKEN in configs.json and don't add configs.json to version control - should be secret!
        """


        # The default-value  is ANSI and the caused a lot of confusion for me before I noticed it.
        # (Good to understand for related cases the difference between the actual coding used in a file and UTF
        # E.g. no sense to later set encoding to utf-8 if file contents originally was read as ANSI-encoded)
        GITHUB_API = "https://api.github.com"
        
        with open('configs.json','r') as inputfile:
            configdata = json.load(inputfile)

        API_TOKEN = configdata['apikey']
        url = GITHUB_API + "/gists"

        with open(filename, encoding='utf-8') as myFile:
            text = myFile.read()

        print("Request URL: %s" % url)

        headers = {'Authorization': 'token %s' % API_TOKEN, 'Content-Type': 'text/html'}
        params = {'scope': 'gist'}

        payload = {"description": self.email, "public": False,
                   "files": {"Review.sql": {"content": text}}}

        res = requests.post(url, headers=headers, params=params, data=json.dumps(payload))
        j = json.loads(res.text)
        return j['html_url']
