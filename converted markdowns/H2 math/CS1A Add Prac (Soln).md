## **RAFFLES INSTITUTION H2 Mathematics (9758) 2026 Year 6** 

## **Additional Practice Questions for Chapter S1A: Permutations and Combinations** 

- **1** In how many ways can a committee of 3 men and 3 women be chosen from a group of 7 men and 6 women? [2] 

The oldest of the 7 men is _A_ and the oldest of the 6 women is _B_ . It is decided that the committee can include at most one of _A_ and _B_ . In how many ways can the committee now be chosen? [3] [700, 550] 

## **9205/2001/01/Q7** 

## **Solution:** 

7 6 Number of ways to form a committee  _C_ 3  _C_ 3  700 

To form a committee which include at most one of _A_ and _B:_ 

Method 1: Consider complement 

7 6 Number of ways without restriction  _C_ 3  _C_ 3  700 6 5 Number of ways which include both _A_ and _B_  _C_ 2  _C_ 2  150 Number of ways which include at most one of _A_ and _B_  700  150  550. 

Method 2: Consider cases 

Case 1: _A_ is included but not _B_ 6 5 Number of ways  _C_ 2  _C_ 3  150 

Case 2: _B_ is included but not _A_ 6 5 Number of ways  _C_ 3  _C_ 2  200 

Case 3: Both _A_ and _B_ are not included 6 5 Number of ways  _C_ 3  _C_ 3  200 

Number of ways which include at most one of _A_ and _B_  150  200  200  550 

_______________________________________________ Additional Practice S1A: Permutations and Combinations 

Page 1 of 14 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

- **2** A box contains 9 balls. Out of these 9 balls, there are 3 identical red balls, 2 identical yellow balls and 4 numbered green balls (each labelled with a different number from 1 to 4). 3 balls are to be picked out of the box, and the order in which they are picked out does not matter. Find the number of possible selections of 3 balls. [3] [31] 

## **SAJC Prelim 9740/2012/02/Q6** 

## **Solution:** 

From 3 identical red balls, 2 identical yellow balls, 4 numbered green balls, we have 6 types of distinct balls. 

Case 1: All three balls distinct Number of possible selections of 3 balls is[6] _C_ 3 

Case 2: Exactly two identical balls (AAB) 5 Number of possible selections =[2] _C_ 1  _C_ 1 (2 types of balls available to choose the 2 identical balls from, then 5 types of balls remaining to choose the last ball) 

Case 3: All three balls are identical (AAA). Number of possible selections = 1 

 Total number of possible selections is 20+10+1=31 

- **3** How many 6-digit numbers 

   - **(i)** are even? 

   - **(ii)** begin and end with different digits? 

[ **(i)** 450000, **(ii)** 810000] 

## **Solution:** 

- **(i)** Number of choices for the first digit = 9. Number of choices for each of the 2[nd] , 3[rd] , 4[th] and 5[th] digit = 10. For the 6-digit number to be even, number of choices for the last digit = 5. 

Total number of 6-digit numbers that are even = 9  10[4]  5= 450000. 

- **(ii)** Number of choices for the first digit = 9. 

 Since the first and last digits are different, number of choices for the last digit = (10 1) = 9. Number of choices for each of the 2[nd] , 3[rd] , 4[th] and 5[th] digit = 10. 

Total number of 6-digit numbers that begin and end with different digits = 9  9  10[4] = 810000 

_______________________________________________ Additional Practice S1A: Permutations and Combinations 

Page 2 of 14 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

- **4** Find the number of distinct arrangements of the letters of the word ' _THERMOMETER_ ' 

   - **(i)** if at least 2 ' _E_ 's are together, 

   - **(ii)** which must start and end with ' _T_ ' or ' _R_ '. 

[ **(i)** 408240, **(ii)** 90720] 

## **AJC Prelim 9233/2003/01/Q7** 

## **Solution:** 

**(i)** There are 11 letters, with 3 'E's, 2 'T's, 2 'M's and 2 'R's, 1 ‘O’, 1 “H” We will use the Complement Method. 11! First find the number of ways to arrange without restriction = 3!2!2!2![= 831600. ] 

