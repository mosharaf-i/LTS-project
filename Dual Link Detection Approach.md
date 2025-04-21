# Dual Link Detection and Representation:

This document is presenting my thought process in assessing, analysing, and coming up with a code to find links in the database that are part of one street, but are shown as two seperate entity.
For analysing the crossing LTS, which was developed later in the project, we needed to find intersections that if part of a dual link, are part of only one intersection, and not two.

## Dual link detection:
Two types of dual link detection:

1.	Both part of the dual link has intersection with another street:(Most of the intersections) 
Only 1 QGIS process: line-line intersection
<p align="center">
  
<img width="414" alt="image" src="https://github.com/user-attachments/assets/b7616d5f-98f9-4ecb-b35e-18804abac8a7" />
</p>

In this intersection we have:
- Same name
- Same intersect link name.
- Opposite SENS_CIR
- (No need for a buffer)

In this type, each street has 2 matching streets as a result. Only the opposite side should be selected:
The parts with different names and Sens_CIR

2.	Only one side of the dual like has intersection with another street.
(Few intersections)
<p align="center">
  
<img width="464" alt="image" src="https://github.com/user-attachments/assets/b8e765f8-5bdf-47d9-9571-6a0bd51d788d" />

  
</p>

In this case we need a buffer to catch the other side. (Buffer = 16 m for now, but du Park>16 m)

In this case: 
- Same name
- Opposite SENS_CIR
- No link between two sides.
This method for Type 2 also includes Type 1 intersections but it’s slower, because of the higher amount of data for processing.

## Questions and Errors:
-	Saint-Joseph / Clark & Saint-Joseph/Drolet doesn’t have a link representation in Geobase, although bikes can pass it.
-	Jean-Talon/Graham/Dresden: very complicated situation:)
-	From the meeting: Atwater/Duvernay: confusing intersection with island and No Bike/Pedestrian sign?!

## Method 3: Peter’s Suggestion
Buffers at the intersection and midpoint of each link. (Working with ID_TRC)
1. Buffers at the intersections 
2. Buffers at each links midpoint

- If both buffers capture the same 2 links → the links are dual matches
- The link connecting them → the short link we’re looking for!
  
<p align="center">
  
![image](https://github.com/user-attachments/assets/2752a5db-c49a-4ea1-b2dd-bf683dbb65a9)
</p>

This method is very good with the simple situation, like Figure 1. 
Some errors appear when there is more complicated situation: 
(Blue links are identified as dual representations and orange links are identified as connecting links)
1.	Separating links (Fork): Avenue Park.
   
<p align="center">
  
![image](https://github.com/user-attachments/assets/c020db2b-f104-4b08-b80d-8e596472c5d8)
</p>

2.	Loops: Avenue Ridgewood
   
   <p align="center">
     
![image](https://github.com/user-attachments/assets/edf4fcd2-9d38-4c26-95d3-030072e5cd08)
</p>

3.	Complicated intersections:
 
   <p align="center">
     
![image](https://github.com/user-attachments/assets/7b7b3cd7-01b9-4dce-bca0-4c3ca86342f7)
</p>

Methods to overcome tested:
- Limitation of the length: several lengths were tested and length < 20 m wworked! (Voila!)

Beside midpoint, 5% & 95% of the links were also tested. However, the errors were more than considering the midpoints.

## Catching the small links represented in 2 links (e.g. Sherbrooke Est st.)

<p align="center">
  
![image](https://github.com/user-attachments/assets/fcfee61d-6215-4f10-a1ad-7f05cb19e113)
</p>

Table 1. Three identified link IDs in each intersection

|  Intersection | ID_TRC_1 | ID_TRC_2 | ID_TRC_3 |
|----------|----------|----------|----------|
| Intersection A    | C     | D     | E     |
| Intersection B    | F     | E     | D     |


After finding the dual links and selecting them, test the phrase: 

If: 
  ID_TRC_2 (A) == ID_TRC_3 (B) And ID_TRC_2 (B) == ID_TRC_3 (A)

Then: E & D are the links. 

This method catches some extra links too (dog leg).
- Rue de Bullion
- Avenue de l’Hotel-de-Ville 
<p align="center">
  
![image](https://github.com/user-attachments/assets/5432f1d6-044e-4dbc-9c68-a68e6d0603e2)
</p>




