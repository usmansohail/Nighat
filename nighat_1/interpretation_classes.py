import time
from nltk.corpus import wordnet

class axiom(object):

    def __init__(self, type):
        # type is a string that summarizes the axiom
        self.type = type

        # get the synonyms of the type word
        syns = wordnet.synsets(self.type)
        self.trigger_words = [syn.lemmas()[0].name() for syn in syns]


class Goal(axiom):

    def __init__(self, eventuality, agent):
        axiom.__init__('goal')
        self.goal_eventuality = eventuality
        self.agent = agent

class Need(axiom):

    def __init__(self, eventuality, constraint):
        axiom.__init__('need')
        self.eventuality = eventuality
        self.constraint = constraint

class Eventuality(axiom):

    def __init__(self, event, constraints=None, rexist=False, make_true=None):
        axiom.__init__('eventuality')
        self.event = event
        self.rexist = rexist
        self.constraints = constraints
        self.make_true = make_true
        syns = wordnet.synsets(self.event)
        self.trigger_words = [syn.lemmas()[0].name() for syn in syns]

        # constraints are the events such that if they occur, then the given event will occur


class Observation():

    def __init__(self, mode, data):
        self.mode = mode
        self.data = data

class Knowledge_base():

    def __init__(self):
        self.axioms = []                            # will be a set of Eventualities, Needs, Goals, Etc.
        self.neccessitators = []                    # axioms that generate an eventuality that has not occured
        self.facilitators = []                      # axioms that generate an eventuality that did occur
        self.inferences = []                        # knowledge inferred from axioms

    def add_knowledge(self, axiom):
        self.axioms.append(axiom)

        if type(axiom) == Need or type(axiom) == Goal:
            self.neccessitators.append(axiom)
        if type(axiom) == Eventuality:
            self.facilitators.append(axiom)


    def get_axioms(self):
        return self.axioms

    def make_inference(self, inference):
        self.inferences.append(inference)

class Interpreter():

    def __init__(self):
        self.interpretation_techiniques = {}           # the set of all tools that can be used to infer things
        self.observations = {}                      # keep all observations as a function of something
        self.knowledge_base = Knowledge_base()

    def observe(self, input, key=time.time()):
        self.observations[key] = input                 # key can be anything, but will be default of time

        # search the facilitators for an axiom that has the input 


########
# Passport info
########
constants = {}

constants['name'] = 'name'


name = "name"
# TODO: use a formal grammar

item_1 = Need(Eventuality(('take', 'tylenol')), ('doctor said', 'prescription'))

item_2 = Need(Eventuality(('take', 'advil')), Eventuality('fever'))

item_3 = Goal(Eventuality('read'), name)



neccessities = []