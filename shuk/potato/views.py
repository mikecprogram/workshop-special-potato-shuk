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
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

from .notificationPlugin import notificationPl
class newNoty():
    def alertspecificrange(self, message, ran):
        for i in ran:
            print("person: %s" % i)
            print(message)
        return ran
    def alert(self, message):
        print(message)

m = SystemService()
new_noty = notificationPl(m)
res = m.initialization_of_the_system(notificationPlugin = new_noty)
if res.isexc:
    print("BUG:")
    print(res.exc)


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
        await new_noty.removeConnection(self)
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
        await new_noty.addConnection(self, message)
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
            holder = str(request.POST['holder-number'])
            holderid = str(request.POST['holder-id'])
            cardid = str(request.POST['card-number'])
            cvv = str(request.POST['cvv'])
            month = str(request.POST['Month'])
            year = str(request.POST['Year'])
            name = str(request.POST['name'])
            address = str(request.POST['address'])
            city = str(request.POST['city'])
            country= str(request.POST['country'])
            zip = str(request.POST['zip'])
            print("TRY TO PURCHASE")
            jsmessage = 'Purchase successfully!'
            res = m.Shopping_cart_purchase(tokenuser,cardid,month,year,holder,cvv,holderid,name, address, city, country, zip)
            if res.isexc:
                print(res.exc)
                jsmessage = res.exc
        elif 'quantity' in request.POST:
            wanted = int(request.POST['quantity'])
            (itemname,shopname) = request.POST['changeamount'].split('|')
            r = m.shopping_carts_check_content(tokenuser)
            if r.isexc:
                return renderError(request, tokenuser, r.exc)
            items = r.res[shopname]
            actual = 0
            for i in items:
                if i['name'] == itemname:
                    actual = int(i['count'])
            diff = wanted - actual
            if diff < 0:
                r = m.shopping_carts_delete_item(tokenuser,itemname,shopname,-diff)
            elif diff > 0:
                r = m.shopping_carts_add_item(tokenuser,itemname,shopname,diff)
            if r.isexc:
                return renderError(request, tokenuser, r.exc)
    res = m.shopping_carts_check_content(tokenuser)
    len_results = 0
    answer = None
    if res.isexc:
        return renderError(request, tokenuser, res.exc)
    else:
        answer = res.res
        for shopname, items in answer.items():
            len_results += len(items)
            for listing in items:
                r = m.calculate_item_price(tokenuser,shopname, listing['name'])
                if r.isexc:
                    return renderError(request, tokenuser, r.exc)
                listing['after'] = r.res
    res = m.calculate_cart_price(tokenuser)
    if res.isexc:
        return renderError(request, tokenuser, res.exc)
    cartprice = res.res
    return makerender(request, tokenuser, 'cart.html', {'cartprice': cartprice,'answer': answer, 'amountOfItems': len_results},
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
        searchterm = request.GET['q']
        searchterm = searchterm.lower()
        newsts = []
        for i in sts:
            if (searchterm in i.name) | (searchterm in i.category) | (searchterm in i.desc):
                newsts.append(i)
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
            notifications = res.res
            if res.isexc:
                errormessage = res.exc
            else:
                return makerender(request, tokenuser, 'homepage.html',
                                  {'tokenuser': tokenuser,'notifications':notifications})
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
            res = m.deleting_item_from_shop_stock(tokenuser, itemname, shopname)
            if res.isexc:
                errormessage = res.exc

        if 'addItemToCart' in request.POST:
            itemname = request.POST['addItemToCart']
            quantity = int(request.POST['quantity'])
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

def shopPolicies(request, shopname):
    tokenuser = getToken(request)
    errormessage = ""
    """if request.method == "GET":
        m.registration_for_the_trading_system(tokenuser,"aleks", "12345678")
        m.login_into_the_trading_system(tokenuser,"aleks", "12345678")
        m.shop_open(tokenuser,"shopname1")
        if len(m.get_shop_policies(tokenuser,"shopname1").res) == 0:
            m.add_policy(tokenuser,10,"isShop")
            m.add_policy(tokenuser, 10, "isShop")
            m.add_purchase_policy_to_shop(tokenuser, "shopname1",1)
            m.add_purchase_policy_to_shop(tokenuser, "shopname1", 2)"""
    if request.method == "POST":
        if "removePolicy" in request.POST:
            (id,dis) = request.POST['removePolicy'].split('|')
            type1 = "discount"
            if dis == 'None':
                type1 = "purchase"
            r = m.delete_policy(tokenuser,shopname, int(id),type1)
            if r.isexc:
                errormessage = r.exc

    policies = m.get_shop_policies(tokenuser,shopname)
    if policies.isexc:
        return renderError(request,tokenuser,policies.exc)
    policies = policies.res
    if policies is None:
        policies = []
    pols = []
    for p in policies:
        if len(p) == 3:
            pols.append(Policy(shopname, p[1],p[0],[],p[2]))
        if len(p) == 2:
            pols.append(Policy(shopname, p[1],p[0],[],None))


    return makerender(request, tokenuser, 'shopPolicies.html',
                      {'myPolicyList': pols,'shopname': shopname}
                      , error=errormessage)


def policies(request,shopname):
    errormessage = ""
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
                     TemplatePolicy("max", ["policy1", "policy2"]),
                     ]
    compositeNames = [t.name for t in compositeBank]
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
            if first == "":
                first = None
            if second == "":
                second = None

            if typeofpolicy in compositeNames:
                if second is None:
                    r = m.compose_policy(tokenuser,shopname, str(typeofpolicy), int(first), None)
                    if r.isexc:
                        errormessage = r.exc
                else:
                    r = m.compose_policy(tokenuser,shopname, str(typeofpolicy), int(first), int(second))
                    if r.isexc:
                        errormessage = r.exc
            else:
                r = m.add_policy(tokenuser,shopname,float(discount),str(typeofpolicy),first,second)
                if r.isexc:
                    errormessage = r.exc



        elif 'applydiscount' in request.POST:
            polid = request.POST['applydiscount']#from 0 to 100
            if 'shopname' in request.POST:
                if shopname is not None:
                    shopname = shopname.strip()
                r = m.add_discount_policy_to_shop(tokenuser,shopname,int(polid))
                if r.isexc:
                    errormessage = r.exc
        elif 'applypurchasepolicy' in request.POST:
            polid = request.POST['applypurchasepolicy']#from 0 to 100
            if 'shopname' in request.POST:
                r = m.add_purchase_policy_to_shop(tokenuser,shopname,int(polid))
                if r.isexc:
                    errormessage = r.exc
    request.POST = {}

    myPolicies = []
    getpol = m.get_my_policies(tokenuser, shopname).res
    if getpol is None:
        getpol=[]
    pol = None
    for p in getpol:
        if p[1] in compositeNames:
            if len(p) == 4:
                pol = Policy(shopname, p[0], p[1], [p[2], p[3]], None)
            if len(p) == 3:
                pol = Policy(shopname, p[0], p[1], [p[2]], None)
            if len(p) == 2:
                pol = Policy(shopname, p[0], p[1], [], None)
        else:
            if len(p) == 5:
                pol = Policy(shopname, p[0], p[1], [p[2], p[3]], p[4])
            if len(p) == 4:
                pol = Policy(shopname, p[0], p[1], [p[2]], p[3])
            if len(p) == 3:
                pol = Policy(shopname, p[0], p[1], [], p[2])
        if pol is not None:
            myPolicies.append(pol)

    r = m.get_founded_shops(tokenuser)
    if r.isexc:
        return renderError(request, tokenuser, r.exc)
    found = r.res

    r = m.get_owned_shops(tokenuser)
    if r.isexc:
        return renderError(request, tokenuser, r.exc)
    own = r.res

    r = m.get_managed_shops(tokenuser)
    if r.isexc:
        return renderError(request, tokenuser, r.exc)
    manage = r.res
    myshops = []
    myshops.extend(found)
    myshops.extend(own)
    myshops.extend(manage)
    return makerender(request, tokenuser, 'policies.html',
                      {'myshops':myshops,'myPolicyList': myPolicies, 'simplePolicies': simpleBank, 'compositePolicies': compositeBank, 'compositeNames': compositeNames}
                      ,error=errormessage)


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

