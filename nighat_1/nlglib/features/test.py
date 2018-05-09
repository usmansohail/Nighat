from nlglib.realisation.simplenlg.realisation import Realiser
from nlglib.microplanning import *


realise_en = Realiser(host='roman.kutlak.info', port=40000)

p = Clause(NP('this', 'example'), VP('show', 'how cool simplenlg is'))
print(realise_en(p))
