""" This program checks user submitted answer-file to sql-exercises
    The user file contains sql-statements and other text """

import re
from typing import List
from checkstatement import CompareTestResult
from checkstatement import StatementChecker
import requests
import json


# git
class SQLFileChecker:
    """
    This class is responsible for checking a file that contains sql-statements.
    Co-operations: StatementCheckers and CompareTestResult
    """

    def __init__(self, modelfile, lang):
        self.modelfile = modelfile
        self.results = List[CompareTestResult]  # Typed List
        self.lang = lang
        self.email = None

    @staticmethod
    def _findstatements(filename):
        with open(filename) as inputfile:
            text = inputfile.read()
        statements = re.findall('select[^;]*;', text,re.I)
        return statements

    def test(self, filename,testrun):
        """
        :param filename: the file to checked (actually given already in constructor)
        :param testrun: 0 normal run (posts results to github), 1 testdrive (default) doesn't post
        :return:
        """
        try:
            filename = filename
            self.results = []
            with open(filename) as myFile:
                text = myFile.read()
                match = re.search(r'(email|email:)[\s]*([\w.-]+?@[\w]+.[\w]+)', text)
                self.email = match.group(2)

            statements = self._findstatements(filename)
            model_statements = self._findstatements(self.modelfile)

            if statements:
                statement_checker = StatementChecker(self.lang)
                contents = ''
                for idx, model_statement in enumerate(model_statements):
                    if (len(statements)-1) < idx:
                        result = CompareTestResult("Missing Statement")
                    else:
                        result = statement_checker.compareSQL(statements[idx], model_statement, "harjoitukset.sqlite")

                    self.results.append(result)
                    print(result.getfeedback(idx))
                    contents = contents + '\n\n' + result.getfeedback(idx)

                    print('Feedback langugage was', self.lang)

                with open('Result.SQL', 'w', encoding='utf-8') as of:
                    of.write('-- email:' + self.email + '\n' + contents )

                tests = ''
                for idx, item in enumerate(self.results):
                    tests = tests + str(item.passlevel.value) + ','
                if testrun:
                    gisturl = "http://example.com"
                else:
                    gisturl = self.postgist('Result.SQL')

                value = self.email + ',' + filename + ',' + gisturl + ',' + tests
            else:
                value = self.email + ',' + filename + ',' + 'No sentences - maybe semicolons missing'
            return value

        except OSError as e:
            print(e)
            exit(1)

        except AttributeError:
            print(f'The file {filename}  doesn\'t contain student\'s email')
            exit(1)

    def postgist(self, filename):
        """
        Note: Keep API-TOKEN in configs.json and don't add configs.json to version control - should be secret!
        """

        # The default-value  is ANSI and the caused a lot of confusion for me before I noticed it.
        # (Good to understand for related cases the difference between the actual coding used in a file and UTF
        # E.g. no sense to later set encoding to utf-8 if file contents originally was read as ANSI-encoded)
        github_api = "https://api.github.com"

        with open('configs.json') as inputfile:
            configdata = json.load(inputfile)

        api_token = configdata['apikey']
        url = github_api + "/gists"

        with open(filename, encoding='utf-8') as myFile:
            text = myFile.read()

        print("Request URL: %s" % url)

        headers = {'Authorization': 'token %s' % api_token, 'Content-Type': 'text/html'}
        params = {'scope': 'gist'}

        payload = {"description": self.email, "public": False,
                   "files": {"Review.sql": {"content": text}}}

        res = requests.post(url, headers=headers, params=params, data=json.dumps(payload))
        j = json.loads(res.text)
        return j['html_url']
