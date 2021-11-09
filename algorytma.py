import math

# -------- Printy zostawiam z komentarzami, żeby można było podejrzeć co jest czym ---------

# przypisanie wpisanego w input numeru do zmiennej
number = input("numer pliku:")

# pobranie pliku
filepath = './Grafy/' + number + '.txt'
file = open(filepath, "r")

filelines = file.readlines()  # lista ze stringiem z pliku txt, wszystkie linie


# ---------------------------------------------------------------------------
# ----------------------- WSPÓŁRZĘDNE WIERZCHOŁKÓW --------------------------
# ---------------------------------------------------------------------------

# pierwsza linia pliku txt czyli wspolrzedne
file1line = filelines[0]

# zapis w innej postaci, żeby mozna było zapisać w postaci listy tupli
file1line = file1line.replace(', ', ',').replace('(', '').replace(')', '')
file1line = file1line.split()
# print(file1line)

# lista tupli ze wspołrzędnymi wierzchołków
wspolrzedne = []

# zapis w tuplach
for i in file1line:
    res = tuple(map(int, i.split(',')))
    wspolrzedne.append(res)

# print("współrzędne w tuplach:")
# print(wspolrzedne)

# ---------------------------------------------------------------------------
# ---------------------- LISTA WIERZCHOŁKÓW ---------------------------------
# ---------------------------------------------------------------------------

# 2 linia pliku to wierzchołki start i meta
file2line = filelines[1]

file2line = file2line.split()
file2line = list(map(int, file2line))
# print(file2line)

wierzcholki = []

# uzupełnienie listy wszystkich wierzchołków
for i in range(file2line[-1]):
    res = i+1
    wierzcholki.append(res)

# print(wierzcholki)

# ---------------------------------------------------------------------------
# słownik wierzchołek : współrzędne
wspolrzedne_slownik = {}

for i in range(len(wierzcholki)):
    wspolrzedne_slownik.update(zip(wierzcholki, wspolrzedne))

# print("współrzędne wierzchołków - słownik:")
# print(wspolrzedne_slownik)

# ---------------------------------------------------------------------------
# ----------------------- MACIERZ SĄSIEDZTWA --------------------------------
# ---------------------------------------------------------------------------

# utworzenie macierzy sąsiedztwa jako lista list [[],[]...]
macierz_sasiedztwa = []

# uzupełnienie macierzy sąsiedztwa, każdy wiersz to osobna lista [[], [], ....]
# odczyt od 3 linii z pliku txt (iteracja od 2), przejście przez każdą linię do końca
for i in range(2, len(filelines)):
    fileiline = filelines[i]  # i-ta linia
    fileiline = fileiline.split()
    fileiline = list(map(float, fileiline))
    # print(fileiline)
    macierz_sasiedztwa.append(fileiline)

# print("macierz sąsiedztwa:")
# print(macierz_sasiedztwa)

# ---------------------------------------------------------------------------
# ----------------------- SĄSIEDZI WIERZCHOŁKÓW -----------------------------
# ---------------------------------------------------------------------------

sasiedzi = {}  # słownik sąsiadów => wierzchołek to klucz, lista to wartość, czyli sąsiedzi

sasiedzi_keys = []
sasiedzi_values = []

# uzupełnienie słownika wierzchołkami i listami z sąsiadami
for i in range(len(wierzcholki)):
    sasiedzi_keys.append(i)  # klucze
    for j in range(len(wierzcholki)):
        # odczyt z macierzy sasiedztwa (jesli wiekszy od 0 to jest sąsiadem, jak 0 to nie)
        if macierz_sasiedztwa[i][j] > 0:
            sasiedzi_values.append(j+1)  # wartości  (iteracja od 0)
            sasiedzi[i+1] = list(sasiedzi_values)
    sasiedzi_values = []  # czyszczenie listy

# print("sąsiedzi wierzchołków:")
# print(sasiedzi)

# ---------------------------------------------------------------------------
# --------------------------- HEURYSTYKA ------------------------------------
# ---------------------------------------------------------------------------

heurystyka = {}

heurystyka_keys = []
heurystyka_values = []