Then find the number of ways E’s are separated using the Slotting Method: 

 T  H  R  M  O  M  T  R  8! Number of ways to arrange the 2T, 2M, 2R, 1O, 1H = 2!2!2![= 5040 ] The 3 ‘E’s can occupy 3 out of the remaining 9  slots in[9] C3 = 84 ways. Number of ways such that the 3 'E's are always separated = 5040  84 = 423360. Therefore, using the Complement Method, number of ways such that at least 2 'E's are together = 831600  423360 = 408240 

**(ii)** Case 1: The arrangement starts and ends with 'T' 9! Number of ways = 3!2!2![= 15120. ] Case 2: The arrangement starts and ends with 'R' A similar argument as Case 1 gives number of ways = 15120. Case 3: The arrangement starts with 'T' and ends with 'R' 9! Number of ways = 3!2![= 30240. ] Case 4: The arrangement starts with 'R' and ends with 'T' A similar argument as Case 3 gives number of ways = 30240. Total number of ways = (15120  2) + (30240  2) = 90720 

_______________________________________________ Additional Practice S1A: Permutations and Combinations 

Page 3 of 14 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

- **5** How many 4-digit numbers greater than 5000 can be formed from the digits 0, 1, 2, 3, 4, 5 if 

   - **(i)** no digit may be repeated? 

   - **(ii)** any digit may be repeated? 

   - **(ii)** only the digit 4 may be repeated? 

- [ **(i)** 60, **(ii)** 215, **(iii)** 73] 

**Solution: (i)** The first digit must be '5', so only 1 way for the first digit. For the next 3 digits, we choose from 0,1,2,3,4 and arrange them. Hence the number of ways = 1 ×[5] P3 = 60 **(ii)** Number of choices for the first digit = 1 Since any digit may be repeated, number of choices for each of the 2[nd] , 3[rd] and 4[th] digits is 6 Since we want a 4-digit number **greater** than 5000, we need to subtract one number, which is 5000 itself. Therefore, number of ways = (1  6[3] )  1 = 215 **(iii)** There is only 1 choice for the first digit. We shall consider cases for the last 3 digits. Case 1:   The last 3 digits are all different From **(i)** , number of ways =[5] P3 = 60. Case 2:   Two of the last 3 digits are the digit '4's There are[4] C1 = 4 choices for the remaining digit (0, 1, 2 or 3). Since the order 3! matters and there are 2 identical digits, number of ways = 4  2![= 12. ] Case 3:  The last 3 digits are all digit '4's Number of ways = 1. Total number of ways = 60 + 12 + 1 = 73 

_______________________________________________ Additional Practice S1A: Permutations and Combinations Page 4 of 14 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

- **6** A school is asked to send a delegation of six pupils selected from six badminton players, six tennis players and five squash players. No pupil plays more than one game. The delegation is to consist of at least one, and not more than three, players drawn from each sport. Giving full details of your working, find the number of ways in which the delegation can be selected. 

[9450] 

## **9205/1989/01/Q19(b)** 

## **Solution:** 

We use Systematic Listing and consider 7 cases. 

**==> picture [399 x 141] intentionally omitted <==**

**----- Start of picture text -----**<br>
Number of  Number of  Number of  Number of ways to select<br>Badminton  Tennis players  Squash players  the 6 players<br>players(6) (6) (5)<br>1  2  3  6C1  6C2  5C3 = 900<br>1  3  2  6C1  6C3  5C2 = 1200<br>2  1  3  6C2  6C1  5C3 = 900<br>2  3  1  6C2  6C3  5C1 = 1500<br>3  1  2  6C3  6C1  5C2 = 1200<br>3  2  1  6C3  6C2  5C1 = 1500<br>2  2  2  6C2  6C2  5C2 = 2250<br>**----- End of picture text -----**<br>


Total number of ways = 900 + 1200 + 900 + 1500 + 1200 + 1500 + 2250 = 9450. 

- **7** Seven cards each have a single digit written on them. The digits on the seven cards are 2, 2, 5, 7, 7, 7, 7 respectively. Find the number of different 4-digit numbers that can be formed by placing four of the cards side by side. [4] [39] 

## **Solution:** 

**==> picture [374 x 205] intentionally omitted <==**

