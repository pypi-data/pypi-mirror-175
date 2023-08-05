# cell calculations
from math import sqrt
from prettytable import PrettyTable
 
'''
Input:
- total_area
- total channels
- cell radius
- N (frequency reuse factor)

Calculations:
- Cell Area = (3*sqrt(3)* r^2)/2
- total_cells = Total Area/ Cell Area
- total clusters = total_cells / N
- channels per cell = total channels / N
- capacity = total channels * total clusters

Outputs:
- All parameters in table format with R=0.8 and 1.6
- Comparision table b/w different values of N=4,7,12 with parameters cluster number, channels per cell, capacity
'''
 
class CellCalc:
    def __init__(self, tot_area: float, tot_channels: float, radius: float, N: int) -> None:
        self.tot_area = tot_area
        self.tot_channels = tot_channels
        self.radius = radius
        self.N = N
 
    def calculate(self, print_table: bool = False):
        self.cell_area = (3*sqrt(3) * (self.radius ** 2))/2
        self.cells_num = self.tot_area/self.cell_area
        self.clusters_num = self.cells_num/self.N
        self.channels_per_cell = self.tot_channels/self.N
        self.capacity = self.tot_channels * self.clusters_num
 
        if print_table:
            table = PrettyTable(['Property', 'Value'])
 
            table.add_row(['N', self.N])
            table.add_row(['Total Area', self.tot_area])
            table.add_row(['Total Channels', self.tot_channels])
            table.add_row(['Radius', self.radius])
            table.add_row(['Cell Area', self.cell_area])
            table.add_row(['No. of Cells', self.cells_num])
            table.add_row(['No. of Clusters', self.clusters_num])
            table.add_row(['Channels/Cell', self.channels_per_cell])
            table.add_row(['Capacity', self.capacity])
            print(table)
 
 
if __name__ == '__main__':
    # calculate for r 0.8 and 1.6
    N4 = CellCalc(
        tot_area=1765,
        tot_channels=336,
        radius=0.8,
        N=4,
    )
    N4.calculate(print_table=True)
 
 
    N7 = CellCalc(
        tot_area=1765,
        tot_channels=336,
        radius=0.8,
        N=7,
    )
    N7.calculate(print_table=True)
 
    N12 = CellCalc(
        tot_area=1765,
        tot_channels=336,
        radius=0.8,
        N=12,
    )
    N12.calculate(print_table=True)
 
    comparision_table = PrettyTable(['N', 'No. of Clusters', 'Channels/Cell', 'Capacity'])
    comparision_table.add_row([N4.N, N4.clusters_num, N4.channels_per_cell, N4.capacity])
    comparision_table.add_row([N7.N, N7.clusters_num, N7.channels_per_cell, N7.capacity])
    comparision_table.add_row([N12.N, N12.clusters_num, N12.channels_per_cell, N12.capacity])
 
    print(comparision_table)