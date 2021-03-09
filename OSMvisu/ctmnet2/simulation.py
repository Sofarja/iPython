
# -*- coding: utf-8 -*-

# @Author: KeyangZhang
# @Email: 3238051@qq.com
# @Date: 2019-12-26 10:42:53
# @LastEditTime: 2020-02-13 22:39:19
# @LastEditors: Keyangzhang

from .base import Section,SignalController,Phase
from .base import _Connector
from random import uniform

def _poisson(lam):
    u = uniform(0,1)
    p = 2.718281828459045**(-lam)
    f = p
    k = 0
    if u < f:
        return k
    else:   
        while f < u:
            p = p*lam/(k+1)
            f += p
            k += 1
        return k-1
    

def _constant(x):
    return x

class _Arrival(object):
    """upstream arrival
    
    it is analogue to the demand, which is measured by traffic volume (pcu/hour).
    
    """
    def __init__(self):
        self.section=[]
        self.volume=[]  # pcu/h
        self.dist_func=[]

    def add(self, section, volume, distribution='poisson'):
        self.section.append(section)
        
        self.volume.append(volume) 
        
        if distribution == 'poisson':
            self.dist_func.append(_poisson) # 储存函数名
        elif distribution == 'constant':
            self.dist_func.append(_constant)
        else:
            raise ValueError('No such type of distribution')

    def __getitem__(self, position):
        return (self.section[position],self.volume[position],self.dist_func[position])

    def update(self):
        for sec, vol, func in self:
            vol = vol/3600 # change the scale from pcu/h to pcu/s
            demand = func(vol)
            flow = min(demand, sec.supply)
            sec.inflow = flow

class _Departure(object):
    """downstream departure

    it defines the capacity or congestion level of downstream of certain sections 
    
    """
    def __init__(self):
        self.section=[]
        self.capacity=[]  # pcu/h
        self.dist_func=[]

    def __getitem__(self, position):
        return (self.section[position],self.capacity[position],self.dist_func[position])
    
    def add(self,section, capacity, distribution='constant'):
        self.section.append(section)
        
        self.capacity.append(capacity) 
        
        if distribution == 'constant':
            self.dist_func.append(_constant)
        else:
            raise ValueError('No such type of distribution')
    
    def update(self):
        for sec, cap, func in self:
            cap = cap/3600 # change scale from pcu/h to pcu/s
            supply = func(cap)
            flow = min(supply, sec.demand)
            sec.outflow = flow

