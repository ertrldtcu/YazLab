######################################################################
#                                                                    #
#               40.000'den fazla verisi olan araçlarla               #
#                   yeni bir csv dosyası oluşturur                   #
#                                                                    #
######################################################################
#
# csv = open("allCars.csv", "rt")
# newcsv = open("allCars_clean.csv", "wt")
#
# arr = [0 for i in range(1116)]
#
# for line in csv:
#     id = int((line.split(",")[3]).replace("\n",""))
#     if type(id) != int:
#         print("Hata !", (line.split(",")[3]))
#         continue
#     arr[id-1] += 1
#
# csv.seek(0)
#
# for line in csv:
#     id = int((line.split(",")[3]).replace("\n",""))
#     if type(id) != int:
#         print("Hata !", (line.split(",")[3]))
#         continue
#     if arr[id-1] > 40000:
#         newcsv.write(line)
#     else:
#         arr[id-1] = 0
#
# sum = 0
# row = 0
# for v in arr:
#     if v > 0:
#         sum += 1
#         row += v
# print("Araç sayısı:",sum,"Toplam veri:",row)

from math import radians, cos, sin, asin, sqrt


def distance(lat1, lon1, lat2, lon2):
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    return c * r


def is_location_fit(lat1, lang1, lat2, lang2):
    if lat1 == 0 and lang1 == 0:
        return False

    dist = distance(lat1, lang1, lat2, lang2)
    if dist < 0.1:
        return False

    return True


csv = open("allCars_clean.csv", "rt")
newcsv = open("allCars_cleanx2.csv", "wt")

previous_lat = 0
previous_lang = 0
for line in csv:
    data = line.replace("\n", "").split(",")
    carid = int(data[3])
    if type(carid) != int:
        print("Hata !", carid)
        continue
    # print(data)
    if is_location_fit(float(data[1]), float(data[2]), previous_lat, previous_lang):
        newcsv.write(line)
        previous_lat = float(data[1])
        previous_lang = float(data[2])
