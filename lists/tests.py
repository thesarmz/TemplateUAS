from lists.models import Item, List
from django.template.loader import render_to_string
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page

class ListAndItemModelsTest(TestCase):

    def test_displays_record_in_specific_url(self): #e
        correct_list = List.objects.create()
        Item.objects.create(guessnumber=22, number=16, result='Kamu kalah!!', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(guessnumber=15, number=14, result='Kamu menang!!', list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'Tebakan: 22')
        self.assertContains(response, 'Angka: 16')
        self.assertContains(response, 'Kamu kalah!!')
        self.assertNotContains(response, 'Tebakan: 15')
        self.assertNotContains(response, 'Angka: 14')
        self.assertNotContains(response, 'Kamu menang!!')

    def test_no_win(self):
        correct_list = List.objects.create()

        Item.objects.create(guessnumber=15, number=14, result='Kamu menang!!', list=correct_list)        

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertNotContains(response, 'Ulala')
        self.assertNotContains(response, 'Ulalala')
        self.assertNotContains(response, 'Uulala')                

    def test_three_win(self):
        correct_list = List.objects.create()

        Item.objects.create(guessnumber=15, number=14, result='Kamu menang!!', list=correct_list)
        Item.objects.create(guessnumber=12, number=12, result='Kamu menang!!', list=correct_list)
        Item.objects.create(guessnumber=25, number=27, result='Kamu menang!!', list=correct_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'Ulala')

    def test_five_win(self):
        correct_list = List.objects.create()

        Item.objects.create(guessnumber=15, number=14, result='Kamu menang!!', list=correct_list)
        Item.objects.create(guessnumber=12, number=12, result='Kamu menang!!', list=correct_list)
        Item.objects.create(guessnumber=25, number=27, result='Kamu menang!!', list=correct_list)
        Item.objects.create(guessnumber=8, number=9, result='Kamu menang!!', list=correct_list)
        Item.objects.create(guessnumber=2, number=1, result='Kamu menang!!', list=correct_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'Ulalala')

    def test_ten_win(self):
    	correct_list = List.objects.create()

    	Item.objects.create(guessnumber=15, number=14, result='Kamu menang!!', list=correct_list)
    	Item.objects.create(guessnumber=12, number=12, result='Kamu menang!!', list=correct_list)
    	Item.objects.create(guessnumber=25, number=27, result='Kamu menang!!', list=correct_list)
    	Item.objects.create(guessnumber=8, number=9, result='Kamu menang!!', list=correct_list)
    	Item.objects.create(guessnumber=2, number=1, result='Kamu menang!!', list=correct_list)
    	Item.objects.create(guessnumber=11, number=12, result='Kamu menang!!', list=correct_list)
    	Item.objects.create(guessnumber=14, number=14, result='Kamu menang!!', list=correct_list)
    	Item.objects.create(guessnumber=22, number=20, result='Kamu menang!!', list=correct_list)
    	Item.objects.create(guessnumber=5, number=6, result='Kamu menang!!', list=correct_list)
    	Item.objects.create(guessnumber=19, number=18, result='Kamu menang!!', list=correct_list)

    	response = self.client.get('/lists/%d/' % (correct_list.id,))

    	self.assertContains(response, 'Uulala')


class ListViewTest(TestCase):

    def test_displaying_record_to_website(self): #b
        correct_list = List.objects.create()
        Item.objects.create(guessnumber=22, number=16, result='Kamu kalah!!', list=correct_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'Tebakan: 22')
        self.assertContains(response, 'Angka: 16')
        self.assertContains(response, 'Kamu kalah!!')

    def test_passes_correct_list_to_template(self): #c
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

class NewListTest(TestCase):

   def test_saving_record_to_database(self): #a
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': '15'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.guessnumber, 15)
        self.assertEqual(new_item.list, correct_list)

class NewItemTest(TestCase):

    def test_saving_a_POST_request_to_an_existing_record_and_displaying_it(self): #d
        correct_list = List.objects.create()
        Item.objects.create(guessnumber=22, number=16, result='Kamu kalah!!', list=correct_list)

        self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': '15'}
        )

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'Tebakan: 22')
        self.assertContains(response, 'Angka: 16')
        self.assertContains(response, 'Kamu kalah!!')
        self.assertEqual(Item.objects.count(), 2)