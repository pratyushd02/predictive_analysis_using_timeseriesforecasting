from contextlib import nullcontext
from django.http import HttpResponse
from django.shortcuts import render,redirect
import ssl
import joblib
import datetime

ssl._create_default_https_context = ssl._create_unverified_context

def home(request):
    c = 1
    fans=''
    cls = joblib.load('pmodel.sav')
    year = request.GET.get('year','default')
    month = request.GET.get('month','default')
    date = str(year)+'-'+month+'-'+'01'
    
    if year=='default':
        c=3
    elif len(year)!=4 or int(year)<2019 or month=='':
        c=2
    elif int(year)==2019:
        if(int(month)>=4):
            element = datetime.datetime.strptime(date,"%Y-%m-%d")

            ans = cls.get_prediction(start=element ,end=element)
            predictions=ans.predicted_mean
            predictions.columns=['sales_predicted','gdp_predicted','sensexp','niftyp','exportp']
            fans = round(predictions['sales_predicted'][0],2)
        else:
            c=2
    else:
        element = datetime.datetime.strptime(date,"%Y-%m-%d")

        ans = cls.get_prediction(start=element ,end=element)
        predictions=ans.predicted_mean
        predictions.columns=['sales_predicted','gdp_predicted','sensexp','niftyp','exportp']
        fans = round(predictions['sales_predicted'][0],2)
    
        
        
    return render(request, 'fineprediction/home.html',{'ans':fans , 'cc':c, 'month':month, 'year':year})