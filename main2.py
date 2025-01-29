# from time import perf_counter
# start = perf_counter()

"""Felhasználói felület nincsen
   Itt kell megadni az adott file elérési útját/nevét
"""
with open("tesztek/I. kategoria/alaprajz3.txt", "r") as file:
    elso_sor = file.readline().strip().split()  #Kiolvassa az első sort
    bitmap = ""  #Ebbe a változóba menti a file tartalmát
    for i in file.readlines():
        bitmap += i

def mellettekord(halmaz):
    mellettielemek = set()
    for i in halmaz:
        mellettielemek.add((i[0], i[1]+1))
        mellettielemek.add((i[0], i[1]-1))
        mellettielemek.add((i[0]+1, i[1]))
        mellettielemek.add((i[0]-1, i[1]))
    return mellettielemek
    
sor, oszlop = int(elso_sor[1]), int(elso_sor[0]) 
def objektumszelektalo(lista, karakter):
    """A bitmapből kigyűjti az adott objektum koordinátáit, 
      és az objektumok koordinátáit listába rakja"""
    objektum_lista = []  #Ide rakjuk a különálló objektumok koordinátáit
    for y in range(len(lista)):  #Végig iterálunk a filon(y tengely)
        for x in range(len(lista[y])): #Végig iterálunk a file akutális során
            if lista[y][x] == karakter:  #Ha a bitmap adott karaktere == a keresett karakterrel(0 vagy 1)
                objektum_lista.append({(x,y)})  #Új setbe belerakva hozzáadjuk a koordinátát a sorhoz

    while True:
        """
        A ciklus célja, hogy az olyan objektumokat kiszűrje, egybekapcsolja
        amit az előző for ciklus nem tudott egybe kapcsolni
        """
        zaszlo2 = True
        for index_1, elem_1 in enumerate(objektum_lista):  
            for index_2, elem_2 in enumerate(objektum_lista):
                # Egymással összehasonlítjuk az elemeket
                if index_2 != index_1 and elem_2 & mellettekord(elem_1):  #Ha van metszet, és nem magukkal hasonlítjuk össze
                    elem_1.update(elem_2) #Az első elemet frissítjük a 2 elem hozzáadásával
                    del objektum_lista[index_2]  #Töröljük a második elemet.
                    zaszlo2 = False
                    break
        if zaszlo2:
            return objektum_lista  #Vissza adjuk az objektumok listáját(itt már nincs redundáns objektum elem)

objektumok = objektumszelektalo([i for i in bitmap.strip().split("\n")], "1")  #Tárgyak koordinátái
objektumok_dict = {
    "fal": max(objektumok, key=len),  #A leghosszabb egybefüggő koordináta lista a fal koordinátái
    "székek": [],
    "asztalok": [],
    "kanapé": [],
    "szobak": []
}
del objektumok[objektumok.index(max(objektumok, key=len))]  #Eltávolítjuk a fal koordinátáit
for elem in sorted(objektumok, key=len):  #Rendezzük hossz alapján az objektumok koordinátáit
    if len(elem) == 1:  #Ha az objektumnak csak 1 koordinátája van
        objektumok_dict["székek"].extend(elem)  #Az az objektum szék lesz
        del objektumok[objektumok.index(elem)]  #Eltávolítjuk a szék koordinátáját
    else:
        #Ha nem szék megvizsgáljuk milyen tárgy
        x_kord = [j[0] for j in elem]  #Tárgy x koordinátái
        y_kord = [j[1] for j in elem]  ##Tárgy y koordinátái
        x_set, y_set = set(x_kord), set(y_kord)
        if len(x_kord) / len(x_set) == len(x_kord) // len(x_set) and len(y_kord) / len(y_set) == len(y_kord) // len(y_set) and (len(x_set) == 2 and len(y_set) >= 2) or (len(y_set) == 2 and len(y_set) >= 2): #Nehéz lenne elmagyarázni.
            objektumok_dict["asztalok"].append(list(elem))  #Akkor az asztal lesz
            del objektumok[objektumok.index(elem)]  #Eltávolítjuk az asztal koordinátáit
        else:
            """Ha nem asztal, akkor kanapé"""
            objektumok_dict["kanapé"].append(list(elem))  #Hozzáadjuk a kanapé koordinátáit
            del objektumok[objektumok.index(elem)]  #Eltávolítjuk a kanapé koordinátáit

alaprajz = [["." for _ in range(sor)] for _ in range(oszlop)]  #Létrehozzuk az alaprajzot
def abrazol(koordinata, tipus):
    """Feltöltjük az alaprajzot a dekódult tárgyakkal"""
    x, y = koordinata
    match tipus:  #Tárgy típusa
        case "fal":
            alaprajz[y][x] = "F"
        case "székek":
            alaprajz[y][x] = "S"
        case "asztalok":
            alaprajz[y][x] = "A"
        case "kanapé":
            alaprajz[y][x] = "K"
        
for objektum_tipusa in objektumok_dict.keys():
    for objektum_elemei in objektumok_dict[objektum_tipusa]:
        if type(objektum_elemei) is list:  #Ha lista típusú, akkor nem szék az objektum és több mint 1 eleme van
            for k in objektum_elemei:
                abrazol(k, objektum_tipusa)  #Meghívjuk az ábrázoló függvényt az objektum koordinátáira
        else:
            """Ha szék, akkor csak 1x kell meghívni rá az ábrázoló függvényt"""
            abrazol(objektum_elemei, objektum_tipusa)
print("Bitmap: ")
[print(*i) for i in bitmap.strip().split("\n")]
print("\nDekódolt alaprajz: ")
[print(*i) for i in alaprajz]  #Kiíratjuk a dekódolt alaprajzot

szobak = objektumszelektalo([i for i in bitmap.strip().split("\n")], "0")  #Szobák koordinátáinak kigyűjtése
for i in szobak:
    x_set = {j[0] for j in i}  #x koordináták
    y_set = {j[1] for j in i}  #koordináták
    if 0 not in x_set and 0 not in y_set and sor -1 not in x_set and oszlop -1 not in y_set:
        """Ha nem pálya szélén van az objektum akkor az szoba lesz"""
        objektumok_dict["szobak"].append(list(i))  #Hozzáadjuk a szobát

print("Szobák száma: ", len(objektumok_dict["szobak"]))  #Kiírjuk a szobák számát
# end = perf_counter()
# print(f"Második program futási ideje: {end - start:.6f} másodperc")

