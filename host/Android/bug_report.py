import datetime
from django.core.mail import EmailMessage
from client.models import ErrorHistory
from django.contrib.sites.models import Site

def android_error(number):
    if number == 1:
        description = bug1()
    elif number == 2:
        description = bug2()
    elif number == 3:
        description = bug3()
    elif number == 4:
        description = bug4()
    elif number == 5:
        description = bug5()
    elif number == 6:
        description = bug6()
    elif number == 7:
        description = bug7()
    elif number == 8:
        description = bug8()
    elif number == 9:
        description = bug9()
        
    send_error_email(description)

def send_error_email(description):
    site = "Android: " + str(Site.objects.get_current().domain) + "\n"
    date_time = "datetime: "+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    description = site + date_time + description
    ErrorHistory.objects.create(description=description).save()
    email = EmailMessage('Android Error', description, to=['mihail_workbuz@abv.bg'])
    email.send()
    
def bug1():
    description = """
            def user_is_logged_in(session_key):
                try:
                    MobileSession.objects.get(session_key=str(session_key))
                    register_error(1)
                    return True
                except:
                    return False
        """
    return description

def bug2():
    description = """
             def get_user_by_sessionkey(session_key):
                try:
                    user_id = MobileSession.objects.get(session_key=session_key).user_id
                    user = User.objects.get(pk=user_id)
                    return user
                except MobileSession.DoesNotExist:
                    register_error(2)
                except User.DoesNotExist:
                    register_error(3)
        """
    return description

def bug3():
    description = """
                def get_user_by_sessionkey(session_key):
                    try:
                        user_id = MobileSession.objects.get(session_key=session_key).user_id
                        user = User.objects.get(pk=user_id)
                        return user
                    except MobileSession.DoesNotExist:
                        register_error(2)
                    except User.DoesNotExist:
                        register_error(3)
        """
    return description

def bug4():
    description = """
    function: confirm_booking
            try:
                user = get_user_by_sessionkey(request.POST['session_key'])
                RegularUser.objects.get(user=user.id)
            except RegularUser.DoesNotExist:
                android_error(4)
        """
    return description

def bug5():
    description = """
    function: confirm_booking
                try:
                    available_spaces = ParkingMarker.objects.get(id=request.POST['parking_id']).availableSpaces
                except ParkingMarker.DoesNotExist:
                    android_error(5)
                    return HttpResponse("ParkingMarker does not exist", content_type="text/html; charset=utf-8")
        """
    return description

def bug6():
    description = """
    function: confirm_booking
                    try:
                        parking = ParkingMarker.objects.get(id=parking_id)
                        parking_address = parking.address
                        lat = parking.lat
                        lng = parking.lng
                        price_list_id = parking.priceList_id
                        price_list = get_price_list_as_string(PriceList.objects.get(id=price_list_id))
                    except ParkingMarker.DoesNotExist:
                        android_error(6)
                        return HttpResponse("ParkingMarker does not exist", content_type="text/html; charset=utf-8")
        """
    return description

def bug7():
    description = """
    function: confirm_booking
                    try:
                        parking = ParkingMarker.objects.get(id=parking_id)
                        parking_address = parking.address
                        lat = parking.lat
                        lng = parking.lng
                        price_list_id = parking.priceList_id
                        price_list = get_price_list_as_string(PriceList.objects.get(id=price_list_id))
                    except ParkingMarker.DoesNotExist:
                        android_error(6)
                        return HttpResponse("ParkingMarker does not exist", content_type="text/html; charset=utf-8")
                    except PriceList.DoesNotExist:
                        android_error(7)
                        return HttpResponse("PriceList does not exist", content_type="text/html; charset=utf-8")
        """
    return description

def bug8():
    description = """
        def remove_licence_plate(request):
            if 'android' in mobile(request):
                if user_is_logged_in(request.POST['session_key']):
                        plate_id = request.POST['plate_id']
                        try:
                            LicencePlates.objects.get(id=plate_id).delete()
                        except LicencePlates.DoesNotExist:
                            android_error(8)
                        return HttpResponse("deletion complete", content_type="text/html; charset=utf-8")        
                else:
                    return HttpResponse("session key does not exist", content_type="text/html; charset=utf-8")
            else:
                return HttpResponse("Error", content_type="text/html; charset=utf-8")
        """
    return description

def bug9():
    description = """
        def cancel_booking(request):
            if 'android' in mobile(request):
                if user_is_logged_in(request.POST['session_key']):
                        booking_id = request.POST["booking_id"]
                        try:
                            booked = BookedSpots.objects.get(id=booking_id)
                            push_booking_request_to_parkingadmin(booked.parking_id, booked, 'delete_request')
                            booked.delete()
                            return HttpResponse("cancelation complete", content_type="text/html; charset=utf-8")
                        except BookedSpots.DoesNotExist:
                            register_error(9)
                            return HttpResponse("BookedSpot does not exist", content_type="text/html; charset=utf-8")
                else:
                    return HttpResponse("session key does not exist", content_type="text/html; charset=utf-8")
            else:
                return HttpResponse("Error", content_type="text/html; charset=utf-8")
        """
    return description