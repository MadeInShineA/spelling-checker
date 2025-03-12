ALPHABET = [chr(c) for c in range(ord("a"), ord("z") + 1)] + ["é", "à", "è", "ù", "â", "ê", "î", "ô", "û", "ë", "ï", "ö", "ü", "ÿ", "ç", "æ", "œ"]
FILENAME = "word_frequencies_200000.tsv"

def ajouter_lettre(mot) -> set[str]:
    """Retourne une liste de mots obtenus en ajoutant chaque lettre de l'
    alphabet à n'importe quelle position du mot."""
    return set([mot[0:i] + letter + mot[i:len(mot)] for i in range(len(mot)+1) for letter in ALPHABET])

def supprimer_lettre(mot) -> set[str]:
    """Retourne une liste de mots obtenus en supprimant une lettre du mot à n'
    importe quelle position."""
    return set([mot[0:i] + mot[i+1:len(mot)] for i in range(len(mot))])

def substituer_lettre(mot) -> set[str]:
    """Retourne une liste de mots obtenus en remplaçant chaque lettre du mot
    par une autre lettre de l'alphabet."""
    return set([mot[0:i] + letter + mot[i+1:len(mot)] for i in range(len(mot)) for letter in ALPHABET])

def transposer_lettres(mot) -> set[str]:
    """Retourne une liste de mots obtenus en échangeant deux lettres contiguës
    dans le mot."""
    return set([mot[0:i] + mot[i+1] + mot[i] + mot[i+2:len(mot)] for i in range(len(mot)-1)])

def edits1(mot)-> set[str]:
    return ajouter_lettre(mot) | supprimer_lettre(mot) | substituer_lettre(mot) | transposer_lettres(mot)

def editsn(mot, n=2)-> set[str]:
    res = edits1(mot)
    base_res = res.copy()

    for i in range(n-1):
        for word in base_res:
            res |= edits1(word)
        base_res = res.copy()
    return res

def load_dictionary(filename: str)-> dict:
    res = {}
    with open(filename, "r") as file:
        # Get rid of the header line
        file.readline()

        while line := file.readline():
            word, frequency = line.split("\t")
            res[word] = int(frequency)

    return res


def correct_spelling(mot: str, max_corr=2) -> str:
    res = ""
    max_freq = 0
    frequency_dict = load_dictionary(FILENAME)

    for i in range(1, max_corr+1):
        edited_words = editsn(mot, i)

        for word in edited_words:
            if word in frequency_dict and frequency_dict[word] > max_freq:
                max_freq = frequency_dict[word]
                res = word
        if res != "":
            break
    return res
