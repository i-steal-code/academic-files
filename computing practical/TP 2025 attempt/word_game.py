from random import *


lst = ['WELL', 'YOGA', 'TRIP', 'WORD', 'RICH', 
       'CAKE', 'BIRD', 'SURF', 'DUCK', 'DOLL', 
       'FAME', 'GIFT', 'SILK', 'LADY', 'EASY',
       'LIKE', 'PATH', 'PLAY', 'REST', 'EPIC',
       'SAIL', 'TREE', 'TAIL', 'SELL', 'LEAF']


from random import *

lst = sample(lst, 5)
print('Welcome to the WORD GAME. You will be given 5 scrambled words to answer ... here we go:\n')

score = 0            
for word in lst:

    random_word = ''.join(sample(list(word), 4))

    answer = input('Enter the word you can form with ' + random_word + ': ').upper()

    if answer == word:
        print('Correct')
        score += 1  
    else:
        print('Incorrect')

print('You have answered ' + str(score) + ' out of 5 correctly.')   

