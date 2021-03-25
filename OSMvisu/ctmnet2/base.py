 # -*- coding: utf-8 -*-

# @Author: KeyangZhang
# @Date: 2019-12-04 17:28:17
# @LastEditTime: 2020-02-13 20:11:15
# @LastEditors: Keyangzhang

def _mid(a,b,c):
    """return the middle value of three numbers"""
    if a<=b<=c or c<=b<=a:
        return b
    elif b<=a<=c or c<=a<=b:
        return a
    elif a<=c<=b or b<=c<=a:
        return c

class _Cell(object):
    """Cell
    
    cell is the basic element of section 
    
    """

    def __init__(self, demand=0, supply=0):
        super(_Cell, self).__init__()
        self.volume = 0
        self.re_volume = 0
        self.demand = 0
        self.supply = 0

class Section(object):
    """road section

    Section is the basic element of the network and it can be signle-lane or multi-lanes
    It can be an artery, a link road, an entrance or an export road of an intersection
    Once the road is initialized the attributes cannot be change
    

    Attributes:
        lanes_length: float, the length of the section, the unit is km
        lanes_number: int, the number of lanes this section contains, default: 1
        cell_length: float, the length of all the cells in this section, default: 0.05km
        free_speed: float, the free speed of vehicles in this section, default: 60km/h
        wave_speed: float, the wave_speed of this section, default：8km/h
                    for its definition, please refer to fundamental diagram theory of traffic flow
        jam_density: float, the jam_density of this section, default: 200veh/(km*lane) 
                    for its definition, please refer to traffic flow theory

    """

    def __init__(self, lanes_length, lanes_number=1,
                 cell_length=0.05, free_speed=60, wave_speed=8,
                 jam_density=200, name='empty'):
        super(Section, self).__init__()

        # constant parameters
        self.lanes_length = lanes_length/1000
        self.lanes_number = lanes_number
        self.cell_length = cell_length
        self.cells_number = int(self.lanes_length/self.cell_length+1)  # the number of cell this section contains
        self.free_speed = free_speed
        self.wave_speed = wave_speed
        self.name = 'empty'

        #   the actual jam density of this secthin
        self.jam_density = jam_density * self.lanes_number

        #   the capacity of each cell
        #   the upper limit value of flow between two directly connected cells
        self.capacity = self.jam_density / \
            (1 / self.free_speed + 1 / self.wave_speed)
        
        #   the initial time interval of each simulation step
        self.interval = self.cell_length * 3600 / self.free_speed
        
        #   the maximum number of vehicles that flow form cell i-1 to cell i during sim interval
        self.max_volume = self.capacity * self.interval / 3600

        #   dynamic parameters
        self.cells = [_Cell() for i in range(self.cells_number)]
        
        if self.cells_number==1:
            self.flows = [0]
        else:
            self.flows = [0 for i in range(self.cells_number-1)]
        
        #   demand of this section, equals to the demand of last cell
        self.demand = 0
        #   supply of this section, equals to the supply of first cell
        self.supply = min(self.max_volume,
                          self.wave_speed / self.free_speed *(self.cell_length * self.jam_density -0)
                          ) / self.interval
        #   inflow of this section per simsecond
        self.inflow = 0
        #   outflow of this section per simsecond
        self.outflow = 0

    def __getitem__(self, position):
        return self.cells[position]

    def __str__(self):
        return str([round(cell.volume,1) for cell in self])

    def calculate_demand(self):
        """calculate demand of each cell and this section"""
        
        for cell in self.cells:
            cell.demand = min(cell.volume, self.max_volume / self.interval)
        self.demand = self.cells[-1].demand

    def calculate_supply(self):
        """calculate supply of each cell and this section"""
        
        for cell in self.cells:
            cell.supply = min(self.max_volume,
                              self.wave_speed / self.free_speed *
                              (self.cell_length * self.jam_density -
                               cell.volume)) / self.interval
        self.supply = self.cells[0].supply

    def calculate_flow(self):
        """calculate flows between each two cells"""
        if self.cells_number>1:
            for i in range(0, self.cells_number-1):
                self.flows[i] = min(self.cells[i].demand, self.cells[i+1].supply)
        else:
            self.flows[0] = 0

    def update_volume(self):
        """update the volume of each cell"""

        # for the first cell
        self.cells[0].re_volume = self.cells[0].volume
        self.cells[0].volume = self.cells[0].volume + \
            self.inflow - self.flows[0]
        # for the intermediate cells
        for i in range(1, self.cells_number-1):
            self.cells[i].re_volume = self.cells[i].volume
            self.cells[i].volume = self.cells[i].volume + \
                self.flows[i-1]-self.flows[i]
        # for the last cells
        self.cells[-1].re_volume = self.cells[-1].volume
        self.cells[-1].volume = self.cells[-1].volume + \
            self.flows[-1] - self.outflow

