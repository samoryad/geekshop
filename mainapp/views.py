from django.shortcuts import render


def main(request):
    content = {
        'user':{
            'first_name': 'andrey',
            'last_name': 'samoryadov'
        }
    }
    return render(request, 'mainapp/index.html', content)


def products(request):
    return render(request, 'mainapp/products.html')


def contact(request):
    return render(request, 'mainapp/contact.html')
