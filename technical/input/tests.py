import pandas as pd
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
import json

from .forms import NewExcelImport, NewSelectForm
from .models import Result, Input
from .ingest import engine


# Create your tests here.
class InputModelTest(TestCase):
    def setUp(self):
        self.invoice = Input.objects.create(
            date='2023-04-30',
            invoice_number=3531,
            value=519.5,
            haircut=10,
            daily_fee=0.125,
            currency='USD',
            revenue_src='Happy Playcrows',
            customer='RunUp INC',
            expected_payment_duration=65,
            epoch=1
        )

    def test_input_model_exists(self):
        # Warning caused by PyCharm Comm. not supporting Django specifics
        invoices = Input.objects.count()
        self.assertEqual(invoices, 1) # The one from the setup

    def test_model_to_json(self):
        invoice = self.invoice
        self.assertEqual(invoice.getData(),{
                'date': '2023-04-30',
                'invoice_number': 3531,
                'value': 519.5,
                'haircut': 10,
                'daily_fee': 0.125,
                'currency': 'USD',
                'revenue_src': 'Happy Playcrows',
                'customer': 'RunUp INC',
                'expected_payment_duration': 65,
                'epoch': 1
            })

    def test_model_to_string(self):
        invoice = self.invoice
        self.assertEqual(str(invoice), json.dumps(
            {
                'date': '2023-04-30',
                'invoice_number': 3531,
                'value': 519.5,
                'haircut': 10,
                'daily_fee': 0.125,
                'currency': 'USD',
                'revenue_src': 'Happy Playcrows',
                'customer': 'RunUp INC',
                'expected_payment_duration': 65,
                'epoch': 1
            }))

class ResultModelTest(TestCase):
    def setUp(self):
        self.result = Result.objects.create(
            revenue_src="test",
            value=3.9,
            advance=3.9,
            expected_fee=3.9,
            epoch=1
        )

    def test_input_model_exists(self):
        # Warning caused by PyCharm Comm. not supporting Django specifics
        result = Result.objects.count()
        self.assertEqual(result, 1) # The one from the setup

    def test_result_model_to_json(self):
        result = self.result
        self.assertEqual(result.getData(), {
            'revenue_src':"test",
            'value':3.9,
            'advance':3.9,
            'expected_fee':3.9,
            'epoch': 1
        })

    def test_result_model_to_string(self):
        result = self.result
        self.assertEqual(str(result), json.dumps(
            {
                'revenue_src':"test",
                'value':3.9,
                'advance':3.9,
                'expected_fee':3.9,
                'epoch': 1
            }))


class IndexPageTest(TestCase):
    def setUp(self):
        self.form = NewExcelImport
        self.select = NewSelectForm

    def test_index_page_returns_200(self):
        response = self.client.get('/dashboard/')
        self.assertTemplateUsed(response, 'input/index.html')
        self.assertEqual(response.status_code, 200)

    def test_index_form_structure_is_correct(self):
        response = self.client.get('/dashboard/')
        self.assertContains(response, '<form ')
        self.assertContains(response, 'enctype="multipart/form-data')
        self.assertContains(response, '<label for')

    def test_index_file_form_cannot_be_empty(self):
        self.assertTrue(issubclass(self.form, NewExcelImport))
        self.assertTrue('file' in self.form.Meta.fields)
        form = self.form({'file': None})
        self.assertFalse(form.is_valid())

    def test_index_select_form_cannot_be_empty(self):
        self.assertTrue(issubclass(self.select, NewSelectForm))
        self.assertTrue('Id' in self.select.Meta.fields)
        form = self.form({'Id': None})
        self.assertFalse(form.is_valid())

    def test_index_file_form_can_be_valid(self):
        self.assertTrue(issubclass(self.form, NewExcelImport))
        self.assertTrue('file' in self.form.Meta.fields)
        # Shenanigans https://docs.djangoproject.com/en/5.0/ref/forms/api/#binding-uploaded-files-to-a-form
        f = SimpleUploadedFile("test.txt", b"Unit Testing")
        file_att = {'file': f}
        form = NewExcelImport({}, file_att)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())

    def test_index_select_form_cam_be_valid(self):
        self.assertTrue(issubclass(self.select, NewSelectForm))
        self.assertTrue('Id' in self.select.Meta.fields)
        select = self.select({'Id': 123})
        self.assertTrue(select.is_valid())


class WebServicesTest(APITestCase):
    def test_ws_excel_returns_200(self):
        f = SimpleUploadedFile("test.txt", b"Unit Testing")
        r = self.client.post(path='/input/', file=f)
        self.assertEqual(r.status_code, 200)

    def test_ws_excel_wrong_format_returns_err(self):
        f = SimpleUploadedFile("test.txt", b"Unit Testing")
        r = self.client.post(path='/input/', file=f)
        self.assertTrue(r.data["status"] == "Error")
        self.assertTrue("Description" in r.data.keys())

    def test_ws_result_returns_200(self):
        r = self.client.get(path='/1234/')
        self.assertEqual(r.status_code, 200) # I dont get it, this works just fine on postman

    def test_ws_result_invalid_id_returns_err(self):
        r = self.client.get(path='/999999999/')
        self.assertEqual(r.json(), {'Error': "The provided ID doesn't exist in the database"})

    def test_ws_wrong_methods_dont_throw_500(self):
        r = self.client.get(path='localhost:8000/input/')
        self.assertNotEquals(r.status_code, 500)
        r = self.client.post(path='localhost:8000/1234/')
        self.assertNotEquals(r.status_code, 500)

    def test_ws_result_correct_result(self):
        result = Result.objects.create(
            revenue_src="test",
            value=3.9,
            advance=3.9,
            expected_fee=3.9,
            epoch=1
        )
        r = self.client.get(path='/1/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(type(r.data), list)
        self.assertEqual(json.dumps(r.data[0]), str(result))

    #TODO: test correct results insert

class IngestionEngineTest(TestCase):
    def test_ingestion_works(self):
        self.assertTrue(engine.insert_into_db(pd.DataFrame(), 1))

    def test_ingest_return_err_description_on_exception(self):
        self.assertTrue(isinstance(engine.insert_into_db(['not_a_dataframe'], 1), dict))







