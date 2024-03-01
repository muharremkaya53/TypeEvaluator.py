import pynput
import time
import tkinter as tk
import sys
import numpy as np
from sklearn.linear_model import LinearRegression

sys.path.append("path/to/Pillow")  # exeye çeviriken resim okumada sıkıntı çektiği için yolunu koydum.


# Keylogger sınıfını tanımlar.
class Keylogger:
    def __init__(self):
        # Kullanıcının yazdığı tuş sayısını sıfırlar.
        self.key_count = 0
        self.spacekey_count = 0
        self.backspacekey_count = 0
        self.start_time = time.time()
        self.time_key = 0
        self.freeze_time = 0
        self.period_count = 0
        self.key_string = None
        self.comma_count = 0
        self.enter_count = 0
        self.caps_lock_count = 0
        self.string_count = 0
        self.ten_multip = 0
        self.key_count_ten = 0
        self.key_count_tweny = 0
        self.key_count_thirt = 0
        self.period_after = 0
        self.press_in_time = 0
        self.sentence_time = 0
        self.sum_sentence_time = 0
        self.direction_key_count = 0
        self.string_net_count = 0
        self.key_count_ten_res = 0
        self.key_count_eight = 0
        self.key_count_nineteen = 0
        self.key_count_twenynine = 0
        self.space_after = 0
        self.sum_words_time = 0
        self.words_time = 0

    def start(self):
        # Kullanıcının yazdığı tuşları tespit eden bir keylogger başlatır.
        with pynput.keyboard.Listener(on_press=self.on_press) as listener:
            try:
                listener.join()
            except Exception as e:
                print(e)

    def on_press(self, key):

        # Kullanıcının yazdığı tuşları tespit eder ve tuş sayısını artırır.
        self.key_count += 1
        self.key_string = str(key)  # yapılan tuşlamaları 'a' biçimine dönüştürür

        self.press_in_time = time.time()

        if self.space_after > 0 and len(self.key_string) == 3:
            self.words_time = self.press_in_time - self.space_after
            self.space_after = 0
            self.sum_words_time += self.words_time

        if self.period_after > 0 and len(self.key_string) == 3:
            self.sentence_time = self.press_in_time - self.period_after
            self.period_after = 0
            self.sum_sentence_time += self.sentence_time

        if self.key_count == 1:  # başlama zamanını ayarlar
            self.freeze_time = time.time()

        self.ten_multip = time.time() - self.freeze_time  # 10'un katlarındaki hız için

        if 0 < self.ten_multip < 9:
            self.key_count_eight = self.key_count / 10

        if 8 < self.ten_multip < 12:  # ilk 10 sndeki hız freeze time hariç
            self.key_count_ten = self.key_count / 10

        if 11 < self.ten_multip < 19:
            self.key_count_nineteen = self.key_count / 20

        if 18 < self.ten_multip < 22:  # ilk 20 sndeki hız
            self.key_count_tweny = self.key_count / 20

        if 21 < self.ten_multip < 29:
            self.key_count_twenynine = self.key_count / 30

        if 28 < self.ten_multip < 32:  # ilk 30 sndeki hız
            self.key_count_thirt = self.key_count / 30

        if len(self.key_string) == 3:  # yapılan karakter tuşlamalarını ayırıyor
            self.string_count += 1

        if key == pynput.keyboard.Key.caps_lock:  # capslock tuşuna basımı sayar
            self.caps_lock_count += 1

        if key == pynput.keyboard.Key.space:  # space tuşuna basımı sayar
            self.spacekey_count += 1
            self.space_after = time.time()

        if key == pynput.keyboard.Key.left:  # sol yön
            self.direction_key_count += 1

        if key == pynput.keyboard.Key.right:  # sağ yön
            self.direction_key_count += 1

        if key == pynput.keyboard.Key.down:  # aşağı yön
            self.direction_key_count += 1

        if key == pynput.keyboard.Key.up:  # yukarı yön
            self.direction_key_count += 1

        if self.key_string == "'.'":  # nokta tuşuna basımı sayar
            self.period_count += 1
            self.period_after = time.time()  # noktaya basılınca zamanı başlatır

        if self.key_string == "','":  # virgül tuşuna basımı sayar
            self.comma_count += 1

        if key == pynput.keyboard.Key.enter:  # enter tuşuna basımı sayar
            self.enter_count += 1

        if key == pynput.keyboard.Key.backspace:  # backspace tuşuna basımı sayar
            self.backspacekey_count += 1

        if key == pynput.keyboard.Key.esc:  # esc tuşuna basılınca countu azaltır
            self.key_count -= 1
            self.stop()
            sys.exit(0)  # işlemi durdurur.

    def stop(self):
        if self.key_count_ten == 0:
            if self.key_count_eight > 0:
                self.key_count_ten = self.key_count_eight

        if self.key_count_tweny == 0:
            if self.key_count_nineteen > 0:
                self.key_count_tweny = self.key_count_nineteen

        if self.key_count_thirt == 0:
            if self.key_count_twenynine > 0:
                self.key_count_thirt = self.key_count_twenynine

        percom_count = self.period_count + self.comma_count
        self.string_count = self.string_count - percom_count
        # Regresyon modeliyle kelime sayısını bulma işlemleri
        # Verilen eşitliklerin girdileri
        X = np.array(
            [[2, 8, 9], [4, 17, 22], [10, 31, 53], [13, 48, 48], [17, 95, 134], [8, 11, 42], [8, 23, 34], [13, 41, 68],
             [11, 16, 82], [12, 6, 78], [20, 11, 135], [20, 14, 156], [28, 8, 130], [10, 71, 88], [21, 11, 98],
             [20, 26, 112], [50, 40, 303], [71, 184, 357], [21, 80, 256], [33, 120, 214], [49, 101, 431],
             [19, 29, 132]])

        # Verilen eşitliklerin çıktıları
        y = np.array([1, 2, 7, 4, 9, 6, 5, 8, 11, 12, 20, 20, 28, 4, 18, 19, 48, 43, 18, 20, 48, 16])

        # Linear Regression modeli oluşturma
        reg = LinearRegression().fit(X, y)

        # Kullanıcıdan girdileri alma
        s = self.spacekey_count  # basılan boşluk
        b = self.backspacekey_count  # basılan silme
        h = self.string_count  # basılan harf

        new_input = np.array([[s, b, h]])
        prediction = reg.predict(new_input)

        # Zaman ölçümünü yaplır.
        # ve tuş sayısını dakika cinsinden hesaplanır.
        freeze_calc_time = self.freeze_time - self.start_time  # ilk tuş basımından başlangıç zamanını çıkarır
        elapsed_time = time.time() - self.freeze_time  # bitiş zamanından, ilk tuşa basım zamanını çıkarırç
        sum_time = freeze_calc_time + elapsed_time  # toplam harcanan zamanı hesaplar
        words_per_minute = self.key_count / elapsed_time * 60  # tuş hızı dakida cinsinden
        words_per_second = self.key_count / elapsed_time  # tuş hızı saniye cinsinden
        self.string_net_count = self.string_count - self.backspacekey_count  # alttaki 3 satır da basılandan yazılanı bulmak için (harf)
        self.string_net_count = self.string_net_count + self.spacekey_count
        self.string_net_count = (self.string_net_count - prediction[0]) + 1
        av_len_word = self.string_net_count / prediction[0]  # kelimedeki ortalama harf sayısı
        if self.ten_multip == 0:
            self.ten_multip = self.key_count_ten_res

        #  Regresyon modeliyle yazılan cümle sayısını bulma
        X = np.array([[7, 8, 91], [8, 39, 14], [15, 28, 140], [11, 46, 60], [5, 47, 60], [24, 43, 303], [7, 24, 47],
                      [8, 32, 89], [12, 57, 131], [23, 75, 21], [10, 48, 9], [16, 75, 220], [21, 112, 177]])

        # Verilen eşitliklerin çıktıları
        y = np.array([2, 6, 4, 7, 5, 8, 7, 6, 9, 23, 10, 10, 18])

        # Linear Regression modeli oluşturma
        reg = LinearRegression().fit(X, y)

        # Kullanıcıdan girdileri alma
        n = self.period_count  # basılan nokta sayısı
        k = prediction[0]  # yazılan yaklaşık kelime sayısı
        s = self.backspacekey_count  # basılan silme tuşu sayısı

        new_input_q = np.array([[n, k, s]])
        prediction_q = reg.predict(new_input_q)

        av_len_sentence = prediction[0] / prediction_q[0]  # ortalama cümle uzunluğu

        if self.sum_words_time > 0:
            asum_words_time = self.sum_words_time / self.spacekey_count
        else:
            asum_words_time = 0

        if self.sum_sentence_time > 0:  # nokta kullanılmayan durumlarda sum sentence none geliyor hata veriyor
            asum_sentence_time = self.sum_sentence_time / self.period_count
        else:
            asum_sentence_time = 0

        # sonuçları txt dosyasına yaz
        with open("Analiz.txt", "w") as file:
            file.write(
                f"---HIZ VERİLERİ---"
                f"\nYapılan tuşlamaların genel hızı: {words_per_minute:.0f} tuş/dakika --- {words_per_second:.2f} tuş/saniye"
                f"\nİlk 10sn deki yaklaşık hız: {self.key_count_ten:.2f} tuş/saniye"
                f"\nİlk 20sn deki yaklaşık hız: {self.key_count_tweny:.2f} tuş/saniye"
                f"\nİlk 30sn deki yaklaşık hız: {self.key_count_thirt:.2f} tuş/saniye"
                f"\n"
                f"\n---ZAMAN VERİLERİ---"
                f"\nYazmaya başlamadan önce beklenen süre: {freeze_calc_time:.2f} saniye"
                f"\nToplam yazma süresi: {elapsed_time:.2f} saniye"
                f"\nToplam geçirilen zaman: {sum_time:.2f} saniye"
                f"\nNoktalardan (cümlelerden) sonra beklenen ortalama süre: {asum_sentence_time:.1f} saniye"
                f"\nBoşluklardan (kelimelerden) sonra beklenen ortalama süre: {asum_words_time:.1f} saniye"
                f"\n"
                f"\n---METİN VERİLERİ---"
                f"\nYazılan yaklaşık harf ve rakamların sayısı: {self.string_net_count:.0f}"
                f"\nYazılan yaklaşık kelime sayısı: {prediction[0]:.0f}"
                f"\nYazılan yaklaşık cümle sayısı: {prediction_q[0]:.0f}"
                f"\nOrtalama kelime uzunluğu: {av_len_word:.1f} harf"
                f"\nOrtalama cümle uzunluğu: {av_len_sentence:.1f} kelime"
                f"\n"
                f"\n---TUŞ VERİLERİ---"
                f"\nBasılan tüm tuşlamaların sayısı: {self.key_count}"
                f"\nBasılan tüm harf ve rakamların sayısı: {self.string_count:}"
                f"\nBasılan Silme tuşu sayısı: {self.backspacekey_count}"
                f"\nBasılan Boşluk tuşu sayısı: {self.spacekey_count}"
                f"\nBasılan Nokta tuşu sayısı: {self.period_count}"
                f"\nBasılan Virgül tuşu sayısı: {self.comma_count}"
                f"\nBasılan Enter tuşu sayısı: {self.enter_count}"
                f"\nBasılan CapsLock tuşu sayısı: {self.caps_lock_count}"
                f"\nBasılan Yön tuşlarının toplam sayısı: {self.direction_key_count}"

            )


