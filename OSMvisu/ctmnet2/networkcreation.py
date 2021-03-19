# -*- coding: utf-8 -*-

# @Author: KeyangZhang
# @Email: 3238051@qq.com
# @Date: 2019-12-26 15:55:54
# @LastEditTime: 2020-02-13 16:32:44
# @LastEditors: Keyangzhang

from .simulation import Simulator
import xml.etree.ElementTree as ET
import re


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
            downstream = re.findall(r"\d+\.?\d*",cnc.find('downstream').text)
            upstream = re.findall(r"\d+\.?\d*",cnc.find('upstream').text)
            green_time = re.findall(r"\d+\.?\d*",cnc.find('green_time').text)
            off_set = eval(cnc.find('off_set').text)
            simulator.connect(upstream,downstream,green_time,off_set)

    return simulator