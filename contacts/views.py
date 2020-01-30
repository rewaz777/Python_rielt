from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # Check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.erorr(request, 'Вы уже сделали запрос')
                return redirect('/listing/'+listing_id)

        contact = Contact(listing=listing, listing_id= listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)

        contact.save()

        # Send email
        send_mail(
            'Запрос недвижимости',
            'Запрос для' + listing + '. Войдите в админку для информации'
            'traversy.fda77777@gmail.com'
            [realtor_email, 'fda77777@gmail.com'],
            fail_silently=False
        )

        messages.success(request, 'Ваш запрос был отправлен, cпециалист свяжется с вами в ближайшее время')
        return redirect('/listings/'+listing_id)