**----- Start of picture text -----**<br>
4 cards selected  Number of 4-digit numbers that can<br>be formed<br>Case 1  7, 7, 7, 7  1<br>Case 2  7, 7, 7, 2  4!<br>4<br>3! []<br>Case 3  7, 7, 7, 5  4!<br>4<br>3! []<br>Case 4  7, 7, 2, 2  4!<br>6<br>2!2! []<br>Case 5  7, 7, 2, 5  4!<br>12<br>2! []<br>Case 6  7, 5, 2, 2  4!<br>12<br>2! []<br>**----- End of picture text -----**<br>


Number of different 4-digit numbers that can be formed  1 4  4  6  12  12  39 

_______________________________________________ Additional Practice S1A: Permutations and Combinations 

Page 5 of 14 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

- **8** A rectangular table has 7 secured seats, 4 being on one side facing the window and 3 being on the opposite side. In how many ways can 7 people be seated at the table 

   - **(i)** if 3 people, X and Y and Z must sit on the side facing the window? 

   - **(ii)** if 2 people, P and Q must sit on opposite sides? 

[ **(i)** 576, **(ii)** 2880] 

## **Solution:** 

**==> picture [459 x 543] intentionally omitted <==**

**----- Start of picture text -----**<br>
(i)                                   WINDOW<br>If 3 people, X and Y and Z must sit on the side facing the window<br>We choose one more person to sit on the same side as X, Y, Z. Number of choices =  [4] C 1  = 4<br>The people in each row can be permuted within the row.<br>Total number of arrangements = 4 x 4! x 3! = 576<br>Alternative 1:<br>Number of ways to arrange 3 out of the remaining 4 people to sit on the side near the<br>window =  [4] P3<br>Number of ways to arrange X, Y, Z and the 4 [th]  person = 4!<br>Total number of arrangements =  [4] P3   4! = 576<br>Alternative 2:<br>Number of ways to choose 3 seats for X, Y, Z, and arrange them =  [4] C 3  3!<br>Number of ways to arrange the remaining 4 people = 4!<br>Total number of arrangements =  [4] C 3  3!   4! = 576<br>(ii)  Case 1:  P is on the side with 4 seats, Q on  Alternative method:<br>the side with 3 seats.<br>Just like in  (i) , we choose 3 people to sit with  Case 1: P sits on the side with 4 seats<br>P (or 2 people to sit with Q), and permute  Number of ways to choose a seat for P =  [4] C 1<br>within the rows.<br>5 Number of ways to choose a seat for Q =  [3] C 1<br>Number of choices   C 3  4!  3! Number of ways to arrange the remaining 5<br>people = 5!<br>Case 2: Q is on the side with 4 seats and P is on the side with 3 seats.  Number of ways   4 C 1  3 C 1  5!<br>Number of choices is as above.<br>Case 2: Q sits on the side with 4 seats<br>Number of ways is as above.<br>Hence, total number of choices<br>5<br> C 3  4!  3!  2  2880 Total number of ways<br>4 3<br> C 1  C 1  5!  2  2880<br>**----- End of picture text -----**<br>


_______________________________________________ Additional Practice S1A: Permutations and Combinations 

Page 6 of 14 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

- **9** 4 boys, 4 girls and a teacher are to be seated at a round table. How many ways can they be arranged if 

   - **(i)** there is no restriction? 

   - **(ii)** the teacher is to be seated between any 2 girls? 

   - **(iii)** none of the boys are to be seated together? 

[ **(i)** 40320, **(ii)** 8640, **(iii)** 2880] 

~~pe~~ **Solution: (i)** Number of ways with no restriction = (9 – 1)! = 40320 **(ii)** The number of ways to choose 2 girls to sit next to the teacher is[4] C2. Hence the teacher can be seated between any 2 girls in[4] C2  2! = 12 ways. Consider the teacher between any 2 girls as one unit: G   G    B    B    B    B   GTG Number of ways = 12  (7 – 1)! = 8640 ~~fo~~ **(iii)** We first seat the teacher and 4 girls. Number of ways = (5 – 1)! = 24. G G G G A T Using the Slotting Method, number of ways such that none of the boys are seated together = 24 [5] P4 = 2880 ~~OO “Or~~ 

_______________________________________________ Additional Practice S1A: Permutations and Combinations 

Page 7 of 14 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

- **10** Three couples who each have a child are to be seated at a round table with ten secured seats. Find the number of ways the nine people can be seated if 

   - **(i)** they do not mind who they are sitting with, [1] 

**(ii)** none of the children are to be seated on adjacent seats. [3] 

