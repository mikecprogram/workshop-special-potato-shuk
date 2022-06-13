import sys
from http.client import HTTPException
from operator import mod
from unicodedata import category
from urllib import response
from django import forms
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
sys.path.append( '..' )
from Dev.ServiceLayer.SystemService import SystemService
from .models import ItemInBasket, Shop, StockItem

from email import message
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

from .notificationPlugin import notificationPl

notifyPlugin = notificationPl()
m = SystemService()
res = m.initialization_of_the_system()
if res.isexc:
    print("BUG:")
    print(response.exception)

def getToken(request):
    if 'tokenuser' in request.COOKIES:
        token = int(request.COOKIES['tokenuser'])
        res = m.is_token_valid(token)
        if res.res:
            print('tok')
            return token
    res = m.get_into_the_Trading_system_as_a_guest()
    print("got token:")
    print(res)
    if res.isexc:
        print("Bug")
        print(res.exc)
    return res.res

class ChatConsumer(AsyncWebsocketConsumer):
    async def disconnect(self, code):
        await notifyPlugin.removeConnection(self)

    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'hello'
        }))

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("Consumer connected via cookie %s" % message)
        await notifyPlugin.addConnection(self, message)


# Create your views here.

def templateforview(request):
    tokenuser = getToken(request)
    """SERVICE LOGIC HERE"""

    return makerender(request, tokenuser, 'HTMLPAGEHERE.html', {"""Params here"""})


def cart(request):
    tokenuser = getToken(request)
    if request.method == 'POST':
        print('OMG POST')
    item1 = ItemInBasket(5, "Dairy", "Milk", "Cow's Milk", 20, 5, 6.5, 2)
    item2 = ItemInBasket(5, "Beverages", "Cola",
                         "Icy Coca Cola", 10, 7.5, 10, 1)
    itemslist = []
    return makerender(request, tokenuser, 'cart.html', {'itemslist': itemslist})


def art(request):
    tokenuser = getToken(request)
    if 'tokenuser' in request.COOKIES:
        tokenuser = int(request.COOKIES['tokenuser']) - 1
    else:
        tokenuser = 5

    st1 = StockItem(1, "Dairy", "Milk", "Fresh Cow's milk",
                    5, None, None, 5.90)
    st2 = StockItem(1, "Alcohol", "Beer", "Root beer", 8, None, None, 7.90)

    sts = [st1, st2]
    sts = sts + sts
    sts = sts + sts
    sts = sts + sts

    if 'q' in request.GET:
        print("ok!")
        searchterm = request.GET['q']
        newsts = []
        for i in sts:
            print("%s %s" % (i.name, 'searchterm'))
            if (searchterm in i.name) | (searchterm in i.category) | (searchterm in i.desc):
                newsts.append(i)
                print("ok")
        sts = newsts
    (request, 'art.html', {'itemslist': sts, 'tokenuser': tokenuser})
    response.set_cookie('tokenuser', tokenuser)
    return response


def homepage(request):
    tokenuser = getToken(request)
    # bla bla
    return makerender(request, tokenuser, 'homepage.html')


