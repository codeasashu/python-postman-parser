import os, json, sys
import argparse

from PostmanParser import PostmanParser as parser
from PostmanRequestManager import PostmanRequestManager as requestmanager


class PostmanRunner(object):
    def __init__(self, filename, parser=parser, requestmanager=requestmanager):
        self.file = filename
        os.stat(filename) #Exception if file not exists
        self.parser = parser()
        self.pmhttp = requestmanager()

    def environment(self, envfile):
        self.envfile = envfile
        os.stat(envfile)

        if not self.parser:
            raise Exception("No parser is set")

        envf = open(envfile, 'rb')
        envcontents = envf.read()
        self.parser.loadenv(json.loads(envcontents))

    def attachFbCallback(self, foldername, level):
        print("\t" * level, foldername)

    def run(self, debug=False):
        self.debug = debug
        f = open(self.file, 'rb')
        contents = f.read()
        try:
            self.json = json.loads(contents)
        except json.decoder.JSONDecodeError:
            raise Exception("Invalid json")

        self.parseCollection()

    def parseCollection(self):
        self.parser.loadItem(self.json)
        for level, request in self.parser.getRequests(self.attachFbCallback):
            print('\t' * level, "Executing: ", request)
            for example in request.getExamples():
                print('\t' * (level + 1), "Example - ", example.getName(), example.getRequestBody())
                success = self.pmhttp.RunExample(example)
                if success is True:
                    print('\t' * (level + 1), "...Success")
                else:
                    print('\t' * (level + 1), "...Errored")
                break
            print('\n')

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Parse postman Collection')
    parser.add_argument('--env',
                        help='Environment file to read')
    parser.add_argument('json', nargs=1,
                        help='Postman collection file')

    args = parser.parse_args()
    filename = args.json[0]
    a = PostmanRunner(filename)
    a.environment(args.env)
    a.run(True)
