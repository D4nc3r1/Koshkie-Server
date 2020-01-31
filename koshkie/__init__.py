#  Copyright (c) Code Written and Tested by Ahmed Emad in 26/01/2020, 17:49
import math
from abc import ABC

from django.db.models import Func


class Sin(Func, ABC):
    function = 'SIN'


class Cos(Func, ABC):
    function = 'COS'


class Asin(Func, ABC):
    function = 'ASIN'


class Sqrt(Func, ABC):
    function = 'SQRT'


def haversine(lat1, lon1, lat2, lon2):
    dlat = (lat2 - lat1) * math.pi / 180.0
    dlon = (lon2 - lon1) * math.pi / 180.0

    lat1 = lat1 * math.pi / 180.0
    lat2 = lat2 * math.pi / 180.0

    a = (pow(Sin(dlat / 2), 2) +
         pow(Sin(dlon / 2), 2) *
         Cos(lat1) * Cos(lat2))
    rad = 6371
    c = 2 * Asin(Sqrt(a))
    return rad * c