from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Union, Optional
import datetime

app = FastAPI(title="Emir Büfe API", version="8.0")

# Güvenlik ve CORS İzinleri
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"],
)

aktif_siparisler = []
garson_cagrilari = []
siparis_id_sayaci = 1

MENU_VERISI = [
    {
        "id": "kategori_kahvalti", "kategoriAdi": "Kahvaltılıklar", "kategoriResmi": "fotolar/bukahvaltı.jpg",
        "urunler": [
            { "id": 601, "ad": "Menemen Çeşitleri", "aciklama": "Taze domates ve biberle, sıcacık", "resim": "fotolar/melemen.jpg", "fiyat": None, "secenekler": [ {"id": "klasik", "ad": "Klasik Menemen", "fiyat": 100}, {"id": "kasarli", "ad": "Kaşarlı Menemen", "fiyat": 130}, {"id": "sucuklu", "ad": "Sucuklu Menemen", "fiyat": 140}, {"id": "kavurmali", "ad": "Kavurmalı Menemen", "fiyat": 160}, {"id": "karisik", "ad": "Karışık Menemen", "fiyat": 180} ] },
            { "id": 602, "ad": "Sahanda Yumurta", "aciklama": "Tereyağında enfes yumurta", "resim": "fotolar/sahandayumurta.webp", "fiyat": None, "secenekler": [ {"id": "klasik", "ad": "Klasik Yumurta", "fiyat": 80}, {"id": "kasarli", "ad": "Kaşarlı Yumurta", "fiyat": 100}, {"id": "sucuklu", "ad": "Sucuklu Yumurta", "fiyat": 120}, {"id": "kavurmali", "ad": "Kavurmalı Yumurta", "fiyat": 140}, {"id": "karisik", "ad": "Karışık Yumurta", "fiyat": 160} ] },
            { "id": 603, "ad": "Kahvaltı Tabağı", "aciklama": "Bol çeşit serpme kahvaltı", "resim": "fotolar/kahvaltılıklar.jpg", "fiyat": 250, "secenekler": None },
            { "id": 604, "ad": "Sadece Sucuk (Porsiyon)", "aciklama": "Özel kasap sucuk tava", "resim": "fotolar/busucuk.jpg", "fiyat": 180, "secenekler": None }
        ]
    },
    {
        "id": "kategori1", "kategoriAdi": "Tost, Sandviç ve Izgara", "kategoriResmi": "fotolar/ızgara.jpg",
        "urunler": [
            { "id": 100, "ad": "Sade Tost", "aciklama": "Bol kaşarlı tost", "resim": "fotolar/kasarli-tost.png", "fiyat": None, "secenekler": [ {"id": "yarim", "ad": "Yarım Ekmek", "fiyat": 90}, {"id": "ucceyrek", "ad": "Üç Çeyrek", "fiyat": 120}, {"id": "tam", "ad": "Tam Ekmek", "fiyat": 150} ] },
            { "id": 101, "ad": "Karışık Tost", "aciklama": "Bol kaşarlı, bol sucuklu tost", "resim": "fotolar/.jpg", "fiyat": None, "secenekler": [ {"id": "yarim", "ad": "Yarım Ekmek", "fiyat": 115}, {"id": "ucceyrek", "ad": "Üç Çeyrek", "fiyat": 145}, {"id": "tam", "ad": "Tam Ekmek", "fiyat": 175} ] },
            { "id": 102, "ad": "Atom Tost", "aciklama": "Sucuk, kaşar, domates, biber, salam", "resim": "fotolar/atom.jpg", "fiyat": None, "secenekler": [ {"id": "yarim", "ad": "Yarım Ekmek", "fiyat": 140}, {"id": "ucceyrek", "ad": "Üç Çeyrek", "fiyat": 170}, {"id": "tam", "ad": "Tam Ekmek", "fiyat": 200} ] },
            { "id": 103, "ad": "Soğuk Sandviç", "aciklama": "Domates, kırmızı biber, yeşil biber, marul, kaşar, zeytin, salam, haşlanmış yumurta", "resim": "fotolar/sandavic.jpg", "fiyat": None, "secenekler": [ {"id": "yarim", "ad": "Yarım Ekmek", "fiyat": 100}, {"id": "ucceyrek", "ad": "Üç Çeyrek", "fiyat": 130}, {"id": "tam", "ad": "Tam Ekmek", "fiyat": 160} ] },
            { "id": 104, "ad": "Köfte Ekmek", "aciklama": "Izgara köfte, sumaklı soğan, domates", "resim": "fotolar/köfte.avif", "fiyat": None, "secenekler": [ {"id": "yarim", "ad": "Yarım Ekmek", "fiyat": 120}, {"id": "ucceyrek", "ad": "Üç Çeyrek", "fiyat": 160}, {"id": "tam", "ad": "Tam Ekmek", "fiyat": 200} ] },
            { "id": 105, "ad": "Sucuk Ekmek", "aciklama": "Kasap sucuk, domates, baharat", "resim": "fotolar/sucuk.webp", "fiyat": None, "secenekler": [ {"id": "yarim", "ad": "Yarım Ekmek", "fiyat": 100},{"id": "ucceyrek ", "ad": "Üç Çeyrek" , "fiyat": 150}, {"id": "tam", "ad": "Tam Ekmek", "fiyat": 180} ] },
            { "id": 106, "ad": "Patso", "aciklama": "Bol patates kızartması, ketçap, mayonez", "resim": "fotolar/patso.jpg", "fiyat": None, "secenekler": [ {"id": "yarim", "ad": "Yarım Ekmek", "fiyat": 60}, {"id": "tam", "ad": "Tam Ekmek", "fiyat": 100} ] }
        ]
    },
    {
        "id": "kategori2", "kategoriAdi": "Gözleme Çeşitleri", "kategoriResmi": "fotolar/gözleme.jpg",
        "urunler": [
            { "id": 201, "ad": "Kaşarlı Gözleme", "aciklama": "El açması yufka, bol erimiş kaşar", "fiyat": 110, "resim": "fotolar/kasarlig.jpg", "secenekler": None },
            { "id": 202, "ad": "Karışık Gözleme", "aciklama": "Sucuk, kaşar, yeşil biber, kırmızı biber", "fiyat": 140, "resim": "fotolar/karişikg.jpg", "secenekler": None },
            { "id": 203, "ad": "Sucuklu Gözleme", "aciklama": "Bol sucuklu gözleme", "fiyat": 130, "resim": "fotolar/sucuklug.jpg", "secenekler": None },
            { "id": 204, "ad": "Patatesli Gözleme", "aciklama": "Özel baharatlı patates dolgulu", "fiyat": 120, "resim": "fotolar/patateslig.jpg", "secenekler": None }
        ]
    },
    {
        "id": "kategori3", "kategoriAdi": "Atıştırmalıklar", "kategoriResmi": "fotolar/atıştırmalık.jpg",
        "urunler": [
            { "id": 301, "ad": "O'benim O", "aciklama": "Çikolatalı atıştırmalık", "fiyat": 20, "resim": "fotolar/benimo.webp", "secenekler": None },
            { "id": 302, "ad": "9 Kat", "aciklama": "Gofret", "fiyat": 15, "resim": "fotolar/dokuzkat.jpg", "secenekler": None },
            { "id": 303, "ad": "Ülker Çikolatalı Gofret", "aciklama": "Klasik lezzet", "fiyat": 10, "resim": "fotolar/ülker.jpg", "secenekler": None },
            { "id": 304, "ad": "Dido Sütlü Çikolata", "aciklama": "Sütlü", "fiyat": 15, "resim": "fotolar/dido.jpg", "secenekler": None },
            { "id": 305, "ad": "Dido Gold", "aciklama": "Gold Çikolata", "fiyat": 18, "resim": "fotolar/gold.jpg", "secenekler": None },
            { "id": 306, "ad": "Metro Çikolata", "aciklama": "Karamelli enerji", "fiyat": 15, "resim": "fotolar/mero.jpg", "secenekler": None },
            { "id": 307, "ad": "Saklıköy (Sütlü Kremalı)", "aciklama": "Sütlü kremalı tam tahıllı bisküvi", "fiyat": 25, "resim": "fotolar/sütlü.jpg", "secenekler": None },
            { "id": 308, "ad": "Saklıköy (Çikolata Kremalı)", "aciklama": "Çikolata kremalı tam tahıllı bisküvi", "fiyat": 25, "resim": "fotolar/çikolatalı.jpg", "secenekler": None },
            { "id": 309, "ad": "Çubuk Kraker", "aciklama": "Tuzlu atıştırmalık", "fiyat": 10, "resim": "fotolar/çubuk.webp", "secenekler": None },
            { "id": 310, "ad": "Popkek Çeşitleri", "aciklama": "Efsane kek", "resim": "fotolar/popkek.jpg", "fiyat": None, "secenekler": [ {"id": "ciko", "ad": "Çikolatalı", "fiyat": 15}, {"id": "visne", "ad": "Vişneli", "fiyat": 15}, {"id": "limon", "ad": "Limonlu", "fiyat": 15}, {"id": "bitter", "ad": "Bitterli", "fiyat": 15}, {"id": "muz", "ad": "Muzlu", "fiyat": 15}, {"id": "portakal", "ad": "Portakallı", "fiyat": 15} ] },
            { "id": 311, "ad": "Biskrem", "aciklama": "Çikolata dolgulu bisküvi", "fiyat": 20, "resim": "fotolar/biskrem.webp", "secenekler": None },
            { "id": 312, "ad": "Ülker Kremalı Bisküvi", "aciklama": "Kremalı bisküvi", "fiyat": 15, "resim": "fotolar/sandaviç bisküvi.jpg", "secenekler": None },
            { "id": 313, "ad": "Nero", "aciklama": "Kakaolu kremalı bisküvi", "fiyat": 20, "resim": "fotolar/nero.jpg", "secenekler": None }
        ]
    },
    {
        "id": "kategori4", "kategoriAdi": "Sıcak İçecekler", "kategoriResmi": "fotolar/sicak.jpg",
        "urunler": [
            { "id": 401, "ad": "Çay", "aciklama": "Tavşan kanı demleme çay", "resim": "fotolar/çay.avif", "fiyat": None, "secenekler": [ {"id": "normal", "ad": "Normal Çay (İnce Belli)", "fiyat": 15}, {"id": "fincan", "ad": "Fincan Çay", "fiyat": 25} ] },
            { "id": 402, "ad": "Türk Kahvesi", "aciklama": "Köpüklü, lokum ile servis edilir", "resim": "fotolar/türk.jpg", "fiyat": None, "secenekler": [ {"id": "sekersiz", "ad": "Şekersiz", "fiyat": 45}, {"id": "orta", "ad": "Orta Şekerli", "fiyat": 45}, {"id": "sekerli", "ad": "Şekerli", "fiyat": 45} ] },
            { "id": 403, "ad": "Nescafe Çeşitleri", "aciklama": "Sıcak ve enerji verici", "resim": "fotolar/kahve.jpg", "fiyat": None, "secenekler": [ {"id": "3u1", "ad": "3'ü 1 Arada", "fiyat": 35}, {"id": "2si1", "ad": "2'si 1 Arada", "fiyat": 35}, {"id": "sade", "ad": "Sade (Klasik)", "fiyat": 35}, {"id": "gold", "ad": "Gold", "fiyat": 45} ] }
        ]
    },
    {
        "id": "kategori5", "kategoriAdi": "İçecekler", "kategoriResmi": "fotolar/içecekler.jpg",
        "urunler": [
            { "id": 501, "ad": "Kutu Kola (330ml)", "aciklama": "Buz gibi", "fiyat": 35, "resim": "fotolar/kutukola.jpg", "secenekler": None },
            { "id": 502, "ad": "Kutu Fanta (330ml)", "aciklama": "Buz gibi", "fiyat": 35, "resim": "fotolar/kutufanta.jpg", "secenekler": None },
            { "id": 503, "ad": "Coca Cola (Büyük Boy)", "aciklama": "Litrelik Kola", "resim": "fotolar/litrelikkola.jpg", "fiyat": None, "secenekler": [ {"id": "1L", "ad": "1 Litre", "fiyat": 45}, {"id": "1.5L", "ad": "1.5 Litre", "fiyat": 55}, {"id": "2L", "ad": "2 Litre", "fiyat": 65}, {"id": "2.5L", "ad": "2.5 Litre", "fiyat": 75} ] },
            { "id": 504, "ad": "Fanta (Büyük Boy)", "aciklama": "Litrelik Fanta", "resim": "fotolar/litrelikfanta.jpg", "fiyat": None, "secenekler": [ {"id": "1L", "ad": "1 Litre", "fiyat": 45}, {"id": "1.5L", "ad": "1.5 Litre", "fiyat": 55}, {"id": "2L", "ad": "2 Litre", "fiyat": 65}, {"id": "2.5L", "ad": "2.5 Litre", "fiyat": 75} ] },
            { "id": 519, "ad": "Su", "aciklama": "Pet şişe su", "fiyat": 15, "resim": "fotolar/su.jpg", "secenekler": None },
            { "id": 505, "ad": "Şeftalili Kutu Meyve Suyu", "aciklama": "Meyve suyu", "fiyat": 25, "resim": "fotolar/şeftali.webp", "secenekler": None },
            { "id": 506, "ad": "Vişneli Kutu Meyve Suyu", "aciklama": "Meyve suyu", "fiyat": 25, "resim": "fotolar/vişne.webp", "secenekler": None },
            { "id": 507, "ad": "Karışık Kutu Meyve Suyu", "aciklama": "Meyve suyu", "fiyat": 25, "resim": "fotolar/karışık.webp", "secenekler": None },
            { "id": 508, "ad": "Didi Soğuk Çay", "aciklama": "Teneke (500ml)", "fiyat": 30, "resim": "fotolar/didi.jpg", "secenekler": None },
            { "id": 509, "ad": "Gazoz", "aciklama": "Serinletici", "fiyat": 30, "resim": "fotolar/gazoz.jpg", "secenekler": None },
            { "id": 510, "ad": "Uludağ Limonata", "aciklama": "Soğuk limonata (0.5 L)", "fiyat": 40, "resim": "fotolar/limonata.jpg", "secenekler": None },
            { "id": 511, "ad": "Ayran", "aciklama": "Köpüklü yayık ayranı", "fiyat": 25, "resim": "fotolar/ayran.jpg", "secenekler": None },
            { "id": 512, "ad": "Sade Soda", "aciklama": "Doğal maden suyu", "fiyat": 20, "resim": "fotolar/sade.jpg", "secenekler": None },
            { "id": 513, "ad": "Limonlu Soda", "aciklama": "Meyveli maden suyu", "fiyat": 25, "resim": "fotolar/limonlu.jpg", "secenekler": None },
            { "id": 514, "ad": "Böğürtlenli Soda", "aciklama": "Meyveli maden suyu", "fiyat": 25, "resim": "fotolar/böğürtlen.jpg", "secenekler": None },
            { "id": 515, "ad": "Burn Enerji İçeceği", "aciklama": "Kutu (330ml)", "fiyat": 60, "resim": "fotolar/siyahburn.jpg", "secenekler": None },
            { "id": 516, "ad": "Redbull", "aciklama": "Enerji İçeceği", "fiyat": 60, "resim": "fotolar/redbul.jpg", "secenekler": None },
            { "id": 517, "ad": "Just Power", "aciklama": "Enerji İçeceği", "fiyat": 40, "resim": "fotolar/just.avif", "secenekler": None }
        ]
    }
]

