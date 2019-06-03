
_PM_ITEM_INFO = {'name': None, 'request': None, 'response': None}
_PM_INFO = {'_postman_id': None, 'name': None, 'description': None, 'schema': None}

class PostmanParser(object):

    counter = 0
    collectionloop = []
    originalCollection = None

    def verifyCollection(self):
        return (_POSTMAN_INFO.keys() == self.item['info'].keys())

    def loadItem(self, collectionItem):
        self.item = collectionItem
        if(self.isValidItem(self.item) is False) or ('item' not in self.item):
            raise Exception("Not a valid postman collection item")

        PostmanParser.originalCollection = self.item['item']
        self.walker = PostmanCollectionWalker(self.item['item'])

    def isValidItem(self, item):
        return list(_PM_ITEM_INFO.keys()).sort() == list(item.keys() & _PM_ITEM_INFO.keys()).sort()

    """
    def parseRequest(self):
        ##

    def parseExamples(self):
        ##

    def parseResponse(self):
        ##
"""

class PostmanCollectionWalker(PostmanParser):
    def __init__(self, collection, init=False):
        self.collection = collection

    def isFolder(self, item):
        return True if 'item' in item else False

    def isDirectRequest(self, item):
        return ('response' in item)

    def walk(self, parent=None, level=0):
        for i, item in enumerate(self.collection):
            if(self.isFolder(item)):
                level +=  1
                # Process a folder
                print("Got a folder: ", item['name'])
                parent = item['name']

                print("Parent", parent, PostmanParser.originalCollection)
                PostmanCollectionWalker(item['item']).walk(parent, level)
            else:
                if(self.isDirectRequest(item)):
                    # Process a direct request
                    print("Parent", parent)
                    #print("Got a request:", self.collection.index(item), level, item['name'])
                    print("Got a request:", item['name'])
                else:
                    print("Got nothing", item)

class PostmanCollectionParser(object):
    def __init__(self, item):
        self.item = item
        self.Name = None
        self.CollectionItems = []
        self._parseCollection()

    def __str__(self):
        return self.item['name'] if 'name' in self.item else None

    def _parseCollection(self):
        self.Name = self.item['name'] if 'name' in self.item else None
        a = self.item if 'item' not in self.item else None
        # This is not inside a folder but a direct request
        for item in self.item['item']:
            self.CollectionItems.append(PostmanCollectionItemParser(item))

    def getCollectionItems(self):
        return self.CollectionItems

class PostmanCollectionItemParser(object):
    def __init__(self, item):
        self.item = item
        self.Examples = []
        self._parseCollectionItems()

    def __str__(self):
        return self.item['name'] if 'name' in self.item else None

    def _parseCollectionItems(self):
        self.Name = self.item['name'] if 'name' in self.item else None
        for example in self.item['response']:
            self.Examples.append(PostmanItemCollectionExample(example))

    def getExamples(self):
        return self.Examples

class PostmanItemCollectionExample(object):
    def __init__(self, example):
        self.example = example

    def __str__(self):
        return self.item['name'] if 'name' in self.item else None
