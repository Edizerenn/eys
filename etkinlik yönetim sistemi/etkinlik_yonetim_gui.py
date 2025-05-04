import tkinter as tk
from tkinter import messagebox, simpledialog

class Etkinlik:
    def __init__(self, id, isim, tarih, lokasyon, kontenjan):
        self.id = id
        self.isim = isim
        self.tarih = tarih
        self.lokasyon = lokasyon
        self.kontenjan = kontenjan
        self.katilimcilar = []

    def katilimci_ekle(self, katilimci):
        if len(self.katilimcilar) < self.kontenjan:
            self.katilimcilar.append(katilimci)
            return True
        return False

    def bilgi_goster(self):
        return f"{self.id}: {self.isim} - {self.tarih} - {self.lokasyon} ({len(self.katilimcilar)}/{self.kontenjan})"

class Katilimci:
    def __init__(self, id, isim, email):
        self.id = id
        self.isim = isim
        self.email = email
        self.biletler = []

    def etkinlige_katil(self, etkinlik):
        if etkinlik.katilimci_ekle(self):
            bilet = Bilet(f"B-{self.id}-{etkinlik.id}", etkinlik.id, self.id)
            self.biletler.append(bilet)
            return bilet
        return None

    def biletleri_goster(self):
        return [bilet.bilet_bilgisi_goster() for bilet in self.biletler]

class Bilet:
    def __init__(self, bilet_no, etkinlik_id, katilimci_id):
        self.bilet_no = bilet_no
        self.etkinlik_id = etkinlik_id
        self.katilimci_id = katilimci_id

    def bilet_bilgisi_goster(self):
        return f"Bilet No: {self.bilet_no} | Etkinlik ID: {self.etkinlik_id} | Katılımcı ID: {self.katilimci_id}"

etkinlik_listesi = []
katilimci_listesi = {}
aktif_kullanici = None
etkinlik_id_counter = 1
katilimci_id_counter = 1

def etkinlikleri_goster():
    etkinlikler_text.delete("1.0", tk.END)
    for etkinlik in etkinlik_listesi:
        etkinlikler_text.insert(tk.END, etkinlik.bilgi_goster() + "\n")

def kayit_ol():
    global katilimci_id_counter
    isim = simpledialog.askstring("Kayıt", "İsim:")
    email = simpledialog.askstring("Kayıt", "E-posta:")
    if email in katilimci_listesi:
        messagebox.showwarning("Uyarı", "Bu e-posta zaten kayıtlı.")
        return
    yeni_katilimci = Katilimci(katilimci_id_counter, isim, email)
    katilimci_listesi[email] = yeni_katilimci
    katilimci_id_counter += 1
    messagebox.showinfo("Başarılı", "Kayıt tamamlandı.")

def giris_yap():
    global aktif_kullanici
    email = simpledialog.askstring("Giriş", "E-posta:")
    if email in katilimci_listesi:
        aktif_kullanici = katilimci_listesi[email]
        messagebox.showinfo("Hoş Geldiniz", f"{aktif_kullanici.isim}")
    else:
        messagebox.showerror("Hata", "Kullanıcı bulunamadı.")

def etkinlige_katil():
    if not aktif_kullanici:
        messagebox.showwarning("Uyarı", "Önce giriş yapmalısınız.")
        return
    try:
        secilen_id = int(simpledialog.askstring("Katıl", "Etkinlik ID girin:"))
        etkinlik = next((e for e in etkinlik_listesi if e.id == secilen_id), None)
        if etkinlik:
            bilet = aktif_kullanici.etkinlige_katil(etkinlik)
            if bilet:
                messagebox.showinfo("Başarılı", f"Etkinliğe katıldınız!\n{bilet.bilet_bilgisi_goster()}")
                etkinlikleri_goster()
            else:
                messagebox.showwarning("Dolu", "Etkinlik kontenjanı dolu.")
        else:
            messagebox.showerror("Hata", "Etkinlik bulunamadı.")
    except ValueError:
        messagebox.showerror("Hata", "Geçersiz ID")

