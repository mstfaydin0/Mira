import cv2
import speech_recognition as sr  # Ses tanıma kütüphanesini sr olarak kısaltıyoruz.
import time  # time modülü ile bekletmeler yapıyoruz
import datetime
from gtts import gTTS  # Google Text To Speech ile yazıları ses dönüştürüyoruz ama bunu değiştirmeyi umuyorum
import random  # Daha ilginç cevap ve diyologlar için random kullanıyoruz.
import os  # Os modülü sayesinde dosyaları yönetebiliyoruz
import commands
import mongodb
from tkinter import *
import wikipedia
from twilio.rest import Client
from mutagen.mp3 import MP3  # mp3 sürelerini ölçmek için kullanıyoruz
from pygame import mixer  # mp3 dosyalarını oynatmak için kullanıyoruz

account_sid_twilio = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
auth_token_twilio = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
client_twilio = Client(account_sid_twilio, auth_token_twilio)

mixer.init()

rand = random.randint(1, 10000)
file = "audio-" + str(rand) + ".mp3"

window = Tk()  # tkinter

var = StringVar()
var1 = StringVar()
var2 = StringVar()

time = time.time()
hour = float(datetime.datetime.fromtimestamp(time).strftime('%H.%M'))
year = int(datetime.datetime.fromtimestamp(time).strftime('%Y'))
month = int(datetime.datetime.fromtimestamp(time).strftime('%m'))
day = int(datetime.datetime.fromtimestamp(time).strftime('%d'))

mic_sound = r"src\audio\mic.mp3"

r = sr.Recognizer()  # ses dönütlerini almak için bir değişken belirliyoruz.


def mask_detect():
    var1.set("Maske Tespit İşlemi Başlatıldı!")
    window.update()
    camera = cv2.VideoCapture(0)  # bu alanda camerayı açtık
    return_value, image = camera.read()
    cv2.imwrite('test.png', image)  # kameradaki fotoğrafı test.png adında kaydettik
    camera.release()
    cv2.destroyAllWindows()  # ekranı kapattık aslında açıldığını görmedik
    var.set("Tespit Ediliyor...")
    window.update()
    os.system("python face_detector\\detect_mask_image.py --image test.png")  # detect mask dosayasını çalıştırmak için
    # cmd komutu ile fotoğrafı belirttik ve çalıştırdık
    var.set("İşlem Tamamlandı")
    window.update()
    var1.set("Hastane Asistanı Mira'Ya\n"
             "Merhaba De!")
    window.update()


def features():
    var.set("Randevunuz Hakkında Bilgi Alabilirsiniz\n"
            "Doktorlar Hakkında Bilgi Alabilirsiniz\n"
            "Doktorun Hastanede Olup Olmadığını Öğrenebilirsiniz\n"
            "Muayenehanelerin yerlerini öğrenebilirsiniz\n"
            "Ve Daha Birçok Şeyi Mira ile Konuşarak Öğrenebilirsiniz!")
    window.update()


def switch_hour(argument):
    switcher = {
        8.3: " Sekiz Otuz",
        10.3: " On Otuz",
        17.3: " On Yedi Otuz",
        18.3: " On Sekiz Otuz",
        19.3: " On Dokuz Otuz",
        22.3: " Yirmi İki Otuz"
    }
    return switcher.get(argument, "bulunamadı")
    # print(switcher.get(argument, "Invalid month"))


def record():
    with sr.Microphone() as source:
        mixer.music.load(mic_sound)
        mixer.music.play()
        var.set("Dinleniyor...")
        window.update()
        print("Dinleniyor...")
        r.pause_threshold = 1
        r.energy_threshold = 400
        audio = r.listen(source)
    try:
        var.set("Tanımlanıyor...")
        window.update()
        print("Tanımlanıyor...")
        voice = r.recognize_google(audio, language='tr-TR')
    except Exception as e:
        print(e)
        return "None"
    var1.set(voice)
    window.update()
    return voice


def exit():
    exit()


