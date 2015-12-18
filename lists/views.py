from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect, render
from lists.models import Item, List
from random import randint

# Create your views here.

def home_page(request):
      items = Item.objects.all()
      itemsCount = Item.objects.count()
      comment = 'yey, waktunya berlibur'

      return render(request, 'home.html', {'comment': comment})

def view_list(request, list_id):
      list_ = List.objects.get(id=list_id)
      komentar = comment(list_)

      return render(request, 'list.html', {'list': list_, 'komentar': komentar})

def new_list(request):
      list_ = List.objects.create()

      number = randint(1,30)
      guessnumber = int(request.POST['item_text'])

      item = Item()
      item.number = number
      item.guessnumber = guessnumber
      item.result = game_result(number, guessnumber)
      item.list = list_
      item.save()
      
      return redirect('/lists/%d/' % (list_.id,))

def add_item(request, list_id):
      list_ = List.objects.get(id=list_id)
      
      number = randint(1,30)
      guessnumber = int(request.POST['item_text'])

      item = Item()
      item.number = number
      item.guessnumber = guessnumber
      item.result = game_result(number, guessnumber)
      item.list = list_
      item.save()

      return redirect('/lists/%d/' % (list_.id,)) 

def game_result(num, gnum):
      range1 = num - 2
      range2 = num + 2

      if gnum > range1 and gnum < range2:
           return 'Kamu menang!!'
      else:
           return 'Kamu kalah!!'

def comment(list_num):
      list_temp =  Item.objects.filter(list=list_num).reverse()
      counter = 0
      komen = ''

      if len(list_temp) < 3:
         return komen

      for i in range(3):
          item = list_temp[i]
          if item.result == 'Kamu menang!!':
               counter = counter +1
    
      if counter == 3:
           komen = 'Ulala'

      if len(list_temp) < 5:
         return komen
      
      counter = 0
      
      for i in range(5):
          item = list_temp[i]
          if item.result == 'Kamu menang!!':
               counter = counter +1
    
      if counter == 5:
           komen = 'Ulalala'

      if len(list_temp) < 10:
           return komen

      counter = 0
      
      for i in range(10):
          item = list_temp[i]
          if item.result == 'Kamu menang!!':
               counter = counter +1
    
      if counter == 10:
           komen = 'Uulala'

      return komen
