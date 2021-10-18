from django.shortcuts import render

def index(request):
    context = {
        'title': 'Главная'
    }
    return render(request, 'mainapp/index.html', context)


def contact(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, 'mainapp/contact.html')

links_menu = [
        {
            'url': 'products',
            'title': 'все'
        },
        {
            'url': 'products_home',
            'title': 'дом'
        },
        {
            'url': 'products_office',
            'title': 'офис'
        },
        {
            'url': 'products_modern',
            'title': 'модерн'
        },
        {
            'url': 'products_classic',
            'title': 'классика'
        },
    ]


def products(request):
    context = {
        'links_menu': links_menu,
        'title': 'Продукты'
    }
    return render(request, 'mainapp/products.html', context=context)

def products_home(request):
    context = {
        'links_menu': links_menu,
        'title': 'Продукты для дома'

    }
    return render(request, 'mainapp/products.html', context=context)

def products_office(request):
    context = {
        'links_menu': links_menu,
        'title': 'Продукты для офиса'
    }
    return render(request, 'mainapp/products.html', context=context)

def products_modern(request):
    context = {
        'links_menu': links_menu,
        'title': 'Продукты модерн'
    }
    return render(request, 'mainapp/products.html', context=context)

def products_classic(request):
    context = {
        'links_menu': links_menu,
        'title': 'Продукты классика'
    }
    return render(request, 'mainapp/products.html', context=context)
