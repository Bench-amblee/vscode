'''
Exercise 5: Display numbers from a list using loop
Write a program to display only those numbers from a list that satisfy the following conditions

The number must be divisible by five
If the number is greater than 150, then skip it and move to the next number
If the number is greater than 500, then stop the loop
Given:

numbers = [12, 75, 150, 180, 145, 525, 50]
'''

numbers = [12, 75, 150, 180, 145, 525, 50]

def list_return(nums):
    correct_list = []
    for num in nums:

        if num > 500:
            break

        if num > 150:
            continue

        if num % 5 == 0:
            correct_list.append(num)

    return correct_list

print(list_return(numbers))