def start():
    # btn2['state'] = 'disabled'
    # btn0['state'] = 'disabled'
    # btn1.configure(bg='orange')
    # label2.pack()
    # label3.pack()
    # btn0.destroy()
    # btn1.destroy()
    mask_detect()
    while True:
        btn1.configure(bg='orange')
        voice = record().lower()
        if 'bay bay' in voice:
            var.set("Güle Güle")
            btn1.configure(bg='#5C85FB')
            btn2['state'] = 'normal'
            btn0['state'] = 'normal'
            window.update()
            speak("Güle Güle")
            break

        if voice in commands.how_are_you:  # Eğer tanımladıklarımızın içinde bu tanım varsa
            c = random.randint(0, len(commands.answer_how_are_you) - 1)
            var.set(commands.answer_how_are_you[c])
            window.update()
            speak(commands.answer_how_are_you[c])

        elif voice in commands.what_time_is_it:  # saati datetime kütüphanesinden alıp söylüyor
            var.set(datetime.datetime.now().strftime("%H:%M"))
            window.update()
            speak(datetime.datetime.now().strftime("%H:%M"))

        elif voice in commands.what_are_you_doing:
            c = random.randint(0, len(commands.anwer_what_are_you_doing) - 1)
            var.set(commands.anwer_what_are_you_doing[c])
            window.update()
            speak(commands.anwer_what_are_you_doing[c])

        elif voice in commands.thanks:
            c = random.randint(0, len(commands.answer_thanks) - 1)
            var.set(commands.answer_thanks[c])
            window.update()
            speak(commands.answer_thanks[c])

        elif "Mira" in voice:
            var.set("Efendim")
            window.update()
            speak("Efendim")

        elif "burada mı" in voice:  # doktorun giriş ve çıkış saatini kontrol ediyor
            mongodb.doctor_name = voice.replace(" burada mı", "").title()
            sonuc = mongodb.is_here()
            hastanede = "Doktor Hastanede"
            degil = "Doktor Hastanede Değil\n Doktorun Hastaneye giriş saati" + str(switch_hour(sonuc[0])) + \
                    "Çıkış saati" + str(switch_hour(float(sonuc[1])))
            if type(sonuc[0]) is str:
                speak(mongodb.is_here())
            elif sonuc[0] <= 23 <= sonuc[1]:
                speak(hastanede)
            else:
                speak(degil)
            mongodb.doctor_name = ""
            # var.set(mongodb.is_here())
            # window.update()
            # speak(mongodb.is_here())

        elif "bilgileri" in voice:  # eğer sesin içinde bu tanım varsa
            mongodb.variable = "bilgileri"
            mongodb.doctor_name = voice.replace(" bilgileri", "").title()
            var.set(mongodb.find_by_name())
            window.update()
            speak(mongodb.find_by_name())

        elif "alanı" in voice:
            mongodb.variable = "alani"
            mongodb.doctor_name = voice.replace(" alanı", "").title()
            var.set(mongodb.find_by_name())
            window.update()
            speak(mongodb.find_by_name())

        elif "nerede" in voice:  # mongodb
            mongodb.variable = "yeri"
            mongodb.doctor_name = voice.replace(" nerede", "").title()
            var.set(mongodb.find_by_name())
            window.update()
            speak(mongodb.find_by_name())

        elif "numarası" in voice:
            mongodb.variable = "no"
            mongodb.doctor_name = voice.replace(" numarası", "").title()
            var.set(mongodb.find_by_name())
            window.update()
            speak(mongodb.find_by_name())

        elif "benimde iyi" in voice:
            speak("Bunu duyduğuma sevindim!")

        elif voice in commands.hello:
            c = random.randint(0, len(commands.hello_answer) - 1)
            var.set(commands.hello_answer[c])
            window.update()
            speak(commands.hello_answer[c])

        elif "iyi" in voice:
            var.set("Bunu duyduğuma sevindim!")
            window.update()
            speak("Bunu duyduğuma sevindim!")

        elif "kötü" in voice:
            var.set("Bunu duyduğuma üzüldüm yapabileceğim bişey varmı?!")
            window.update()
            speak("Bunu duyduğuma üzüldüm yapabileceğim bişey varmı?")

        elif "canın sağolsun" in voice:
            var.set("Beni çok üzüyorsun")
            window.update()
            speak("Beni çok üzüyorsun")

        elif "nerelisin" in voice:
            var.set("İnternetliyim peki sen nerelisin?")
            window.update()
            speak("İnternetliyim peki sen nerelisin?")

        elif 'nedir' in voice:

            try:
                wikipedia.set_lang("tr")
                speak("vikipedyada aranıyor")
                donut = voice.replace("nedir", "")
                results = wikipedia.summary(donut, sentences=2)
                metin = results
                metinlen = len(metin)
                list1 = list(metin)
                list1[int(metinlen / 3)] += "-\n"
                list1[int(metinlen / 1.5)] += "-\n"
                metin = "".join(list1)
                speak("vikipedyaya göre")
                var2.set(metin)
                window.update()
                speak(results)
            except Exception as e:
                print(e)
                var.set('Üzgünüm herhangi bir sonuç bulunamadı')
                window.update()
                speak('Üzgünüm herhangi bir sonuç bulunamadı')

        elif "randevum vardı" in voice:
            var.set("randevu sıra numaranızı öğrenebilir miyim?")
            window.update()
            speak("randevu sıra numaranızı öğrenebilir miyim?")
            mongodb.appointment_variable = "randTarihi"
            mongodb.appointment_number = int(gt_ekle())
            deger = str(mongodb.appointment_query())
            if deger == mongodb.patient_not_found:
                speak(mongodb.appointment_query())
            else:
                randyili = int(deger[0:4])
                randayi = int(deger[5:7])
                randgunu = int(deger[8:10])
                randsaati = int(deger[11:13])
                randakika = int(deger[14:16])
                if randyili == year:
                    if randayi == month:
                        if randgunu == day:
                            if randsaati - 12 <= hour <= randsaati + 12:
                                randsaatyaz = ("Randevu Saati: " + str(randsaati) + ":" + str(randakika) + "\n")
                                mongodb.appointment_variable = "ranSiraNo"
                                randsirayaz = ("Sıra No: " + str(mongodb.appointment_query()) + "\n")
                                mongodb.appointment_variable = "isim"
                                randhastaadiyaz = ("Hasta Adı: " + str(mongodb.appointment_query()) + "\n")
                                mongodb.appointment_variable = "tcno"
                                randhastatc = ("Hasta TC: " + str(mongodb.appointment_query()) + "\n")
                                mongodb.appointment_variable = "randBolumu"
                                randevubolum = ("Bölümü: " + str(mongodb.appointment_query()) + "\n")
                                mongodb.appointment_variable = "randDoktoru"
                                randevudoktor = ("Doktor: " + str(mongodb.appointment_query()))
                                mongodb.appointment_variable = "telefon"
                                randbilgi = randsaatyaz + randsirayaz + randhastaadiyaz + \
                                            randhastatc + randevubolum + randevudoktor

                                message = client_twilio.messages.create(
                                    messaging_service_sid='MG0cf578544b35c6a8a281dd451b891a83',
                                    body=randbilgi,
                                    to=str(mongodb.appointment_query())
                                )

                                speak("randevunuz onaylanmıştır, randevu bilgileriniz aşağıdaki gibidir")
                                var2.set(randbilgi)
                                var1.set("Randevu Bilgileri")
                                window.update()
                                time.sleep(7)
                            else:
                                speak("randevunuz saatini kaçırdınız ?")  # diğerleri de bunun gibi olmalı
                                var.set("randevunuz saatini kaçırdınız ?")
                                window.update()
                        else:
                            speak("randevu günü doğru değil")
                            var.set("randevu günü doğru değil")
                            window.update()
                    else:
                        speak("böyle bir randevu bulunamadı ay")
                        var.set("böyle bir randevu bulunamadı ay")
                        window.update()
                else:
                    speak("böyle bir randevu bulunamadı")
                    var.set("böyle bir randevu bulunamadı")
                    window.update()

        elif voice in commands.exit:  # çıkış
            c = random.randint(0, len(commands.answer_exit) - 1)
            var.set(commands.answer_exit[c])
            window.update()
            speak(commands.answer_exit[c])
            # time.sleep(1)
            exit()  # çıkış

        else:  # eğer dediklerimiz tanmlı değilse yapacağı işlem
            var.set("bu cümlenin karşılığı yok")
            window.update()
            speak("bu cümlenin karşılığı yok")
            mongodb.variable = voice
            mongodb.add_incomprehensible_value()