# Modeller
class SiparisKalemi(BaseModel):
    sepetId: Union[str, int]
    ad: str
    fiyat: float
    quantity: int

class SiparisOlustur(BaseModel):
    masa_no: str
    sepet: List[SiparisKalemi]
    notlar: str = ""

class FiyatGuncelleModel(BaseModel):
    kategori_id: str
    urun_id: int
    secenek_id: Optional[str] = None
    yeni_fiyat: float

class UrunEkleModel(BaseModel):
    kategori_id: str
    ad: str
    fiyat: float

# Yönlendirmeler
@app.delete("/api/admin/urun-sil/{kategori_id}/{urun_id}")
def urun_sil(kategori_id: str, urun_id: int):
    for kat in MENU_VERISI:
        if kat["id"] == kategori_id:
            kat["urunler"] = [u for u in kat["urunler"] if u["id"] != urun_id]
            return {"mesaj": "Silindi"}
    raise HTTPException(status_code=404, detail="Bulunamadı")

@app.get("/api/menu")
def menuyu_getir():
    return MENU_VERISI

@app.post("/api/admin/fiyat-guncelle")
def fiyat_guncelle(data: FiyatGuncelleModel):
    for kat in MENU_VERISI:
        if kat["id"] == data.kategori_id:
            for urun in kat["urunler"]:
                if urun["id"] == data.urun_id:
                    if data.secenek_id and urun.get("secenekler"):
                        for sec in urun["secenekler"]:
                            if sec["id"] == data.secenek_id:
                                sec["fiyat"] = data.yeni_fiyat
                                return {"mesaj": "Güncellendi"}
                    else:
                        urun["fiyat"] = data.yeni_fiyat
                        return {"mesaj": "Güncellendi"}
    raise HTTPException(status_code=404, detail="Bulunamadı")

