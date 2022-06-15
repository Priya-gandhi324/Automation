from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import requests
from datetime import datetime
from .serializers import TotalSerializer
from .models import Courts, Total
from django.core.mail import send_mail
from project.settings import EMAIL_HOST_USER
import pandas as pd
# Create your views here.


def automate(request):
    courts = {
        'Confonet': 0,
        'Supremecourt': 10,
        'Ecourt-Highcourt': 2,
        'Delhi-Highcourt': 4,
        'Bombay-Highcourt': 5,
        'CAT': 13,
        'CESTAT': 18,
        'Ecourt District': 1,
        'NCLT': 17,
        'NCLAT': 23,
        'DRT': 11
    }

    till_date = datetime.now().date()

    for court_name, scrape_type in courts.items():
        _, created = Courts.objects.get_or_create(
            court_name=court_name, scrape_type=scrape_type)

    data_count = {
        "order": 0,
        "judgement": 0
    }

    for scrape_type in courts.values():
        data_count["scrape_type"] = scrape_type
        for order_type, count in data_count.items():
            if order_type != "scrape_type":
                url = f'https://scraper-dev.legistrak.com/api/v1/orders?order_type={order_type}&scrape_type={scrape_type}'

                headers = {
                    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2LCJ1c2VybmFtZSI6Im1hbm1pbmRlcnRvbWFyQGdtYWlsLmNvbSIsImVtYWlsIjoibWFubWluZGVydG9tYXJAZ21haWwuY29tIn0.I2XBFBhHE0UAVWf-AoB-Q2ONjlm78za7wC_fc-P0Of8'
                }

                response = requests.get(url, headers=headers)

                data_count[order_type] = response.json()["totalDocs"]

        if Total.objects.filter(till_date=till_date, scrape_type=data_count["scrape_type"]):
            pass
        else:
            totals = Total(
                till_date=till_date, scrape_type=data_count["scrape_type"], orders=data_count["order"], judgements=data_count["judgement"])
            totals.save()

    totals = Total.objects.all()
    serializer = TotalSerializer(totals, many=True)
    return JsonResponse(serializer.data, safe=False)


def getTotalDocs(request):
    params = request.GET
    till_date = params.get('date', str(datetime.now().date()))
    till_date = datetime.strptime(till_date, "%Y-%m-%d")
    totals = Total.objects.filter(till_date=till_date)
    return render(request, 'home.html', {'totals': totals})


def sendingMail(request):
    subject = 'Data till date'
    till_date = datetime.now().date()
    totals = Total.objects.filter(till_date=till_date)
    message = pd.DataFrame.from_records(totals.values(
        'till_date', 'scrape_type', 'orders', 'judgements')).to_string()
    email_from = EMAIL_HOST_USER
    recipient = ['pihugandhirest@gmail.com']
    send_mail(subject, message, email_from, recipient)
    return render(request, 'home.html', {'totals': totals})


def differences(request):
    params = request.GET
    date1 = params.get('date1', str(datetime.now().date()))
    date1 = datetime.strptime(date1, "%Y-%m-%d")
    date2 = params.get('date2', str(datetime.now().date()))
    date2 = datetime.strptime(date2, "%Y-%m-%d")
    totals1 = Total.objects.filter(till_date=date1)
    totals2 = Total.objects.filter(till_date=date2)

    orders = []
    judgements = []

    for total1, total2 in zip(totals1, totals2):
        orders.append(total2.orders - total1.orders)
        judgements.append(total2.judgements - total1.judgements)

    df1 = pd.DataFrame.from_records(totals1.values(
        'till_date', 'scrape_type', 'orders', 'judgements'))
    df2 = pd.DataFrame.from_records(totals2.values(
        'till_date', 'scrape_type', 'orders', 'judgements'))
    df3 = pd.DataFrame(list(zip(orders, judgements)), columns=[
                       'Orders Difference', 'Judgements Difference'])
    df = pd.concat([df1, df2, df3], axis=1)
    page_df = df.to_html()

    subject = 'Data Difference between today and yesterday'
    message = df.to_string()
    email_from = EMAIL_HOST_USER
    recipient = ['pihugandhirest@gmail.com']
    send_mail(subject, message, email_from, recipient)

    return HttpResponse(page_df)
