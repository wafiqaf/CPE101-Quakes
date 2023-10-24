import quake_funcs
import sys
import utils


def main():

    my_file = open(sys.argv[1], 'r')
    # list of Earthquake(content), Earthquake(content)...
    inquakes = quake_funcs.read_quakes_from_file(my_file)
    filtquakes = None
    programrun = True
    filtered = False

    while programrun:
        print("\nEarthquakes:\n------------")

        if filtered:
            display_data(filtquakes)
            filtered = False
        else:
            display_data(inquakes)

        # options here
        print("\nOptions:")
        print("\n(s)ort\n(f)ilter\n(n)ew quakes\n(q)uit\n")

        optionchoice = input("Choice: ")
        # SORTING WORKS!
        if optionchoice == "s" or optionchoice == "S":
            sortchoice = input("Sort by (m)agnitude, (t)ime,"
                               " (l)ongitude, or l(a)titude? ")
            if sortchoice == "m" or sortchoice == "M":
                inquakes.sort(key=get_mag, reverse=True)
            elif sortchoice == "t" or sortchoice == "T":
                inquakes.sort(key=get_time, reverse=True)
            elif sortchoice == "l" or sortchoice == "L":
                inquakes.sort(key=get_long)
            else:
                inquakes.sort(key=get_lat)
        # FILTERING WORKS!
        elif optionchoice == "f" or optionchoice == "F":
            filchoice = input("Filter by (m)agnitude or (p)lace? ")
            filtered = True
            if filchoice == "m" or optionchoice == "M":
                low = input("Lower bound: ")
                up = input("Upper bound: ")
                magquakes = quake_funcs.filter_by_mag(inquakes, low, up)
                filtquakes = magquakes
            if filchoice == "p" or optionchoice == "P":
                strchoice = input("Search for what string? ")
                placequakes = quake_funcs.filter_by_place(inquakes, strchoice)
                filtquakes = placequakes

        elif optionchoice == "n" or optionchoice == "N":
            www = 'http://earthquake.usgs.gov/earthquakes/feed/' \
                  'v1.0/summary/1.0_hour.geojson'
            dictionary = utils.get_json(www)
            features = dictionary['features']
            found = False

            for item in features:
                currentquake = quake_funcs.quake_from_feature(item)
                if not currentquake in inquakes:
                    inquakes.append(currentquake)
                    found = True

            if found:
                print("\nNew quakes found!!!")

        elif optionchoice == "q" or optionchoice == "Q":
            reorder = open(sys.argv[1], 'w')
            for quake in inquakes:
                place = quake.place
                confirmplace = place.strip('"')
                orgform = ("%r %r %r %r %s\n" % (quake.mag,
                                                 quake.longitude,
                                                 quake.latitude,
                                                 quake.time,
                                                 confirmplace))
                reorder.write(orgform)
            programrun = False

    my_file.close()
    reorder.close()


def display_data(quakes):
    for i in quakes:
        time = utils.time_to_str(i.time)
        print("(%.2f) %40s at %s (%8.3f, %7.3f)" % (i.mag, i.place,
                                                    time, i.longitude,
                                                    i.latitude))


def get_mag(quake):
    return quake.mag


def get_time(quake):
    return quake.time


def get_long(quake):
    return quake.longitude


def get_lat(quake):
    return quake.latitude


if __name__ == '__main__':
    main()
