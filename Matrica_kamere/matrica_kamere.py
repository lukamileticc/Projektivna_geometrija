import numpy as np
from numpy import linalg as la

#ulaz je matrica kamere T(3x4),funkcija vraca parametre kamere redom K,A,C
def parametri_kamere(T):
    #prvo odredjujemo centar kamere C u odnosu na svetske koordinate
    #to je tkzv. null prostor matrice T*C=0 -- koristimo Sarusovo pravilo
    C = np.zeros(4).reshape(1,4)
    C[0][0] = la.det(np.array(T[:,1:]))
    C[0][1] = -la.det(np.asarray(T[:,[0,2,3]]))
    C[0][2] = la.det(np.asarray(T[:,[0,1,3]]))
    C[0][3] = -la.det(np.asarray(T[:,:-1]))
    C /= C[0][3]
    C = C[0,:-1]
    #primenjujemo u sustini QR dekompoziciju(Gram Smitov postupak)
    T0 = np.asarray(T[:,:-1])
    if la.det(T0) < 0:
        T0 = T0*-1
    Q,R = la.qr(la.inv(T0))
    #posto qr algoritam ne vodi racuna o determinantama moramo voditi racuna o znakovima
    for i in range(3):
        if R[i][i] < 0:
            R[i,:] *= -1
            Q[:,i] *= -1
    #od ovoga treba da dobijemo K i A
    # K = R^-1 , A = (Q^-1) ----> Q^T = Q^-1 jer Q*Q^T = E
    K = np.dot(T0,Q)
    K = la.inv(R)
    K /= K[-1,-1]
    A = np.transpose(Q)

    return K,A,C

#funkcija za date originalne tacke(u prostoru) i za date projekcije(piksel koordinate na slici) vraca matricu kamere 3x4
def camera_dlp(original_points,image_points):

    #kao kod dlt algoritam pravimo matricu (2*n)x12 gde je n broj tacaka,a imamo 12 nepoznatih ,znaci minum 6 tacaka
    n = len(original_points)
    matrix = np.zeros((2 * n, 12))
    i = 0
    for src, dst in zip(original_points, image_points):
        x, y, z, t = src[:]
        h, c, v = dst[:]
        matrix[i] = [0, 0, 0, 0 , -v * x, -v * y, -v * z,-v * t, c * x, c * y, c * z, c * t]
        matrix[i + 1] = [v * x, v * y, v * z, v * t, 0, 0, 0, 0, -h * x, -h * y, -h * z, -h * t]
        i += 2

     #Radimo SVD dekompoziciju matrice A i uzimamo poslednju vrstu poslednje matrice u nizu
    U, S, V  = la.svd(matrix)
    #print(V.shape) ---> 12x12
    T = V[-1].reshape(3,4)

    return  T/T[0,0]

def main():

    #primenjujemo fukciju parametri_kamere na test_primer Matricu T
    n = 1 #broj_indeksa = 91 za test_primer(poslednja cifra)
    T = np.asarray([[5, -1-2*n, 3, 18-3*n],
                    [0, -1 , 5, 21],
                    [0, -1, 0 , 1]])
    K,A,C = parametri_kamere(T)
    print("Matrica kalibracija kamere K: \n",K)
    print("Matrica rotacije kamere A: \n", A)
    print("Centar kamere: C: \n", C)
    print("#########################################")
    # n originala i n projekcija ---- > n >= 6
    i = 1  # poslednja cifra broja indeksa(91)
    # originali
    m1 = [460, 280, 250, 1]
    m2 = [50, 380, 350, 1]
    m3 = [470, 500, 100, 1]
    m4 = [380, 630, 50 * i, 1]
    m5 = [30 * i, 290, 0, 1]
    m6 = [580, 0, 130, 1]
    # projekcije
    m1p = [288, 251, 1]
    m2p = [79, 510, 1]
    m3p = [470, 440, 1]
    m4p = [520, 590, 1]
    m5p = [365, 388, 1]
    m6p = [365, 20, 1]
    original_points = [m1, m2, m3, m4, m5, m6]
    image_points = [m1p, m2p, m3p, m4p, m5p, m6p]
    T = camera_dlp(original_points,image_points)
    np.set_printoptions(suppress=True)
    print("Matrica projekcije T: \n",np.round(T,decimals=4))

if __name__ == '__main__':
    main()