Mr Bean, who knows the three families well, is invited to take a seat at the table. Find the number of ways to seat the ten people if each child is to be seated adjacent to both his or her parents. [3] [ **(i)** 362880; **(ii)** 151200, 48] 

## **RI Y6 CT2 9740/Q8** 

## **Solution:** 

**(i)** Considering the empty seat as a distinct object, this is an arrangement of 10 distinct objects in a circle.  Number of ways  (10  1)!  362880 **(ii)** Consider the 6 adults and empty seat as 7 distinct objects.   Number of ways of arranging them in a circle (7 1)! Number of ways to slot and arrange the 3 children in 3 of the 7 spaces between the 7 distinct 7 7 objects  _P_ 3 or _C_ 3  3!  Number of ways in which none of the children are seated on adjacent seats  (7  1)!  7 _P_ 3  151200 Consider each couple and their child as a unit.   Number of ways of arranging 4 distinct units in a circle (4 1)! Each couple can arrange amongst themselves in 2! ways. 

3  Number of ways in which each child is seated between their parents  (4  1)!  2!  48 

_______________________________________________ Additional Practice S1A: Permutations and Combinations 

Page 8 of 14 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

- **11** The following diagram shows 12 **distinct** points on the sides of a triangle _ABC_ . 

   - **(i)** How many line segments are there joining any two points on different sides? 

   - **(ii)** How many triangles can be formed by joining any one point on side _AB_ , any one point on side _BC_ and any one point on side [ **(i)** 47, **(ii)** 60] 

   - _AC_ ? 

- **Solution: (i)** Number of ways to join a point on side _AB_ to any point on the other two sides = 3  9 = 27 Number of ways to join a point on side _BC_ to a point on side _AC_ = 4  5 = 20. Total number of ways to form a line segment = 27 + 20 = 47. 

- **(ii)** Choose a point on each of the 3 sides, thus number of ways =[3] C1 [4] C1 [5] C1= 60 

- ~~a~~ 

- **12** Six identical boxes are arranged in 3 rows as shown in the following diagram. 

Top Row Middle Row Bottom Row 

Sandra is given 1 green, 2 blue and 3 red balls. The balls are identical except for their colour. She is to put one ball in each box.  Find the number of ways she can do this when 

**(i)** there is no restriction, [2] **(ii)** the balls in the bottom row are of different colours, [2] **(iii)** there are at least 2 red balls in the bottom row. [3] [ **(i)** 60, **(ii)** 18, **(iii)** 30] **MI Prelims 9740/2013/02/Q6 Solution: (i)** 6! Number of ways with no restriction is 60 2!3![] ~~TS~~ **(ii)** 3! Number of ways to place 1 blue and 2 red balls into top and middle row boxes is 2! Number of ways to place 3 different balls into bottom row boxes is 3! Number of ways such that the balls in the bottom row are of different colours is 3!(3!)  18 2! **(iii)** Number of ways such that there are at least 2 red balls in the bottom row 3! 3! 3! 3! = 2!  2!(3!)  2!. 2!  30 3R bottom     2R+1B bottom    2R+1G bottom ~~je. =~~ _______________________________________________ 

Additional Practice S1A: Permutations and Combinations 

Page 9 of 14 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

- **13** There are nine **different** waterslides at an amusement park. A person is allowed to go on each slide once only. However, he can choose to skip the slide or go on it. 

   - **(i)** If John goes on at least two slides at the amusement park, how many ways can he select the slides to go on? 

   - **(ii)** At another theme park, there are _n_ different slides. John visits the theme park frequently and selects 2 slides to go on during every visit. At each visit, he makes a different selection, and first realizes that this was no longer possible on the 29th visit. Determine algebraically, the value of _n_ . 

   - **(iii)** Give an example of a situation involving waterslides to which the expression 

_n_ ! is the solution. _r_ !( _n_  _r_ )! 

[ **(i)** 502, **(ii)** _n_  8] 

## **Solution:** 

**(i)** Consider the first slide. John can choose to go on the slide or skip the slide, so he has 2 choices for the 1[st] slide. Similarly, he has 2 choices for each of the other 8 slides. 9 Number of selections for all 9 slides  2  2 2 2 2 2 2 2 2  2  512 . 