class _Connector(object):
    """Connector

    the connector connects the upstream sections and downstream sections
    and it does not have volume and is used merely for calcuate flows between sections

    Attributes:
        upstream: list/tuple or Section, the upstream section/sections
        downstream: list/tuple or Section, the downstream section/sections
    """

    def __init__(self, upstream, downstream, green_time, off_set=0):
        super(_Connector, self).__init__()
        self.upstream = upstream
        self.downstream = downstream
        self.green_time = [int(i) for i in green_time]
        self.phase = [0]
        m = 0
        for i in self.green_time:
            m+=i
            self.phase.append(m)
        self.off_set = int(off_set)
        self.cycle = sum(self.green_time)

        if len(upstream)==3:
            self._func=self.phase_t
        elif len(upstream)==4:
            self._func=self.phase_f
        elif len(upstream)==1:
            self._func=self.phase_s
    
    def phase_s(self, current_time):
        u=self.upstream[0]
        d=self.downstream[0]
        d.inflow=min(d.supply,u.demand)
        u.outflow=d.inflow

    def phase_t(self, current_time):
        current_time=(current_time+self.off_set)%self.cycle
        u1, u2, u3 = self.upstream
        d1, d2, d3 = self.downstream
        if self.phase[0]<=current_time<self.phase[1]:
            u1.outflow=min(u1.demand/2,d3.supply)
            d3.inflow=u1.outflow
            d2.inflow=min(u3.demand/2,u2.supply)
            d1.inflow=min(u2.demand/2+u3.demand/2,d1.supply)
            u2.outflow=min(u2.demand/2,d1.supply*u2.demand/(u2.demand+u3.demand))
            u3.outflow=min(u3.demand/2,d1.supply-u2.outflow)+d2.inflow
        elif self.phase[1]<=current_time<self.phase[2]:
            d1.inflow=min(u2.demand/2,d1.supply)
            d2.inflow=min(u3.demand/2,d2.supply)
            u3.outflow=d2.inflow
            d3.inflow=min(u1.demand/2+u2.demand/2,d3.supply)
            u1.outflow=min(u1.demand/2,d3.supply*u1.demand/(u1.demand+u2.demand))
            u2.outflow=min(u2.demand/2,d3.supply-u1.outflow)+d1.inflow
        elif self.phase[2]<=current_time<self.phase[3]:
            d1.inflow=min(u2.demand/2,d1.supply)
            u2.outflow=d1.inflow
            d3.inflow=min(u1.demand/2,d3.supply)
            d2.inflow=min(u1.demand/2+u3.demand/2,d2.supply)
            u3.outflow=min(u3.demand/2,d2.supply*u3.demand/(u1.demand+u3.demand))
            u1.outflow=min(u1.demand/2,d2.supply-u3.outflow)+d3.inflow
    
    def phase_f(self, current_time):
        current_time=(current_time+self.off_set)%self.cycle
        u1, u2, u3, u4 = self.upstream
        d1, d2, d3, d4 = self.downstream
        if self.phase[0]<=current_time<self.phase[1]-3:
            d2.inflow=min(u3.demand/3,d2.supply)
            d4.inflow=min(u1.demand/3,d4.supply)
            d1.inflow=min(u2.demand/3+u3.demand/3,d1.supply)
            d3.inflow=min(u1.demand/3+u4.demand/3,d3.supply)
            u2.outflow=min(u2.demand/3,d1.supply*u2.demand/(u2.demand+u3.demand))
            u4.outflow=min(u4.demand/3,d3.supply*u4.demand/(u1.demand+u4.demand))
            u3.outflow=min(u3.demand/3,d1.supply-u2.outflow)+d2.inflow
            u1.outflow=min(u1.demand/3,d3.supply-u4.outflow)+d4.inflow
        elif self.phase[1]-3<=current_time<self.phase[1]:
            d1.inflow=0
            u1.outflow=0
            d2.inflow=0
            u2.outflow=0
            d3.inflow=0
            u3.outflow=0
            d4.inflow=0
            u4.outflow=0
        elif self.phase[1]<=current_time<self.phase[2]-3:
            d1.inflow=min(u2.demand/3,d1.supply)
            d3.inflow=min(u4.demand/3,d3.supply)
            d2.inflow=min(u1.demand/3+u3.demand/3,d2.supply)
            d4.inflow=min(u1.demand/3+u3.demand/3,d4.supply)
            u2.outflow=d1.inflow
            u4.outflow=d3.inflow
            u3.outflow=min(u3.demand/3,(d4.supply+d2.supply)*u3.demand/(u1.demand+u3.demand))
            u1.outflow=min(u1.demand/3,(d4.supply+d2.supply)*u1.demand/(u1.demand+u3.demand))
        elif self.phase[2]-3<=current_time<self.phase[2]:
            d1.inflow=0
            u1.outflow=0
            d2.inflow=0
            u2.outflow=0
            d3.inflow=0
            u3.outflow=0
            d4.inflow=0
            u4.outflow=0
        elif self.phase[2]<=current_time<self.phase[3]-3:
            d1.inflow=min(u2.demand/3,d1.supply)
            d3.inflow=min(u4.demand/3,d3.supply)
            d2.inflow=min(u3.demand/3+u4.demand/3,d2.supply)
            d4.inflow=min(u1.demand/3+u2.demand/3,d4.supply)
            u1.outflow=min(u1.demand/3,d4.supply*u1.demand/(u1.demand+u2.demand))
            u3.outflow=min(u3.demand/3,d2.supply*u3.demand/(u3.demand+u4.demand))
            u2.outflow=min(u2.demand/3,d4.supply-u1.outflow)+d1.inflow
            u4.outflow=min(u4.demand/3,d2.supply-u3.outflow)+d3.inflow
        elif self.phase[3]-3<=current_time<self.phase[3]:
            d1.inflow=0
            u1.outflow=0
            d2.inflow=0
            u2.outflow=0
            d3.inflow=0
            u3.outflow=0
            d4.inflow=0
            u4.outflow=0
        elif self.phase[3]<=current_time<self.phase[4]-3:
            d2.inflow=min(u3.demand/3,d2.supply)
            d4.inflow=min(u1.demand/3,d4.supply)
            d1.inflow=min(u2.demand/3+u4.demand/3,d1.supply)
            d3.inflow=min(u2.demand/3+u4.demand/3,d3.supply)
            u1.outflow=d4.inflow
            u3.outflow=d2.inflow
            u2.outflow=min(u2.demand/3,(d1.supply+d3.supply)*u2.demand/(u2.demand+u4.demand))
            u4.outflow=min(u4.demand/3,(d1.supply+d3.supply)*u4.demand/(u2.demand+u4.demand))
        elif self.phase[4]-3<=current_time<self.phase[4]:
            d1.inflow=0
            u1.outflow=0
            d2.inflow=0
            u2.outflow=0
            d3.inflow=0
            u3.outflow=0
            d4.inflow=0
            u4.outflow=0

    def calculate_flow(self, current_time):
        """calculate the inflows and outflows for the upstream and downstream sections"""
        self._func(current_time)