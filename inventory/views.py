import json
from django.shortcuts import render
from .models import Product,Category,Supplier
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

@csrf_exempt
#GET-ALL AND POST METHOD
def products(request):

    if request.method == "POST":
        body = json.loads(request.body)

        category_id = body["category"]
        supplier_id = body["supplier"]

        if body["stock"] < 0:
             return JsonResponse({
                 "message" : "Stock cannot be negative"
                },status=400)
        else:
            product = Product.objects.create(
                name = body["name"],
                price = body["price"],
                stock = body["stock"],
                category_id = category_id,
                supplier_id = supplier_id
            )

            return JsonResponse({
                "id" : product.id,
                "name" : product.name,
                "price" : product.price,
                "stock" : product.stock,
                "category" : {
                    "id": product.category.id,
                    "name" : product.category.name
                },
                "supplier" : {
                    "id": product.supplier.id,
                    "name" : product.supplier.name
                }
            },status = 201)

    products = Product.objects.select_related("category","supplier").all()

    data = []

    for product in products:
        data.append({
            "id" : product.id,
            "name" : product.name,
            "price" : product.price,
            "stock" : product.stock,
            "category" : {
                "id": product.category.id,
                "name" : product.category.name
            },
            "supplier" : {
                "id": product.supplier.id,
                "name" : product.supplier.name
            }
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
#GET,PUT,PATCH AND DELETE METHOD
def product_detail(request,id):

    try:
        product = Product.objects.select_related("category", "supplier").get(id=id)

    except Product.DoesNotExist:
        return JsonResponse({
            "message" : "Product does not exist"
        },status=404)
    
    if request.method == "PATCH":
        body = json.loads(request.body)

        if "name" in body:
            product.name = body["name"]
        if "price" in body:
            product.price = body["price"]
        if "stock" in body:
                if body["stock"] < 0:
                    return JsonResponse({
                        "message" : "Stock cannot be negative"
                    },status=400)
                else:
                    product.stock = body["stock"]
        if "category" in body:
            product.category_id = body["category"]
        if "supplier" in body:
            product.supplier_id = body["supplier"]

        product.save()

    if request.method == "PUT":
        body = json.loads(request.body)

        product.name = body["name"]
        product.price = body["price"]
        if body["stock"] < 0:
            return JsonResponse({
                "message" : "Stock cannot be negative"
            })
        else:
            product.stock = body["stock"]
        product.category_id = body["category"]
        product.supplier_id = body["supplier"]
        
        product.save()

    if request.method == "DELETE":
        product.delete()

        return JsonResponse({
            "message" : "Product Deleted Successfully"
        })

    data = {
        "id":product.id,
        "name":product.name,
        "price":product.price,
        "stock":product.stock,
        "category": {
            "id": product.category.id,
            "name": product.category.name
        },
        "supplier": {
            "id": product.supplier.id,
            "name": product.supplier.name
        }
    }

    return JsonResponse(data)


    

def category_products(request,id):
    products = Product.objects.filter(category_id=id)
    data = []
    for product in products:
        data.append({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock
        })
    return JsonResponse(data, safe=False)


def supplier_products(request,id):
    products = Product.objects.filter(supplier_id=id)
    data = []
    for product in products:
        data.append({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock
        })
    return JsonResponse(data, safe=False)


@csrf_exempt
def signup(request):

    if request.method != "POST":
        return JsonResponse({
            "message" : "Only POST method is allowed"
        },status = 405)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "message" : "Invalid JSON"
        },status = 400)

    if "username" not in body or "password" not in body:
        return JsonResponse({
            "message" : "Username and Password is required"
        },status =400)
    
    username = body["username"]
    password = body["password"]

    if User.objects.filter(username = username).exists():
        return JsonResponse({
            "message" : "Username already exists"
        },status = 400)

    user = User.objects.create_user(
        username = username,
        password = password
    )

    token = Token.objects.create(user=user)

    return JsonResponse({
        "message": "User created successfully",
        "token" : token.key
    },status=201)

@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({
            "message" : "Only POST method is allowed"
        },status = 405)
    
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "message" : "Invalid JSON"
        },status = 400)
    
    if "username" not in body or "password" not in body:
        return JsonResponse({
            "message" : "Username and Password is required"
        },status =400)
        
    username = body["username"]
    password = body["password"]
    
    user = authenticate(
        username=username,
        password=password
    )

    if user is None:
        return JsonResponse({
            "message" : "Invalid username or password"
        },status = 401)

    token,created = Token.objects.get_or_create(user=user) #f this user already has a token, give me that token. Otherwise, create one."

    return JsonResponse({
        "message" : "Login successful",
        "token" : token.key
    })