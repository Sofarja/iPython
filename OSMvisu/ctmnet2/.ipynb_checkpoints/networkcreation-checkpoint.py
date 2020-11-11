# -*- coding: utf-8 -*-

# @Author: KeyangZhang
# @Email: 3238051@qq.com
# @Date: 2019-12-26 15:55:54
# @LastEditTime: 2020-02-13 16:32:44
# @LastEditors: Keyangzhang

from .simulation import Simulator
import xml.etree.ElementTree as ET


def create_from_xml(netfile=None,sigfile=None,simulator=None):

    if simulator is None:
        simulator = Simulator()

    # create section and connection
    if netfile is not None:
        tree = ET.parse(netfile)
        root = tree.getroot()
        paras = ['lanes_length','lanes_number',
            'cell_length','free_speed',
            'wave_speed','jam_density']
        for sec in root.iter('section'):
            sec_id = sec.attrib['id']
            argdict = {para:eval(sec.find(para).text) for para in paras}
            simulator.create('Section',sec_id, argdict)

        for cnc in root.iter('connection'):
            downstream = cnc.find('downstream').text.split(' ')
            if len(downstream)==1:
                downstream = downstream[0]
            
            upstream = cnc.find('upstream').text.split(' ')
            if len(upstream)==1:
                upstream = upstream[0]
            
            priority = cnc.find('priority').text
            if priority is None:
                simulator.connect(upstream,downstream)
            else:
                priority = list(map(eval,priority.slipt(' ')))
                simulator.connect(upstream,downstream)
    
    # config signal control
    if sigfile is not None:
        tree = ET.parse(sigfile)
        root = tree.getroot()

        # create signal controllers
        paras = ['cycle','offset']
        for sc in root.iter('signalcontroller'):
            sc_id = sc.attrib['id']
            argdict = {para:eval(sc.find(para).text) for para in paras}
            simulator.create('SignalController',sc_id,argdict)
        
        # create phase
        paras = ['green_start','green_end']
        for ph in root.iter('phase'):
            ph_id = ph.attrib['id']
            argdict = {para:eval(ph.find(para).text) for para in paras}
            simulator.create('Phase',ph_id,argdict)
        
        # create lamp
        for lamp in root.iter('lamp'):
            controller_id = lamp.find('controller_id').text
            ph_id = lamp.find('phase_id').text
            sec_id = lamp.find('section_id').text.split(' ')
            simulator.add_lamp(controller_id,ph_id,sec_id)

    return simulator