However, in one of these selections, all the slides were skipped. Also, number of ways John can choose only one slide to go on =[9] C1= 9. 

Thus, using the Complement Method, number of ways John can choose at least two slides to go on = 512  1  9 = 502. 

**(ii)** There are 28 different selections of 2 slides out of _n_ slides. Thus _[n]_ C2 = 28. 

_n_ ! _[n]_ C2 =  28 2!( _n_  2)! _n_ ( _n_  1)   28 2 _n_ 2  _n_  56  0 ( _n_  8)( _n_  7)  0 Therefore _n_ = 8 or _n_ =  7 (Reject since _n_ is a positive integer). 

_x_ OR: Use GC Table of values with _y_ 1  _C_ 2 

**(iii)** The number of ways to choose _r_ waterslides to go on out of _n_ slides. 

OR: The number of ways to choose _r_ waterslides to skip (i.e. not to go on) out of _n_ slides. 

_______________________________________________ Additional Practice S1A: Permutations and Combinations 

Page 10 of 14 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

- **14** Ten chefs, six males and four females, qualify for the final phase of a ‘Top Chef’ competition consisting of nine ‘Elimination Challenges’. One chef is eliminated after every challenge and the last chef remaining is the winner of the competition. 

   - **(i)** In how many ways can the eliminations be done? [1] 

   - **(ii)** For the first challenge, the ten chefs are divided into two groups of five. In how many ways can the two groups be formed such that each group has at least one female chef? [2] 

   - **(iii)** After the first challenge, a particular male chef was eliminated. At a photography session before the next challenge, nine chairs are arranged in two rows: four in front and five at the back. In how many ways can the remaining chefs be arranged so that the male chefs and the female chefs must alternate? [3] [ **(i)** 3628800, **(ii)** 120, **(iii)** 5760] 

## **ACJC Prelim 9740/2013/02/Q7 modified** 

## **Solution:** 

**(i)** Number of ways of eliminations is 10! =3 628 800 

**(ii)** Method 1 **:** By Complement Required number 

 = (Number of ways to form 2 groups of 5 without restriction) (Number of ways where one group has no female chefs) = 10 _C_ 5  6 _C_ 5  120 2! 

Method 2: 

Case 1: one group has 1 female chef, the other has 3 female chefs. 

Number of ways to form the groups is equivalent to number of ways to form the group of 1 female chef and 4 male chefs[6] _C_ 4  4 _C_ 1  60 Case 2: both groups have exactly 2 female chefs. 

Number of ways to form the groups is 6 _C_ 3  4 _C_ 2  60 2! 

(Note that there is a need to divide by “2!” as both groups each consist of 2 female chefs and 3 male chefs) 

Total number of ways = 60 + 60 = 120 

**(iii)** Two cases for male and female chefs to alternate: _M F M F M M F M F M_ or _F M F M M F M F_ Number of ways = 5!  4!  2  5760 

_______________________________________________ Additional Practice S1A: Permutations and Combinations 

Page 11 of 14 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

- **15** 2 men and 5 women go to a restaurant. They choose an outdoor round table with 7 seats for their meal. Find the number of ways the group can be seated if 

   - **(i)** the two men are not seated next to each other. [2] 

   - **(ii)** one of the women, Mary, is to be seated between the two men. [2] 

Before their orders arrive, they request to shift to a table in the 'non-smoking' section of the restaurant. They are then given a round table with 10 seats. 

Find the number of ways they can be seated if 

**(iii)** the empty seats are adjacent to each other. [2] 

- **(iv)** none of the empty seats are adjacent to each other and there must be more than 1 person between any two empty seats. [2] [ **(i)** 480, **(ii)** 48, **(iii)** 5040, **(iv)** 5040] 

## **TJC Prelim 9740/2012/02/Q5** 

## **Solution:** 

**(i)** Complement method: Number of ways = (Total number of ways) – (Number of ways men are together)  6!   5! 2!  480 Slotting method (Arrange women first, then slot in men): Number of ways =  5  1  !  5 _P_ 2  480 

**(ii)** Group Mary and the 2 men as one unit. Number of ways   5  1  !  2!  48 

- **(iii)** Group 3 empty seats as one unit. Number of ways   8  1  !  5040 

- **(iv)** Method 1 

The condition of more than 1 person 

between empty chair leads to the 

following unique configuration where 

the “arrow” is the empty chair. 

