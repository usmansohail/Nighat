from system_tools import SystemTools
import time
from nltk.corpus import wordnet


#CONSTANTS
MAX_ITER = 25

class axiom(object):

    def __init__(self, type, func=None):
        # type is a string that summarizes the axiom
        self.type = type

        # get the synonyms of the type word
        syns = wordnet.synsets(self.type)
        self.trigger_words = [type] + [syn.lemmas()[0].name() for syn in syns]

        self.function = func

class Goal(axiom):

    def __init__(self, eventuality, agent='self'):
        axiom.__init__(self, 'goal')
        self.goal_eventuality = eventuality
        self.agent = agent
        self.trigger_words = ['like', 'want']


class Need(axiom):

    def __init__(self, eventuality, constraint):
        axiom.__init__(self, 'need')
        self.eventuality = eventuality
        self.constraint = constraint

        # get trigger words for the constraint
        syns = wordnet.synsets(constraint)
        self.constraint_triggers = [constraint] + [syn.lemmas()[0].name() for syn in syns]


class Eventuality(axiom):

    def __init__(self, event, constraints=None, rexist=False, make_true=None, weights=None):
        axiom.__init__(self, 'eventuality')
        self.event = event
        self.rexist = rexist
        self.constraints = constraints
        self.make_true = make_true
        syns = wordnet.synsets(self.event)
        self.trigger_words = [syn.lemmas()[0].name() for syn in syns]
        self.weights = weights

        # constraints are the events such that if they occur, then the given event will occur

def fever_heart_rate(heart_rate):
    if int(heart_rate) > 102:
        return 'fever'
    else:
        return None

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

        # add manual functions
        self.axioms.append(axiom('heart_rate', func=fever_heart_rate))
        self.add_knowledge(Need(Eventuality('take', constraints='tylenol'), 'fever'))
        self.add_knowledge(Goal(Eventuality('cook', constraints='pasta')))

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

    def find_axiom(self, key_word, need=False):

        # iterate through each axiom to find the relevant ones
        for axiom in self.axioms:
            for key in axiom.trigger_words:
                if key_word in key:

                    # if we are searching for a need then impose this constraint
                    if need:
                        if type(axiom) == Need:
                            return axiom
                    else:
                        return axiom
        return None


class Inference:

    def __init__(self, axiom_used, words_in_order=None, action=None, ref_object=None, subject='None', observation=None):
        self.words_in_order = words_in_order
        self.action = action
        self.ref_object = ref_object
        self.subject = subject
        self.observation = observation
        self.trigger_words = axiom_used.trigger_words
        self.axiom = axiom_used

        # create a dictionary with all these elements in it
        self.content = {}
        self.content['words_in_order'] = self.words_in_order
        self.content['action'] = self.action
        self.content['ref_object'] = self.ref_object
        self.content['subject'] = self.subject
        self.content['observation'] = self.observation

    def get_content_keys(self):
        # return all the keys that lead to something
        valid_keys = []
        for key in self.content.keys():
            if self.content[key] is not None:
                valid_keys.append(key)
        return valid_keys

    def is_equal(self, existing_inference):
        # assume the two inferences are the same
        equal = True
        for key in self.content.keys():
            if self.content[key] != existing_inference.content[key]:
                equal = False
        return equal


