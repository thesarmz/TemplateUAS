from django.http import HttpResponse
from django.shortcuts import redirect, render
from lists.models import Item, List

# Create your views here.
def home_page(request):
    #if request.method == 'POST':
    #    Item.objects.create(text=request.POST['item_text'])
    #    return redirect('/lists/the-only-list-in-the-world/')

    #items = Item.objects.all()
    countsItem = Item.objects.count()
    comment = 'yey, waktunya berlibur'

    return render(request, 'home.html', {'comment': comment})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    comment = ''
    countList = Item.objects.filter(list_id=list_.id).count()
    if countList == 0:
        comment = 'yey, waktunya berlibur'
    elif (countList > 0) and (countList < 5):
        comment = 'sibuk tapi santai'
    else:
        comment = 'oh tidak'
    return render(request, 'list.html', {'list': list_, 'comment': comment})

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id,))