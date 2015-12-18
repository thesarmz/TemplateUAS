from django.http import HttpResponse
from django.shortcuts import redirect,render
from lists.models import Item, List
from random import randint

def home_page(request):
#    if request.method == 'POST':      
#        Item.objects.create(text=request.POST['item_text'])  #2
#        return redirect('/lists/the-only-list-in-the-world/')

    comment = 'yey, waktunya berlibur'
	
    items = Item.objects.all()
    return render(request, 'home.html', {'comment': comment})

	
def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)

    comment = ''
    countlist = Item.objects.filter(list_id=list_.id).count()
    if countlist == 0 :
        comment = 'yey, waktunya berlibur'
    elif (countlist > 0) and (countlist < 5) :
        comment = 'sibuk tapi santai'
    else :
        comment = 'oh tidak'

    return render(request, 'list.html', {'list': list_, 'comment':comment})
	
def new_list(request):
    list_ = List.objects.create()

    number = randint(1,30)
    guessnumber = int(request.POST['item_text'])

    item = Item()
    item.number = number
    item.guessnumber = guessnumber
    item.result = game_result(guessnumber,number)
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
    
def game_result(guessnumber, number):
    range1 = number - 2
    range2 = number + 2

    if guessnumber > range1 and guessnumber < range2:
       return 'Kamu menang!!'
    else:
       return 'Kamu kalah!!' 
