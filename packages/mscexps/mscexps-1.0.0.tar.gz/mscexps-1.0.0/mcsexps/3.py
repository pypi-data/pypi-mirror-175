from math import sqrt, log10
from prettytable import PrettyTable
 
def repeat_till_valid():
    is_valid = False
    i0 = int(input('[+] i0: '))
    n = int(input('[+] n: '))
 
    while not is_valid:
        N = int(input('[+] N: '))
        is_valid = calculate(n, N, i0, True)
 
def calculate(n:int, N:int, i0:int, print_table:bool=True):
    Q = sqrt(3*N)
    signal_interference = 10 * log10((Q ** n) / i0)
    is_acceptable = False
    
    if signal_interference > 15:
        is_acceptable = True
 
    if print_table:
        table = PrettyTable(['property', 'value'])
        table.add_row(['n', n])
        table.add_row(['N', N])
        table.add_row(['i0', i0])
        table.add_row(['Q', Q])
        table.add_row(['S/I', signal_interference])
        table.add_row(['valid', is_acceptable])
 
        print(table)
 
    return is_acceptable
 
 
if __name__ == '__main__':
    repeat_till_valid()