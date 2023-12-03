"""

FizzBuzz
Write a program that prints the numbers from 1 to 100. But for multiples of 3, print "Fizz" instead of the number, and for multiples of 5, print "Buzz." For numbers that are multiples of both 3 and 5, print "FizzBuzz."

"""

def fizzbuzz(nums):
    for num in nums:
        if num % 5 == 0 and num % 3 == 0:
            print ("FizzBuzz")

        elif num % 3 == 0:
            print ("Fizz")

        elif num % 5 ==0:
            print('Buzz')



test_list = []

for i in range(1,100):
    test_list.append(i)


fizzbuzz(test_list)