from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import File
from django.test import TestCase
from .forms import NewInputForm, NewExcelImport
import json

# Create your tests here.
# class InputModelTest(TestCase):
#     def setUp(self):
#         self.invoice = Input.objects.create(
#             date='2023-04-30',
#             invoice_number=3531,
#             value=519.5,
#             haircut=10,
#             daily_fee=0.125,
#             currency='USD',
#             revenue_src='Happy Playcrows',
#             customer='RunUp INC',
#             expected_payment_duration=65,
#             epoch=1
#         )
# 
#     def test_input_model_exists(self):
#         # Warning caused by PyCharm Comm. not supporting Django specifics
#         invoices = Input.objects.count()
#         self.assertEqual(invoices, 1) # The one from the setup
# 
#     def test_model_to_json(self):
#         invoice = self.invoice
#         self.assertEqual(invoice.getData(),{
#                 'date': '2023-04-30',
#                 'invoice_number': 3531,
#                 'value': 519.5,
#                 'haircut': 10,
#                 'daily_fee': 0.125,
#                 'currency': 'USD',
#                 'revenue_src': 'Happy Playcrows',
#                 'customer': 'RunUp INC',
#                 'expected_payment_duration': 65,
#                 'posix': 1
#             })
# 
#     def test_model_to_string(self):
#         invoice = self.invoice
#         self.assertEqual(str(invoice), json.dumps(
#             {
#                 'date': '2023-04-30',
#                 'invoice_number': 3531,
#                 'value': 519.5,
#                 'haircut': 10,
#                 'daily_fee': 0.125,
#                 'currency': 'USD',
#                 'revenue_src': 'Happy Playcrows',
#                 'customer': 'RunUp INC',
#                 'expected_payment_duration': 65,
#                 'posix': 1
#             }))
# 
# 
# class ResultModelTest(TestCase):
#     def setUp(self):
#         self.result = Result.objects.create(
#             revenue_src="test",
#             value=3.9,
#             advance=3.9,
#             expected_fee=3.9
#         )
# 
#     def test_input_model_exists(self):
#         # Warning caused by PyCharm Comm. not supporting Django specifics
#         result = Result.objects.count()
#         self.assertEqual(result, 1) # The one from the setup
# 
#     def test_result_model_to_json(self):
#         result = self.result
#         self.assertEqual(result.getData(), {
#             'revenue_src':"test",
#             'value':3.9,
#             'advance':3.9,
#             'expected_fee':3.9
#         })
# 
#     def test_result_model_to_string(self):
#         result = self.result
#         self.assertEqual(str(result), json.dumps(
#             {
#                 'revenue_src':"test",
#                 'value':3.9,
#                 'advance':3.9,
#                 'expected_fee':3.9
#             }))
# 
# 
class IndexPageTest(TestCase):
    def setUp(self):
        self.form = NewExcelImport

    def test_index_page_returns_200(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'input/index.html')
        self.assertEqual(response.status_code, 200)

    def test_index_form_structure_is_correct(self):
        response = self.client.get('/')
        self.assertContains(response, '<form enctype="multipart/form-data')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, '<label for')

    def test_index_form_cannot_be_empty(self):
        self.assertTrue(issubclass(self.form, NewExcelImport))
        self.assertTrue('file' in self.form.Meta.fields)
        form = self.form({'file': None})
        self.assertFalse(form.is_valid())

    def test_index_form_can_be_valid(self):
        self.assertTrue(issubclass(self.form, NewExcelImport))
        self.assertTrue('file' in self.form.Meta.fields)
        # Shenanigans https://docs.djangoproject.com/en/5.0/ref/forms/api/#binding-uploaded-files-to-a-form
        f = SimpleUploadedFile("test.txt", b"Unit Testing")
        file_att = {'file': f}
        form = NewExcelImport({}, file_att)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())



    # def test_index_form_can_be_valid_or_display_error(self):
    #     response = self.client.get('/')
    #     self.assertTrue(issubclass(self.form, NewInputForm))
    #     self.assertTrue('date' in self.form.Meta.fields)
    #     self.assertTrue('invoice_number' in self.form.Meta.fields)
    #     self.assertTrue('value' in self.form.Meta.fields)
    #     form = self.form({
    #         'date': '2023-04-30',
    #         'invoice_number': 3531,
    #         'value': 519.5,
    #         'haircut': 10,
    #         'daily_fee': 0.125,
    #         'currency': 'USD',
    #         'revenue_src': 'Happy Playcrows',
    #         'customer': 'RunUp INC',
    #         'expected_payment_duration': 65
    #     })
    #     self.assertTrue('haircut' in self.form.Meta.fields)
    #     self.assertTrue('daily_fee' in self.form.Meta.fields)
    #     self.assertTrue('currency' in self.form.Meta.fields)
    #     self.assertTrue('revenue_src' in self.form.Meta.fields)
    #     self.assertTrue('customer' in self.form.Meta.fields)
    #     self.assertTrue('expected_payment_duration' in self.form.Meta.fields)
    #     self.assertTrue(form.is_valid())
    #
    #     form = self.form({
    #         'date': '',
    #         'invoice_number': 3531,
    #         'value': 519.5,
    #         'haircut': 10,
    #         'daily_fee': 0.125,
    #         'currency': 'USD',
    #         'revenue_src': 'Happy Playcrows',
    #         'customer': 'RunUp INC',
    #         'expected_payment_duration': 65
    #     })
    #     self.assertContains(response, '<ul class="errorlist">')
    # def test_index_page_has_inputs(self):
    #     invoice = self.invoice
    #     response = self.client.get('/')
    #     self.assertContains(response, invoice)


# TODO:
# class ResultPageTest(TestCase):
#     def setUp(self):
#         self.invoice = Input.objects.create(
#             date='2023-04-30',
#             invoice_number=3531,
#             value=519.5,
#             haircut=10,
#             daily_fee=0.125,
#             currency='USD',
#             revenue_src='Happy Playcrows',
#             customer='RunUp INC',
#             expected_payment_duration=65
#         )
#         self.secret = Input.objects.create(
#             date='2023-01-01',
#             invoice_number=9999,
#             value=519.5,
#             haircut=10,
#             daily_fee=0.125,
#             currency='USD',
#             revenue_src='SECRET',
#             customer='SECRET',
#             expected_payment_duration=65
#         )
#
#     def test_result_page_returns_200(self):
#         response = self.client.get(f'/{self.invoice.id}/')
#         self.assertTemplateUsed(response, 'input/result.html')
#         self.assertEqual(response.status_code, 200)
#
#     def test_result_page_contains_data(self):
#         response = self.client.get(f'/{self.invoice.id}/')
#         self.assertTemplateUsed(response, 'input/result.html')
#         #TODO: Need to define the type of output in my calculations
#         self.assertContains(response, str(self.invoice))
#         self.assertNotContains(response, str(self.invoice))
#

