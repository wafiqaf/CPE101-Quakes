import math


class Earthquake:
    """A class to represent an Earthquake."""
    def __init__(self, place, mag, longitude, latitude, time):
        self.place = place
        self.mag = mag
        self.longitude = longitude
        self.latitude = latitude
        self.time = time

    def __eq__(self, other):
        return (
                self.place == other.place and
                math.isclose(self.mag, other.mag) and
                math.isclose(self.longitude, other.longitude) and
                math.isclose(self.latitude, other.latitude) and
                math.isclose(self.time, other.time)
                )

    def __repr__(self):
        return "Earthquake(%r, %r, %r, %r, %r)" % (self.place,
                                                   self.mag,
                                                   self.longitude,
                                                   self.latitude,
                                                   self.time)


def quake_from_feature(feature):
    location = feature['properties']['place']
    mag = feature['properties']['mag']
    time = feature['properties']['time']
    longitude = feature['geometry']['coordinates'][0]
    latitude = feature['geometry']['coordinates'][1]

    return Earthquake(location, mag, longitude, latitude, int((time / 1000)))


# NOTE: This function takes an already open file as input.  You *will not*
# be opening anything in this function.
def read_quakes_from_file(file):
    store_quake = []
    quake_loc = []
    final_list = []

    for line in file:
        for obj in line.split():
            store_quake.append(obj)
        length = len(store_quake)
        i = 4
        while i < (length):
            quake_loc.append(store_quake[i])
            i += 1

        confirmlocation = " ".join(quake_loc)

        new_quake = Earthquake(confirmlocation, float(store_quake[0]),
                               float(store_quake[1]), float(store_quake[2]),
                               int(store_quake[3]))

        final_list.append(new_quake)
        store_quake = []
        quake_loc = []

    return final_list


def filter_by_mag(quakes, low, high):
    mag_quakes = []

    for index in quakes:
        if index.mag >= float(low) and index.mag <= float(high):
            mag_quakes.append(index)

    return mag_quakes


def filter_by_place(quakes, word):
    place_quakes = []

    for index in quakes:
        formatind = index.place
        if word.upper() in formatind.upper():
            place_quakes.append(index)

    return place_quakes
