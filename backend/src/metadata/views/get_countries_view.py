from django.http import JsonResponse
from django_countries import countries


def get_countries(request):
    country_data = [{'code': code, 'name': name} for code, name in countries]
    return JsonResponse(country_data, safe=False)
