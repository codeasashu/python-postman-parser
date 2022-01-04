import re

# @TODO use Set instead of dicts below
_PM_ITEM_INFO = {'name': None, 'request': None, 'response': None}
_PM_INFO = {'_postman_id': None, 'name': None, 'description': None, 'schema': None}
_PM_ENV = {'id': None, 'name': None, 'values': None}
_regex = r"\{\{[a-zA-Z0-9_.]+\}\}"

class PostmanParser(object):

    envjson = {}

    def verifyCollection(self):
        return (_POSTMAN_INFO.keys() == self.item['info'].keys())

    def loadItem(self, collectionItem):
        self.item = collectionItem
        if(self.isValidItem(self.item) is False) or ('item' not in self.item):
            raise Exception("Not a valid postman collection item")

        self.walker = PostmanCollectionWalker()

    # env must be a json decoded dict
    def loadenv(self, env):
        if not self.isValidEnv(env):
            raise Exception("Not a valid postman env file")
        if 'values' not in env:
            raise Exception("Not a valid postman env file")

        PostmanParser.envjson = self.convert_list_to_dict(env['values'], (["key", "value"]))

    def getenv(self):
        return PostmanParser.envjson

    def convert_list_to_dict(self, json, sep=set([None, None])):
        if(sep[0] is None or sep[0] is None):
            raise Exception("Separator needs a key val pair. Missing key val")
        if isinstance(json, list):
            newkv = {}
            for item in json:
                if not sep[0] in item:
                    break
                if not sep[1] in item:
                    break
                newkv[item[sep[0]]] = item[sep[1]]
            return newkv

        return json


    def getRequests(self, callback=None):
        self.walker = PostmanCollectionWalker(callback)
        return self.walker.getRequests(self.item['item'])

    def isValid(self, prefixset, item):
        return list(prefixset.keys()).sort() == list(item.keys() & prefixset.keys()).sort()

    def isValidItem(self, item):
        return self.isValid(_PM_ITEM_INFO, item)

    def isValidEnv(self, item):
        return self.isValid(_PM_ENV, item)


class PostmanCollectionWalker(PostmanParser):
    def __init__(self, callback=None):
        self.func = callback

    def setcbfunc(self, func):
        self.func = func

    def isFolder(self, item):
        return True if 'item' in item else False

    def isDirectRequest(self, item):
        return ('response' in item)

    def getRequests(self, items, level=0, folder=None):
        level += 1
        for item in items:
            if self.isFolder(item):
                if(self.func is not None):
                    self.func(item['name'], (level - 1))
                s = self.getRequests(item['item'], level, item['name'])
                yield from s
            if self.isDirectRequest(item):
                yield (level - 1), PostmanRequestParser(item)
        level -= 1


class PostmanRequestParser(PostmanParser):
    def __init__(self, request):
        self.request = request

    def __str__(self):
        return self.getName()

    def __getitem__(self, key):
        return self.request[key]

    def getName(self):
        return self.request['name']

    def getExamples(self):
        if 'response' in self.request:
            for response in self.request['response']:
                yield PostmanExampleParser(response)

class PostmanExampleParser(PostmanParser):
    def __init__(self, example):
        self.example = example
        self.envjson = super().getenv()

    def __str__(self):
        return self.getName()

    def replaceenv(self, value):
        matches = re.findall(_regex, value)
        envkeys = [key for key in PostmanParser.envjson]
        for match in matches:
            _key = match.strip("{{").strip("}}")
            if _key in envkeys:
                val = PostmanParser.envjson[_key]
                value = value.replace(match, val)
        return value

    def getMethod(self):
        return self.example['originalRequest']['method']

    def getName(self):
        return self.example['name'] if 'name' in self.example else None

    def getHost(self):
        if not 'originalRequest' in self.example:
            return None
        return self.replaceenv(self.example['originalRequest']['url']['raw'])

    def getResponseCode(self):
        return self.example['code']

    def getRequestHeaders(self):
        headers = {}
        for header in self.example['originalRequest']['header']:
            headers[header['key']] = self.replaceenv(header['value'])
        return headers

    def getRequestBody(self):
        if 'body' not in self.example['originalRequest']:
            return None
        requestBody = self.example['originalRequest']['body']
        mode = requestBody['mode']
        if mode in ['formdata', 'urlencoded']:
            body = {}
            for item in requestBody[mode]:
                body[item["key"]] = self.replaceenv(item["value"])
        elif mode == "raw":
            body = requestBody[mode]
        return body

    def getResponseBody(self):
        return self.example['body']


