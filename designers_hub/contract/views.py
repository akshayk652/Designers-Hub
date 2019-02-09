import os

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404


from .forms import UploadFileForm, ContractForm
from .models import ContractFile, Contract, Rating
from user_profile.models import Designer

from designers_hub.settings import BASE_DIR

User = get_user_model()

@login_required
def contract_details(request, pk):
    template_name = 'contract/contract_details.html'
    contract = Contract.objects.get(id=pk)
    files = ContractFile.objects.filter(contract=contract)
    print(files)
    context = {
            'contract': contract,
            'files': files
    }
    return render(request, template_name, context)


@login_required
def upload_file(request, pk):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            cf = ContractFile()
            cf.description = form.cleaned_data['description']
            cf.file_path = form.cleaned_data['file_path']
            cf.contract = get_object_or_404(Contract, id=pk)
            cf.save()
            return redirect('contract-details', pk=pk)
    else:
        form = UploadFileForm()
        return render(request, 'contract/file_upload.html', {'form': form})


@login_required
def download(request, pk):
    contract = ContractFile.objects.get(id=pk)
    path = str(contract.file_path)
    file_path = os.path.join(BASE_DIR, 'media', path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

@login_required
def contracts_list(request):
    template_name = "contract/contracts.html"
    is_exists = False
    user = get_object_or_404(User, username=request.user.username)
    if user.is_client:
        contracts = Contract.objects.filter(client=user)
        is_exists = len(contracts)
        user_info = user
        account_type ="client"
    else:
        designer = get_object_or_404(Designer, user=user)
        contracts = Contract.objects.filter(designer=designer)
        is_exists = len(contracts)
        user_info = user 
        account_type = False
    context = {
        "contracts": contracts,
        "account_type": account_type,
        "is_exists" : is_exists,
        "user_info": user_info
    }
    return render(request, template_name, context)
    

def email(request,subject, message, type=None ):
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['nikhil.backto@gmail.com',]
    if type:
        message = "A chat room is created by {0}, click on the link to chat - {1}".format(request.user.username, message)
        send_mail( subject, message, email_from, recipient_list )
        return None
    send_mail( subject, message, email_from, recipient_list )
    return redirect('contracts-list')

@login_required
def contract_create_form(request):
    template_name = "contract/contract-form.html"    
    if request.method == "POST":
        form = ContractForm(request.POST)
        if form.is_valid(): 
            designer = form.cleaned_data["username"]
            client = get_object_or_404(User, username=request.user.username)
            contract = Contract()
            contract.client = client
            contract.designer = get_object_or_404(Designer, user=designer)
            contract.title = form.cleaned_data["title"]
            contract.description = form.cleaned_data["description"]
            contract.save()
            subject = "Contract {0}".format(contract.title)
            message = "A contract {0} has been created by {1}".format(contract.title, request.user.username)
            email(request, subject,message)
            return redirect('contract-details', pk=contract.id)       
    else:
        form = ContractForm() 
    return render(request, template_name, {'form':form})

@login_required    
def delete_contract(request, pk):
    if request.method == "POST":
        contract = Contract.objects.get(id=pk)
        contract.status = "deactive"
        contract.save()
        subject = "Contract {0}".format(contract.title)
        message = "Your contract {0} with {1} has been deleted".format(contract.title, request.user.username)
        email(request, subject,message)

    return redirect('contracts-list')

@login_required
def complete_contract(request,pk):
    if request.method == "POST":
        contract = Contract.objects.get(id=pk)
        contract.status = "completed"
        contract.save()

        subject = "Contract {0}".format(contract.title)
        message = "Congratulations, your contract {0} with {1} has been Completed".format(contract.title, request.user.username)
        email(request, subject, message)
        return redirect('contract-rating', pk=pk)
    return redirect('contracts-list')

@login_required
def rating(request, pk):
    if request.method == "POST":
        rated = request.POST["rate"]
        ratings = Rating()
        contract_detail = Contract.objects.get(id=pk)
        ratings.contract = contract_detail
        ratings.designer = contract_detail.designer
        ratings.rating = rated
        ratings.save()
        return redirect('payments')
    return render(request, "contract/ratings.html", {"pk": pk})

@login_required
def get_rating(request, designer_name):
    designer = User.objects.get(username = designer_name)
    designer = Designer.objects.get(user = designer)
    rating = Rating.objects.filter(designer=designer).aggregate(Avg('rating'))
    if not rating:
        rating=0
    print(rating)
    return rating["rating__avg"]


