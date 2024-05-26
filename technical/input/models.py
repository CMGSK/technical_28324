from django.db import models
import json


class Result(models.Model):
    """
    Definition of the average data provided by a single revenue source within an excel insertion
    """
    revenue_src = models.TextField(blank=False, null=False)
    value = models.FloatField(blank=False, null=False)
    advance = models.FloatField(blank=False, null=False)
    expected_fee = models.FloatField(blank=False, null=False)
    epoch = models.IntegerField(blank=False, null=False) #grouping?

    def __str__(self):
        return json.dumps({
            'revenue_src':self.revenue_src,
            'value':self.value,
            'advance':self.advance,
            'expected_fee':self.expected_fee,
            'epoch': self.epoch
        })

    def getData(self):
        return {
            'revenue_src':self.revenue_src,
            'value':self.value,
            'advance':self.advance,
            'expected_fee':self.expected_fee,
            'epoch': self.epoch
        }

class Input(models.Model):
    """
    A single row of data within an excel file
    """
    date = models.DateField(blank=False, null=False)
    invoice_number = models.IntegerField(blank=False, null=False)
    value = models.FloatField(blank=False, null=False)
    haircut = models.FloatField(blank=False, null=False)
    daily_fee = models.FloatField(blank=False, null=False)
    currency = models.TextField(blank=False, null=False)
    revenue_src = models.TextField(blank=False, null=False)
    customer = models.TextField(blank=False, null=False)
    expected_payment_duration = models.IntegerField(blank=False, null=False)
    epoch = models.IntegerField(blank=False, null=False) #grouping?

    def __str__(self):
        return json.dumps({
            'date': self.date,
            'invoice_number': self.invoice_number,
            'value': self.value,
            'haircut': self.haircut,
            'daily_fee': self.daily_fee,
            'currency': self.currency,
            'revenue_src': self.revenue_src,
            'customer': self.customer,
            'expected_payment_duration': self.expected_payment_duration,
            'epoch': self.epoch
        })

    def getData(self):
        return {
            'date': self.date,
            'invoice_number': self.invoice_number,
            'value': self.value,
            'haircut': self.haircut,
            'daily_fee': self.daily_fee,
            'currency': self.currency,
            'revenue_src': self.revenue_src,
            'customer': self.customer,
            'expected_payment_duration': self.expected_payment_duration,
            'epoch': self.epoch
        }


class Excel(models.Model):
    """
    Structure of the upload file form
    """
    file = models.FileField(blank=False, null=False)


class ResultFromTargetId(models.Model):
    """
    Structure of the result from id form.
    """
    epoch = models.IntegerField(blank=False, null=False, name="Id")


# class InputResource(resources.ModelResource):
#     class Meta:
#         model = Input