@app.post("/api/admin/urun-ekle")
def urun_ekle(data: UrunEkleModel):
    for kat in MENU_VERISI:
        if kat["id"] == data.kategori_id:
            mevcut_idler = [u["id"] for u in kat["urunler"]]
            yeni_id = max(mevcut_idler) + 1 if mevcut_idler else 1
            yeni_urun = { "id": yeni_id, "ad": data.ad, "fiyat": data.fiyat, "aciklama": "Yeni Eklendi", "resim": "fotolar/logo.png", "secenekler": None }
            kat["urunler"].append(yeni_urun)
            return {"mesaj": "Eklendi"}
    raise HTTPException(status_code=404, detail="Bulunamadı")

@app.post("/api/siparis-ver")
def siparis_ver(data: SiparisOlustur):
    global siparis_id_sayaci
    toplam_tutar = sum(item.fiyat * item.quantity for item in data.sepet)
    yeni_siparis = { "id": siparis_id_sayaci, "masa_no": data.masa_no, "urunler": [{"ad": item.ad, "adet": item.quantity, "fiyat": item.fiyat} for item in data.sepet], "toplam_tutar": toplam_tutar, "durum": "Hazırlanıyor", "zaman": datetime.datetime.now().strftime("%H:%M") }
    aktif_siparisler.append(yeni_siparis)
    siparis_id_sayaci += 1
    return {"mesaj": "İletildi", "siparis_id": yeni_siparis["id"]}

