import datetime
from django.core.mail import EmailMessage
from client.models import ErrorHistory
from django.contrib.sites.models import Site

def register_error(number):
    if number == 1:
       description = bookedspot_does_not_exist()
    elif number == 2:
       description = client_does_not_exist()
    elif number == 3:
       description = regularuser_does_not_exist()
    elif number == 4:
       description = parkingmarker_does_not_exist()
    elif number == 5:
       description = parkingmarker_does_not_exist2()
    elif number == 6:
       description = pricelist_does_not_exist()
    elif number == 7:
       description = bookedspot_does_not_exist2()
    elif number == 8:
       description = client_does_not_exist2()
    elif number == 9:
       description = parkingmarker_does_not_exist3()
    elif number == 10:
       description = licenceplate_does_not_exist()
    elif number == 11:
       description = client_does_not_exist3()
    elif number == 12:
       description = parkingmarker_does_not_exist4()
    elif number == 13:
       description = client_does_not_exist4()
    elif number == 14:
       description = parkingmarker_does_not_exist5()
    elif number == 15:
       description = bookedspot_does_not_exist3()
    elif number == 16:
       description = confirm_acctivation_email_error1()
    elif number == 17:
       description = confirm_acctivation_email_error2()
    elif number == 18:
       description = confirm_acctivation_email_error3()
    elif number == 19:
       description = confirm_acctivation_email_error4()
       
    send_error_email(description)

def send_error_email(description):
    site = "website: " + str(Site.objects.get_current().domain)
    date_time = "datetime: "+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    description = date_time + description
    ErrorHistory.objects.create(description=description).save()
    email = EmailMessage('PS Error', description, to=['mihail_workbuz@abv.bg'])
    email.send()

def bookedspot_does_not_exist():
    description = """
        function:  save_parking_info
        fragment:
                try:
                    spot = BookedSpots.objects.get(id=request.POST['booking_id'])
                except BookedSpots.DoesNotExist:
                    register_error(1)
        """
    return description

def client_does_not_exist():
    description = """
        function:  get_parking_requests
        fragment:
            try:
                parking_id = Client.objects.get(user=request.user.id).parking_id
            except Client.DoesNotExist:
                register_error(2)
        """
    return description
    
def regularuser_does_not_exist():
    description = """
        function:  confirm_booking
        fragment:
            try:           
                RegularUser.objects.get(user=request.user.id)
            except RegularUser.DoesNotExist:
                register_error(3)
        """
    return description

def parkingmarker_does_not_exist():
    description = """
        function:  confirm_booking
        fragment:
            try:
                available_spaces = ParkingMarker.objects.get(id=request.POST['parking_id']).availableSpaces
            except ParkingMarker.DoesNotExist:
                register_error(4)
        """
    return description

def parkingmarker_does_not_exist2():
    description = """
        function:  confirm_booking
        fragment:
            try:
                price_list_id = ParkingMarker.objects.get(id=parking_id).priceList_id
                price_list = get_price_list_as_string(PriceList.objects.get(id=price_list_id))
                parking_address = ParkingMarker.objects.get(id=parking_id).address
            except ParkingMarker.DoesNotExist:
                register_error(5)
        """
    return description

def pricelist_does_not_exist():
    description = """
        function:  confirm_booking
        fragment:
                    try:
                        price_list_id = ParkingMarker.objects.get(id=parking_id).priceList_id
                        price_list = get_price_list_as_string(PriceList.objects.get(id=price_list_id))
                        parking_address = ParkingMarker.objects.get(id=parking_id).address
                    except ParkingMarker.DoesNotExist:
                        register_error(5)
                        return HttpResponse("ParkingMarker does not exist", content_type="text/html; charset=utf-8")
                    except PriceList.DoesNotExist:
                        register_error(6)
        """
    return description

def bookedspot_does_not_exist2():
    description = """
        function:  cancel_booking
        fragment:
                try:
                    booked = BookedSpots.objects.get(id=booking_id)
                    push_booking_request_to_parkingadmin(booked.parking_id, booked, 'delete_request')
                    return HttpResponse("deletion complete", content_type="text/html; charset=utf-8")
                except BookedSpots.DoesNotExist:
                    register_error(7)
        """
    return description

