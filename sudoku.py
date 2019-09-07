import numpy as np
from msvcrt import getwche

t = np.empty((9, 9), dtype=set)

def tesztbemenet():
    """Előre eltárolt adatok használata"""
    global t
    t = np.array([[{4}, {}, {3}, {}, {7}, {2}, {6}, {}, {}], [{}, {7}, {}, {}, {}, {}, {}, {}, {}], [{9}, {}, {}, {}, {}, {8}, {1}, {}, {}], [{}, {}, {}, {2}, {8}, {}, {}, {}, {3}], [{5}, {}, {}, {9}, {}, {7}, {}, {}, {6}], [{3}, {}, {}, {}, {4}, {5}, {}, {}, {}], [{}, {}, {1}, {8}, {}, {}, {}, {}, {9}], [{}, {}, {}, {}, {}, {}, {}, {3}, {}], [{}, {}, {8}, {7}, {9}, {}, {4}, {}, {2}]])
    
def beolv():
    """Adatok beolvasása"""
    for i in range(3):
        print("-"*25, end="\n")
        for j in range(3):
            for k in range(3):
                print("| ", end="", flush=True)
                for l in range(3):
                    ch = getwche()
                    if ch=="x":
                        tesztbemenet()
                        return
                    while not (ch.isdigit() or ch == " "):
                        print("\b \b", end="", flush=True)
                        ch = getwche()
                    if ch=="0" or ch==" ":
                        t[3*i+j][3*k+l] = {}
                        print("\b_ ", end="", flush=True)
                    else:
                        t[3*i+j][3*k+l] = {int(ch)}
                        print(" ", end="", flush=True)
            print("|", end="\n")
    print("-"*25)

def kiir():
    """Adatok kiírása"""
    print("")
    for i in range(3):
        print("-"*25, end="\n")
        for j in range(3):
            for k in range(3):
                print("| ", end="")
                for l in range(3):
                    print(t[3*i+j][3*k+l].pop(), end=" ")
            print("|")
    print("-"*25)

def negyzet(*args):
    """Megadja, hogy egy adott koordináta melyik 3×3-as csoportban van (a bal-felső koordinátát)"""
    if len(args)==2:
        return 3*int(args[0]/3), 3*int(args[1]/3)
    elif len(args)==1:
        return 3*(args[0]%3), 3*int(args[0]/3)
    else:
        raise ValueError("negyzet fv. " + arg_str(len(args)) + "paramétert kapott")

def jo_e(a, x, y):
    """Megnézi, hogy egy adott szám kerülhet-e egy adott pozícióba"""
    for i in range(9):
        if a in t[x][i] and len(t[x][i])==1 and i != y:
            return False
    for i in range(9):
        if a in t[i][y] and len(t[i][y])==1 and i != x:
            return False
    x0, y0 = negyzet(x, y)
    for i in range(x0, x0+3):
        for j in range(y0, y0+3):
            if a in t[i][j] and len(t[i][j])==1 and i != x and j != y:
                return False
    return True

def megoldva():
    """Megadja, hogy a sudoku meg van-e oldva."""
    for i in range(9):
        for j in range(9):
            if len(t[i][j]) != 1:
                return False
    return True

def lehets():
    """Megkeresi minden helyre az odatehető számokat"""
    global t
    valt = False
    for i in range(9):
        for j in range(9):
            uj = [x+1 for x in range(9) if jo_e(x+1, i, j)]
            if len(uj) < len(t[i][j]) or len(t[i][j]) == 0:
                t[i][j] = set(uj)
                valt = True
            if len(uj) == 0:
                raise Exception("rossz próba")
    return valt

def kov(elo):
    """Megadja egy adott halmaz után következőt
    {1}, {2}, ..., {9}, {1, 2}, {1, 3}, ... {8, 9}, {1, 2, 3}, ..."""
    if len(elo) >= 9:
        return False
    kov = elo.copy()
    i = 9
    while len(elo)>0:
        if i in elo:
            elo.remove(i)
        else:
            kov.add(max(elo)+1)
            kov.remove(max(elo))
            return kov
        i -= 1
    return set(range(1, len(kov)+2))

