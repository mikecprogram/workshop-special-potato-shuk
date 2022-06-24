from pydoc import describe
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
from .models import ItemInBasket, Shop, StockItem, Policy, TemplatePolicy

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
            return token
    res = m.get_into_the_Trading_system_as_a_guest()
    if res.isexc:
        print(res.exc)
    return res.res


class ChatConsumer(AsyncWebsocketConsumer):
    async def disconnect(self, code):
        print("TRYING DISCONNECT")
        await notifyPlugin.removeConnection(self)
        print("Success DISCONNECT")

    async def connect(self):
        print("TRYING connect")
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'hello'
        }))
        print("Success connect")

    async def receive(self, text_data=None, bytes_data=None):
        print("TRYING receive")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("Consumer connected via cookie %s" % message)
        await notifyPlugin.addConnection(self, message)
        print("Success receive")


# Create your views here.

def templateforview(request):
    tokenuser = getToken(request)
    """SERVICE LOGIC HERE"""

    return makerender(request, tokenuser, 'HTMLPAGEHERE.html', {"""Params here"""})


def cart(request):
    tokenuser = getToken(request)
    jsmessage = ""
    if request.method == 'POST':
        if 'purchase' in request.POST:
            jsmessage = 'Purchase successfully!'
            res = m.Shopping_cart_purchase(tokenuser)
            if res.isexc:
                jsmessage = res.exc
                print(res.exc)
        elif 'quantity' in request.POST:
            quantity = request.POST['quantity']
            (itemname,shopname) = request.POST['changeamount'].split('|')
            r = m.shopping_carts_check_content(tokenuser)
            if r.isexc:
                return renderError(request, tokenuser, r.exc)
            items = r.res[shopname]
            amount = -1
            for i in items:
                if i['name'] == itemname:
                    amount = i['count']
            diff = amount - quantity
            if diff < 0:
                r = m.shopping_carts_delete_item(tokenuser,itemname,shopname,diff)
            elif diff > 0:
                
            if r.isexc:
                return renderError(request, tokenuser, r.exc)
    res = m.shopping_carts_check_content(tokenuser)
    print("---------------")
    print(res.res)
    len_results = 0
    answer = None
    if res.isexc:
        renderError(request, tokenuser, res.exc)
    else:
        answer = res.res
        print(answer)
        for _, items in answer:
            len_results += len(items)

    return makerender(request, tokenuser, 'cart.html', {'answer': answer, 'amountOfItems': len_results},
                      error=jsmessage)


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
        searchterm = searchterm.lower()
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
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'autofocus': ''}))

    password = forms.CharField(min_length=8,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class CreateShopForm(forms.Form):  # Note that it is not inheriting from forms.ModelForm
    shopname = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shop name', 'autofocus': ''}))


def createShop(request):
    tokenuser = getToken(request)
    errormessage = ''
    form = CreateShopForm()
    if request.method == 'POST':
        form = CreateShopForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            shopname = cd.get('shopname')
            res = m.shop_open(tokenuser, shopname)
            if (res.isexc):
                errormessage = "Error: %s" % res.exc
            else:
                return redirect('manage')
    return makerender(request, tokenuser, 'createshop.html',
                      {"form": form, "errormessage": errormessage, })


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
            res = m.login_into_the_trading_system(tokenuser, username, password)
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
            res = m.registration_for_the_trading_system(tokenuser, username, password)
            if res.isexc:
                errormessage = res.exc
            else:
                return login(request)
    return makerender(request, tokenuser, 'loginregister.html',
                      {"form": form, 'state': "Register", "screen": "register", "errormessage": errormessage,
                       'tokenuser': tokenuser})


class AddItemForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name', 'autofocus': ''}))
    category = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category'}))
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}))
    amount = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Count', 'min': 0}))
    price = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price', 'min': 0}))


def additem(request, shopname):
    tokenuser = getToken(request)
    errormessage = ''
    form = AddItemForm()
    if request.method == 'POST':
        form = AddItemForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd.get('name')
            category = cd.get('category')
            description = cd.get('description')
            amount = cd.get('amount')
            price = cd.get('price')
            res = m.adding_item_to_the_shops_stock(tokenuser, name, shopname, category, description, price, amount)
            if res.isexc:
                return makerender(request, tokenuser, 'additem.html', {'shopname': shopname, 'form': form},
                                  error=res.exc)
            return redirect('/shop/%s/' % shopname)
    return makerender(request, tokenuser, 'additem.html', {'shopname': shopname, 'form': form})


