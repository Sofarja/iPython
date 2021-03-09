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
        self.lanes_number = lanes_number*2
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

class SignalController(object):
    """SignalController
    
    this class resembles the signal controller at the intersection, 
    which controls the signal light status of each entrance

    Attributes:
        entrances: list, contains the sections controled by this signal controller
                   and its phase is recorded in the corresponding position of phase list
        phases: list, contains the phases applied by this signal controller
                and each phase is corresponding to a entrance in the entrance list
        cycle: the cycle of the signal plan applied by this signal controller, the unit is second
               for its definition, please refer to the traffic signal control theory
        offset: the offset of the signal plan applied by this signal controller, the unit is second
                for its definition, please refer to the traffic signal control theory

    """
    
    def __init__(self, cycle, offset=0):
        super(SignalController, self).__init__()
        self.entrances = []
        self.phases = []
        self.cycle = cycle
        self.offset = offset
    
    def add_lamp(self,section,phase):
        """add a lamp on a section"""
        s = phase.green_start%self.cycle
        e = phase.green_end%self.cycle
        self.entrances.append(section)
        self.phases.append((s,e))
    
    def update_signal(self,current_time):
        """update the status of light controled by this signal controller"""
        time = (current_time+self.offset)%self.cycle
        for sec,(s,e) in zip(self.entrances,self.phases):
            if not (s<=time<=e):
                # when the light is red, the section cannot generate demand
                sec.demand=0

class Phase(object):
    """Phase

    A phase is a specific movement that has a unique signal indication
    different intersections can have the same phase combination

    Attributes:
        green_start: the start time of green status of a lamp in the cycle, the unit is second
        green_end: the end time of green status of a lamp in the cycle, the unit is second

    """
    def __init__(self, green_start, green_end):
        super(Phase, self).__init__()
        self.green_start = green_start
        self.green_end = green_end

