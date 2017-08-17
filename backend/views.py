from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json, hashlib, time
from django.conf import settings

def getData(request):
	List = ['自强学堂', '渲染Json到模板']
	return render(request, 'getData.html', {'List': List})

@csrf_exempt
def test(request):
	data = {"name": "Jing"}
    #ensure_ascii=False用于处理中文
	return JsonResponse(data)

@ensure_csrf_cookie
def store_image(request):
    file = request.FILES['image']
    md5 = hashlib.md5()
    md5.update(str(int(time.time())).encode('utf8'))
    name = md5.hexdigest() + '.png'
    with open('frontend/static/upload/' + name, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    with open('frontend/dist/static/upload/' + name, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return JsonResponse({'url': '/static/upload/' + name})

@ensure_csrf_cookie
def customer_active(request):
    return render(request, 'customer_active.html')

@ensure_csrf_cookie
def enterprise_manage(request):
    return render(request, 'enterprise_manage.html')