def edititem(request, shopname):
    tokenuser = getToken(request)
    errormessage = ''
    # This request had a user press save
    if request.method == 'POST':
        olditemname = request.GET['edit']
        form = AddItemForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd.get('name')
            category = cd.get('category')
            description = cd.get('description')
            amount = cd.get('amount')
            price = cd.get('price')
            print("Price : %f" % price)
            res = m.change_items_details_in_shops_stock(tokenuser, olditemname, shopname, name, description, category,
                                                        price, amount)
            if res.isexc:
                return makerender(request, tokenuser, 'edititem.html', {'shopname': shopname, 'form': form},
                                  error=res.exc)
            return redirect('/shop/%s/' % shopname)
            # This request is only for showing the initial edit page

    if request.method == 'GET':
        itemname = request.GET['edit']
        res = m.info_about_item_in_shop(tokenuser, itemname, shopname)
        if res.isexc:
            return redirect('/shop/%s/' % shopname)
        form = AddItemForm(initial=res.res)
        return makerender(request, tokenuser, 'edititem.html', {'shopname': shopname, 'form': form})
    return redirect('/shop/%s/' % shopname)


@csrf_exempt
def shop(request, shopname):
    tokenuser = getToken(request)
    errormessage = ""
    if request.method == 'POST':  # Add to cart or deleteItem
        if 'deleteItem' in request.POST:
            itemname = request.POST['deleteItem']
            print("delelting %s" % itemname)
            res = m.deleting_item_from_shop_stock(tokenuser, itemname, shopname)
            if res.isexc:
                errormessage = res.exc

        if 'addItemToCart' in request.POST:
            itemname = request.POST['addItemToCart']
            quantity = int(request.POST['quantity'])
            print(itemname)
            print(quantity)
            res = m.shopping_carts_add_item(tokenuser, itemname, shopname, quantity)
            if res.isexc:
                errormessage = res.exc

    shopinfo = m.info_about_shop_in_the_market_and_his_items_name(tokenuser, shopname)
    if shopinfo.isexc:
        return renderError(request, tokenuser, shopinfo.exc)
    shopinfo = shopinfo.res
    # TODO, fetch also the discounts

    showAddItem = True

    return makerender(request, tokenuser, 'shop.html', \
                      {'shopname': shopinfo['name'], \
                       'items': shopinfo['items'], \
                       'founder': shopinfo['founder'], \
                       'owners': mike_join(shopinfo['owners']), \
                       'managers': mike_join(shopinfo['managers']), \
                       'showAddItem': showAddItem}, \
                      error=errormessage)


def shops(request):
    tokenuser = getToken(request)
    # res = m.get()
    # if res.isexc:
    #    return renderError(request,tokenuser,res.exc)

    shops = []  # todo: get shops from servise
    shops.append(Shop(5, "Wow", "Open", "Me", ['one'], ['Two'], 'None.'))
    shops.append(Shop(5, "Mi", "Open", "Me", ['one'], ['Two'], 'None.'))
    shops.append(Shop(5, "Ma", "Open", "Me", ['one'], ['Two'], 'None.'))
    return makerender(request, tokenuser, 'shops.html', {'itemslist': shops})

"""
class addPolicyForm(forms.Form):
    arg1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    arg2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
"""

def policies(request):
    tokenuser = getToken(request)
    simpleBank = [TemplatePolicy("hasAmount", ["item name","amount"]),
                  TemplatePolicy("hasPrice", ["item name", "price"]),
                  TemplatePolicy("isShop", []),
                  TemplatePolicy("isItem", ["item name"]),
                  TemplatePolicy("isAfterTime", ["hour", "minute"]),
                  TemplatePolicy("isAge", ["age"]),
                  TemplatePolicy("isCategory", ["category"]),
                  TemplatePolicy("isFounder", []),
                  TemplatePolicy("isMember", [])
                  ]
    compositeBank = [TemplatePolicy("not", ["policy"]),
                     TemplatePolicy("and", ["policy1", "policy2"]),
                     TemplatePolicy("or", ["policy1", "policy2"]),
                     TemplatePolicy("xor", ["policy1", "policy2"]),
                     TemplatePolicy("add", ["policy1", "policy2"]),
                     ]
    if request.method == 'POST':  # Add to cart or deleteItem
        if 'addpolicy' in request.POST:
            typeofpolicy = request.POST['addpolicy']
            first = None
            second = None
            discount = request.POST['discount']#from 0 to 100
            if 'bob0' in request.POST:
                first = request.POST['bob0']
            if 'bob1' in request.POST:
                second = request.POST['bob1']
            if first is not None:
                first = first.strip()
            if second is not None:
                second = second.strip()
        elif 'applydiscount' in request.POST:
            polid = request.POST['applydiscount']#from 0 to 100
        elif 'applypurchasepolicy' in request.POST:
            polid = request.POST['applypurchasepolicy']#from 0 to 100
    request.POST = {}



    myPolicies = [Policy(p[0], p[1], [p[2], p[3]], p[4]) for p in m.get_my_policies(tokenuser).res]
    myPolicies.append(Policy(1, "hasAmount", ["milk", 5], 10))
    myPolicies.append(Policy(2, "hasPrice", ["beer", 10], 5))
    return makerender(request, tokenuser, 'policies.html',
                      {'myPolicyList': myPolicies, 'simplePolicies': simpleBank, 'compositePolicies': compositeBank})


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
    response = render(request, 'exit.html', {"userStatus": "", 'jsmessage': ""})
    response.delete_cookie('tokenuser')
    return response


