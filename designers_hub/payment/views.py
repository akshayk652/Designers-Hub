from django.shortcuts import render
import stripe
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm

stripe.api_key = settings.STRIPE_SECRET_KEY

def payment(request):
    context = {
        'key' : settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request,'payment/payment_process.html',context)

def charge(request):
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount = 1000,
            currency = 'usd',
            description = "To make payment",
            source = request.POST['stripeToken']
        )
        return render(request, 'payment/payment_done.html')


def payment_process(request):
    paypal_dict = {
        'business': 'deveshj04-fas@gmail.com',
        'amount': '1000.00',
        'item_name': 'Item_Name_xyz',
        'currency':'INR',
        'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
        'return': request.build_absolute_uri(reverse('payment_done')),
        'cancel_return': request.build_absolute_uri(reverse('payment_canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/payment_process.html', {'form': form })