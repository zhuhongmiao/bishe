import json

from django.http import JsonResponse



class ResponseMessage():

    @staticmethod
    def success(data,status=200,msg="success"):
        result = {"code":status,"msg":msg,"data":data}
        return JsonResponse(result,safe=False)

    @staticmethod
    def failed(msg,status=400,data={}):
        result = {"code": 400, "msg": msg, "data": data}
        return JsonResponse(result, safe=False)