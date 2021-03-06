import xml.etree.ElementTree as et

from helpers.stringhelper import generate_code
from resources.namespaces import *
from models.bpmn.container import Container

class Definitions(Container):

    def __init__(self, **args):
        Container.__init__(self, **args)

        self.ignore_attrs('collaboration')

        self.elements['process'] = []
        self.elements['message'] = []

        self.collaboration = args.get('collaboration', 'Collaboration_' + generate_code())

    def serialize(self):
        # register namespaces
        self.register_namespaces()

        # instantiate element
        element = Container.serialize(self)

        # Create a collaboration element
        collaboration = et.Element(bpmn + 'collaboration')
        collaboration.attrib['id'] = self.collaboration

        # Append participants elements to collaboration element
        for process in self.elements['process']:
            # get the participant id
            participant_id = 'participant_' + generate_code() if process.participant == None else str (process.participant)
            # prepare an xml node
            participant = et.Element(bpmn + 'participant')
            participant.attrib['id'] = participant_id
            participant.attrib['processRef'] = str (process.id)
            if process.name != None: participant.attrib['name'] = str (process.name)
            # configure process
            process.participant = participant_id

            collaboration.append(participant)

        # Append message flows to collaboration
        for message in self.elements['message']:
            collaboration.append(message.serialize())

        # Prepend collaboration
        element.insert(0, collaboration)

        return element

    # responsible for registring namespaces
    def register_namespaces(self):
        for prefix in namespaces.keys():
            et.register_namespace(prefix, namespaces[prefix])