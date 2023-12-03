'''
As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?
'''

calibration_test = ['1abc2', 'pqr3stu8vwx', 'a1b2c3d4e5f', 'treb7uchet']

def calibration_sum(document):
    values = []

    for item in document:
        full_num = ""
        for x in item:
            if x.isnumeric() == True:
                full_num = full_num + x

        calibration_value = full_num[0] + full_num[-1]
        values.append(int(calibration_value))

    return sum(values)

calibration_sum(calibration_test)

