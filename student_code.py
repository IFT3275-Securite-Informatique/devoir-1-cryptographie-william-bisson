from collections import Counter
import random as rnd
import requests

# Fonction pour charger le texte d'un corpus depuis une URL et enlever les 10 000 premiers caractères
def load_text_from_web(url):
    response = requests.get(url)
    response.raise_for_status()  # Vérifie que la requête a réussi
    return response.text[10000:]  # Enlever les 10 000 premiers caractères

# Fonction pour couper un texte en paires de caractères
def cut_string_into_pairs(text):
    pairs = []
    for i in range(0, len(text) - 1, 2):
        pairs.append(text[i] + text[i + 1])
    if len(text) % 2 != 0:
            pairs.append(text[-1] + '_')  # Ajoute un caractère de remplissage si nécessaire
    return pairs

# Fonction pour analyser le corpus et créer la liste de symboles
def analyser_corpus(text):
    caracteres = list(set(list(text)))
    nb_caracteres = len(caracteres)
    nb_bicaracteres = 256 - nb_caracteres
    bicaracteres = [item for item, _ in Counter(cut_string_into_pairs(text)).most_common(nb_bicaracteres)]
    symboles = caracteres + bicaracteres
    return symboles

# Fonction pour générer un dictionnaire de substitution
def gen_key(symboles):
    l = len(symboles)
    if l > 256:
        return False

    rnd.seed(1337)
    int_keys = rnd.sample(list(range(l)), l)
    dictionary = {s: "{:08b}".format(k) for s, k in zip(symboles, int_keys)}
    return dictionary

# Fonction principale de déchiffrement qui prend un cryptogramme `C` en paramètre
def decrypt(C):
    # Charger et combiner les deux corpus pour générer la clé de déchiffrement
    url1 = "https://www.gutenberg.org/ebooks/13846.txt.utf-8"
    url2 = "https://www.gutenberg.org/ebooks/4650.txt.utf-8"
    corpus1 = load_text_from_web(url1)
    corpus2 = load_text_from_web(url2)
    corpus = corpus1 + corpus2
    
    # Analyse du corpus pour créer la liste de symboles
    symboles = analyser_corpus(corpus)
    
    # Générer le dictionnaire de substitution et l'inverser
    K = gen_key(symboles)
    if not K:
        raise ValueError("Erreur : le nombre de symboles dépasse la limite autorisée de 256.")
    
    K_inverse = {v: k for k, v in K.items()}
    
    # Segmenter en blocs de 8 bits et déchiffrer
    bit_segments = [C[i:i+8] for i in range(0, len(C), 8)]
    decoded_text = ''.join([K_inverse.get(segment, '?') for segment in bit_segments])
    
    # Imprimer le message déchiffré
    print("Message déchiffré :", decoded_text)
    
    return decoded_text
