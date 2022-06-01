from pymongo import MongoClient
import pprint
import datetime
import time

# table doktorlar
variable = ""
doctor_name = "doctor_name"  # değişkenleri diğer dosyadan değiştirebilmek için ekledim
doctor_profession = "doctor_profession"
doctor_place = "doctor_place"
working_start_time = 8.30
working_end_time = 17.30
doctor_number = 9999

# polikinlik
policlinic = "pol"

# table randevular
appointment_number = 911
appointment_variable = ""
patient_name = "Mustafa Muharrem"
patient_id = 134999782133
appointment_department = "Dahiliye"
appointment_doctor = "Mehmet Avcı"

time = time.time()
date = str(datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S'))
hour = float(datetime.datetime.fromtimestamp(time).strftime('%H.%M'))

doctor_not_found = "Böyle Bir Doktor Bulunamadı"
patient_not_found = "Böyle Bir Hasta Bulunamadı"

pp = pprint.PrettyPrinter(indent=4)
try:
    cluster = MongoClient(
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    db = cluster['Mira']
    doctors_table = db['Doktorlar']
    policlinic_table = db['poliklinikler']
    patients_table = db['Hastalar']
    incomprehensible = db['Anlasilmayan']

    print("bağlantı başarılı")
except Exception as e:
    print(e)


# a = collection.find({ "_id": 1})
#
# for element in a:
#     isim = element['isim']
#     print(isim)

def add_incomprehensible_value():
    data = {
        "Anlasilmayan": variable,
        "Tarih": date
    }
    incomprehensible.insert_one(data)


def find_by_name():
    try:
        if variable == "bilgileri":
            a = doctors_table.find({"isim": doctor_name})
            for element in a:
                value = "İsim: " + element["isim"] + "\n" + "Alanı: " + element["alani"] + "\n" + "Yeri: " + element[
                    "yeri"]
            return value
        else:
            a = doctors_table.find({"isim": doctor_name})
            for element in a:
                value = element[variable]
            return value

    except Exception as name_error:
        print(name_error)
        return doctor_not_found


def is_here():
    global cikissaati, girissaati
    try:
        a = doctors_table.find({"isim": doctor_name})
        for element in a:
            girissaati = element["giris"]
            cikissaati = element["cikis"]
        return girissaati, cikissaati
    except Exception as is_here_error:
        print(is_here_error)
        return doctor_not_found


def appointment_query():
    global value
    try:
        a = patients_table.find({"ranSiraNo": appointment_number})
        for element in a:
            value = element[appointment_variable]
        return value
    except Exception as appoinment_error:
        print(appoinment_error)
        return str(patient_not_found)