for i in range(len(wierzcholki)):
    heurystyka_keys.append(i+1)

    if len(sasiedzi[i+1]) == 0:
        heurystyka_values[i+1].append(-1)
        continue

    # heurystyka - obliczanie odległości między wierzchołkami
    # pierwiastek [ (x1 - x2)^2 + (y1 - y2)^2 ]
    # (wsp x wierzcholka i-tego - wsp x wierzcholka mety)^2 + (wsp y wierzcholka i-tego - wsp y wierzcholka mety)^2
    x = wspolrzedne_slownik[i+1][0] - wspolrzedne_slownik[wierzcholki[-1]][0]
    y = wspolrzedne_slownik[i+1][1] - wspolrzedne_slownik[wierzcholki[-1]][1]

    heur = math.sqrt(x**2 + y**2)
    # print(heur)

    heurystyka_values.append(heur)

    # tworzenie słownika
    heurystyka.update(zip(heurystyka_keys, heurystyka_values))

# print("heurystyka:")
# print(heurystyka)


# ---------------------------------------------------------------------------
# --------------------------- ALGORYTM A* -----------------------------------
# ---------------------------------------------------------------------------


def algorytmA(start=wierzcholki[0], meta=wierzcholki[-1]):

    start = wierzcholki[0]
    meta = wierzcholki[-1]
    rozpatrywane = {start}  # startowy wierzchołek
    przyszedlZ = {}

    g = {}  # mapa w której klucze to wierzchołki, domyślnie inf
    g_keys = []
    g_values = []  # na początku nieskończoność

    # uzupełnienie kluczy wierzchołkami, wartości nieskonczonosc
    for i in range(len(wierzcholki)):
        g_keys.append(i+1)
        g_values.append(math.inf)
        g.update(zip(g_keys, g_values))

    f = {}  # mapa w której klucze to wierzchołki, domyślnie inf
    f_keys = []
    f_values = []  # na początku nieskończoność

    # uzupełnienie kluczy wierzchołkami, wartości nieskonczonosc
    for i in range(len(wierzcholki)):
        f_keys.append(i+1)
        f_values.append(math.inf)
        f.update(zip(f_keys, f_values))

    g[start] = 0
    f[start] = heurystyka[start]

    # dopóki rozpatrywane jest niepusty
    while len(rozpatrywane) > 0:
        minf = math.inf  # na początku zawsze nieskończoność

        # wierzchołek z rozpatrywane o najmniejszym f[x]
        for i in rozpatrywane:
            if f[i] < minf:
                x = i  # wierzchołek z rozpatrywanych z najmniejszym f[x]
                minf = f[i]
                # print(minf)

        # jeżeli obecny wierzchołek jest metą
        if x == meta:
            # wysyłanie funkcji rekonstrukcji trasy
            trasa = zrekonstruuj_trase(przyszedlZ, x)

            # należy odwrócić listę, bo wierzchołki są od końca
            trasa.reverse()

            # przetworzenie listy (trasy) w string
            trasaString = " ".join([str(t) for t in trasa])

            # print("trasa:")
            print(trasaString)
            break
        # print(rozpatrywane)

        rozpatrywane.remove(x)  # usuń x z rozpatrywane

        # dla każdego i spośród sąsiadów x
        for i in sasiedzi[x]:
            waga_krawedzi = float(macierz_sasiedztwa[x-1][i-1])
            tymczasowe_g = g[x] + waga_krawedzi

            # jeśli (tymczasowe_g) < g[i]
            if tymczasowe_g < g[i]:
                przyszedlZ[i] = x
                g[i] = tymczasowe_g
                f[i] = g[i] + heurystyka[i]

                # jeśli i nie jest w rozpatrywane
                if not(i in rozpatrywane):
                    rozpatrywane.add(i)
    return "Brak"  # zwróć porażkę :(


# print("f:")
# print(f)
# print("g:")
# print(g)

# ---------------------------------------------------------------------------

# funkcja zrekonstruuj trasę

def zrekonstruuj_trase(przyszedlZ, obecny_wierzcholek):
    trasa = [obecny_wierzcholek]

    # dopóki istnieje przyszedlZ[obecny_wierzcholek]
    while obecny_wierzcholek in przyszedlZ:
        obecny_wierzcholek = przyszedlZ[obecny_wierzcholek]
        trasa.append(obecny_wierzcholek)
    return trasa

# ---------------------------------------------------------------------------


# wywołanie funkcji algorytm A*
algorytmA()