class Interpreter():

    def __init__(self):
        self.interpretation_techiniques = {}           # the set of all tools that can be used to infer things
        self.observations = {}                      # keep all observations as a function of something
        self.knowledge_base = Knowledge_base()
        self.inferences = {}
        self.last_inference = None

    def observe(self, input, key=time.time()):
        self.observations[key] = input                 # key can be anything, but will be default of time

        # search the facilitators for an axiom that has the input 

    def observe_file(self, input_file):
        for observation in input_file.readlines():
            observation = observation.split(',')
            key = observation[0]
            value = observation[-1]
            self.observe(observation, key=key)
            self.infer(observation)
        self.secondary_infer()

    def infer(self, observation):
            # find the right axiom
            r_axiom = self.knowledge_base.find_axiom(observation[0])

            # if an axiom was found, try and use the function defined by it
            if r_axiom is not None:
                if r_axiom.function is not None:
                    inference_observation = r_axiom.function(observation[-1])
                    print("Observation: ", observation, " lead to the inference: ", inference_observation)
                    new_inference = Inference(r_axiom, observation=inference_observation)
                    self.inferences[time.time()] = new_inference
                    self.last_inference = new_inference

    def is_new_inference(self, inference):
        # assume it is a new inference
        is_new = True
        for existing_inference in self.inferences.items():
            if inference.is_equal(existing_inference[1]):
                is_new = False
        return is_new

    def secondary_infer(self, iteration=0):
        # keep track of how many inferences were made
        num_inference = 0

        # ensure that the algorithm hasn't gone past the max recursive depth
        if iteration < MAX_ITER:

            # store  the new inferences
            temp_inferences = []

            # go through all the inferences recursively, to see if they combine to create any new observations
            for inference in self.inferences.items():

                # check if the axiom was used or not
                axiom_used = False
                for axiom in self.knowledge_base.axioms:
                    if type(axiom) == Need:
                        for trigger_word in axiom.constraint_triggers:
                            if not axiom_used:
                                if trigger_word == inference[1].observation:
                                    # the axiom has been used
                                    axiom_used = True

                                    # infer what is needed
                                    action_needed = axiom.eventuality.event
                                    object_needed = axiom.eventuality.constraints
                                    new_inference = Inference(axiom, words_in_order=[action_needed, object_needed],
                                                              action=action_needed, ref_object=object_needed)

                                    # ensure that this inference has not been made before
                                    if self.is_new_inference(new_inference):

                                        # display results
                                        print("Infer: ", action_needed, " ", object_needed, "   ", new_inference)

                                        # store the new inference
                                        self.last_inference = new_inference
                                        temp_inferences.append((time.time(), new_inference))

                                        # increment inferences
                                        num_inference += 1

            # recursively iterate, if an inference was made
            if num_inference > 0:
                for inference in temp_inferences:
                    self.inferences[inference[0]] = inference[1]
                self.secondary_infer(iteration + 1)

    def apply_inferences(self, sentence_words):
        return_sentences = [sentence_words]
        for i, word in enumerate(sentence_words):
            for inference in self.inferences.values():
                new_sentence = sentence_words.copy()
                valid_change = False
                if inference.trigger_words is not None:
                    for i_word in inference.trigger_words:
                        if i_word == word:
                            # replace the next word with the constraint of the axiom
                            if i + 1 < len(sentence_words):
                                if type(inference.axiom) == Need:
                                    new_sentence[i + 1] = inference.axiom.eventuality.constraints
                                valid_change = True
                    if valid_change:
                        return_sentences.append(new_sentence)
        return return_sentences

    def interpret(self, observation_file, symbols_file):
        # make the observations and store them
        self.observe_file(observation_file)

        # create the blissymbolics builder
        system_tools = SystemTools()

        # open the file with the test set
        book_1 = symbols_file

        # for each line, build a sentence
        lines = []
        for i, line in enumerate(book_1):
            if line[0] is not "#":
                l = str(line).split(' ')
                for j, word in enumerate(l):
                    l[j] = str(word).split(',')
                    l[j] = [int(x.strip()) for x in l[j] if x is not '\n']
                lines.append(l)
                print("Input: ", l)
                sentence_words = system_tools.build_sentence(l, articles=False)

                # search the words to see if any should be modified based on observations/inferences
                possible_sentences = self.apply_inferences(sentence_words)

                # print each sentence
                print('\nPossible sentences: \n')
                for sentence in possible_sentences:
                    system_tools.get_most_likely_sentence([[x] for x in sentence])

    # def interpret_word(self, word_ids):