class SearchForm(forms.Form):  # Note that it is not inheriting from forms.ModelForm
    q = forms.CharField(required=False, disabled=True, label=False,
                        widget=forms.TextInput(
                            attrs={'hidden': True, 'readonly': '', 'class': 'form-control', 'placeholder': 'Price',
                                   'min': 0}))
    category = forms.CharField(required=False,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Price', 'min': 0}))
    min_Price = forms.FloatField(required=False,
                                 widget=forms.NumberInput(
                                     attrs={'class': 'form-control', 'placeholder': 'Price', 'min': 0}))

    max_Price = forms.FloatField(required=False,
                                 widget=forms.NumberInput(
                                     attrs={'class': 'form-control', 'placeholder': 'Price', 'min': 0}))


def search(request):
    tokenuser = getToken(request)
    answer = None
    len_results = 0
    query = ""
    category = request.GET['category'] if 'category' in request.GET else ""
    min_Price = request.GET['min_Price'] if 'min_Price' in request.GET else 0
    max_Price = request.GET['max_Price'] if 'max_Price' in request.GET else 0
    if request.method == 'GET':
        query = request.GET['q']
        query = query.lower()
        res = m.general_items_searching(tokenuser, query, category, min_Price, max_Price)
        if res.isexc:
            print(res.exc)
            renderError(request, tokenuser, res.exc)
        else:
            answer = res.res
            for _, items in answer:
                len_results += len(items)
    return makerender(request, tokenuser, 'searchItems.html',
                      {'len_results': len_results, 'answer': answer, 'searchterm': query, 'category': category,
                       'min_Price': min_Price, 'max_Price': max_Price})

def mike_join(lst):
    if len(lst) == 0:
        return "No one."
    else:
        return ', '.join([m for m in lst])
def manage(request):
    tokenuser = getToken(request)
    counter = 0
    found = []
    own = []
    manage = []
    res = m.get_founded_shops(tokenuser)
    if res.isexc:
        return renderError(request, tokenuser, res.exc)
    for shopname in res.res:
        res = m.info_about_shop_in_the_market_and_his_items_name(tokenuser, shopname)
        if res.isexc:
            return renderError(request, tokenuser, res.exc)
        s = res.res
        res = m.get_eligible_members_for_shop(tokenuser, shopname)
        if res.isexc:
            return renderError(request, tokenuser, res.exc)
        eligible = res.res
        found.append(
            {'name': s['name'], 'founder': s['founder'],
             'managers': mike_join(s['managers']),
             'owners': mike_join(s['owners']),
             'shopopen': s['shopopen'],
             'eligible': eligible}
        )
        counter = counter + 1
    userlist = ["What?", "When?"]
    m.get_founded_shops(tokenuser)
    return makerender(request, tokenuser, 'manage.html',
                      {'found': found,
                       'own': own,
                       'manage': manage, "userlist": userlist})


def makemanager(request):
    tokenuser = getToken(request)
    return makerender(request, tokenuser, 'makemanager.html')


def storeHistoryPurchases(request,shopname):
    tokenuser = getToken(request)
    shopinfo = m.in_shop_purchases_history_request(tokenuser, shopname)
    if shopinfo.isexc:
        return renderError(request, tokenuser, shopinfo.exc)
    history = shopinfo.res
    if history == "" or history is None:
        history = "There is no history"
    return makerender(request, tokenuser, 'storehistory.html',{"shopname":shopname,"history":history})


def premissions(request):
    tokenuser = getToken(request)
    return makerender(request, tokenuser, 'premissions.html')


def renderError(request, tokenuser, err, page="homepage.html"):
    return makerender(request, tokenuser, page, error=err)


@csrf_exempt
def makerender(request, tokenuser, page, optparams=None, error=None):
    if optparams is None:
        optparams = {}
    optparams['token'] = tokenuser
    r = m.shopping_carts_check_content(tokenuser)
    cartamount = sum([len(result) for result in r.res.values()])
    optparams['cartamount'] = cartamount
    if error is None:
        optparams['jsmessage'] = ""
    else:
        optparams['jsmessage'] = error
    optparams['userStatus'] = m.get_user_state(tokenuser).res  # should return Guest or Username
    response = render(request, page, optparams)

    response.set_cookie('tokenuser', tokenuser)
    return response
