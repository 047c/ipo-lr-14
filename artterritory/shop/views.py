from django.http import HttpResponse
from . import specialty_search
  
def index(request):
    return HttpResponse("Приложение для управления работает!")

def author(request):
    return HttpResponse("<div><h1>Лабу сделал:</h1><h2>Имя: Владислав</h2><h2>Фамилия: Цветков</h2><h2>Отчество: Артурович</h2><h2>Группа: 82ТП</h2></div>")

def shop(request):
    return HttpResponse('<div><h1>Тема лабы:</h1><h2 style="width: 50%">Магазин наборов для рисования граффити (баллончики, трафареты).</h2></div>')

def specialty_byid(request, id):
    return HttpResponse(specialty_search.spSearch(by_id=id))

def specialty(request):
    return HttpResponse(specialty_search.spSearch())

def main(request):
    return HttpResponse('<div style="display: flex; align-items: center; flex-direction: column;"><h1>Добро пожаловать!</h1><div style="display: flex; justify-content: space-around; width: 100%"><h2 style="width: 50%"><a href="author/">Автор</a></h2><h2><a href="shop/">Магазин</a></h2></div></div>')