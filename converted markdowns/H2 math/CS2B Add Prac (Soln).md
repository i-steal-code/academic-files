## **RAFFLES INSTITUTION H2 Mathematics (9758) 2026 Year 6** 

## **Additional Practice Questions for Chapter S2B: Binomial Distribution** 

- **1** Published articles in medical journals indicate that, on average, 35 out of 100 patients having a lumbar puncture will suffer SSH (‘Severe Spinal Headache’). Twelve patients are given a lumbar puncture. 

   - **(i)** Using a binomial model, find the expected number of patients who will suffer SSH, and find also the standard deviation. [3] 

**(ii)** Find the probability that four or more of the twelve patients will suffer SSH. [2] [ **(i)** 4.2, 1.65 **(ii)** 0.653] 

## **Solution:** 

**(i)** Let _X_ be the **number** of patients, out of 12, who will suffer SSH. Then _X_ ~ B(12,0.35) . Note that it is compulsory to define the random variable and write down its distribution. Expected number of patients who will suffer SSH  12  0.35   4.2 273 Standard deviation  12(0.35)(1  0.35)   1.65 (3.s.f) 10 

## **Note:** 

Assumptions needed for _X_ to be modelled using a binomial distribution are (1) The event that a patient suffers SSH is independent of the event that another patient suffers SSH. (2) The probability of a patient suffering SSH remains constant at 0.35 for all patients. **(ii)** P( _X_  4)  1 P( _X_  3)  0.65335 = 0.653 (3.s.f) 

- **2** The random variable _X_ ~ B (16, _p_ ), where _p_ < 0.5. If the variance of _X_ is 3.36, find the value of _p_ . Find also the probability that _X_ is less than its mean. 

[ _p_  0.3 , 0.450] 

## **Solution:** 

Variance of _X_ = (16)( _p_ )(1  _p_ ) = 3.36, which gives _p_ = 0.3 or 0.7 (rejected since _p_ < 0.5) Hence, _p_ = 0.3 Mean of _X_ = E( _X_ ) = 16(0.3) = 4.8 P( _X_  4.8)  P( _X_  4)  0.450 (3 s.f.) 

__________________________________________ Additional Practice S2B: Binomial Distribution 

Page 1 of 15 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

- **3** A factory produces chocolate which are packed into boxes of 20 and delivered to shops for sale. A chocolate will not meet the minimum criteria for packing for sale if it weighs less than 20 grams. On average, 2% of the chocolate produced did not meet the minimum criteria. 

   - **(i)** Find the probability that a randomly chosen box contain at least 1 chocolate that does not meet the minimum criteria. [2] 

   - **(ii)** Find the probability that out of 4 randomly chosen boxes of chocolate, there are exactly 2 boxes with at least 1 chocolate that does not meet the minimum criteria. [2] [ **(i)** 0.332 **(ii)** 0.295] 

**==> picture [482 x 353] intentionally omitted <==**

**----- Start of picture text -----**<br>
TPJC Prelim 2007/02/Q5<br>Solution:<br>(i)  Let  X  be the  number  of chocolates, out of 20, not meeting the minimum criteria.<br>Then  X ~ B(20,0.02)<br>Pay attention to how a random variable which<br>P( X  1)  1 P( X  0) follows Binomial Distribution is defined.<br> 0.33239<br><br>0.332  (3 s.f.)<br>Note:<br>Assumptions needed for  X  to be modelled using a binomial distribution are<br>(1)  The event that a chocolate does not meet the minimum criteria is independent of the event<br>that another chocolate does not meet the minimum criteria.<br>(2)  The probability of a chocolate not meeting the minimum criteria remains constant at 0.02<br>for all chocolates.<br>(ii)  Let  Y  be the  number  of boxes of chocolates, out of 4, with at least 1 chocolate that doesn’t<br>meet the minimum criteria.<br>Then  Y ~ B(4,0.33239)<br>Use appropriate accuracy (at least 5 s.f.)<br>P( Y  2)  0.295 (3 s.f.)  for the value of  p<br>**----- End of picture text -----**<br>


