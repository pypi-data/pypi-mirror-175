# Pr = Pt.Gt.Gr.(ht.hr)^2
#      ------------------
#             d^4

from matplotlib import pyplot as plt
from prettytable import PrettyTable
from math import pi
import numpy as np


fc = 800*(10**6)
c_light = 3*(10**8)
lamda = c_light/fc

Gt = 1
Gr = 1
Pt = 1
L = 1
ht = 30
hr = 2

# always use int64 else it'll wrap around and introduce bug
d_tx_rx_km = np.arange(1, 10+1, dtype=np.int64)
d_tx_rx_m = d_tx_rx_km*(10**3)

PRG = (Pt * Gt * Gr * (ht*hr)**2) / np.power(d_tx_rx_m, 4)
PRGD = 10*np.log10(PRG)
# print(f'PRG: {PRG}')
# print(f'PRGD: {PRGD}\n')

plt.plot(d_tx_rx_km, PRGD, '-o')
plt.xlabel('Distance between transmitter and receiver')
plt.ylabel('Received Power(dB)')
plt.title('Modelling of 2 Ray Ground Reflection Model')
plt.legend('Two-Ray-Model')

# create table
table = PrettyTable()
table.add_column(fieldname='distance (in km)', column=d_tx_rx_km)
table.add_column(fieldname='Power Received (dB)', column=PRGD)
print(table)


# free space propagation model
PrFS = (Pt * Gt * Gr * (lamda**2))/((4*pi*d_tx_rx_m)**2 * L)
PrFSdb = 10 * np.log10(PrFS)

plt.plot(d_tx_rx_km, PrFSdb, '-o')
plt.legend('Free Space Model')

plt.show()
