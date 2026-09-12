import json
from django.shortcuts import render
from .models import Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def products(request):

    if request.method == "POST":
        body = json.loads(request.body)
        product = Product.objects.create(
            name = body["name"],
            price = body["price"],
            stock = body["stock"]
        )

        return JsonResponse({
            "id" : product.id,
            "name" : product.name,
            "price" : product.price,
            "stock" : product.stock
        },status = 201)

    products = Product.objects.all()

    data = []

    for product in products:
        data.append({
            "id" : product.id,
            "name" : product.name,
            "price" : product.price,
            "stock" : product.stock
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def product_detail(request,id):

    product = Product.objects.get(id=id)

    if request.method == "PATCH":
        body = json.loads(request.body)

        if "name" in body:
            product.name = body["name"]
        if "price" in body:
            product.price = body["price"]
        if "stock" in body:
            product.stock = body["stock"]

        product.save()

    if request.method == "PUT":
        body = json.loads(request.body)

        product.name = body["name"]
        product.price = body["price"]
        product.stock = body["stock"]

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
        "stock":product.stock
    }

    return JsonResponse(data)


    