def update(ind):
    frame = frames[ind % 100]
    ind += 1
    label.configure(image=frame)
    window.after(100, update, ind)


def gt_ekle():
    rObject = sr.Recognizer()

    with sr.Microphone() as source:
        mixer.music.load(mic_sound)
        mixer.music.play()
        print("Konuşun...")

        audio = rObject.listen(source, phrase_time_limit=5)
    print("Durdu.")  # limit 5 saniye

    try:

        text = rObject.recognize_google(audio, language='tr-TR')
        speak("şunu söylediniz, doğru mu: ")
        speak(text)
        print(text)
        rObject = sr.Recognizer()

        with sr.Microphone() as source:
            mixer.music.load(mic_sound)
            mixer.music.play()
            print("Konuşun...")

            audio = rObject.listen(source, phrase_time_limit=5)
        print("Durdu.")  # limit 5 saniye
        cvp = rObject.recognize_google(audio, language='tr-TR')
        print(cvp)
        if cvp == "Evet":
            return text
        else:
            speak("işlem sonlandırıldı")
            yeniden()
    except Exception as e:
        print(e)
        speak("Anlaşılamadı, işlem sonlandırıldı")
        yeniden()
        return ''


def speak(string):  # Ses dosyalarını oynatırken hata olmaması için speak fonksiyonunu kullanıyoruz
    tts = gTTS(string, lang="tr")  # Türkçe konuşmasını ayarlıyoruz
    tts.save(file)  # Dosyayı kaydediyoruz.
    mixer.music.load(file)
    mixer.music.play()  # Dosyayı oynatıyoruz
    audio = MP3(file)
    duration = audio.info.length
    time.sleep(duration)
    mixer.music.unload()
    os.remove(file)  # Dosyayı siliyoruz.


