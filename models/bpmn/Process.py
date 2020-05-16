import xml.etree.ElementTree as et

from models.bpmn.Container import Container
from models.bpmn.Lane import Lane


class Process(Container):

    def __init__(self, **args):
        Container.__init__(self, **args)

        self.definitions = self.expects(args, 'definitions')

        if self.definitions != None:
            self.definitions.add('process', self)

        self.ignore_attrs('definitions')

    def serialize(self):
        processElement = Container.serialize(self)

        if 'lane' in self.elements:
            laneSetElement = et.Element("laneSet")

            for lane in self.elements['lane']:
                laneElement = lane.serialize()
                laneSetElement.append(laneElement)

            processElement.append(laneSetElement)

        return processElement

    def add(self, name, *items):
        Container.add(self, name, *items)

        if name == 'lane':
            for lane in items:
                lane.process = self