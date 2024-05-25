from technical.API.models import Input, Result
import pandas as pd


def insert_into_db(df, id):
    inputs = [
        Input(  # TODO: avoid case sensitivity
            date=row['date'],
            invoice_number=row['invoice number'],
            value=row['value'],
            haircut=row['haircut percent'],
            daily_fee=row['Daily fee percent'],
            currency=row['currency'],
            revenue_src=row['Revenue source'],
            customer=row['customer'],
            expected_payment_duration=row['Expected payment duration'],
            epoch=id
        )
        for _, row in df.iterrows()
    ]
    Input.objects.bulk_create(inputs)
    calculate_totals(id)


def calculate_totals(id):
    result = {'id': id, 'totals': []}
    inputs = list(Input.objects.filter(epoch=id).values_list('revenue_src', flat=True).distinct())
    for src in inputs:
        data = Input.objects.all().filter(epoch=id, revenue_src=src).values()
        for entry in data:
            advance = entry['value'] * (1 - (entry['haircut'] / 100))
            expected_fee = entry['value'] * (entry['daily_fee'] / 100) * entry['expected_payment_duration']
            result['totals'].append(Result(revenue_src=src,
                                           value=entry['value'],
                                           advance=advance,
                                           expected_fee=expected_fee,
                                           epoch=id))
    Result.objects.bulk_create(result['totals'])

