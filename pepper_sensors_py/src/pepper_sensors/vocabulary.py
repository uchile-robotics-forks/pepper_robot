voc = {'confirm' :[
        'pepper yes',
        'pepper no'
    ],
    'pepperconfidencetest' : [
        'bring me a',
        'apple',
        'lemon',
        'potato'
    ]
}
"""Vocabulary as dict. The keys of this dict is directly linked to the rostopic under which the sentences under that 
keys are published.
Example: Under the key 'confirm' there lies a list of variants of confirms (yes/ no). If Pepper hears one of this 
sentences, it will be published under the rostopic /pepper/speechrec/confirm . 
"""


def generateVocabularies(pathToBNFs):
    """
    TODO: Write this method. Should generate the vocabularies out of the grammar of the jsgf files.
    :param pathToBNFs: a list of paths to the bnf files which contains the grammar to which shall be listened
    :return: 
    """
    pass

