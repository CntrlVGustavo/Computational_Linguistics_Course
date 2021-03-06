import math
from scipy.stats import spearmanr
from embeddings import Embeddings


def read_simlex(embeddings, infile = 'data/SimLex-999.txt'):
    simlex = {}
    for idx, item in enumerate(open(infile)):
        if idx == 0: continue
        w1, w2, pos, val = item.strip().lower().split('\t')[0:4]
        if pos != 'n': continue
        if not (w1 in embeddings and w2 in embeddings): continue
        simlex[(w1,w2)] = float(val) / 10.0
    return simlex

def read_wordsim(embeddings, infile = 'data/wordsim353_set2.tab'):
    wordsim = {}
    for idx, item in enumerate(open(infile)):
        if idx == 0: continue
        w1, w2, val = item.strip().lower().split('\t')[0:3]
        if not (w1 in embeddings and w2 in embeddings): continue
        wordsim[(w1,w2)] = float(val) / 10.0
    return wordsim

def score_word_dataset(embeddings, dataset):
    """
    Calculate Spearman's Rho for word similarity on the given dataset.

    The dataset is obtained from the read_simlex or read_wordsim functions.

    To do this, collect lists of the gold similarity values and the
    model values generated by word embedding similarity, and pass
    both lists to the spearmanr function. The spearmanr function
    has two return values, you want to return only the first one.

    Parameters
    ----------
    dataset : dict of the form { (word, word) : similarity_val }
        WordSim-353 or SimLex-999 dataset.

    Returns
    -------
    float
        The Spearman's Rho ranked correlation coefficient between 
        the emeddings and the human judgments.
    """
    # >>> YOUR ANSWER HERE
    model_values = []
    golden_values = []
    #looping through the keys of the dictionary "dataset" to get a list of golden values and a list of model generated values
    for key in dataset:
        w1 = key[0]
        w2 = key[1]

        #calculating word similarity using the word vectors
        model_values.append(embeddings.cosine_similarity( w1, w2))
        #getting the human scores of word similarity
        golden_values.append(dataset[key])

    return spearmanr(golden_values, model_values)[0]
    # >>> END YOUR ANSWER
    


if __name__ == '__main__':
    embeddings = Embeddings()    

    simlex = read_simlex(embeddings)
    wordsim = read_wordsim(embeddings)

    print('WordSim-353 score:', score_word_dataset(embeddings, wordsim))
    print('SimLex-999 score:', score_word_dataset(embeddings, simlex))
    
