#!/usr/bin/python3

import numpy as np

def vrati_afine(point):
	
	if point[-1] != 0:
		afin_coords = [round(x/point[-1]) for x in point]
		afin_coords.pop()
		return afin_coords
	
	raise "Deljenje nulom"

def nevidljivo(points):
	
	#prava p1 nastaje od tacke C i tacke F
	p1 = np.cross(points[2],points[5])
	#prava p2 nastaje od tacke B i tacke E
	p2 = np.cross(points[1],points[4])
	yb = np.cross(p1,p2)
	
	#prava q1 nastaje od tacke B i tacke C
	q1 = np.cross(points[1],points[2])
	#prava q2 nastaje od tacke A i tacke D
	q2 = np.cross(points[0],points[3])
	xb = np.cross(q1,q2)
	
	#konacno, tacka xb i G daju pravu a1
	a1 = np.cross(xb,points[6])
	#konacno , tacka yb i A daju pravu a2
	a2 = np.cross(yb,points[0])
	
	nevidljivo_teme = vrati_afine(np.cross(a1,a2))
	return nevidljivo_teme

def main():
	
	points = []
	#korisnik unosi koordinate za 7 tacaka
	i = 0
	while(i < 7):
		x = int(input("Enter x coordinate for {}. point: ".format(i)))
		y = int(input("Enter y coordinate for {}. point: ".format(i)))
		#ovde odmah formiramo homogene dodajuci i z koordinatu(z=1)
		points.append([x,y,1])
		i+=1
		
	nevidljivo_teme = nevidljivo(points)
	print(nevidljivo_teme)

if __name__ == '__main__':
	main()
