import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import time
from datetime import datetime, timedelta
import json
import os
import winsound

class KlavyeHizTesti:
    def __init__(self):
        self.pencere = tk.Tk()
        self.pencere.title("Klavye Hız Testi")
        self.pencere.geometry("1000x700")
        
        # Tema ayarları
        self.temalar = {
            "Açık": {
                "ana_bg": "#F5F6FA",
                "ana_fg": "#2D3436",
                "kontrol_bg": "#FFFFFF",
                "kontrol_fg": "#2D3436",
                "metin_bg": "#FFFFFF",
                "metin_fg": "#2D3436",
                "giris_bg": "#F5F6FA",
                "giris_fg": "#2D3436",
                "dogru_renk": "#00B894",
                "yanlis_renk": "#FF7675",
                "vurgu_renk": "#6C5CE7",
                "buton_bg": "#6C5CE7",
                "buton_fg": "#FFFFFF"
            },
            "Koyu": {
                "ana_bg": "#2D3436",
                "ana_fg": "#DFE6E9",
                "kontrol_bg": "#353B48",
                "kontrol_fg": "#DFE6E9",
                "metin_bg": "#353B48",
                "metin_fg": "#DFE6E9",
                "giris_bg": "#2D3436",
                "giris_fg": "#DFE6E9",
                "dogru_renk": "#00B894",
                "yanlis_renk": "#FF7675",
                "vurgu_renk": "#6C5CE7",
                "buton_bg": "#6C5CE7",
                "buton_fg": "#FFFFFF"
            }
        }
        self.aktif_tema = "Koyu"
        
        # Kelime listeleri
        self.kelime_listeleri = {
            "Varsayılan": "kelimeler.txt"
        }
        self.aktif_liste = "Varsayılan"
        
        # Kelime listesini yükle
        self.kelimeler = self.kelime_listesi_yukle(self.kelime_listeleri[self.aktif_liste])
        
        # Değişkenler
        self.kalan_sure = 0
        self.test_aktif = False
        self.dogru_kelimeler = 0
        self.yanlis_kelimeler = 0
        self.baslangic_zamani = None
        self.mevcut_kelime_index = 0
        self.kelime_listesi = []
        self.son_kelime_label = None
        
        # Yüksek skorları yükle
        self.yuksek_skorlar = self.yuksek_skorlari_yukle()
        
        # Ses dosyaları için kontrol
        self.ses_acik = True
        
        # Menü çubuğu
        self.menu_olustur()
        
        # Ana çerçeve
        self.ana_frame = ttk.Frame(self.pencere, style="Ana.TFrame")
        self.ana_frame.pack(padx=30, pady=30, fill=tk.BOTH, expand=True)
        
        # Başlık
        self.baslik_frame = ttk.Frame(self.ana_frame, style="Baslik.TFrame")
        self.baslik_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.baslik_label = ttk.Label(
            self.baslik_frame,
            text="⌨️ Profesyonel Klavye Hız Testi",
            style="Baslik.TLabel"
        )
        self.baslik_label.pack(pady=10)
        
        # Kontrol çerçevesi
        self.kontrol_frame = ttk.Frame(self.ana_frame, style="Kontrol.TFrame")
        self.kontrol_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Süre seçimi için özel çerçeve
        self.sure_frame = ttk.Frame(self.kontrol_frame, style="Kontrol.TFrame")
        self.sure_frame.pack(side=tk.LEFT, padx=20)
        
        self.sure_label = ttk.Label(
            self.sure_frame,
            text="Test Süresi:",
            style="Etiket.TLabel"
        )
        self.sure_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.sure_secimi = ttk.Combobox(
            self.sure_frame,
            values=["1 Dakika", "3 Dakika", "5 Dakika", "Pratik"],
            state="readonly",
            width=10,
            style="Combo.TCombobox"
        )
        self.sure_secimi.set("1 Dakika")
        self.sure_secimi.pack(side=tk.LEFT)
        
        # Başlat butonu için özel çerçeve
        self.buton_frame = ttk.Frame(self.kontrol_frame, style="Kontrol.TFrame")
        self.buton_frame.pack(side=tk.LEFT, padx=20)
        
        self.basla_buton = ttk.Button(
            self.buton_frame,
            text="Testi Başlat",
            command=self.testi_baslat,
            style="Basla.TButton"
        )
        self.basla_buton.pack()
        
        # Kalan süre için özel çerçeve
        self.sure_gosterge_frame = ttk.Frame(self.kontrol_frame, style="Kontrol.TFrame")
        self.sure_gosterge_frame.pack(side=tk.RIGHT, padx=20)
        
        self.sure_label = ttk.Label(
            self.sure_gosterge_frame,
            text="⏱️ Kalan Süre: 0:00",
            style="Sure.TLabel"
        )
        self.sure_label.pack()
        
        # Hedef metin çerçevesi
        self.metin_frame = ttk.Frame(self.ana_frame, style="Metin.TFrame")
        self.metin_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Son yazılan kelime için label
        self.son_kelime_frame = ttk.Frame(self.metin_frame, style="Metin.TFrame")
        self.son_kelime_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Mevcut kelime için label
        self.hedef_metin = ttk.Label(
            self.metin_frame,
            text="Test başlatıldığında burada yazmanız gereken kelime görünecek...",
            style="HedefMetin.TLabel"
        )
        self.hedef_metin.pack(pady=10)
        
        # Sonraki kelimeler için label
        self.sonraki_kelimeler = ttk.Label(
            self.metin_frame,
            text="",
            style="SonrakiKelimeler.TLabel"
        )
        self.sonraki_kelimeler.pack(pady=5)
        
        # Giriş alanı çerçevesi
        self.giris_frame = ttk.Frame(self.ana_frame, style="Giris.TFrame")
        self.giris_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Giriş alanı arka plan çerçevesi
        self.giris_bg_frame = tk.Frame(
            self.giris_frame,
            background=self.temalar[self.aktif_tema]["vurgu_renk"],
            padx=2,
            pady=2
        )
        self.giris_bg_frame.pack(pady=10)
        
        self.giris_alani = tk.Entry(
            self.giris_bg_frame,
            width=50,
            font=("Cascadia Code", 20, "bold"),  # Yazı boyutunu ve kalınlığını artırdık
            state="disabled",
            bg=self.temalar[self.aktif_tema]["giris_bg"],
            fg=self.temalar[self.aktif_tema]["vurgu_renk"],  # Yazı rengini vurgu rengi yaptık
            insertbackground=self.temalar[self.aktif_tema]["vurgu_renk"],  # İmleç rengini değiştirdik
            insertwidth=3,  # İmleç kalınlığını artırdık
            justify="center"  # Yazıyı ortaya hizaladık
        )
        self.giris_alani.pack(padx=2, pady=2)
        self.giris_alani.bind("<KeyRelease>", self.kelime_kontrol)
        
        # Sonuç çerçevesi
        self.sonuc_frame = ttk.Frame(self.ana_frame, style="Sonuc.TFrame")
        self.sonuc_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # İstatistik etiketleri
        self.dogru_label = ttk.Label(
            self.sonuc_frame,
            text="Doğru: 0",
            style="Istatistik.TLabel"
        )
        self.dogru_label.pack(side=tk.LEFT, padx=20)
        
        self.yanlis_label = ttk.Label(
            self.sonuc_frame,
            text="Yanlış: 0",
            style="Istatistik.TLabel"
        )
        self.yanlis_label.pack(side=tk.LEFT, padx=20)
        
        self.dpm_label = ttk.Label(
            self.sonuc_frame,
            text="DPM: 0",
            style="Istatistik.TLabel"
        )
        self.dpm_label.pack(side=tk.LEFT, padx=20)
        
        # Stil ayarları
        self.stil_ayarla()
        
    def stil_ayarla(self):
        style = ttk.Style()
        tema = self.temalar[self.aktif_tema]
        
        # Ana çerçeve stilleri
        style.configure("Ana.TFrame",
            background=tema["ana_bg"],
            relief="flat"
        )
        
        style.configure("Baslik.TFrame",
            background=tema["kontrol_bg"],
            relief="flat"
        )
        
        style.configure("Kontrol.TFrame",
            background=tema["kontrol_bg"],
            relief="flat"
        )
        
        style.configure("Metin.TFrame",
            background=tema["metin_bg"],
            relief="flat"
        )
        
        # Başlık stili
        style.configure("Baslik.TLabel",
            font=("Segoe UI", 28, "bold"),
            foreground=tema["vurgu_renk"],
            background=tema["kontrol_bg"],
            padding=(20, 10)
        )
        
        # Etiket stilleri
        style.configure("Etiket.TLabel",
            font=("Segoe UI", 12),
            foreground=tema["kontrol_fg"],
            background=tema["kontrol_bg"]
        )
        
        style.configure("Sure.TLabel",
            font=("Segoe UI", 14, "bold"),
            foreground=tema["vurgu_renk"],
            background=tema["kontrol_bg"]
        )
        
        # Hedef metin stili
        style.configure("HedefMetin.TLabel",
            font=("Cascadia Code", 26, "bold"),
            foreground=tema["metin_fg"],
            background=tema["metin_bg"],
            padding=(20, 15)
        )
        
        # Sonraki kelimeler stili
        style.configure("SonrakiKelimeler.TLabel",
            font=("Cascadia Code", 14),
            foreground=tema["kontrol_fg"],
            background=tema["metin_bg"],
            padding=(10, 5)
        )
        
        # Doğru/Yanlış stilleri
        style.configure("Dogru.TLabel",
            font=("Cascadia Code", 16),
            foreground=tema["dogru_renk"],
            background=tema["metin_bg"]
        )
        
        style.configure("Yanlis.TLabel",
            font=("Cascadia Code", 16),
            foreground=tema["yanlis_renk"],
            background=tema["metin_bg"]
        )
        
        # Buton stili
        style.configure("Basla.TButton",
            font=("Segoe UI", 12, "bold"),
            padding=(20, 10),
            background=tema["buton_bg"],
            foreground=tema["buton_fg"]
        )
        
        # Entry stili
        style.configure("Giris.TFrame",
            background=tema["giris_bg"],
            relief="flat"
        )
        
        style.configure("Istatistik.TLabel",
            font=("Segoe UI", 12, "bold"),
            foreground=tema["kontrol_fg"],
            background=tema["kontrol_bg"],
            padding=(10, 5)
        )
    
    def testi_baslat(self):
        if self.test_aktif:
            return
            
        # Süreyi ayarla
        sure_secenekleri = {
            "1 Dakika": 60,
            "3 Dakika": 180,
            "5 Dakika": 300,
            "Pratik": float("inf")
        }
        self.kalan_sure = sure_secenekleri[self.sure_secimi.get()]
        self.baslangic_zamani = datetime.now()
        
        # Test değişkenlerini sıfırla
        self.test_aktif = True
        self.dogru_kelimeler = 0
        self.yanlis_kelimeler = 0
        
        # Kelime listesini hazırla
        self.kelime_listesi = random.sample(self.kelimeler, 50)
        self.mevcut_kelime_index = 0
        
        # İlk kelimeyi göster
        self.kelime_goster()
        
        # Giriş alanını aktifleştir
        self.giris_alani.config(state="normal")
        self.giris_alani.delete(0, tk.END)
        self.giris_alani.focus()
        
        # Zamanlayıcıyı başlat
        self.sure_guncelle()
        
    def sure_guncelle(self):
        if not self.test_aktif:
            return
        
        if self.sure_secimi.get() == "Pratik":
            self.sure_label.config(text="⏱️ Pratik Modu")
            self.pencere.after(1000, self.sure_guncelle)
            return
            
        gecen_sure = int((datetime.now() - self.baslangic_zamani).total_seconds())
        kalan_sure = max(0, int(self.kalan_sure - gecen_sure))
        
        if kalan_sure <= 0:
            self.testi_bitir()
            return
            
        dakika = kalan_sure // 60
        saniye = kalan_sure % 60
        self.sure_label.config(text=f"⏱️ Kalan Süre: {dakika}:{saniye:02d}")
        
        self.pencere.after(1000, self.sure_guncelle)
        
    def kelime_goster(self):
        if self.mevcut_kelime_index < len(self.kelime_listesi):
            # Mevcut kelimeyi göster
            self.hedef_metin.config(
                text=self.kelime_listesi[self.mevcut_kelime_index]
            )
            
            # Sonraki 5 kelimeyi göster
            sonraki_kelimeler = self.kelime_listesi[self.mevcut_kelime_index + 1:self.mevcut_kelime_index + 6]
            self.sonraki_kelimeler.config(
                text="Sonraki: " + " ".join(sonraki_kelimeler)
            )
        else:
            # Yeni kelimeler ekle
            yeni_kelimeler = random.sample(self.kelimeler, 30)
            self.kelime_listesi.extend(yeni_kelimeler)
            self.kelime_goster()
    
    def kelime_efekti_goster(self, kelime, dogru_mu):
        # Önceki efekti temizle
        if self.son_kelime_label:
            self.son_kelime_label.destroy()
        
        # Yeni efekti göster
        self.son_kelime_label = ttk.Label(
            self.son_kelime_frame,
            text=f"{'✓' if dogru_mu else '✗'} {kelime}",
            style="Dogru.TLabel" if dogru_mu else "Yanlis.TLabel"
        )
        self.son_kelime_label.pack(pady=5)
        
        # Efekti 1 saniye sonra kaldır
        self.pencere.after(1000, lambda: self.son_kelime_label.destroy() if self.son_kelime_label else None)
        
    def kelime_kontrol(self, event):
        if not self.test_aktif:
            return
            
        yazilan = self.giris_alani.get().strip()
        mevcut_kelime = self.kelime_listesi[self.mevcut_kelime_index]
        
        # Eğer yazılan kelime, mevcut kelime ile aynı uzunlukta ve eşitse
        if yazilan == mevcut_kelime:
            self.dogru_kelimeler += 1
            self.ses_cal("dogru")
            
            # Efekti göster
            self.kelime_efekti_goster(mevcut_kelime, True)
            
            # Sonraki kelimeye geç
            self.mevcut_kelime_index += 1
            self.kelime_goster()
            
            # Giriş alanını temizle
            self.giris_alani.delete(0, tk.END)
            
            # Sonuçları güncelle
            gecen_dakika = (datetime.now() - self.baslangic_zamani).total_seconds() / 60
            dpm = int(self.dogru_kelimeler / gecen_dakika) if gecen_dakika > 0 else 0
            
            self.dogru_label.config(text=f"✅ Doğru: {self.dogru_kelimeler}")
            self.yanlis_label.config(text=f"❌ Yanlış: {self.yanlis_kelimeler}")
            self.dpm_label.config(text=f"🚀 DPM: {dpm}")
        
        # Eğer yazılan kelime yanlışsa ve boşluk tuşuna basıldıysa
        elif event.keysym == "space":
            self.yanlis_kelimeler += 1
            self.ses_cal("yanlis")
            
            # Efekti göster
            self.kelime_efekti_goster(mevcut_kelime, False)
            
            # Sonraki kelimeye geç
            self.mevcut_kelime_index += 1
            self.kelime_goster()
            
            # Giriş alanını temizle
            self.giris_alani.delete(0, tk.END)
            
            # Sonuçları güncelle
            self.yanlis_label.config(text=f"❌ Yanlış: {self.yanlis_kelimeler}")
        
    def testi_bitir(self):
        self.test_aktif = False
        self.giris_alani.config(state="disabled")
        
        # Final sonuçlarını hesapla
        toplam_sure = (datetime.now() - self.baslangic_zamani).total_seconds() / 60
        dpm = int(self.dogru_kelimeler / toplam_sure)
        dogruluk = (self.dogru_kelimeler / (self.dogru_kelimeler + self.yanlis_kelimeler) * 100)
        
        # Ses efekti
        self.ses_cal("bitis")
        
        # Yüksek skor kontrolü ve kayıt
        skor = {
            "dpm": dpm,
            "dogru": self.dogru_kelimeler,
            "yanlis": self.yanlis_kelimeler,
            "dogruluk": dogruluk
        }
        
        if not self.yuksek_skorlar or dpm > self.yuksek_skorlar[-1]["dpm"]:
            self.yuksek_skor_kaydet(skor)
            messagebox.showinfo("Tebrikler!", "🎉 Yeni bir yüksek skor elde ettiniz!")
        
        # Sonuçları göster
        messagebox.showinfo(
            "Test Sonuçları",
            f"🎯 Test bitti!\n\n"
            f"✅ Doğru Kelime: {self.dogru_kelimeler}\n"
            f"❌ Yanlış Kelime: {self.yanlis_kelimeler}\n"
            f"🚀 Dakika Başına Kelime (DPM): {dpm}\n"
            f"📊 Doğruluk Oranı: {dogruluk:.1f}%"
        )
        
    def baslat(self):
        self.pencere.mainloop()

    def menu_olustur(self):
        menubar = tk.Menu(self.pencere)
        self.pencere.config(menu=menubar)
        
        # Dosya menüsü
        dosya_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Dosya", menu=dosya_menu)
        dosya_menu.add_command(label="Kelime Listesi Ekle", command=self.kelime_listesi_ekle)
        dosya_menu.add_separator()
        
        # Kelime listeleri alt menüsü
        self.liste_menu = tk.Menu(dosya_menu, tearoff=0)
        dosya_menu.add_cascade(label="Kelime Listesi Seç", menu=self.liste_menu)
        self.kelime_listelerini_guncelle()
        
        # Ayarlar menüsü
        ayarlar_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayarlar", menu=ayarlar_menu)
        
        # Tema alt menüsü
        tema_menu = tk.Menu(ayarlar_menu, tearoff=0)
        ayarlar_menu.add_cascade(label="Tema", menu=tema_menu)
        for tema in self.temalar:
            tema_menu.add_command(label=tema, command=lambda t=tema: self.tema_degistir(t))
        
        ayarlar_menu.add_separator()
        ayarlar_menu.add_checkbutton(label="Ses Efektleri", 
                                   command=self.ses_degistir, 
                                   variable=tk.BooleanVar(value=True))
        
        # Test modu menüsü
        mod_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Mod", menu=mod_menu)
        mod_menu.add_command(label="Zamanlı Test", command=lambda: self.mod_degistir("zamanli"))
        mod_menu.add_command(label="Pratik Modu", command=lambda: self.mod_degistir("pratik"))
        
        # Yüksek skorlar menüsü
        menubar.add_command(label="Yüksek Skorlar", command=self.yuksek_skorlari_goster)
    
    def kelime_listesi_yukle(self, dosya_adi):
        try:
            with open(dosya_adi, "r", encoding="utf-8") as f:
                return f.read().split()
        except FileNotFoundError:
            messagebox.showerror("Hata", f"{dosya_adi} dosyası bulunamadı!")
            return []
    
    def kelime_listesi_ekle(self):
        dosya = filedialog.askopenfilename(
            title="Kelime Listesi Seç",
            filetypes=[("Metin Dosyaları", "*.txt")]
        )
        if dosya:
            liste_adi = os.path.splitext(os.path.basename(dosya))[0]
            self.kelime_listeleri[liste_adi] = dosya
            self.kelime_listelerini_guncelle()
            messagebox.showinfo("Başarılı", f"{liste_adi} kelime listesi eklendi!")
    
    def kelime_listelerini_guncelle(self):
        # Menüyü temizle
        self.liste_menu.delete(0, tk.END)
        
        # Listeleri ekle
        for liste in self.kelime_listeleri:
            self.liste_menu.add_command(
                label=liste,
                command=lambda l=liste: self.kelime_listesi_sec(l)
            )
    
    def kelime_listesi_sec(self, liste_adi):
        self.aktif_liste = liste_adi
        self.kelimeler = self.kelime_listesi_yukle(self.kelime_listeleri[liste_adi])
        messagebox.showinfo("Bilgi", f"{liste_adi} listesi seçildi!")
    
    def tema_degistir(self, tema_adi):
        self.aktif_tema = tema_adi
        tema = self.temalar[tema_adi]
        
        # Pencere arka planı
        self.pencere.configure(bg=tema["ana_bg"])
        
        # Giriş alanı güncellemesi
        self.giris_bg_frame.configure(background=tema["vurgu_renk"])
        self.giris_alani.configure(
            bg=tema["giris_bg"],
            fg=tema["vurgu_renk"],
            insertbackground=tema["vurgu_renk"]
        )
        
        # Stilleri güncelle
        style = ttk.Style()
        
        style.configure("Ana.TFrame", background=tema["ana_bg"])
        style.configure("Kontrol.TFrame", background=tema["kontrol_bg"])
        style.configure("Metin.TFrame", background=tema["metin_bg"])
        style.configure("Giris.TFrame", background=tema["giris_bg"])
        style.configure("Sonuc.TFrame", background=tema["kontrol_bg"])
        
        style.configure("Baslik.TLabel",
            font=("Segoe UI", 28, "bold"),
            foreground=tema["vurgu_renk"],
            background=tema["kontrol_bg"],
            padding=(20, 10)
        )
        
        style.configure("Etiket.TLabel",
            foreground=tema["kontrol_fg"],
            background=tema["kontrol_bg"]
        )
        
        style.configure("HedefMetin.TLabel",
            foreground=tema["metin_fg"],
            background=tema["metin_bg"]
        )
        
        style.configure("SonrakiKelimeler.TLabel",
            foreground=tema["kontrol_fg"],
            background=tema["metin_bg"]
        )
        
        style.configure("Dogru.TLabel",
            foreground=tema["dogru_renk"],
            background=tema["metin_bg"]
        )
        
        style.configure("Yanlis.TLabel",
            foreground=tema["yanlis_renk"],
            background=tema["metin_bg"]
        )
        
        style.configure("Istatistik.TLabel",
            foreground=tema["kontrol_fg"],
            background=tema["kontrol_bg"]
        )
    
    def mod_degistir(self, mod):
        if mod == "pratik":
            self.sure_secimi.set("Pratik")
            self.sure_secimi["state"] = "disabled"
            self.kalan_sure = float("inf")  # Sonsuz süre
        else:
            self.sure_secimi["state"] = "readonly"
            self.sure_secimi.set("1 Dakika")
        
        messagebox.showinfo("Mod Değişti", 
            "Pratik moduna geçildi. Süre sınırı olmadan pratik yapabilirsiniz." if mod == "pratik" 
            else "Zamanlı test moduna geçildi.")
    
    def ses_degistir(self):
        self.ses_acik = not self.ses_acik
    
    def ses_cal(self, tur):
        if not self.ses_acik:
            return
            
        if tur == "dogru":
            winsound.Beep(1000, 50)  # 1000 Hz, 50 ms
        elif tur == "yanlis":
            winsound.Beep(500, 100)  # 500 Hz, 100 ms
        elif tur == "bitis":
            winsound.Beep(800, 200)  # 800 Hz, 200 ms
    
    def yuksek_skorlari_yukle(self):
        try:
            with open("yuksek_skorlar.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def yuksek_skor_kaydet(self, skor):
        yeni_skor = {
            "tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "dpm": skor["dpm"],
            "dogru": skor["dogru"],
            "yanlis": skor["yanlis"],
            "dogruluk": skor["dogruluk"]
        }
        
        self.yuksek_skorlar.append(yeni_skor)
        self.yuksek_skorlar.sort(key=lambda x: x["dpm"], reverse=True)
        self.yuksek_skorlar = self.yuksek_skorlar[:5]  # En iyi 5 skoru tut
        
        with open("yuksek_skorlar.json", "w", encoding="utf-8") as f:
            json.dump(self.yuksek_skorlar, f, indent=2)
    
    def yuksek_skorlari_goster(self):
        if not self.yuksek_skorlar:
            messagebox.showinfo("Yüksek Skorlar", "Henüz yüksek skor kaydedilmemiş!")
            return
        
        mesaj = "🏆 YÜKSEK SKORLAR 🏆\n\n"
        for i, skor in enumerate(self.yuksek_skorlar, 1):
            mesaj += f"{i}. Tarih: {skor['tarih']}\n"
            mesaj += f"   DPM: {skor['dpm']}\n"
            mesaj += f"   Doğruluk: {skor['dogruluk']:.1f}%\n"
            mesaj += f"   Doğru/Yanlış: {skor['dogru']}/{skor['yanlis']}\n\n"
        
        messagebox.showinfo("Yüksek Skorlar", mesaj)

if __name__ == "__main__":
    uygulama = KlavyeHizTesti()
    uygulama.baslat() 