def unpackcategories(cats):
    categories = set()
    for catinshop in cats.values():
        for cat in catinshop:
            categories.add(cat)
    return categories
def search(request):
    tokenuser = getToken(request)
    r = m.get_all_categories()
    if r.isexc:
        return renderError(request, tokenuser, r.exc)
    categories = unpackcategories(r.res)
    answer = None
    len_results = 0
    query = ""
    errormessage = ""
    category = str(request.GET['category'] if 'category' in request.GET else "")
    min_Price = float(request.GET['min_Price'] if 'min_Price' in request.GET else 0)
    max_Price = float(request.GET['max_Price'] if 'max_Price' in request.GET else 0)
    if 'q' in request.GET:
        query = request.GET['q']
        query = query.lower()
        res = m.general_items_searching(tokenuser, query, category, min_Price, max_Price)
        if res.isexc:
            return renderError(request, tokenuser, res.exc)
        else:
            answer = res.res
            for _, items in answer.items():
                len_results += len(items)
    if request.method == 'POST':
        (itemname, shopname) = request.POST['addItemToCart'].split('|')
        quantity = int(request.POST['quantity'])
        res = m.shopping_carts_add_item(tokenuser, itemname, shopname, quantity)
        if res.isexc:
            errormessage = res.exc

    return makerender(request, tokenuser, 'searchItems.html',
                      {'categories':categories,'len_results': len_results, 'answer': answer, 'searchterm': query, 'category': category,
                       'min_Price': min_Price, 'max_Price': max_Price},error=errormessage)

