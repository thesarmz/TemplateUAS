from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.models import Item, List
from lists.views import home_page


class ListAndItemModelsTest(TestCase):

    def test_displays_record_in_specific_url(self): #e
        correct_list = List.objects.create()
        Item.objects.create(guessnumber=22, number=16, result='Kamu kalah!!', list = correct_list))
       
         other_list = List.objects.create()
        Item.objects.create(guessnumber=15, number=14, result='Kamu menang!!', list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'Tebakan: 22')
        self.assertContains(response, 'Angka: 16')
        self.assertContains(response, 'Kamu kalah!!')
        self.assertNotContains(response, 'Tebakan: 15')
        self.assertNotContains(response, 'Angka: 14')
        self.assertNotContains(response, 'Kamu menang!!')


class ListViewTest(TestCase):

    def test_displays_record_to_website(self):#b
        correct_list - List.objects.create()
        Item.objects.create(guessnumber=22,number=1,result='Kamu kalah!!', list=correct_list)

        response = self.client.get('/list/%d/' % (correct_list.id,))
    
        self.assertContains(response, 'Tebakkah angka: 22')
        self.assertContains(response, 'Angka: 1')
        self.assertContains(response, 'Kamu kalah!!')

    

    def test_passes_correct_list_to_template(self): #c
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)
        self.assertNotEqual(response.context['list'], other_list)
    
    
class NewListTest(TestCase):
     
    def test_saving_record_to_database(self): #a
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/add_item' % (coorect_list.id),
            data={'item_text': '15'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.guessnumber, 15)

    
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
