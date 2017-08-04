from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
from django.conf import settings

def getData(request):
	List = ['自强学堂', '渲染Json到模板']
	return render(request, 'getData.html', {'List': List})

@csrf_exempt
def test(request):
	data = {"name": "Jing"}
    #ensure_ascii=False用于处理中文
	return JsonResponse(data)

@csrf_exempt
def validate_customer(request):
    file = request.FILES['image']
    req = request.POST['user']
    with open('image/aa.jpg', 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return JsonResponse({'message': req})

@csrf_exempt
def customer_active(request):
    return render(request, 'customer_active.html')