from django.shortcuts import render,HttpResponse
import logging
def test_log(request):
    try:
        lists = [1,3,2,4,5,6,7]
    except Exception as err:
        logging.error(err)
    return HttpResponse('hah')

