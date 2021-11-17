#!/usr/bin/python3.8
from cv2 import cv2
import  numpy as np
from numpy import linalg as la
import math

pixels = []
intro = True

def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_FLAG_LBUTTON:
       #print(f'Pikseli: [{x},{y}]')
       if len(pixels) != 4:
            pixels.append([x,y,1])

def print_menu():
    print("###############################################################################")
    print("Please press 4 points in the image with mouse leftclick that from a rectangle!")
    print('To show pixels of 4 points that you\'ve pressed, press SPACE!')
    print('To remove projective distorsion, press Shift!')
    print("To exit picture press ESC!")
    print("###############################################################################")

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
    #ili posladnje kolona V^T
    V = np.transpose(V)
    P_matrix = np.asarray(V[:,-1])
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
   # p2_matrix = from_canonical_to_random(image_points)

   # return p2_matrix.dot(p1_inverse_matrix)
    return  p1_inverse_matrix

def remove_distorsion(points,image):
    global intro
    if intro == False:
        print("You have already press the SHIFT!")
        return
    if len(pixels) != 4:
        print("Please press 4 points on image!")
        return

    ##ovde otklanjamo distorziju!
    perspective_matrix = DLT_algoritam(pixels,[[500,400,1],[800,400,1],[800,500,1],[500,500,1]])
    dst = cv2.warpPerspective(image,perspective_matrix,(1300, 900))

    cv2.imshow('After',dst)
    intro = False

def main():

    cv2.namedWindow('Before')
    cv2.setMouseCallback('Before',onMouse)
    image = cv2.imread('otklanjanje_distorzije_before.png')
    print(image.shape)
    print("To open the menu, press ENTER!")

    while(True):
        cv2.imshow('Before',image)
        k = cv2.waitKey(0)
        if k == 27: #ESC is pressed
            break
        elif k == 32:
            print(pixels)
        elif k == 13:
            print_menu()
        elif k == 225 or k == 226:
            remove_distorsion(pixels,image)

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()