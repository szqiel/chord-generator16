"""
trainer.py
Modul ini bertanggung jawab untuk melatih (training) model probabilitas
berdasarkan korpus data, mengimplementasikan 1st-Order dan 2nd-Order Markov Chain.
"""

from collections import defaultdict

def train_first_order_markov(corpus):
    """
    Membangun matriks transisi probabilitas Orde-1.
    Probabilitas keadaan berikutnya P(X_{t+1}) hanya bergantung pada P(X_t).
    """
    counts = defaultdict(lambda: defaultdict(int))
    
    for song in corpus:
        for i in range(len(song) - 1):
            curr_chord = song[i]
            next_chord = song[i+1]
            counts[curr_chord][next_chord] += 1
            
    probability_matrix = defaultdict(dict)
    for curr_chord, transitions in counts.items():
        total = sum(transitions.values())
        for next_chord, count in transitions.items():
            probability_matrix[curr_chord][next_chord] = count / total
            
    return probability_matrix

def train_second_order_markov(corpus):
    """
    Membangun matriks transisi probabilitas Orde-2 (Implementasi lanjutan).
    Menggunakan Tuple (X_{t-1}, X_t) sebagai kunci (key) untuk menentukan X_{t+1}.
    """
    counts = defaultdict(lambda: defaultdict(int))
    
    for song in corpus:
        for i in range(len(song) - 2):
            # Mendefinisikan riwayat dua keadaan sebelumnya sebagai tuple
            state_history = (song[i], song[i+1])
            next_chord = song[i+2]
            counts[state_history][next_chord] += 1
            
    probability_matrix = defaultdict(dict)
    for history, transitions in counts.items():
        total = sum(transitions.values())
        for next_chord, count in transitions.items():
            probability_matrix[history][next_chord] = count / total
            
    return probability_matrix