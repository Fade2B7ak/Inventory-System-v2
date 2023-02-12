from .models import NewProduct
from .forms import RegisterForm, AddProductsForm, UpdateProductForm
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm


def registration(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            messages.success(request, "Registration successful.")
            return redirect("invent:login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = RegisterForm()
    return render(request=request, template_name="inventorySystem/registration.html",
                  context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("invent:list")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request=request, template_name="invent:list", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("invent:login")


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.object.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "Inventory/templates/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Dano Tehnics',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html",
                  context={"password_reset_form": password_reset_form})


@login_required
def index(request):

    return render(request, 'inventoryTemplates/index.html')


@login_required
def inventory_list(request):
    inventories = NewProduct.objects.all()
    context = {
        "title": "Inventory List",
        "inventories": inventories
    }
    return render(request, 'inventoryTemplates/inventory_list.html', context=context)


@login_required
def add_product(request):
    if request.method == "POST":
        add_form = AddProductsForm(data=request.POST)
        if add_form.is_valid():
            new_inventory = add_form.save(commit=False)
            new_inventory.input = float(add_form.data['price_per_piece']) * float(add_form.data['quantity'])
            new_inventory.save()
            return redirect("/list/")
    else:
        add_form = AddProductsForm()

    return render(request, 'inventoryTemplates/add_product.html', {"form": add_form})


@login_required
def update_product(request, pk):
    inventory = get_object_or_404(NewProduct, pk=pk)
    if request.method == "POST":
        updateForm = UpdateProductForm(data=request.POST)
        if updateForm.is_valid():
            inventory.itemClass = updateForm.data['itemClass']
            inventory.name = updateForm.data['name']
            inventory.model = updateForm.data['model']
            inventory.quantity = updateForm.data['quantity']
            inventory.cost_per_piece = float(updateForm.data['price_per_piece'])
            inventory.save()
            return redirect("/list/")
    else:
        updateForm = UpdateProductForm(instance=inventory)
        context = {
            "form": updateForm
        }
    return render(request, 'inventoryTemplates/update_product.html', {"form": updateForm})


@login_required
def delete_product(request, pk):
    inventory = get_object_or_404(NewProduct, pk=pk)
    inventory.delete()
    return redirect("/list/")


@login_required
def product_info(request, pk):
    inventory = get_object_or_404(NewProduct, pk=pk)
    context = {
        'inventory': inventory,
    }
    return render(request, 'inventoryTemplates/product_info.html', context=context)


def about(request):
    context = {

    }
    return render(request, 'inventoryTemplates/about.html')
