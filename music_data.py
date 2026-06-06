"""
music_data.py
Modul ini mendefinisikan ruang keadaan (state space) dalam bentuk graf berbobot,
serta menyediakan korpus (corpus) dataset untuk melatih rantai Markov (Markov Chain).
"""

# ---------------------------------------------------------
# 1. GRAF TRANSISI AKOR (Voice Leading & Circle of Fifths)
# ---------------------------------------------------------
# Himpunan simpul (V) dan sisi (E) direpresentasikan menggunakan Adjacency List.
# Bobot sisi merepresentasikan tingkat disonansi musikal.
CHORD_GRAPH = {
    'C': {'G': 1, 'F': 1, 'Am': 2, 'E7': 3, 'Fm': 4}, 
    'Dm': {'G': 1, 'G7': 1, 'Am': 2},
    'Em': {'Am': 1, 'A7': 2, 'F': 3}, 
    'F': {'C': 1, 'G': 2, 'Dm': 2, 'Fm': 1},
    'Fm': {'C': 1, 'G': 2}, 
    'G': {'C': 1, 'Am': 2, 'E7': 3},
    'G7': {'C': 1, 'Am': 2},
    'Am': {'F': 1, 'Dm': 2, 'Em': 2, 'D7': 3}, 
    'A7': {'Dm': 1, 'F': 3},
    'D7': {'G': 1, 'G7': 1},
    'E7': {'Am': 1, 'F': 3},
    'Bdim': {'C': 1, 'Am': 2}
}

# ---------------------------------------------------------
# 2. KORPUS DATASET (Untuk melatih model stokastik)
# ---------------------------------------------------------
# Merepresentasikan data historis dari progresi musik genre Alternative Rock.
CORPUS_DATA = [
    ['C', 'F', 'Fm', 'C', 'E7', 'Am', 'F', 'G'],  # Karakteristik pergerakan mayor ke minor (F -> Fm)
    ['C', 'G', 'Am', 'Em', 'F', 'C', 'Dm', 'G7'], # Pergerakan standar diatonis
    ['Am', 'F', 'C', 'G', 'Am', 'F', 'E7', 'Am'], # Resolusi dominan sekunder (E7 -> Am)
    ['C', 'Am', 'F', 'G', 'C', 'F', 'Fm', 'C']    # Pola progresi pop-rock klasik
]

# ---------------------------------------------------------
# 3. TEMPLATE KENDALA BACKTRACKING (Constraint Satisfaction)
# ---------------------------------------------------------
# Array template untuk memaksa algoritma Backtracking melewati simpul tertentu.
# 'None' merepresentasikan status variabel bebas (unassigned variable).
TARGET_LENGTH = 16
CONSTRAINT_TEMPLATE = ['Am'] + [None]*6 + ['F'] + [None]*7 + ['E7'] 
# Hasil array: ['Am', None, None, None, None, None, None, 'F', None, None, None, None, None, None, None, 'E7']