______________________________________ Additional Practice S2B: Binomial Distribution 

Page 2 of 15 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

- **4** In a multi-national company with a large population, 13.5% of the staff owns a vehicle. 

   - **(i)** Find the probability that in a random sample of 30 staff, exactly 5 of them will own a vehicle. 

         - [2] 

   - **(ii)** The probability that there is at least one staff who owns a vehicle in a random sample of size _n_ is greater than 0.95. Find the least value of _n_ . [3] 

      - [ **(i)** 0.170 **(ii)** 21] 

## **CJC Prelim 2006/02/Q25** 

## **Solution:** 

- **(i)** Let _X_ be the **number** of staff, out of 30, who owns a vehicle. Then _X_ ~ B(30,0.135) 

   - P( _X_  5)  0.17018  0.170 (3 s.f.) 

## **Note:** 

Assumptions needed for _X_ to be modelled using a binomial distribution are 

   - (1)  The event that a staff owns a vehicle is independent of the event that another staff owns a vehicle. 

   - (2)  The probability of a staff owning a vehicle remains constant at 0.135 for all staff. 

- **(ii)** Let _Y_ be the **number** of staff, out of _n_ , who owns a vehicle. _Y_ ~ B( _n_ , 0.135) 

P( _Y_  1)  0.95  1 P( _Y_  0)  0.95 **OR**  P( _Y_  0)  0.05 From P( _Y_  0)  0.05  (1  0.135) _n_  0.05 Using a GC, When _n_ = 20, P( _Y_ =0)  0.054995 > 0.05 ln0.05  _n_   20.7 When _n_ = 21, P( _Y_ =0)  0.047571 < 0.05 ln0.865  _n_  21 **Note:** If you choose to use the GC, the above working is required. 

Least value of _n_ is 21. 

______________________________________ Additional Practice S2B: Binomial Distribution 

Page 3 of 15 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

- **5** Market research showed that 3 out of 10 households in a housing estate subscribe to fibre broadband internet services. 

   - **(a)** 20 households from a particular block of flats in the estate were surveyed. 

      - **(i)** Show that the probability of more than 3 and less than 9 of the households surveyed subscribe to fibre broadband internet services is 0.780, correct to 3 decimal places.  [2] 

      - **(ii)** Find the least value of _k_ such that the probability that at most _k_ of the households surveyed subscribe to fibre broadband internet services is at least 0.75. [2] 

   - **(b)** There are a total of 50 blocks of flats in the estate. 20 households from each block of flats were surveyed. 

Find the probability that there are exactly 39 blocks of flats with more than 3 and less than 9 households surveyed that subscribe to fibre broadband services. [2] 

[ **(a)(ii)** least _k_  7 **(b)** 0.135] 

## **RVHS Prelim 2014/02/Q9 (part)** 

## **Solution:** 

**(a)** Let _X_ be the **number** of households that subscribe to broadband internet services out of 20 **(i)** households. 

_X_ ~ B  20,0.3  P  3  _X_  9   P  4  _X_  8   P  _X_  8   P  _X_  3   0.77958 For a show question, this intermediate step is mandatory.  0.780  3 d.p.  shown  

## **Note:** 

Assumptions needed for _X_ to be modelled using a binomial distribution are 

   - (1) The event that a household subscribes to broadband internet services is independent of the event that another household subscribes to broadband internet services. 

   - (2) The probability of a household subscribing to broadband internet services remains constant at 0.3 for all households. 

- **(a)** P  _X_  _k_   0.75 

- **(ii)** Using the GC to set up a table of values, 

> P  _X_  6   0.608  0.75 

> P  _X_  7   0.772  0.75 The least value of _k_ is 7. 

______________________________________ Additional Practice S2B: Binomial Distribution Page 4 of 15 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

**(b)** Let _Y_ be the **number** of blocks, with more than 3 and less than 9 households subscribing to broadband internet services, out of 50 blocks each with 20 households surveyed. _Y_ ~ B  50,0.780  Since we were asked to show this value in **(a)(i)** , we can P  _Y_  39  use this value in 3 d.p. instead of using the 5 d.p. value.  0.13511  0.135  3 s.f.  **OR** _Y_ ~ B  50,0.77958  P  _Y_  39   0.13510  0.135  3 s.f.  

