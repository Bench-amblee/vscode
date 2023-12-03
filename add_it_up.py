''' 
Write a function, add_it_up(), that takes a single integer as input and returns the sum of the integers from zero to the input parameter.
The function should return 0 if a non-integer is passed in.
'''

def add_it_up(number):
    x = 0
    for i in range(number):
        x += i
    
    return x

print(add_it_up(5))