def mike_join(lst):
    if len(lst) == 0:
        return ""
    else:
        return ', '.join([m for m in lst])
def temp(request):
    u = getToken(request)
    m.registration_for_the_trading_system(u, "username", "password")
    m.login_into_the_trading_system(u, "username", "password")
    u2 = m.get_into_the_Trading_system_as_a_guest().res
    m.registration_for_the_trading_system(u2, "mike", "password")
    m.login_into_the_trading_system(u2, "mike", "password")
    m.shop_open(u, "Mega")
    m.shop_open(u, "Shufersal")
    m.shop_manager_assignment(u,"Mega","mike")
    m.shop_owner_assignment(u,"Shufersal","mike")
    m.adding_item_to_the_shops_stock(u, "name", "Mega", "category", "description", 70.0, 5)
    m.shop_open(u2, "MOMMMMM")
    m.logout(u)
    m.shopping_carts_add_item(u2, "name", "Mega", 3)
    request.COOKIES['tokenuser'] = u2
    return cart(request)

def unpack_managed_shop(tokenuser,res):
    shops = []
    for shopname in res:
        res = m.info_about_shop_in_the_market_and_his_items_name(tokenuser, shopname)
        if res.isexc:
            raise res.exc
        s = res.res
        res = m.get_eligible_members_for_shop(tokenuser, shopname)
        if res.isexc:
            raise res.exc
        eligible = res.res
        shops.append(
            {'name': s['name'], 'founder': s['founder'],
             'managers': mike_join(s['managers']), 'managerslist': s['managers'],
             'owners': mike_join(s['owners']), 'ownerslist': s['owners'],
             'shopopen': s['shopopen'],
             'eligible': eligible}
        )
    return shops
def manage(request):
    tokenuser = getToken(request)
    errormessage = ""

    if request.method == "POST":
        if 'closeshop' in request.POST:
            r = m.shop_closing(tokenuser,str(request.POST['closeshop']))
            if r.isexc:
                return renderError(request, tokenuser, r.exc)
        elif 'reopenshop' in request.POST:
            r = m.shop_reopen(tokenuser,str(request.POST['reopenshop']))
            if r.isexc:
                return renderError(request, tokenuser, r.exc)
        else:
            person = request.POST['person']
            if 'editpermission' in request.POST:
                return redirect("/shop/%s/%s"%(request.POST['editpermission'],person))
            elif 'makeman' in request.POST:
                r = m.shop_manager_assignment(tokenuser, str(request.POST['makeman']),person)
                if r.isexc:
                    errormessage = r.exc
            elif 'delman' in request.POST:
                r = m.delete_shop_manager(tokenuser, str(request.POST['delman']),person)
                if r.isexc:
                    errormessage = r.exc
            elif 'makeown' in request.POST:
                r = m.shop_owner_assignment(tokenuser, str(request.POST['makeown']),person)
                if r.isexc:
                    errormessage = r.exc
            elif 'delown' in request.POST:
                r = m.delete_shop_owner(tokenuser, str(request.POST['delown']),person)
                if r.isexc:
                    errormessage = r.exc
    request.POST = {}

    res = m.get_founded_shops(tokenuser)
    if res.isexc:
        return renderError(request, tokenuser, res.exc)
    found = unpack_managed_shop(tokenuser,res.res)

    res = m.get_owned_shops(tokenuser)
    if res.isexc:
        return renderError(request, tokenuser, res.exc)
    own = unpack_managed_shop(tokenuser, res.res)

    res = m.get_managed_shops(tokenuser)
    if res.isexc:
        return renderError(request, tokenuser, res.exc)
    manage = unpack_managed_shop(tokenuser, res.res)

    return makerender(request, tokenuser, 'manage.html',
                      {'found': found,
                       'own': own,
                       'manage': manage}, errormessage)


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
