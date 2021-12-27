## Primena projektivne geometrije u racunarstvu

**Repozitorijum koji sadrzi resanja(programi,slike) zanimljivih problema koji su dati u okviru domacih zadataka.**


- **Zadatak: Nevidljive tacke**

    Slikati neki predmet koji ima oblik kvadra i na osnovu piksela njegovih vidljivih temena odrediti piksele nevidljivog temena.
    Program kao ulaz treba primiti koordinate(piksele) tih vidljivih temena,a kao izlaz treba ispisati piksele nevidljih temena.
    
    `Detaljniji opis zadatka, koriscenu sliku predmeta, kao i program mozete naci u repozitorijumu Domaci_1`
    
- **Zadatak:  Računanje projektivnog preslikavanja, otklanjanje projektivne distorzije**

    Napisan naivni algoritam, DLT(Direct linear transform) i modifikovani DLT(sa normalizacijom tacaka) algoritam koji vracaju matricu
    preslikavanja koja slika originalne tacke u njihove slike. Algoritmi primaju kao ulaz homogene koordinate originalnih tacaka kao i njihovih slika.
    
    `Napisana mini aplikacija koja koristi ove algoritme tako sto levim klikom misa izaberemo 4 originalne tacke na ucitanoj slici a kao izlaz dobijamo
    sliku sa eliminisanom projektivnom distorzijom.`

- **Zadatak: Algoritmi transformacija odnosno afinih preslikavanja koje cuvaju orijentaciju(Izometrije)**

    Zadatak je implementirati 6 funkcija koje vrse ove transformacije iz oblika u oblik. Oblici mogu biti: 
    
    - Vektor oko koga se rotira, ugao za koliko se rotira
    - Matrica rotacije A(3x3)
    - Ojlerovi uglovi 
    - Kvaternioni

- **Zadatak: Matrica kamere**
   
   Potrebno je implementirati 2 funkcije:
   - *ParametriKamere* ---> funkcija koja za datu matricu kamere T vraca redom matricu kalibracije K, matricu rotacije kamere A, i vektor-poziciju kamere u svetskim koord. C
   - *KameraDlp*  ---> funkcija koja za date originalne tacke u prostoru i za date projekcije(piksel koordinate na slici) vraca matricu kamere T 3x4 
    
   Dodatni primer: `Namestiti 3D scenu ,izabrati odgovarajuce tacke(da ne bude sve u istoj ravni) i odrediti im koordinate(mereci rastojanje od svetskog koordinatnog pocetka -- ugao sobe) i odrediti piksel koordinate projekcija. Sustina price je da pokrenemo KameraDlp koja ce nam vratiti matricu kamere T, onda pozovati ParametriKamere za tu matricu T, iz koje mozemo zakljuciti koordinate kamere u odnosu na svetski koordinatni pocetak(taj koji smo mi zadali), a mozemo zakljuciti i ziznu daljinu , crop translaciju , i naravno rotaciju kamere i trenutku slikanja.`
