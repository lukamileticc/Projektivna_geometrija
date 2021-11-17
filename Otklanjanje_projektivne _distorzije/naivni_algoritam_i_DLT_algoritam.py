#!/usr/bin/python3
import numpy as np
from numpy import linalg as la
import math

def input_coords(points, text,num_of_points = 4):
    print(text)
    for i in range(0, num_of_points):
        print(f'----{i + 1}. tacka----')
        print('X Y Z koordinate: ')
        x, y, z = map(int, input().split())
        points.append([x, y, z])

def from_canonical_to_random(points):
    #naprravim matricu
    delta = np.array([points[0],
                      points[1],
                      points[2]])
    #transponujem je
    delta = np.transpose(delta)
    #izracunam determinantu
    det_value = la.det(delta)

    p_matrix = np.zeros((3, 3))
    for i in range(0, 3):
        #racunamo ostale delte
        coef = delta.copy()
        coef[:,i] = points[3]
        coef = la.det(coef)
        lambda_coef = coef / det_value
        p_matrix[:, i] = np.array(points[i]) * lambda_coef

    return  p_matrix

def naivni_algoritam(original_points,image_points):
    p1_inverse_matrix = la.inv(from_canonical_to_random(original_points))
    p2_matrix = from_canonical_to_random(image_points)

    return p2_matrix.dot(p1_inverse_matrix)

def DLT_algoritam(original_points,image_points):

    n = len(original_points)
    matrix = np.zeros((2*n,9))
    i = 0
    for src,dst in zip(original_points,image_points):
        x,y,z = src[:]
        h,c,v = dst[:]
        matrix[i] = [0, 0, 0 ,-v * x ,-v * y, -v * z, c * x, c * y, c * z]
        matrix[i+1] = [v *x, v * y, v * z, 0, 0, 0, -h * x, -h * y, -h * z]
        i+=2

    # print("Matrica A:")
    # print(matrix)
    # print("Radimo SVD dekompoziciju matrice A i uzimamo poslednju vrstu poslednje matrice u nizu")
    U, S, V = la.svd(matrix)
    #poslednja vrsta matrice V --> shape(9,9)
    V = np.transpose(V)
    P_matrix = np.asarray(V[:, -1])
    P_matrix = P_matrix.reshape(3,3)

    return P_matrix

def affinize(points):
    points = np.asarray(points)
    points =  np.asarray([point / point[2] for point in points])
    points = points.tolist()
    for point in points:
        point.pop()
    return points

def teziste(points):
    points = np.asarray(points)
    return np.sum(points,axis=0)/float(len(points))
def average_distance(points):
    points = np.asarray(points)
    tmp = np.sqrt(np.sum(points,axis=1))
    return teziste(tmp)
def normalize_points(points):
    # vratiti koordinate iz homogenih u afine
    affine_points = affinize(points)
    # trazimo teziste tacaka
    t = teziste(affine_points)
    translation_matrix = np.eye(3)
    translation_matrix[0][-1] = -t[0]
    translation_matrix[1][-1] = -t[1]
    affine_points = [point - t for point in affine_points]
    vectors_len = [point ** 2 for point in affine_points]
    d = average_distance(vectors_len)
    scaling_matrix = np.eye(3)
    scaling_matrix[0][0] = math.sqrt(2) / d
    scaling_matrix[1][1] = math.sqrt(2) / d
    # matrica normalizacije koju direktno primenjujemo na homogene koordinate
    T_matrix = np.asarray(scaling_matrix).dot(translation_matrix)
    T_matrix = np.asarray(T_matrix)
    points = [T_matrix.dot(point) for point in points]
    return points

def normalizovani_DLT_algoritam(src,dst):
    src = normalize_points(src)
    dst = normalize_points(dst)
    return DLT_algoritam(src,dst)

def main():
    #ucitavanje n originalnih tacaka i n njihovih slika
    original_points = []
    image_points = []
    n = int(input("Unesite broj tacka, a zatim i koordinate: "))
    input_coords(original_points, f'Unesite redom Homogene koordinate za {n} originalne tacke: ', n)
    input_coords(image_points, 'Unesite redom Homogene koordinate za njihove slike: ', n)

   #primenjujemo naivni algoritam
    if n == 4:
        print('Rezultat naivnog algoritma: ')
        mapping_matrix = naivni_algoritam(original_points,image_points)
        print(mapping_matrix / mapping_matrix[1][1])

    # #primenjujemo DLT algoritam
    print('Rezultat DLT algoritma')
    DLT_matrix = DLT_algoritam(original_points,image_points)
    DLT_matrix = DLT_matrix / DLT_matrix[1][1]
    np.set_printoptions(suppress = True)
    print(np.round(DLT_matrix,decimals=5))


    #primenjujemo modifikovani DLT algoritam
    print('Rezultat modifikovanog DLT algoritma')
    DLT_normalized_matrix = normalizovani_DLT_algoritam(original_points, image_points)
    DLT_normalized_matrix = DLT_normalized_matrix/DLT_normalized_matrix[1][1]
    np.set_printoptions(suppress=True)
    print(np.round(DLT_normalized_matrix, decimals=5))

    # print('Matrice poredimo tako sto DLT matricu podelimo sa DLT[1][1] pa pomnozimo sa P[1][1] gde je P matrica dobijena naivnim algoritmom')
    # print(DLT_matrix / DLT_matrix[1][1] * mapping_matrix[1][1])
    # print(mapping_matrix)


if __name__ == '__main__':
    main()