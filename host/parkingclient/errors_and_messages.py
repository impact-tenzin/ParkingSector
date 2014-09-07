import datetime
from django.core.mail import EmailMessage
from parkingclient.models import ErrorHistory
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
       
    send_error_email(description)

def send_error_email(description):
    site = "website: " + str(Site.objects.get_current().domain)
    date_time = "datetime: "+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    description = site + date_time + description
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
                    BookedSpots.objects.get(id=booking_id).delete()
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