def start_keylogger():
    keylogger = Keylogger()
    root.withdraw()  # Tkinter penceresini gizler
    keylogger.start()
    exit()


from tkinter import *
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Type Evaluator Pro")
root.iconbitmap("icon.ico")

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

root.config(bg="black", bd=10, relief="solid")

img = Image.open("image.jpg")
img = img.resize((width // 4, height // 4), Image.LANCZOS)
img = ImageTk.PhotoImage(img)

label = Label(root, image=img)
label.pack(fill=BOTH, expand=True)

start_button = tk.Button(root, text="Start", command=start_keylogger, font=("Roboto", 24, "bold"), relief="raised")
start_button.pack(pady=height // 50, anchor=CENTER)
start_button.lift()


def open_help():
    help_window = tk.Toplevel(root)
    help_window.title("Yardım")
    help_window.iconbitmap("icon.ico")
    help_window.config(bg="black", bd=3, relief="solid")

    label = tk.Label(help_window,
                     text=">Type Evalatuor, metin yazma becerinizi test eden Keylogger Tabanlı bir programdır.\n"
                          ">'Start' butonuna basıldığında çalışmaya başlar ve 'Escape' tuşuna basılınca durur.\n"
                          ">Sonuçları 'Analiz.txt' olarak program klasörüne çıkartır.\n"
                          ">Fare kullanımını mümkün olduğunca minumum seviyede tutunuz...\n"
                     , font=("Roboto", 12), bg="white", fg="black", justify='left')
    label.pack(fill=BOTH, expand=True, padx=10, pady=10, )


help_button = tk.Button(root, text="?", command=open_help, font=("Roboto", 18, "bold",), relief="raised")
help_button.pack(pady=height // 700, anchor=CENTER)

root.mainloop()