def yeniden():
    while 1:
        mixer.music.load(mic_sound)
        mixer.music.play()
        speak("gerçekleştirmek istediğiniz işlemi tekrar söyleyin")
        voice = record().lower()  # lower ekledim ki bütün harfleri küçültsün
        print(voice)
        start()


label4 = Label(window, bg='#FFFFFF')
label4.config(font=("Courier", 20))
label4.pack()

label2 = Label(window, textvariable=var1, bg='#FAB60C')
label2.config(font=("Courier", 20))
var1.set('Mira İle Konuşmak\nİçin Butona Tıkla')
label2.pack()

label1 = Label(window, textvariable=var, bg='#ADD8E6')
label1.config(font=("Courier", 18))
var.set('Merhaba')
label1.pack()

label3 = Label(window, textvariable=var2, bg='#FFFFFF')
label3.config(font=("Courier", 12))
label3.pack()

frames = [PhotoImage(file='src/img/Assistant.gif', format='gif -index %i' % i) for i in range(100)]
window.title('MIRA SESLI ASISTAN')
window.iconbitmap(r"src\img\doktor.ico")
window.attributes('-fullscreen', True)
label = Label(window, width=600, height=500)
label.pack()
window.after(0, update, 0)

btn0 = Button(text='Neler Yapabilirim', width=20, command=features, bg='#5C85FB')
btn0.config(font=("Courier", 12))
btn0.pack()
btn1 = Button(text='Konuş', width=20, command=start, bg='#5C85FB')
btn1.config(font=("Courier", 12))
btn1.pack()
btn2 = Button(text='Çıkış', width=20, command=exit, bg='#5C85FB')
btn2.config(font=("Courier", 12))
btn2.pack()
window.tk_setPalette("white")
window.geometry("1680x1050")
window.mainloop()

#
# def yeniekran():
#     label4 = Label(window, textvariable=var, bg='#ADD8E6')
#     label4.config(font=("Courier", 18))
#     var.set('Merhaba')
#     label4.pack()
#
#     labell = Label(window, width=500, height=500)
#     labell.pack()
#     window.after(0, update, 0)
#
#     window.tk_setPalette("white")
#     window.geometry("500x500")
#     window.mainloop()
#
#
# yeniekran()
