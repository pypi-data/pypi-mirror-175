# Pr = Pt.Gt.Gr.lam^2
#      --------------
#      (4pi)^2. d^2. L

from math import pi
from matplotlib import pyplot as plt
from prettytable import PrettyTable
import numpy as np

fc = 800*(10**6)
c_light = 3*(10**8)
lamda = c_light/fc
Gt = 1
Gr = 1
Pt = 1
L = 1

d_tx_rx_km = np.arange(1, 10+1)
d_tx_rx_m = d_tx_rx_km*(10**3)

PRF = (Pt * Gt * Gr * (lamda**2))/((4*pi*d_tx_rx_m)**2 * L)
PRFD = 10*np.log10(PRF)
# print(f'PRFD: {PRFD}')

# create table
table = PrettyTable()
table.add_column(fieldname='distance (in km)', column=d_tx_rx_km)
table.add_column(fieldname='Power Received (dB)', column=PRFD)
print(table)

# plot data
plt.plot(d_tx_rx_km, PRFD, '-o')
plt.xlabel('Distance between transmitter and receiver')
plt.ylabel('Received Power(dB)')
plt.title('Modelling of Free Space Propogation Model')
plt.legend('Free Space Model')
plt.show()
