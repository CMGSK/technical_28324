import pandas as pd

from ..models import Input, Result
from celery import shared_task
from typing import Union


def insert_into_db(df, id) -> Union[bool, dict]:
    """
    Insert excel file into database.
    :param df: pandas excel file instance
    :param id: epoch identifier
    :return:
    """
    if not isinstance(df, pd.DataFrame):
        return {'error': f"DataFrame object was expected, type {type(df)} received"}

    inputs = [
        Input(  # TODO: avoid case sensitivity?
            date=row['date'],
            invoice_number=row['invoice number'],
            value=row['value'],
            haircut=row['haircut percent'],
            daily_fee=row['Daily fee percent'],
            currency=row['currency'],
            revenue_src=row['Revenue source'].strip(),  # This was a sneaky one
            customer=row['customer'],
            expected_payment_duration=row['Expected payment duration'],
            epoch=id
        )
        for _, row in df.iterrows()
    ]

    try:
        Input.objects.bulk_create(inputs)
    except Exception as err: #TODO: Define non generic exception
        return {'error': str(err)}

    calculate_totals(id)
    return True


@shared_task()
def calculate_totals(id):
    """
    Calculates the totals given an excel file insertion identified by unix time
    :param id: epoch
    :return: void
    """
    totals = []
    # Retrieve sources as flat list
    inputs = list(Input.objects.filter(epoch=id).values_list('revenue_src', flat=True).distinct())

    #I'd use a try block and log within the app that the calculation failed and why, since it would probably be caused
    #by wrong data provided by the user.
    for src in inputs:
        data = Input.objects.filter(epoch=id, revenue_src=src).values()
        arr_advances = []
        arr_fees = []
        value = 0
        for entry in data:
            arr_advances.append(entry['value'] * (1 - (entry['haircut'] / 100)))
            arr_fees.append(entry['value'] * (entry['daily_fee'] / 100) * entry['expected_payment_duration'])
            value += entry['value']
        totals.append(Result(revenue_src=src,
                             value=value,
                             advance=sum(arr_advances),
                             expected_fee=sum(arr_fees),
                             epoch=id))
    Result.objects.bulk_create(totals)
