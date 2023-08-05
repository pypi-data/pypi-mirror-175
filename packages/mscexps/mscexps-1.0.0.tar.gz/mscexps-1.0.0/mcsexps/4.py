from math import exp, sqrt


# N = float(input('[+] No. of cells/Cluster: '))
# r = float(input('[+] Radius of cell: '))
# tot_channels = float(input('[+] Total No. of channels: '))
# i = float(input('[+] Traffic intensity: '))
# lamda = float(input('[+] Request Rate: '))

N = 4
r = 1.5
tot_channels = 60
i = 0.03 # Au
lamda = 2
g = 0.02 # grade of service


# user/km^2
A = 8 # total traffic intensity
u = int(A/i) # number of users
area = (3 * sqrt(3) * (r**2))/2 # area of cell
y = int(u/area) # no of users/area

print('No. of user/km^2:', y)

# probability that delayed call will have to waitfor more than 15s
h = 54 # holding time in seconds
t = 15 # delay time in seconds
channels_per_cell = tot_channels/N # no. of channels/cell
p = exp(-(channels_per_cell-A)*t/h) * 100
print(p)

# Probability that the call will be delayed for more than 15s
S = p * g
print(S)