- **6** It is known that 36% of the customers of a certain supermarket will bring their own environmentally friendly bags. On a certain day, there are 3 cashiers and each cashier has 5 customers in queue. 

   - **(i)** Find the probability that among all the customers in queue, at least 4 of them brought their own environmentally friendly bags. [2] 

   - **(ii)** If exactly 4 customers in queue brought their own environmentally friendly bags, find the probability that each cashier will have at least 1 customer bringing his or her own environmentally friendly bag. [4] 

      - [ **(i)** 0.847 **(ii)** 0.549] 

## **RI CT2/H1/2018/Q5** 

## **Solution:** 

**(i)** Let _X_ be the **number** of customers, out of 15, who brought their own environmentally friendly bags. _X_  B  15,0.36  P( _X_  4)  1 P( _X_  3)  0.84694  0.847 (3 s.f.) **(ii)** Let _Y_ be the **number** of customers, out of 5, who brought their own environmentally friendly bags. _Y_  B  5,0.36  P (each cashier will have at least 1 customer bringing his or her own environmentally friendly bag given that _X_ = 4) 

> [=][ 1) ][][ P(] _[Y]_[2][=][ 1) ][][ P(] _[Y]_[3][=][ 2)] =[3 ][][ P(] _[Y]_[1] P( _X_ = 4) 

______________________________________ Additional Practice S2B: Binomial Distribution Page 5 of 15 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

> [][ 0.33974] =[3 ][][ (0.30199)][2] 0.16917 ≈ 0.54945 = 0.549  (3 s.f .) 

- **7** A factory produces watches. The probability that a watch is defective is 0.02. The watches are packed into boxes which contain 55 watches each before being shipped. 

   - **(i)** State, in context, two assumptions for the number of defective watches in a box to be well modelled by a binomial distribution. [2] 

   - **(ii)** Show that the probability for a box to contain at least 1 defective watch is 0.671. [2] 

   - **(iii)** A customer ordered 40 boxes of watches. He will be compensated if more than 19 boxes contain defective watches. Find the probability that the customer will be compensated. [3] 

   - **(iv)** Find the least number of watches to be added to a box of 55 watches such that the probability of finding at least 53 non-defective watches is more than 0.99. [3] 

      - [ **(iii)** 0.992 **(iv)** least number is 2] 

## **MJC Prelim 2010/02/Q8 (modified) Solution:** 

**(i)** (1) The event that a watch is defective is independent of the event that another watch is defective. (2) The probability of a watch being defective is constant at 0.02 for all watches. **(ii)** Let _X_ be the **number** of defective watches in a box of 55. _X_ ~ B (55, 0.02) P  _X_  1   1 P  _X_  0   1 0.32918  0.67082  0.671(3 s.f.)  shown  **(iii)** Let _W_ be the **number** of boxes out of 40, which contain defective watches. _W_ ~ B (40, 0.671) P  _W_  19   1 P  _W_  19  Since we were asked to show this value in **(ii)** , we can use this value in 3 s.f. instead of using  0.99189  0.992 (3 s.f.) the 5 s.f. value. **OR** _W_ ~ B (40, 0.67082) P  _W_  19   1 P  _W_  19   0.99184  0.992 (3 s.f.) 

______________________________________ Additional Practice S2B: Binomial Distribution Page 6 of 15 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

**(iv)** Let _Y_ be the **number** of non-defective watches in a box of 55+ _n_ watches. _Y_ ~ B(55  _n_ , 0.98) P( _Y_  53)  0.99  1 P( _Y_  52)  0.99  P( _Y_  52)  0.01 From GC, For _n_ =1, P( _Y_  52)  0.0258 > 0.01 For _n_ =2, P( _Y_  52)  0.00566 < 0.01 Therefore, the least number of watches to be added is 2. 

- **8** A test consists of 15 multiple choice questions, where each question has _n_ possible options, of which only one is correct. A student took the test by randomly choosing an answer to each question.  It is known that the probability of answering exactly 3 questions correctly is the same as the probability of answering exactly 4 questions correctly. 

**(i)** By forming an equation in terms of _n_ , find the value of _n_ . [3] 

Each correct answer is awarded 3 marks and each incorrect answer carries a penalty of 1 mark. The score is the total marks awarded based on the number of correct and incorrect answers. 

**(ii)** Find the expected score, _s_ , obtained by the student. 

[3] 

**(iii)** Find the probability that the score obtained by the student is within 4 marks of _s_ . [2] [ **(i)** 4 **(ii)** 0 **(iii)** 0.450] 

## **DHS Prelim 9758/2018/02/Q6** 

**Solution: (i)** Let _X_ be the **number** of questions answered correctly out of 15.  1  _X_  B  15,   _n_  P( _X_  3)  P( _X_  4) 3 12 4 11  15  1  _n_  1   15  1  _n_  1    3  _n_  _n_   4  _n_  _n_   _n_  1   1     3    _n_   _n_  _n_  4 **Note:** Using your GC to check the answer From GC, _n_  4 

______________________________________ Additional Practice S2B: Binomial Distribution 

Page 7 of 15 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

xX oT Ya | Y2 | 

## **(ii) Method 1** 

**==> picture [268 x 101] intentionally omitted <==**

## **Method 2** 

**==> picture [166 x 79] intentionally omitted <==**

## **Method 3** 

Let _Y_ be the number of questions answered incorrectly out of 15.  3  _Y_  B  15,  .  4  _s_  3E( _X_ )  E( _Y_ )  3  15  1    15  3   0   4    4  **(iii)** P(  4 _T_  4)  P(  4 4 _X_  15  4)  P(2.75  _X_  4.75)  P(3  _X_  4)  P( _X_  4)  P( _X_  2)  or  2P( _X_  4)  or  2P( _X_  3)  0.450398  0.450 (3 s.f.) 

______________________________________ Additional Practice S2B: Binomial Distribution 

Page 8 of 15 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

- **9** The random variable _X_ is the number of successes in _n_ independent trials of an experiment in which the probability of a success in any one trial is _p_ . Show that 

**==> picture [303 x 31] intentionally omitted <==**

1 Find the most probable number of successes when _n_  10 and _p_  . 4 

[most probable number = 2] 

## **N1982/01/Q13** 

**Solution:** 

_X~_ B( _n_ , _p_ ) 

**==> picture [232 x 223] intentionally omitted <==**

We want to know the values of _k_ such that P( _X_  _k_  1)  P( _X_  _k_ ) . 

10  _k_ Consider  1  10  _k_  3 _k_  3 3 _k_  3 7  _k_  4 Largest _k_ is 1, where P( _X_  2)  P( _X_  1) . This implies that P  _X_  0   P  _X_  1   P  _X_  2  . 7 We also have P( _X_  _k_  1)  P( _X_  _k_ ) whenever _k_  . 4 Smallest _k_ is 2, where P  _X_  2   P  _X_  3  . This implies that P  _X_  2   P  _X_  3   P  _X_  10  . 

Hence the most probable number of successes (mode) is 2. 

______________________________________ Additional Practice S2B: Binomial Distribution Page 9 of 15 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

**10** A game is played using a fair six-sided die, a pawn and a simple board as shown below. 

**S** 1 2 3 4 5 **E** 

Initially, the pawn is placed on square **S** .  The game is played by throwing the die and moving the pawn in the following manner: 

**S** 1  2  3  4  5 **E** 5  4  3  2  1  2  3  4  5 **E** ……… 

Thus, for example, if the first and second throw of the die gives a “5” and “4” respectively, the final position of the pawn will be on square “3”. 

The game will stop when the pawn stops at square **E** . 

Let _X_ be the random variable denoting the number of throws of the die required to move the pawn such that it stops at square **E** . 

**==> picture [451 x 24] intentionally omitted <==**

- **(ii)** Find the probability that more than two throws of the die are needed for the pawn to stop at square **E** given that the first throw of the die gives an even number. [3] 

It is now given that for each game, a player has a maximum of 3 throws of the die and a special prize is given to any player who uses not more than two throws for the pawn to stop at square **E** . 

- **(iii)** Find the probability of a player winning a special prize in at least three but not more than eight games out of ten games. [3] 

- **(iv)** Find the least number of games needed so that the probability of winning at least a special prize is at least 0.998. 

**==> picture [129 x 24] intentionally omitted <==**

**==> picture [459 x 141] intentionally omitted <==**

______________________________________ Additional Practice S2B: Binomial Distribution Page 10 of 15 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

> **(ii)** P  _X_  2 | _D_ 1 is even   P  _X_  2 and _D_ 1 is even  

> P  _D_ 1 is even  

> P  _D_ 1  2, _D_ 2  4  +P  _D_ 1  4, _D_ 2  2  = 

> P  _D_ 1 is even  1  5  1  5       = 6  6  6  6   5 3 9 6 **(iii)** Let _W_ be the **number** of games, out of 10, that a special prize is won. P(winning a special prize) 1 5 11 = P _X_  1  P _X_  2        6 36 36  11  _W_ ~ B  10,36  Probability required 

> = P  3  _W_  8   P  _W_  8   P  _W_  2   0.63173  0.632 (3 s.f) **(iv)** Let _n_ be the number of games needed. Let _Y_ be the **number** of games, out of _n_ , that a special prize is won.  11  _Y_ ~ B  _n_   ,36  P _Y_  1  0.998  1 P _Y_  0  0.998     Using GC, 

> _n_ 1  P  _Y_  0  17 ≈ 0.99797 < 0.998 18 ≈ 0.99859 > 0.998 Least _n_ = 18 

______________________________________ Additional Practice S2B: Binomial Distribution Page 11 of 15 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

- **11** A factory produces ballpoint pens. On average 6% of the pens are faulty. The pens are packed in boxes of 100 for sale to retail outlets. It should be assumed that the number of faulty pens in a box of 100 pens follows a binomial distribution. 

For quality control purposes a random sample of 10 pens from each box is tested. If 2 or fewer faulty pens are found in the sample of 10, the box is accepted for sale. Otherwise the box is rejected. 

- **(i)** Find the probability that a randomly chosen box of 100 pens is accepted for sale. [1] 

- **(ii)** One morning 75 boxes are tested in this way. Find the probability that more than 5% of these boxes are rejected. [4] 

An alternative testing procedure is trialled in which a random sample of 5 pens is initially taken from a box and tested. 

- If there are no faulty pens in this sample of 5,  the box is accepted. 

- If there are 3 or more faulty pens in this sample of 5,  the box is rejected. 

- If there are 1 or 2 faulty pens in this sample,  a second random sample of 5 pens is taken from the box. When the second sample has been tested, the box is accepted if the total number of faulty pens found in the combined sample of 10 is 2 or fewer and rejected otherwise. 

- **(iii)** Find the probability that a randomly chosen box of 100 pens is accepted for sale when the alternative testing procedure is used. [5] 

**(iv)** Explain why the factory manager might prefer to use the alternative testing procedure. [1] [ **(i)** 0.981 **(ii)** 0.0535 **(iii)** 0.983] 

**9758/2020/02/Q9 part** 

**Solution:** 

**(i)** Let _X_ be the **number** of faulty pens out of 10. _X_ ~ B  10,0.06  P  _X_  2   0.98116  0.981 

**(ii)** Let _Y_ be the **number** of faulty boxes out of 75. _Y_ ~ B  75,1  0.98116   B  75,0.018838  P  _Y_  5% of 75   P  _Y_  3.75   1 P  _Y_  3   0.053454  0.0535 (3 s.f.) 

______________________________________ Additional Practice S2B: Binomial Distribution Page 12 of 15 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

**(iii)** Let _T_ be the **number** of faulty pens out of 5. _T_ ~ B  5,0.06  P  a box is accepted   P  _T_ 1  0   P  _T_ 1  1  P _T_ 2  1   P  _T_ 1  2  P _T_ 2  0   P  _T_  0   P  _T_  1  P _T_  1   P  _T_  2  P _T_  0   0.983  (3 s.f.) 

**(iv)** Probability of a box being accepted for the alternative testing process is 0.983 which is similar (or slightly higher) than the initial testing process which is 0.981. In addition, the expected number of pens sampled for the alternative testing process is smaller and hence it may be more efficient and cost saving. 

**12** In a computer game, a counter moves along a straight line and is originally placed at _k_  0. At each stage, it takes one step to the right with probability _p_ or one step to the left with probability _q_ , where _q_  1 _p_ . Each step is of length 1 unit and the step taken at each stage is independent of one another. 

For illustration purpose, the counter is seen to be at _k_  2 in the diagram below. 

**==> picture [312 x 49] intentionally omitted <==**

**==> picture [9 x 9] intentionally omitted <==**

The counter takes 10 consecutive steps. 

**==> picture [451 x 12] intentionally omitted <==**

8 2 **(ii)** Show that the probability that the counter ends at _k_  6 is 45 _p q_ . [2] 

- **(iii)** Given that the most probable end-point of the counter is _k_  6, find exactly the range of values of _p_ in the form _p_ 1  _p_  _p_ 2 where _[p]_ 1[ and ] _[p]_ 2[ are constants to be determined. ] [4] 

**==> picture [451 x 45] intentionally omitted <==**

______________________________________ Additional Practice S2B: Binomial Distribution Page 13 of 15 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

## **DHS Prelim 9758/2021/02/Q8** 

## **Solution:** 

Let _R_ and _L_ be the number of right and left steps taken respectively. **(i)** Note that since counter starts at 0, _R_  _L_ gives the number of the ending position. For the counter to end at _k_  7, _R_  _L_  7  _R_  _L_  7 Also, since game is played for 10 stages, _R_  _L_  10. Hence, ( _L_  7)  _L_  10  _L_  32 (Or show that _R_  172 ) But _L_ must be integer, hence it’s not possible for counter to end at _k_  7. 

**Alternative** 

Case 1: _R_ is odd, _L_ is odd (since must add up 10)  _R_  _L_ is even. Case 2: _R_ is even, _L_ is even  _R_  _L_ is  even 

Hence, one can never end at an odd numbered position with 10 steps starting at 0. 

**(ii)** For the counter to end at _k_  6, _R_  _L_  6 and _R_  _L_  10 . Hence _R_  8 and _L_  2 . 8 2 Any combination of 8 right steps and 2 left steps occurs with probability _p q_ .  10  Number of such combinations is    45    8  8 2 Hence the probability that the counter ends at _k_  6 is 45 _p q_ . 

**(iii)** _R_ ~ B(10, _p_ ) 

For the most probable end-point to be _k_  6, the mode of _R_ is 8. As _R_ is binomial, it suffices to ensure the two inequalities below are satisfied:  10  7 3  10  8 2   _p q_    _p q_  (1)  7   8   10  9 1  10  8 2   _p q_    _p q_  (2)  9   8  8 From (1), 8(1  _p_ )  3 _p_  _p_  11 9 From (2) 2 _p_  9(1  _p_ )  _p_  11 8 9 8 9 Hence we have 11  _p_  11 i.e. _p_ 1  11, _p_ 2  11. 

______________________________________ Additional Practice S2B: Binomial Distribution 

Page 14 of 15 

Raffles Institution H2 Mathematics 

2026 Year 6 

_____________________________________________________________________________________________ 

**(iv)** Note that when _p_  _p_ 1[,] the modes of _R_ are 7 and 8 i.e. most probable end-points for the counter are _k_  4 and _k_  6. When _p_  1 _p_ 1 (complement probability), most probable end-points for the counter will be _k_  4 and _k_  6. (by symmetry since interchange right with left) **OR** 8 3 _p_  1  11 11  3  _R_ ~ B  10,11  Modes of _R_  2 and 3 The two most probable end-points for the counter will be _k_  4 and _k_  6. 

## _**THE END**_ 

______________________________________ Additional Practice S2B: Binomial Distribution Page 15 of 15 

