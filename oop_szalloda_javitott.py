from abc import ABC, abstractmethod
from datetime import datetime

class Szoba(ABC):                                               # A Szoba absztrakt osztály, az Egyagyas és Ketagyas osztályok szülője
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam
    
    @abstractmethod
    def get_tipus(self):                                        # minden alosztálban kötelezően legyen egy getter
        pass

class EgyagyasSzoba(Szoba):                                     # Példányosítható osztály, egy plusz attribútummal és egy getterrel
    tipus="egyágyas"
    def get_tipus(self):
        return "Egyágyas szoba"

class KetagyasSzoba(Szoba):                                     # Példányosítható osztály, egy plusz attribútummal és egy getterrel
    tipus="kétágyas"
    def get_tipus(self):
        return "Kétágyas szoba"

class Foglalas:                                                 # A Foglalas osztály példányai fogják magukba foglalni egy adott foglalás adatait (szoba, nap)
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

class Szalloda:                                                 #A Szalloda osztály példányai egy adott szálloda adatait foglalják magukba (egyedi név, szobaobjektumok listája, Foglalas objektumok listája)
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def add_szoba(self, szoba):                                 # Szoba hozzáadása metódus
        self.szobak.append(szoba)

    def add_foglalas(self, foglalas):                           # Foglalás hozzáadása metódus inputvalidációval
        if any(f.datum == foglalas.datum and f.szoba.szobaszam == foglalas.szoba.szobaszam for f in self.foglalasok):
            print(f"Nem sikerült foglalni: a(z) {foglalas.szoba.szobaszam} szoba már foglalt ezen a napon.")
        else:
            self.foglalasok.append(foglalas)                    # Sikeres foglalás két eredménye: 1) a foglalás bekerül a Szalloda objektum foglglasok attribútumát képező listába
            return foglalas.szoba.ar                            # 2) és visszaadja a foglalt szoba árát

    def foglalas(self, szobaszam, datum):                       #a Foglalas osztály példányosítása = adott paraméterekkel rendekező foglalás létrehozása inputvalidáció után
        szoba = next((szoba for szoba in self.szobak if szoba.szobaszam == szobaszam), None)
        if szoba is None:
            print("Nincs ilyen szobaszám!")
            return None
        if any(foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum for foglalas in self.foglalasok):
            print("Erre a szobára és dátumra már van foglalás!")
            return None                                         # bármilyen sikertelenség esetén None értékkel tér vissza, de ha sikeres, akkor:
        uj_foglalas = Foglalas(szoba, datum)                    # 1) példány létrehozása
        self.add_foglalas(uj_foglalas)                          # 2) és az új példány hozzáfűzése a foglalásokhoz az erre szolgáló metóduson keresztül
        return szoba.ar                                         # 3) a foglalt szoba árának visszaadása

    def foglalas_ar(self, datum):
        for foglalas in self.foglalasok:
            if foglalas.datum == datum:
                return foglalas.szoba.ar
        return None

    def lemondas(self, szoba, datum):                           # az input paramétereknek megfelelő foglalás törlése a szálloda foglalásai közül (egy booleanban visszaadja, sikeres volt-e a művelet)
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szoba and foglalas.datum == datum:
                self.foglalasok.remove(foglalas)
                return True
        return False

    def listaz_foglalasok(self):                                # az adott szálloda foglalásainak "végigpörgetése" és kiíratása   
        rendezett_foglalasok = sorted(self.foglalasok, key=lambda f: (f.szoba.szobaszam, f.datum))  # rendezze a foglalásokat szobaszám, majd dátum szerint növekvő sorrendbe
        print(f"A {self.nev} jelenlegi foglalásai:")
        for foglalas in rendezett_foglalasok:            
            print(f"Szoba: {foglalas.szoba.szobaszam} ({foglalas.szoba.tipus}), Dátum: {foglalas.datum.strftime('%Y-%m-%d')}, Ár: {foglalas.szoba.ar} Ft")

    


                                                                # Tesztadatok feltöltése: szálloda-, szoba- és foglaláspéldányok létrehozása