def client_does_not_exist2():
    description = """
        function:  actualise_price_list
        fragment:
            try:
                parking_id = Client.objects.get(user=request.user.id).parking_id
            except Client.DoesNotExist:
                register_error(8)
        """
    return description

def parkingmarker_does_not_exist3():
    description = """
        function:  actualise_price_list
        fragment:
                try:
                    price_list_id = ParkingMarker.objects.get(id=parking_id).priceList_id
                except ParkingMarker.DoesNotExist:
                    register_error(9)
        """
    return description

def licenceplate_does_not_exist():
    description = """
        function:  remove_licence_plate
        fragment:
                try:
                    LicencePlates.objects.get(id=plate_id).delete()
                except LicencePlates.DoesNotExist:
                    register_error(10)
        """
    return description

def client_does_not_exist3():
    description = """
        function:  get_price_list
        fragment:
                try:
                    parking_id = Client.objects.get(user=request.user.id).parking_id
                    price_list_id = ParkingMarker.objects.get(id=parking_id).priceList_id
                    price_list = PriceList.objects.filter(id=price_list_id)
                    data = serializers.serialize("json", price_list)
                    return HttpResponse(data, content_type="application/json; charset=utf-8")
                except Client.DoesNotExist:
                    register_error(11)
        """
    return description

def parkingmarker_does_not_exist4():
    description = """
        function:  get_price_list
        fragment:
                try:
                    parking_id = Client.objects.get(user=request.user.id).parking_id
                    price_list_id = ParkingMarker.objects.get(id=parking_id).priceList_id
                    price_list = PriceList.objects.filter(id=price_list_id)
                    data = serializers.serialize("json", price_list)
                    return HttpResponse(data, content_type="application/json; charset=utf-8")
                except Client.DoesNotExist:
                    register_error(11)
                    return HttpResponse("Error on getting pricelist", content_type="text/html; charset=utf-8")
                except ParkingMarker.DoesNotExist:
                    register_error(12)
        """
    return description

def client_does_not_exist4():
    description = """
        function:  actualise_available_spaces
        fragment:
                try:
                    parking_id = Client.objects.get(user=request.user.id).parking_id
                    ParkingMarker.objects.filter(id=parking_id).update(availableSpaces=available_spaces)
                except Client.DoesNotExist:
                    register_error(13)
        """
    return description

def parkingmarker_does_not_exist5():
    description = """
        function:  profile
        fragment:
            try:
                parking_id = Client.objects.get(user=request.user.id).parking_id
                current_available_spaces = ParkingMarker.objects.get(id=parking_id).availableSpaces
                return render_to_response('clientprofile.html', {'available_spaces':current_available_spaces}, context_instance=RequestContext(request))
            except Client.DoesNotExist:
                pass
            except ParkingMarker.DoesNotExist:
                register_error(14)
        """
    return description

def bookedspot_does_not_exist3():
    description = """
        function:  cancel_booking_admin
        fragment:
                try:
                    BookedSpots.objects.get(id=booking_id).delete()
                    return HttpResponse("deletion complete", content_type="text/html; charset=utf-8")
                except BookedSpots.DoesNotExist:
                    register_error(15)
        """
    return description

def confirm_acctivation_email_error1():
    description = """
        function:  email_confirmation.confirm
        fragment:
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    HttpResponseRedirect('/error_page/')
                    register_error(16)
        """
    return description

def confirm_acctivation_email_error2():
    description = """
        function:  email_confirmation.confirm
        fragment:
                try:
                    profile = UserProfile.objects.get(user=user)
                    if profile.activation_key == activation_key:# and user.date_joined > (datetime.datetime.now()-datetime.timedelta(days=1)):
                        user.is_active = True
                        user.save()
                        #user.backend='django.contrib.auth.backends.ModelBackend' 
                        #auth_login(request,user)
                        return redirect_to_login(request)
                    else:
                        register_error(17)
                        return HttpResponseRedirect('/error_page/')
        """
    return description

def confirm_acctivation_email_error3():
    description = """
        function:  email_confirmation.confirm
        fragment:
                except UserProfile.DoesNotExist:
                    return HttpResponseRedirect('/error_page/')
                    register_error(18)
        """
    return description

def confirm_acctivation_email_error4():
    description = """
        function:  email_confirmation.confirm
        fragment:
                except:
                    HttpResponseRedirect('/error_page/')
                    register_error(19)
        """
    return description