class Simulator(object):
    """Simulator
    
    the simulator is designed for creating, connecting and storing elements of the network
    it provides basic functions to execute simulation

    Attributes:
        sections: dict, contains created sections and their ids
        signalcontrollers: dict, contains created signal controllers and their ids
        phases: dict, contains designed phases and their ids
        connectors: list, contains the created connectors

    """
    
    def __init__(self):
        super(Simulator, self).__init__()
        self.sections = {}
        self.signalcontrollers = {}
        self.phases = {}
        self.connectors = []
        self.currenttime = 0
        self.arrival = _Arrival()
        self.departure = _Departure()

    def create(self,objclass,objid,kargs):
        """ create network elements

        it can create the network elements including Section, SignalController, Phase

        Args:
            objclass: str, it should be one of the Section, SignalController or Phase
            kargs: dict, contains the parameters and value for the object you want to create
                   the keys should be consistent with the parameters of the inital function
                   e.g. for Section, it may be {'lanes_length':5,'lanes_number':3,'cell_length':0.5}     

        """
        if objclass=='Section':
            obj = Section(**kargs)
            self.sections[objid]=obj
            return obj
        
        elif objclass=='SignalController':
            obj = SignalController(**kargs)
            self.signalcontrollers[objid]=obj
            return obj
        
        elif objclass=='Phase':
            obj = Phase(**kargs)
            self.phases[objid]=obj
            return obj
        
        elif objclass=='Intersection':
            pass
        
        else:
            raise ValueError('Invalid object creation: '+objclass)

    def connect(self,id_upstream,id_downstream,priority=None):
        """ connect sections

        it is used to connect the created sections 
        
        Args:
            id_upstream: id or tuple/list, the id or the tuple/list of ids of the upstream sections
            id_downstream: id or tuple/list, the id or the tuple/list of ids of the downstream sections
            priority: float, the relative weight of the flows  
        """
        if isinstance(id_upstream,(list,tuple)):
            upstream = [self.sections[i] for i in id_upstream]
            downstream = self.sections[id_downstream]
            cnct = _Connector(upstream,downstream,priority)
            self.connectors.append(cnct)
   
        elif isinstance(id_downstream,(list,tuple)):
            upstream = self.sections[id_upstream]
            downstream = [self.sections[i] for i in id_downstream]
            cnct = _Connector(upstream,downstream,priority)
            self.connectors.append(cnct)
        
        else:
            upstream = self.sections[id_upstream]
            downstream = self.sections[id_downstream]
            cnct = _Connector(upstream,downstream)
            self.connectors.append(cnct)



    def add_lamp(self,controller_id,phase_id,section_id):
        """ add lamp

        add a lamp that controled by a sigal controller on a particular section with designative phase

        Args:
            controller_id, the id of signal controllers that controls this lamp
            pahse_id, the id of phase applied on the lamp
            section_id, the id or tuple/list of id of section on which you want to add a lamp
        """
        sig = self.signalcontrollers[controller_id]
        pha = self.phases[phase_id]
        
        if isinstance(section_id,(tuple,list)):
            for i in section_id:
                sec = self.sections[i]
                sig.add_lamp(sec,pha)
        else:
            sec = self.sections[section_id]
            sig.add_lamp(sec,pha)

    def set_arrival(self,section_id,arrival_volume,distribution='poisson'):
        """set number of vehicles arriving from the upstream
        
        Args:
            section_id: id 
            arrival_volume: int , average number of vehicles arriving per hour
            distribution: str, distribution of arrival

        """
        self.arrival.add(self.sections[section_id],arrival_volume, distribution)
    
    def set_departure(self,section_id,departure_capacity, distribution='constant'):
        """set number of vehicles departing to the downstream
        
        Args:
            section_id: id 
            departure: integer , average number of vehicles departing per second
            distribution: str, distribution of downstream capacity

        """
        self.departure.add(self.sections[section_id],departure_capacity, distribution)
        


    def run(self,sumtime,resfile):
        """ run simulation for sumtime
        
        do NOT make a mixture use of simulator.run and simulator.run_single_step

        Args:
            sumtime: integer, total time of simulation
            resfile: str, output file of the result
        """
        t = 0
        while t<=sumtime:
            self.run_single_step()
            t+=1         

    def run_single_step(self):
        """execute a single step of simulation
        
        do NOT make a mixture use of simulator.run_single_step and simulator.run
        
        """
        # calculate demand and supply
        for sec in self.sections.values():
            sec.calculate_demand()
            sec.calculate_supply()

        # update signal status
        for sig in self.signalcontrollers.values():
            sig.update_signal(self.currenttime)
            
        for sec in self.sections.values():
            sec.inflow=0
            sec.outflow=0

        # set the demand and downstream capacity
        self.arrival.update()
        self.departure.update()

        # calculate flow
        for sec in self.sections.values():
            sec.calculate_flow()
        for cnct in self.connectors:
            cnct.calculate_flow()

        # update volume
        for sec in self.sections.values():
            sec.update_volume()

        self.currenttime+=1
    
    def get_volume(self, level='cell'):
        """get the volume (pcu) of each cell/section at current sim-second

        Args:
            level:str,  it can be cell or section.
        
        Returns:
            volumes: dict, the key is section id and the value is list of volumes of each cell.
                     if level='section', the value is total volume of this section.
            
        """
        volumes = {}
        if level=='cell':
            for i,sec in self.sections.items():
                volumes[i] = [round(c.volume,1) for c in sec]
        elif level=='section':
            for i,sec in self.sections.items():
                volumes[i] = round(sum([c.volume for c in sec]))
        else :
            raise ValueError('no such level for collecting data')
        return volumes
    
    def get_density(self, level='cell'):
        """get the average single-lane density(pcu/km) of each cell/section at current sim-second

        Args:
            level:str,  it can be cell or section.
    
        Returns:
            densities: dict, the key is section id and the value is list of densities of each cell.
                       if level='section', the value is the average signle-lane density of this section
            
        """
        densities = {}
        if level=='cell':
            for i,sec in self.sections.items():
                densities[i] = [round(c.volume/(sec.cell_length*sec.lanes_number),3) for c in sec]
        elif level=='section':
            for i,sec in self.sections.items():
                volume = sum([c.volume for c in sec])
                densities[i] = round(volume/(sec.lanes_length*sec.lanes_number),3)
        else :
            raise ValueError('no such level for collecting data')
        
        return densities
        
    
    def get_occupancy(self,level='cell'):
        """get the occupancy of each cell/section at current sim-second

        Args:
            level:str,  it can be cell or section.
       
        Returns:
            occupancies: dict, the key is section id and the value is list of occupancies of each cell.
                         if level='section', the value is occupancy of this section.
            
        """
        occupancies = {}
        if level=='cell':
            for i,sec in self.sections.items():
                occupancies[i] = [round(c.volume/sec.max_volume,3) for c in sec]
        elif level=='section':
            for i,sec in self.sections.items():
                volume = sum([c.volume for c in sec])
                occupancy = volume/(sec.max_volume*sec.cells_number)
                occupancies[i]=round(occupancy,3)
        else :
            raise ValueError('no such level for collecting data')
        
        return occupancies
    
    def get_velocity(self,level='cell'):
        """get the operation velocity(km/h) of each cell/section at current sim-second

        this velocity is calculated through outflow of each cell

        Args:
            level:str,  it can be cell or section.
  
        Returns:
            velocities: dict, the key is section id and the value is list of velocities of each cell
                        if level='section', the value is average operation velocity of this section.
            
        """
        
        velocities = {}
        if level=='cell':
            for i,sec in self.sections.items():
                
                vels = []
                
                for k, flow in enumerate(sec.flows):
                    vol = sec[k].re_volume
                    if vol==0:
                        vels.append(sec.free_speed)
                    else:
                        vels.append(round(flow*3600/sec.interval/(vol/sec.cell_length),2))
                        #if flow/vol>=0.48:
                            #print("out",sec[k-1].volume,sec[k-1].demand,sec[k].supply,sec[k].volume,sec[k].demand,sec[k+1].supply,sec[k+1].volume,sec[k+1].demand,sec[k+2].supply,vels[-1])
                
                # calculate for the last cell
                flow = sec.outflow
                vol = sec[-1].re_volume
                if vol==0:
                    vels.append(0)
                else:
                    vels.append(round(flow*3600/sec.interval/(vol/sec.cell_length),2))

                velocities[i] = vels
        elif level=='section':
            
            for i,sec in self.sections.items():
                flow = sum(sec.flows)+sec.outflow
                volume = sum([c.volume for c in sec])
                if volume==0:
                    vel = 0
                else:
                    vel = round(flow*3600/sec.interval/(volume/sec.lanes_length),2)
                velocities[i]=vel
                
        
        return velocities
                
    def get_saturation(self, level='cell'):
        pass
                
