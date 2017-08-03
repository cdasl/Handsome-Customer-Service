from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt

def getData(request):
	List = ['自强学堂', '渲染Json到模板']
	return render(request, 'getData.html', {'List': List})

@csrf_exempt
def test(request):
	data = {"name": "Jing"}
    #ensure_ascii=False用于处理中文
	return JsonResponse(data)