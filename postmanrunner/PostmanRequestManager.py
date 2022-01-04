import requests


class PostmanRequestManager(object):

    def getMethod(self, request):
        return request.getMethod()

    def getHeaders(self, request):
        return request.getRequestHeaders()

    def getData(self, request):
        return request.getRequestBody()

    def RunExample(self, example):
        url = example.getHost()
        headers = example.getRequestHeaders()
        data = example.getRequestBody()
        method = example.getMethod()

        response = requests.request(method, url, headers=headers, data=data)
        print(response)
        return True
