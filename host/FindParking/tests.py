from django.test import TestCase
from FindParking.views import distance
from FindParking.models import ParkingMarker

class Distance_FindParking(TestCase):
    def test_distanceWithTrivialParameters(self):
        seattle = [47.621800, -122.350326]
        olympia = [47.041917, -122.893766]
        actualDistance = distance(seattle, olympia)
        expectedDistance = 76.38661579954869
        self.assertEqual(expectedDistance, actualDistance)
        
    def test_distanceWithPredictableOutput(self):
        pointA = [0.0, 0.0]
        pointB = [1.0, 1.0]
        distanceAB = distance(pointA, pointB)
        pointC = [0.0, 0.0]
        pointD = [-1.0, -1.0]
        distanceCD = distance(pointC, pointD)
        self.assertEqual(distanceAB, distanceCD)
        
    def test_distanceWithZeroValues(self):
        pointA = [0.0, 0.0]
        pointB = [0.0, 0.0]
        actualDistance = distance(pointA, pointB)
        expectedDistance = 0.0
        self.assertEqual(expectedDistance, actualDistance)
        
class ModelsReturnFunctions(TestCase):
    def test_getLat_getLng(self):
        parking = ParkingMarker.objects.create(lat=55.12344, lng=32.44412)
        expectedLat = 55.12344
        actualLat = parking.getLat()
        expectedLng = 32.44412
        actualLng = parking.getLng()
        self.assertEqual(expectedLat, actualLat)
        self.assertEqual(expectedLng, actualLng)