# Note that it is not inheriting from forms.ModelForm
class LoginRegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username','autofocus':''}))

    password = forms.CharField(min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class CreateShopForm(forms.Form):  # Note that it is not inheriting from forms.ModelForm
    shopname = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shop name','autofocus':''}))


def createShop(request):
    tokenuser = getToken(request)
    errormessage = ''
    form = CreateShopForm()
    if request.method == 'POST':
        form = CreateShopForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            shopname = cd.get('shopname')
            res = m.shop_open(tokenuser,shopname)
            if(res.isexc):
                errormessage = "Error: %s"% res.exc
            else:
                return redirect('manage')
    return makerender(request, tokenuser, 'createshop.html',
                      {"form": form,  "errormessage": errormessage, })


def login(request):
    tokenuser = getToken(request)
    errormessage = ''
    form = LoginRegisterForm()
    if request.method == 'POST':
        form = LoginRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd.get('username')
            password = cd.get('password')
            print("LOGIN %s %s" % (cd.get('username'), cd.get('password')))
            res = m.login_into_the_trading_system(tokenuser,username,password)
            if res.isexc:
                errormessage = res.exc
            else:
                return makerender(request, tokenuser, 'homepage.html',
                      {'tokenuser': tokenuser})
    return makerender(request, tokenuser, 'loginregister.html',
                      {"form": form, 'state': "Login", "screen": "login", "errormessage": errormessage,
                       'tokenuser': tokenuser})


def register(request):
    tokenuser = getToken(request)
    errormessage = ''
    form = LoginRegisterForm()
    if request.method == 'POST':
        form = LoginRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # now in the object cd, you have the form as a dictionary.
            username = cd.get('username')
            password = cd.get('password')
            print("Register %s %s" % (cd.get('username'), cd.get('password')))
            res = m.registration_for_the_trading_system(tokenuser,username,password)
            if res.isexc:
                errormessage = res.exc
            else:
                return makerender(request, tokenuser, 'homepage.html',
                      {'tokenuser': tokenuser},'You have registered successfully')
    return makerender(request, tokenuser, 'loginregister.html',
                  {"form": form, 'state': "Register", "screen": "register", "errormessage": errormessage,
                   'tokenuser': tokenuser})
@csrf_exempt
def shop(request, shopname):
    tokenuser = getToken(request)
    
    if request.method == 'POST':
        if 'addItemToCart' in request.POST:
            itemid = request.POST['addItemToCart']
            quantity = request.POST['quantity']
            print(itemid)
            print(quantity)
    st1 = StockItem(1, "Dairy", "Milk", "Fresh %s's milk" %
                    shopname, 5, None, None, 5.90)
    st2 = StockItem(5, "Alcohol", "Beer", "Root beer", 8, None, None, 7.90)

    sts = [st1, st2]
    sts = sts + sts
    sts = sts + sts
    sts = sts + sts
    return makerender(request, tokenuser, 'shop.html', {'shopname': shopname, 'itemslist': sts, 'tokenuser': tokenuser})


def shops(request):
    tokenuser = getToken(request)
    shops = []  # todo: get shops from servise
    shops.append(Shop(5,"Wow","Open","Me",['one'],['Two'],'None.'))
    shops.append(Shop(5,"Wow","Open","Me",['one'],['Two'],'None.'))
    shops.append(Shop(5,"Wow","Open","Me",['one'],['Two'],'None.'))
    return makerender(request, tokenuser, 'shops.html', {'itemslist': shops})


def item(request, itemname):
    tokenuser = getToken(request)
    if itemname == '':
        return HTTPException(404)
    tokenuser = getToken(request)
    item = StockItem(1, "Dairy", "Milk", "Fresh %s's milk" %
                     itemname, 5, None, None, 5.90)

    return makerender(request, tokenuser, 'item.html', {'item': item, })

def exit(request):
    tokenuser = getToken(request)
    m.Trading_system_quitting(tokenuser)
    response = render(request, 'exit.html',{"userStatus":"",'jsmessage' :""})
    response.delete_cookie('tokenuser')
    return response

def searchItems(request):
    tokenuser = getToken(request)
    
    return makerender(request,tokenuser, 'searchItems.html')

def manage(request):
    tokenuser = getToken(request)
    counter = 0
    found = []
    own = []
    manage = []
    res = m.get_founded_shops(tokenuser)
    if res.isexc :
        return renderError(request,tokenuser, res.exc)
    for shopname in res.res:
        res = m.info_about_shop_in_the_market_and_his_items_name(tokenuser,shopname)
        if res.isexc :
            return renderError(request,tokenuser, res.exc)
        s = res.res
        res = m.get_eligible_members_for_shop(tokenuser,shopname)
        if res.isexc :
            return renderError(request,tokenuser, res.exc)
        eligible = res.res
        found.append(
            {'name' : s['name'] ,'founder' : s['founder'],
            'managers': ', '.join([m for m in s['managers']]),
            'owners': ', '.join([m for m in s['owners']]),
            'shopopen': s['shopopen'],
            'eligible':eligible}
        )
        counter = counter + 1
    userlist = ["What?","When?"]
    m.get_founded_shops(tokenuser)
    return makerender(request,tokenuser, 'manage.html',
    {'found':found,
    'own':own,
    'manage':manage,"userlist":userlist})

def makemanager(request):
    tokenuser = getToken(request)
    return makerender(request,tokenuser, 'makemanager.html')

def storeHistoryPurchases(request):
    tokenuser = getToken(request)
    return makerender(request,tokenuser, 'storeHistoryPurchases.html')

def premissions(request):
    tokenuser = getToken(request)
    return makerender(request,tokenuser, 'premissions.html')


def renderError(request, tokenuser,err):
    return makerender(request,tokenuser, 'homepage.html',error=err)
@csrf_exempt
def makerender(request, tokenuser, page, optparams=None,error =None):
    if optparams is None:
        optparams = {}
    optparams['token'] = tokenuser
    if error is None:
        optparams['jsmessage'] = ""
    else:
        optparams['jsmessage'] = error
    optparams['userStatus'] = m.get_user_state(tokenuser).res#should return Guest or Username
    response = render(request, page, optparams)

    response.set_cookie('tokenuser', tokenuser)
    return response
