import numpy as np
from numpy import linalg as la
import math
#Euler2A kao parametre prima 3 ojlerova ugla, a vraca ortogonalnu matricu rotacije
def Euler2A(psi,teta,fi):

    matrixA = np.zeros((3,3))
    sinFi, cosFi = math.sin(fi), math.cos(fi)
    sinTeta, cosTeta =  math.sin(teta), math.cos(teta)
    sinPsi, cosPsi = math.sin(psi), math.cos(psi)

    matrixA[0] = [cosTeta * cosPsi ,
                  cosPsi * sinTeta * sinFi - cosFi * sinPsi,
                  cosFi * cosPsi * sinTeta + sinFi * sinPsi]
    matrixA[1] = [cosTeta * sinPsi,
                  cosFi * cosPsi + sinTeta * sinFi * sinPsi,
                  cosFi * sinTeta * sinPsi - cosPsi * sinFi]
    matrixA[2] = [-sinTeta, cosTeta * sinFi, cosTeta * cosFi]

    return matrixA

#kao ulaz prima Ortogonalnu matricu A a kao izlaz vraca vektor oko koga se vrsi rotacija i ugao fi koji predstavlja
#za koliko se frsi rotacija: A = Rp(fi) --- kretanje(izometrija)
def A2AngleAxis(matrixA):

    # if la.det(matrixA) != 1:
    #     raise Exception("Matrica A mora biti ortogonalna ----> det(A) = 1")

    E = np.identity(3)
    sistem = matrixA - E
    #trebalo bi se proveriti da li su vektori sistem0 i sistem1 isti!
    sistem0_jedinicni = jedinicni(sistem[0])
    sistem1_jedinicni = jedinicni(sistem[1])
    if sistem1_jedinicni[0] != sistem0_jedinicni[0]:
        p_vector = np.cross(sistem[0],sistem[1])
    else:
        p_vector = np.cross(sistem[0],sistem[2])

    p_jedicni = jedinicni(p_vector)

    #nalazimo vektor u koji je bio normalan na p_vector(bilo koji od ona 3)
    #svi su ortogonalni i na njega primenjujemo matricu A
    u_vector = jedinicni(sistem[0])
    u_new_vector = jedinicni(matrixA.dot(u_vector))

    #nalazimo ugao izmedju u i u' vektora (oba su jedinicna)
    fi = math.acos(u_vector.dot(u_new_vector))

    #jos proveravamo orijentaciju ova tri vektora da bismo odredili znak vektora p
    #to proveravamo pomocu mesovitog proizvoda
    mesoviti = np.cross(u_vector,u_new_vector).dot(p_jedicni)
    if mesoviti < 0 :
        p_jedicni = -p_jedicni


    return p_jedicni,fi

def jedinicni(vector):
    return vector / math.sqrt(sum(i**2 for i in vector))

#ova funkcija prima kao ulaz jedinicni vektor p oko koga se vrsi rotacija i ugao fi a vraca matricu rotacije A
#inverzna je u donosu na funkciju A2AngleAxis
def Rodrigez(p_vector,fi):

    p_transponovani = np.asarray(p_vector).reshape(3,1)
    p_vector= np.asarray(p_vector).reshape(1,3)
    prvi_cin = p_transponovani.dot(p_vector)

    E = np.identity(3)
    drugi_cin = math.cos(fi) * (E - prvi_cin)

    p_x = np.zeros((3,3))
    p_vector = np.asarray(p_vector).reshape(1,3)
    p_x[0] = [0, -p_vector[0][2], p_vector[0][1]]
    p_x[1] = [p_vector[0][2], 0, -p_vector[0][0]]
    p_x[2] = [-p_vector[0][1], p_vector[0][0], 0]
    treci_cin = math.sin(fi) * p_x

    A_matrix = prvi_cin + drugi_cin + treci_cin
    return  A_matrix

#ova funkcija prima kao ulaz matricu rotacije i vraca 3 Ojlerova ugla redom psi,teta,fi koji predstavljaju rotacije
#oko osa Z,Y,X
def A2Euler(A_matrix):

    if la.det(A_matrix) != 1:
        raise Exception("Matrica A mora biti ortogonalna ----> det(A) = 1")

    if A_matrix[2][0] < 1:
        if A_matrix[2][0] > -1: #jedinstveno resenje
            psi = math.atan2(A_matrix[1][0],A_matrix[0][0])
            teta = math.asin(-A_matrix[2][0])
            fi = math.atan2(A_matrix[2][1],A_matrix[2][2])
        else: #ako je zapravo =-1
            psi = math.atan2(-A_matrix[0][1],A_matrix[1][1])
            teta = math.pi/2
            fi = 0
    else: #ako je zapravo = 1
        psi = math.atan2(-A_matrix[0][1],A_matrix[1][1])
        teta = -math.pi/2
        fi = 0

    return  psi,teta,fi

