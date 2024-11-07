from collections import Counter
import random as rnd

# Fonction pour analyser le corpus et créer la liste de symboles
def analyser_corpus(text):
    def cut_string_into_pairs(text):
        pairs = []
        for i in range(0, len(text) - 1, 2):
            pairs.append(text[i] + text[i + 1])
        if len(text) % 2 != 0:
            pairs.append(text[-1] + '_')  # Ajouter un caractère de remplissage si nécessaire
        return pairs

    caracteres = list(set(list(text)))
    nb_caracteres = len(caracteres)
    nb_bicaracteres = 256 - nb_caracteres
    bicaracteres = [item for item, _ in Counter(cut_string_into_pairs(text)).most_common(nb_bicaracteres)]
    symboles = caracteres + bicaracteres
    return symboles

# Fonction pour générer un dictionnaire de substitution et l'inverser
def gen_key(symboles):
    l = len(symboles)
    if l > 256:
        return False

    rnd.seed(1337)
    int_keys = rnd.sample(list(range(l)), l)
    dictionary = {s: "{:08b}".format(k) for s, k in zip(symboles, int_keys)}
    return dictionary

# Fonction principale de déchiffrement, autonome
def decrypt(C):
    # Utiliser un exemple de corpus pour générer la clé
    corpus = "texte d'exemple pour générer les symboles pour le déchiffrement par substitution"
    
    # Étape 1 : Analyse du corpus pour créer la liste de symboles
    symboles = analyser_corpus(corpus)
    
    # Étape 2 : Générer le dictionnaire de substitution et l'inverser
    K = gen_key(symboles)
    if not K:
        raise ValueError("Erreur : le nombre de symboles dépasse la limite autorisée de 256.")
    
    K_inverse = {v: k for k, v in K.items()}
    
    # Étape 3 : Déchiffrer le texte chiffré
    bit_segments = [C[i:i+8] for i in range(0, len(C), 8)]
    decoded_text = ''.join([K_inverse.get(segment, '?') for segment in bit_segments])
    
    return decoded_text

# Appel de la fonction pour voir le résultat du déchiffrement
message_dechiffre = decrypt()
print("Message déchiffré :", message_dechiffre)
