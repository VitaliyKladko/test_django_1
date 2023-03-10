from django.http import HttpResponse
from django.http import JsonResponse
from vacancies.models import Vacancy


# from django.shortcuts import render


def index(request):
    return HttpResponse('index page')


def hello(request):
    return HttpResponse('Hello, Dima')


def index_vacancies(request):
    """
    В request (класс) есть практически вся инфа о поступившем запросе
    objects - это формально ORM и в дальнейшем позволит нам обращаться к данным из БД
    """
    if request.method == 'GET':
        vacancies = Vacancy.objects.all()

        # реализуем поиск по вакансии по ее полному тексту (просто как пример)
        # get вызываем у атрибута .GET так как если этого не сделать, то падаем с ошибкой MultiValueDictKeyError
        # MultiValueDictKeyError - не передали text в квери-параметрах
        search_text = request.GET.get('text', None)
        if search_text is not None:
            vacancies = vacancies.filter(text=search_text)

        response = []
        for vacancy in vacancies:
            response.append(
                {
                    'id': vacancy.id,
                    'text': vacancy.text,
                }
            )
        # safe=False позволяет "скушать" JsonResponse словарь, говоря, что ничего не сломается при серриализации и
        # отключи все проверки при переводе в json
        return JsonResponse(response, safe=False)


def get_vacancies_from_id(request, vacancy_id):
    if request.method == 'GET':
        try:
            vacancy = Vacancy.objects.get(pk=vacancy_id)
        except Vacancy.DoesNotExist:
            return JsonResponse({
                'error': 'Not found'
            }, status=404)

        return JsonResponse({
            'id': vacancy.id,
            'text': vacancy.text,
        })