def kot_bov():
    """Megkeresi minden helyre az odatehető számokat"""
    global t
    csop = {1}
    while lehets():
        continue
    while csop!=False:
        #sorok
        for i in range(9):
            lehetosegek = 0
            csokkent = False
            for j in range(9):
                if len(csop & t[i][j]) > 0:
                    lehetosegek += 1
                    if len(t[i][j] - csop) > 0:
                        csokkent = True
            if lehetosegek < len(csop):
                raise ValueError("nincs elég hely a " + csop + " csoportnak a(z) " + i+1 + ". sorban")
            elif lehetosegek == len(csop) and csokkent:
                for j in range(9):
                    if len(csop & t[i][j]) > 0:
                        t[i][j] &= csop
                return True

        #oszlopok
        for i in range(9):
            lehetosegek = 0
            csokkent = False
            for j in range(9):
                if len(csop & t[j][i]) > 0:
                    lehetosegek += 1
                    if len(t[j][i] - csop) > 0:
                        csokkent = True
            if lehetosegek < len(csop):
                raise ValueError("nincs elég hely a " + csop + " csoportnak a(z) " + i+1 + ". oszlopban")
            elif lehetosegek == len(csop) and csokkent:
                for j in range(9):
                    if len(csop & t[j][i]) > 0:
                        t[j][i] &= csop
                return True
        
        #négyzetek
        for x in range(9):
            x0, y0 = negyzet(x)
            lehetosegek = 0
            csokkent = False
            for i in range(x0, x0+3):
                for j in range(y0, y0+3):
                    if len(csop & t[i][j]) > 0:
                        lehetosegek += 1
                        if len(t[i][j] - csop) > 0:
                            csokkent = True
            if lehetosegek < len(csop):
                raise ValueError("nincs elég hely a " + csop + " csoportnak a(z) " + i+1 + ". oszlopban")
            elif lehetosegek == len(csop) and csokkent:
                for i in range(x0, x0+3):
                    for j in range(y0, y0+3):
                        if len(csop & t[i][j]) > 0:
                            t[i][j] &= csop
                return True
        csop = kov(csop)
    return False

def kot():
    """Minden kötelező zámnak megkeresi a helyét, ha egyértelmű"""
    global t
    while lehets():
        continue
    valt = False
    print(t, end="->")
    #sorok
    for i in range(9):
        lehetosegek = [0]*9
        for j in range(9):
            for szam in t[i][j]:
                if len(t[i][j])!=1:
                    lehetosegek[szam-1] += 1
        jok = set([i+1 for i in range(9) if lehetosegek[i]==1])
        for j in range(9):
            if len(jok & t[i][j])==1:
                t[i][j] &= jok
                valt = True
    print(t)
    while lehets():
        continue
    #oszlpopk
    for i in range(9):
        lehetosegek = [0]*9
        for j in range(9):
            for szam in t[j][i]:
                if len(t[j][i])!=1:
                    lehetosegek[szam-1] += 1
        jok = set([i+1 for i in range(9) if lehetosegek[i]==1])
        for j in range(9):
            if len(jok & t[j][i])==1:
                t[j][i] &= jok
                valt = True
    print(t)
    while lehets():
        continue
    #négyzetek
    for x in range(9):
        x0, y0 = negyzet(x)
        lehetosegek = [0]*9
        for i in range(x0, x0+3):
            for j in range(y0, y0+3):
                for szam in t[i][j]:
                    if len(t[i][j])!=1:
                        lehetosegek[szam-1] += 1
        jok = set([i+1 for i in range(9) if lehetosegek[i]==1])
        for i in range(x0, x0+3):
            for j in range(y0, y0+3):
                if len(jok & t[i][j])==1:
                    t[i][j] &= jok
                    valt = True
    print(t)
    return valt

def probal():
    """Egy elem kivételével próbálja elősegíteni a sudoku megoldását"""
    global t
    for x in range(2,9):
        for i in range(9):
            for j in range(9):
                if len(t[i][j]) == x:
                    masolat = t.copy()
                    t[i][j] = {max(t[i][j])}
                    try:
                        while kot_bov():
                            continue
                    except Exception:
                        t = masolat.copy()
                        t[i][j].remove(max(t[i][j]))
                        while kot_bov():
                            continue
                    finally:
                        return
    print(t)
    raise LookupError("A sudoku nem megoldható vagy már meg volt oldva")

beolv()
while kot_bov():
    continue
while not megoldva():
    probal()
kiir()