class _Connector(object):
    """Connector

    the connector connects the upstream sections and downstream sections
    and it does not have volume and is used merely for calcuate flows between sections

    Attributes:
        upstream: list/tuple or Section, the upstream section/sections
        downstream: list/tuple or Section, the downstream section/sections
        connect_type: string, there are following three types of connection
                      confluent: the upstream has mutilple sections (<=3) while the downstream only has one
                      split: the upstream has one section while the downstream has severals (<=3)
                      straight: the upstream and downstream both only have one section
        

    """

    def __init__(self, upstream, downstream,priority=None):
        super(_Connector, self).__init__()
        self.upstream = upstream
        self.downstream = downstream
        
        if isinstance(upstream,(tuple,list)) and isinstance(downstream,Section) :
            self.upnum = len(upstream)
            self.downnum = 1
            self.connect_type='confluent'
            self._func=self._confluent
            
            if priority is not None:
                s = sum(priority)
                self.priority = [p/s for p in priority]  # standardize the priority
            else:
                self.priority = [1/self.upnum for i in range(self.upnum)]
        
        elif isinstance(upstream,Section) and isinstance(downstream,(tuple,list)):
            self.upnum=1
            self.downnum=len(downstream)
            self.connect_type = 'split'
            self._func=self._split
            
            if priority is not None:
                s = sum(priority)
                self.priority = [p/s for p in priority]  # standardize the priority
            else:
                self.priority = [1/self.downnum for i in range(self.downnum)]
        
        elif isinstance(upstream,Section) and isinstance(downstream,Section) :
            self.upnum=1
            self.downnum=1
            self.connect_type = 'straight'
            self._func = self._straight
        
        else:
            raise ValueError('cannot connect these two objects')


    def _straight(self):
        """the calculate method for staright connection"""
        
        flow = min(self.upstream.demand, self.downstream.supply)
        self.upstream.outflow = flow
        self.downstream.inflow = flow
    
    def _split(self):
        """the calculate method for split connection"""
        
        temp = [self.upstream.demand]
        for item, p in zip(self.downstream, self.priority):
            temp.append(item.supply)
        
        flow = min(temp) # total flow
        
        self.upstream.outflow = flow
        
        for item, p in zip(self.downstream, self.priority):
            item.inflow += p * flow

    def _confluent(self):
        """the calculate method for confluent connection"""
        
        # self.upnum == 2 means that this is a conflunce section
        if self.upnum == 2 :
            u1, u2 = self.upstream
            p1, p2 = self.priority
            supply = self.downstream.supply
            if (u1.demand+u2.demand)/2 <= supply:
                u1.outflow += u1.demand/2
                u2.outflow += u2.demand/2
                self.downstream.inflow = (u1.demand+u2.demand)/2
            else:
                flow1 = _mid(u1.demand/2, supply-u2.demand/2, p1*supply)
                flow2 = _mid(u2.demand/2, supply-u1.demand/2, p2*supply)
                u1.outflow += flow1
                u2.outflow += flow2
                self.downstream.inflow = (flow1+flow2)
        
        # self.upnum == 3 means that this connector is in the intersection
        elif self.upnum == 3:
            
            # use "rec" to record entrance that is not in red (demand is not 0)
            rec = [] 
            for i,item in enumerate(self.upstream):
                if item.demand == 0:
                    item.outflow=0
                else:
                    rec.append(i)
            
            if len(rec) == 2 :
                u1 = self.upstream[rec[0]]
                p1 = self.priority[rec[0]]
                u2 = self.upstream[rec[1]]
                p2 = self.priority[rec[1]]
                
                # adjust p1 and p2 to satisfy the condition sum(priorities)=1
                s = p1 + p2
                p1 = p1/s
                p2 = p2/s
                
                supply = self.downstream.supply
                if (u1.demand+u2.demand)/3 <= supply:
                    u1.outflow = u1.demand/3
                    u2.outflow = u2.demand/3
                    self.downstream.inflow = (u1.demand+u2.demand)/3
                else:
                    flow1 = _mid(u1.demand/3, supply-u2.demand/3, p1*supply)
                    flow2 = _mid(u2.demand/3, supply-u1.demand/3, p2*supply)
                    u1.outflow = flow1
                    u2.outflow = flow2
                    self.downstream.inflow = (flow1+flow2)/3
            elif len(rec) == 1:
                u = self.upstream[rec[0]]
                flow = min(u.demand/3, self.downstream.supply)
                u.outflow = flow
                self.downstream.inflow = flow
            else:
                # that means len(rec)==3 
                sumdemand = sum([item.demand for item in self.upstream])/3
                if sumdemand <= self.downstream.supply:
                    for item in self.upstream:
                        item.outflow += item.demand/3
                    self.downstream.inflow = sumdemand
                else:
                    u1, u2, u3 = self.upstream
                    p1, p2, p3 = self.priority
                    supply = self.downstream.supply
                    flow1 = _mid(u1.demand/3, supply-u2.demand/3-u3.demand/3, p1*supply)
                    flow2 = _mid(u2.demand/3, supply-u1.demand/3-u3.demand/3, p2*supply)
                    flow3 = _mid(u3.demand/3, supply-u1.demand/3-u2.demand/3, p3*supply)
                    u1.outflow += flow1
                    u2.outflow += flow2
                    u3.outflow += flow3
                    self.downstream.inflow = (flow1+flow2+flow3)
                    
                    """"flows = [p*self.downstream.supply for p in self.priority]
                    sumdemand = 0
                    for item, flow in zip(self.upstream, flows):
                        item.outflow = min(flow, item.demand)
                        sumdemand = sumdemand+item.outflow
                    self.downstream.inflow = sumdemand"""

        else:
            raise ValueError('there is a confluentor having more than three branches.')
    
    def calculate_flow(self):
        """calculate the inflows and outflows for the upstream and downstream sections"""
        self._func()