def biletleri_goster():
    if not aktif_kullanici:
        messagebox.showwarning("Uyarı", "Önce giriş yapmalısınız.")
        return
    biletler = aktif_kullanici.biletleri_goster()
    if biletler:
        messagebox.showinfo("Biletleriniz", "\n".join(biletler))
    else:
        messagebox.showinfo("Biletleriniz", "Henüz biletiniz yok.")

def etkinlik_ekle():
    global etkinlik_id_counter
    isim = simpledialog.askstring("Yeni Etkinlik", "Etkinlik Adı:")
    tarih = simpledialog.askstring("Yeni Etkinlik", "Tarih (YYYY-AA-GG):")
    lokasyon = simpledialog.askstring("Yeni Etkinlik", "Lokasyon:")
    kontenjan = int(simpledialog.askstring("Yeni Etkinlik", "Kontenjan:"))
    yeni_etkinlik = Etkinlik(etkinlik_id_counter, isim, tarih, lokasyon, kontenjan)
    etkinlik_listesi.append(yeni_etkinlik)
    etkinlik_id_counter += 1
    messagebox.showinfo("Başarılı", "Etkinlik oluşturuldu.")
    etkinlikleri_goster()

def etkinlik_sil():
    global etkinlik_listesi
    try:
        silinecek_id = int(simpledialog.askstring("Etkinlik Sil", "Silmek istediğiniz etkinliğin ID’sini girin:"))
        yeni_liste = [e for e in etkinlik_listesi if e.id != silinecek_id]
        if len(yeni_liste) != len(etkinlik_listesi):
            etkinlik_listesi = yeni_liste
            messagebox.showinfo("Başarılı", f"{silinecek_id} ID'li etkinlik silindi.")
            etkinlikleri_goster()
        else:
            messagebox.showwarning("Bulunamadı", "Bu ID'ye sahip bir etkinlik yok.")
    except ValueError:
        messagebox.showerror("Hata", "Geçersiz ID girişi.")

pencere = tk.Tk()
pencere.title("Etkinlik Yönetim Sistemi")

etkinlikler_text = tk.Text(pencere, height=30, width=80)
etkinlikler_text.pack(pady=10)

btn_frame = tk.Frame(pencere)
btn_frame.pack()

tk.Button(btn_frame, text="Etkinlikleri Göster", command=etkinlikleri_goster).grid(row=0, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Kayıt Ol", command=kayit_ol).grid(row=0, column=1, padx=5, pady=5)
tk.Button(btn_frame, text="Giriş Yap", command=giris_yap).grid(row=0, column=2, padx=5, pady=5)
tk.Button(btn_frame, text="Etkinliğe Katıl", command=etkinlige_katil).grid(row=0, column=3, padx=5, pady=5)
tk.Button(btn_frame, text="Biletlerim", command=biletleri_goster).grid(row=0, column=4, padx=5, pady=5)
tk.Button(btn_frame, text="Etkinlik Ekle", command=etkinlik_ekle).grid(row=0, column=5, padx=5, pady=5)
tk.Button(btn_frame, text="Etkinlik Sil", command=etkinlik_sil).grid(row=0, column=6, padx=5, pady=5)

etkinlik_listesi.append(Etkinlik(1, "Meditasyon ve Farkındalık Atölyesi", "2025-06-10", "İstanbul", 30))
etkinlik_listesi.append(Etkinlik(2, "Tiyatro Oyunculuğu Eğitimi", "2025-06-15", "İzmir", 20))
etkinlik_listesi.append(Etkinlik(4, "Doğa Yürüyüşü ve Kamp Deneyimi", "2025-07-10", "Bolu", 50))
etkinlik_listesi.append(Etkinlik(5, "Yaratıcı Yazarlık Atölyesi", "2025-07-20", "Bursa", 15))
etkinlik_listesi.append(Etkinlik(7, "Kahve Tadımı ve Demleme Teknikleri", "2025-08-12", "İstanbul", 25))
etkinlik_listesi.append(Etkinlik(9, "Psikoloji ve İlişki Yönetimi Semineri", "2025-09-05", "Online", 100))
etkinlik_listesi.append(Etkinlik(10, "Sağlıklı Yaşam ve Beslenme Eğitimi", "2025-09-20", "Online", 150))
etkinlik_id_counter = 11

pencere.mainloop()