#funkcija koja od vektora oko koga se rotira za ugao koliko se rotira neki objekat vraca kvaternion koji zapravo predstavlja tu Rotaciju
def AngleAxis2Q(p_vector, fi):

#ako je fi = 0 onda je w = cos0 = 1,pa samim tim sin(0) = 0 i ceo vector v_jedinicni je zapravo 0 vektor
#q = [(0,0,0),1] = 0*x + 0*y + 0*z + w = 1
    if fi == 0:
        return [0,0,0,1]

    w = math.cos(fi/2)
    p_vector = jedinicni(np.asarray(p_vector))
    [x,y,z] = math.sin(fi/2)*p_vector
#kvaternion je oblika [v_jedinicni * sin(fi/2),cos(fi/2)]
    q = [x,y,z,w]
    return  q

#funkcija inverzna funckiji AngleAxis2Q jer prime kvaternion a kao izlaz vraca vektor p i ugao fi
def Q2AngleAxis(q):
    #nalazimo jedinicni vektor q
    q_vector = jedinicni(np.asarray(q))
    #na poslednjoj poziciji u kvaternionu krije se w = cos(fi)
    if q_vector[3] < 0:
        q_vector = -q_vector

    fi = math.acos(q_vector[3]) * 2
    #ukoliko je q_vecor[3] tj. w = 1 ili w = -1 onda imamo da je ugao rotacije zapravo 0 stepini tako da uzimamo bilo koji vektor za p_vector
    if abs(q_vector[3]) == 1:
        return  ([1,0,0],0)
    else:
        return (jedinicni(q_vector[:-1]),math.degrees(fi))


def main():

    #njihov test primer
    print("Euler2A algoritam za ulaz(Ojlerove uglove): ",math.atan(4),-math.asin(8/9),-math.atan(1/4))
    A = Euler2A(math.asin(0.5),-math.asin(8/9),-math.atan(1/4))
    print("Izlaz je matrica A: \n",np.round(A, decimals=4))
    #moj test primer
    #psi,teta,fi = map(int , input("Unesite redom Ojlerove uglove Psi,Teta, Fi u stepenima: ").split())
    #A = Euler2A(math.radians(psi),math.radians(teta),math.radians(fi))
    #print(np.round(A,decimals=4))
    try:
        print("##########################")
        print("A2AngleAxis algoritam za matricu A:")
        print("Izlaz je vektor p i ugao fi: ")
        p_vector, fi = A2AngleAxis(A)
        print(p_vector, fi)
    except Exception as error:
        print("Doslo je do ispaljivanja izuzetka,vodite racuna!")
        print(error)

    print("##########################")
    print("Rodrigez algoritam koji kao ulaz prima vektor p i ugao fi: ")
    print("Izlaz je matrica A: ")
    A_matrix = Rodrigez(p_vector,fi)
    print(np.round(A_matrix,decimals=4))

    print('Da li su matrice A i A_matrix identicne?')
    print('A / A_matrix = \n',A / A_matrix)

    try:
        print("##########################")
        print("A2Euler algoritam koji kao ulaz prima matricu A: ")
        print("Ko izlaz vraca identicne Ojlerove uglove kao sa pocetka: ")
        psi,teta , fi = A2Euler(A)
        print(psi,teta, fi)
    except Exception as error:
        print("Doslo je do ispaljivanja izuzetka,vodite racuna!")
        print(error)

    print("##########################")
    print("AxisAngle2Q algoritam koji za ulaz prima vektor oko koga se rotira i ugao rotacije: ")
    p_vector = [1/3, -2/3, 2/3]
    fi = math.pi/2
    print("Vektor oko koga se rotira: ",p_vector)
    print("Ugao rotacije: ", math.degrees(fi))
    print("Kao izlaz vraca kvaternion tj.vektor dimenzije 4: ")
    q_vector = AngleAxis2Q(p_vector,fi)
    print(q_vector)

    print("##########################")
    print("Q2AngleAxis algoritam koji kao ulaz sada prima prethodni_kvaternion: ")
    print(q_vector)
    print("Kao izlaz vraca vektor p oko koga se rotira za ugao fi: ")
    print(Q2AngleAxis(q_vector))




if __name__ == '__main__':
    main()