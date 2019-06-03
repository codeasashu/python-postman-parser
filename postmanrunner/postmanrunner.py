import os, json, sys

from PostmanParser import PostmanParser as parser
#import RequestManager as request


class PostmanRunner(object):
    def __init__(self, filename):
        f = open(filename, 'rb')
        contents = f.read()
        self.json = json.loads(contents)
        self.parser = parser()

    def parseCollection(self):
        self.parser.loadItem(self.json)
        self.parser.walker.walk()

"""
        items = self.json['item']
        for collection in items:
            self.parser.loadItem(collection)
            self.parser.walker.setCallback(lambda: x)
            collections = 
            collectionItem = self.parser.getCollection()
            print("Running collection - ", collectionItem)
            ## Get all examples here
            for item in collectionItem.getCollectionItems():
                print("\t Running collection item: %s",item)
"""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Not enough arguments")
        sys.exit(2)
    filename = sys.argv[-1]
    a = PostmanRunner(filename)
    a.parseCollection()
