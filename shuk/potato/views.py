from http.client import HTTPException
from operator import mod
from unicodedata import category
from urllib import response
from django import forms
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from SystemService import SystemService
from potato.service import Service
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
    # TODO: check if the token is valid, else, do enter()
    if 'tokenuser' in request.COOKIES:
        return int(request.COOKIES['tokenuser'])
    else:
        res = m.enter()
        if res.isexc :
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
        text_data_json = await json.loads(text_data)
        message = await text_data_json['message']
        await print("Consumer connected via cookie %s" % message)
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
    itemslist = [item1, item2]
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
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class AddShopForm(forms.Form):  # Note that it is not inheriting from forms.ModelForm
    shopname = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shop name'}))
    shopAddress = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    shopManager = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Manager Name'}))


def createShop(request):
    tokenuser = getToken(request)
    errormessage = ''
    form = AddShopForm()
    if request.method == 'POST':
        form = AddShopForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            shopname = cd.get('shopname')
            shopAddress = cd.get('shopAddress')
            shopManager = cd.get('shopManager')
            print("Create new Shop %s %s %s" % (cd.get('shopname'),
                  cd.get('shopAddress'), cd.get('shopManager')))
            errormessage = "Error while Creating new shop"
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
            errormessage = "Error while login"
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
            service.login(tokenuser, username,password)
            errormessage = "WOW"
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
    shops.append(Shop("Shop for Fun", "Open 24/7",
                 "Michael with Tomer", "Michael"))
    shops.append(Shop("Brown", "Open 24/7", "Michael with Tomer", "Michael"))
    shops.append(Shop("Blue", "Open 24/7", "Michael with Tomer", "Michael"))
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
    service.exit(tokenuser)
    response = render(request, 'exit.html',{"userStatus":""})
    response.delete_cookie('tokenuser')
    return response

def exit(request):
    tokenuser = getToken(request)
    service.exit(tokenuser)
    response = render(request, 'exit.html',{"userStatus":""})
    response.delete_cookie('tokenuser')
    return response

def searchItems(request):
    tokenuser = getToken(request)
    
    return makerender(request,tokenuser, 'searchItems.html')

def manage(request):
    tokenuser = getToken(request)
    shop1 = Shop(1,"Cool Shop","Open","Finder",["Who?","He?"],["No one"],"None.")
    shop2 = Shop(2,"Awesome Shop","Open","Finder",["Who?","He?"],["No one"],"None.")
    shops = [shop1,shop2]
    userlist = ["What?","When?"]
    return makerender(request,tokenuser, 'manage.html',{'itemslist':shops,"userlist":userlist})

def makemanager(request):
    tokenuser = getToken(request)
    
    return makerender(request,tokenuser, 'makemanager.html')

@csrf_exempt
def makerender(request, tokenuser, page, optparams=None):
    if optparams is None:
        optparams = {}
    optparams['token'] = tokenuser
    optparams['userStatus'] = service.getUserStatus()#should return Guest or Username
    response = render(request, page, optparams)
    response.set_cookie('tokenuser', tokenuser)
    return response