- Method 2 

Seat the 7 people around the table in (7  1)!  6! 

ways. Insert the first empty chair in 7 possible slots, (only 1 such “2-3-2” configuration) followed by the next empty chair with 2 persons between the first and second empty chair and the last empty chair with 3 persons in between the second and last empty chair. 

There are 7!  5040 ways to seat 7 people in the distinct positions A, B, C, D, E, F, G. 

**==> picture [100 x 92] intentionally omitted <==**

**----- Start of picture text -----**<br>
G<br>A<br>F<br>B<br>E C<br>D<br>**----- End of picture text -----**<br>


Number of ways = (6!)7  7! = 5040 

_______________________________________________ Additional Practice S1A: Permutations and Combinations Page 12 of 14 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

- **16 (a)** A student is arranging 4 blue flags, 4 red flags, 1 green, 1 yellow and 1 purple flag in a line. All the flags are identical except for the colour. Find the number of different possible ways to arrange the flags if 

   - **(i)** the green, yellow and purple flags must be placed together, [2] **(ii)** no blue flags are placed next to each other, [2] **(iii)** a red flag at the beginning and another red flag at the end of the line. [2] 

   - **(b)** Ten people at a company dinner consist of 7 guests and 3 hosts. The group is to be seated at a round table. 

      - **(i)** Find the number of arrangements such that there are at least two guests seated between any two hosts. [3] 

      - **(ii)** Two particular guests could not make it to the dinner. Find the number of ways to arrange the remaining guests and hosts with 10 identical chairs. [3] 

[ **(a)(i)** 3780, **(a)(ii)** 14700, **(a)(iii)** 7560, **(b)(i)** 30240, **(b)(ii)** 181440] 

## **NJC Common Test 9740/2012/02/Q4** 

## **Solution:** 

|**NJC Common Test 9740/2012/02/Q4**|**NJC Common Test 9740/2012/02/Q4**|
|---|---|
|**Solution:**||
|**(a)**<br>**(i)**|Consider the green, yellow and purple flags as 1 unit.<br>Number of ways to arrange the unit with the rest of the flags =<br>9!<br>4!4!<br>Number of ways to arrange the green, yellow and purple flags within the unit = 3!<br>Thus, number of possible arrangements for the flags =<br>9!<br>3!<br>4!4!<br>=3780|
|**(a)**<br>**(ii)**|Use Slotting Method, i.e. arrange the non-blue flags first, then slot in the blue flags:<br>Number of ways to arrange the 4 red flags, 1 green, 1 yellow and 1 purple flag =<br>7!<br>4! <br>Number of ways to slot in the blue flags =8<br>4<br>C <br>Number of possible arrangements such that no blue flags are placed next to another<br>=<br>7!<br>4!8<br>4<br>C =14 700|
|**(a)**<br>**(iii)**|Since the flags at the beginning and end are red, there are only 2 red flags left to be arranged<br>in between.<br>Hence number of possible arrangements such that a red flag at the beginning and another red<br>flag at the end of the line is equivalent to arranging 4 blue flags, 2 red flags, 1 green, 1<br>yellow and 1 purple flag =<br>(4<br>2<br>3)!<br>4!2!<br><br><br>= 7560|



_______________________________________________ Additional Practice S1A: Permutations and Combinations Page 13 of 14 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

**==> picture [450 x 252] intentionally omitted <==**

**----- Start of picture text -----**<br>
(b)  Seat the 7 guests around the table in  (7  1)!  6! ways.   G  J<br>(i)<br>A<br>Insert the first host in 7 possible slots, followed by the next  F<br>B<br>host with 2 guests between the first and second hosts and<br>the last host with 3 guests in between the second and last  E  C<br>D<br>hosts. Since the three hosts are distinct, there are  3! ways to<br>permute them.<br>  Number of ways =  (6!)  7 3!  30240<br>(b)  5 guests, 3 hosts and 2 empty identical chairs<br>(ii)<br>If the 2 empty chairs are distinct, number of ways to arrange the 8 people and 2 empty chairs<br>round a table =  9!<br>9!<br>Since the 2 chairs are identical, required number of ways is  181440<br>2! []<br>**----- End of picture text -----**<br>


## **THE END** 

_______________________________________________ Additional Practice S1A: Permutations and Combinations 

Page 14 of 14 

