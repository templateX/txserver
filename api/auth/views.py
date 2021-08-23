from django.http import HttpResponse

def github_callback(request):
    print(request.GET)
    return HttpResponse('Done')
