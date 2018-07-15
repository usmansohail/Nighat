# nighat
This is a program that will translate [Blissymbolics](http://www.blissymbolics.org/) to English sentences. From the Blissymbolics website:
> Blissymbolics is a semantic graphical language that is currently composed of more than 5000 authorized symbols - Bliss-characters and Bliss-words. It is a generative language that allows its users to create new Bliss-words as needed. It is used by individuals with severe speech and physical impairments around the world, but also by others for language learning and support, or just for the fascination and joy of this unique language representation. For more information on Blissymbolics. 


#### Example 
The program can take the [following symbols](nighat_1/documentation/images/ex_for_a_boy.JPG), and output: 
```
for a boy and his family
``` 

#### Structure
Most of the classes used in the system are included in the *classes.py* file, 
with the exception of the n-gram model class stored in *n_gram.py*. Any user adjustments 
should be made in the *system_tools.py* file. 



###### Citations
Bird, Steven, Edward Loper and Ewan Klein (2009), Natural Language Processing with Python. O’Reilly Media Inc (https://nltk.org)
Nick Johnson, Algorithm of the Week: Damn Cool Levenshtein Automata \(2013\), DZone (https://dzone.com/articles/algorithm-week-damn-cool-1)
