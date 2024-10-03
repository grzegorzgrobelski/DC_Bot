import re

def check_pattern(s):
    if s and s[0] in ['+', '-']:
        pattern = r'^[+-]?\d+\.\d+$'
        match = re.match(pattern, s)
        return match is not None
    else:
        return False
    

def checkPatern_own(s):
    if s[0] in ['+', '-'] and '.' in s:
        try:
            number = s[1:]
            first_part = int(number.split('.')[0])
            second_part = int(number.split('.')[1])
            if first_part in range(0,10) and second_part in range(0,100):
                return True
        except ValueError:
            return False
    else:
        return False


        



#1/4
number_to_check = '+11.43+'


print('Chat: ' + str(check_pattern(number_to_check)))
print('Gres: ' + str(checkPatern_own(number_to_check)))