#2020-07-04
#Add Github

from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
# pk_f528d62c397b424d93a1b4c766bd0b52

def home(request):
    import requests
    import json

    if request.method == 'POST':
        ticker = request.POST["ticker"]
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_f528d62c397b424d93a1b4c766bd0b52")

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error"
        return render(request, 'quotes/home.html', {"api":api})

    else:
        return render(request, 'quotes/home.html', {"ticker":"Enter a ticker symbol"})

def about(request):
    return render(request, 'quotes/about.html', {})

def add_stock(request):
    import requests
    import json


    if request.method == 'POST':
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Has Been Added"))
            return redirect('add_stock')
    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_f528d62c397b424d93a1b4c766bd0b52")

            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error"

        return render(request, 'quotes/add_stock.html', {'ticker':ticker, 'output':output})

def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, (item.ticker + ' has been deleted'))
    return redirect('delete_stock')

def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'quotes/delete_stock.html', {'ticker':ticker})