@app.post("/api/garson-cagir")
async def garson_cagir(veri: dict):
    garson_cagrilari.append({
        "masa_no": veri.get("masa_no"),
        "zaman": datetime.datetime.now().strftime("%H:%M")
    })
    return {"status": "success"}

@app.get("/api/mutfak/bekleyen-isler")
def mutfak_ekrani():
    return {"siparisler": [s for s in aktif_siparisler if s["durum"] == "Hazırlanıyor"], "garson_cagrilari": garson_cagrilari}

@app.post("/api/mutfak/garson-tamamla")
async def garson_tamamla(veri: dict):
    global garson_cagrilari
    masa = veri.get("masa_no")
    garson_cagrilari = [g for g in garson_cagrilari if g["masa_no"] != masa]
    return {"mesaj": "Tamamlandı"}

@app.post("/api/mutfak/siparis-tamamla/{siparis_id}")
def siparis_tamamla(siparis_id: int):
    for siparis in aktif_siparisler:
        if siparis["id"] == siparis_id: siparis["durum"] = "Tamamlandı"
    return {"mesaj": "Tamamlandı"}

@app.get("/api/patron/rapor")
def patron_raporu():
    tamamlananlar = [s for s in aktif_siparisler if s["durum"] == "Tamamlandı"]
    bekleyenler = [s for s in aktif_siparisler if s["durum"] == "Hazırlanıyor"]
    return {
        "gunluk_ciro": sum(s["toplam_tutar"] for s in tamamlananlar),
        "bekleyen_ciro": sum(s["toplam_tutar"] for s in bekleyenler),
        "tamamlanan_siparis_sayisi": len(tamamlananlar),
        "bekleyen_siparis_sayisi": len(bekleyenler),
        "gecmis": aktif_siparisler[::-1] 
    }

app.mount("/", StaticFiles(directory=".", html=True), name="static")