szalloda = Szalloda("Grand Hotel Objektum Orient")
szalloda.add_szoba(EgyagyasSzoba(20000, 11))
szalloda.add_szoba(KetagyasSzoba(30000, 21))
szalloda.add_szoba(EgyagyasSzoba(25000, 12))

szalloda.add_foglalas(Foglalas(szalloda.szobak[0], datetime(2024, 6, 10)))
szalloda.add_foglalas(Foglalas(szalloda.szobak[1], datetime(2024, 6, 15)))
szalloda.add_foglalas(Foglalas(szalloda.szobak[2], datetime(2024, 6, 20)))
szalloda.add_foglalas(Foglalas(szalloda.szobak[0], datetime(2024, 6, 25)))
szalloda.add_foglalas(Foglalas(szalloda.szobak[1], datetime(2024, 6, 30)))

                                                                # Felhasználói interfész, csak egy fapados CLI... :)
while True:
    print("\n1. Foglalás")
    print("2. Lemondás")
    print("3. Foglalások listázása")
    print("4. Kilépés")
    valasztas = input("\nVálassz egy műveletet: ")

    if valasztas == "1":                                        # Foglalás
        
        while True:                                             #addig nem enged tovább, amíg nem adunk meg valós szobaszámot
            szobaszam = input("Adja meg a szoba számát: ")
            try:
                szobaszam = int(szobaszam)
            except ValueError:
                print("Kérem, csak számokat adjon meg")
                continue
            if szobaszam not in [szoba.szobaszam for szoba in szalloda.szobak]:
                print("Nincs ilyen szobaszám!")
                continue
            else:
                break                                           # ha valid szobaszámot adunk meg, csk akkor lép ki a while True végtelen hátultesztelő ciklusból
        while True:                                             #addig nem enged tovább, amíg nem adunk meg valós és jövőbeli dátumot, módszer u. a. mint a szobaszámnál
            datum_str = input("Adja meg a foglalás dátumát (YYYY-MM-DD formátumban): ")
            try:
                datum = datetime.strptime(datum_str, "%Y-%m-%d")
            except ValueError:
                print("Nem megfelelő dátumformátum")  
                continue  
            if datum < datetime.now():
                print("Csak jövőbeli dátumra lehet foglalni.")
            else:
                break
         
        
       
        ar = szalloda.foglalas(szobaszam, datum)                # Ha van validált szobaszám és szoba, mehet a foglalás metódus meghívása
        if ar:                                                  # A foglalas metódus None értékkel tér vissza, ha a foglalás nem sikerült, és az árral, ha sikerült
            print(f"Foglalás sikeres! A szoba ára: {ar} Ft")

    elif valasztas == "2":                                      # Lemondás
        while True:                                             #addig nem enged tovább, amíg nem adunk meg valós szobaszámot
            szobaszam = input("Adja meg a szoba számát: ")
            try:
                szobaszam = int(szobaszam)
            except ValueError:
                print("Kérem, csak számokat adjon meg")
                continue
            if szobaszam not in [szoba.szobaszam for szoba in szalloda.szobak]:
                print("Nincs ilyen szobaszám!")
                continue
            else:
                break
        while True:                                             #addig nem enged tovább, amíg nem adunk meg valós dátumot
            datum_str = input("Adja meg a foglalás dátumát (YYYY-MM-DD formátumban): ")
            try:
                datum = datetime.strptime(datum_str, "%Y-%m-%d")
            except ValueError:
                print("Nem megfelelő dátumformátum")  
                continue              
            else:
                break
                                                                # Ellenőrzi, hogy tényleg létezik-e a törlendő foglalás
        if not any(foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum for foglalas in szalloda.foglalasok):
            print("Nincs ilyen foglalás.")
            continue

        szalloda.lemondas(szobaszam, datum)                     # Ha van, meghívja a lemondás metódust
        print("Lemondás sikeres!")

    elif valasztas == "3":                                      # Foglalások listázása metódus meghívása
        szalloda.listaz_foglalasok()

    elif valasztas == "4":                                       # Kilépés
        break

    else:
        print("Nincs ilyen menüpont")
