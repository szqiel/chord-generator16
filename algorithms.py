"""
algorithms.py
Modul ini mengimplementasikan algoritma penelusuran graf dan model probabilistik.
Setiap fungsi menerima state awal dan mengembalikan array progresi akor.
"""

import random
from collections import deque
from music_data import CHORD_GRAPH, TARGET_LENGTH, CONSTRAINT_TEMPLATE

def greedy_search(start_chord):
    """Mengeksekusi penelusuran heuristik Greedy (Optimal Lokal)."""
    path = [start_chord]
    curr = start_chord
    for _ in range(TARGET_LENGTH - 1):
        neighbors = CHORD_GRAPH[curr]
        if not neighbors:
            break
        # Memilih transisi dengan bobot disonansi paling rendah
        next_chord = min(neighbors, key=neighbors.get)
        path.append(next_chord)
        curr = next_chord
    return path

def dfs_search(start_chord):
    """Mengeksekusi Depth-First Search dengan pengacakan cabang (Shuffling)."""
    stack = [(start_chord, [start_chord])]
    random.seed(42) # Menjaga konsistensi eksperimen pengujian waktu
    
    while stack:
        curr, path = stack.pop()
        
        if len(path) == TARGET_LENGTH:
            return path
            
        neighbors = list(CHORD_GRAPH[curr].keys())
        random.shuffle(neighbors)
        
        for neighbor in neighbors:
            stack.append((neighbor, path + [neighbor]))
    return []

def bfs_search(start_chord):
    """
    Mengeksekusi Breadth-First Search dengan optimasi pemangkasan level-state
    untuk mencegah kompleksitas eksponensial (State-Space Explosion).
    """
    queue = deque([(start_chord, [start_chord])])
    
    for level in range(TARGET_LENGTH - 1):
        next_queue = deque()
        visited_in_level = set()
        
        while queue:
            curr, path = queue.popleft()
            for neighbor in CHORD_GRAPH[curr]:
                if neighbor not in visited_in_level:
                    visited_in_level.add(neighbor)
                    next_queue.append((neighbor, path + [neighbor]))
        queue = next_queue
        if not queue:
            return []
            
    return queue[0][1] if queue else []

def backtracking_search(curr, path):
    """
    Mengeksekusi Backtracking (Constraint Satisfaction).
    Mengintegrasikan pemangkasan estetika harmoni dan array template (wajib melewati simpul tertentu).
    """
    current_depth = len(path)
    if current_depth == TARGET_LENGTH:
        return path
    
    # KENDALA 1: Array Template (Mengecek apakah kedalaman saat ini memiliki akor wajib)
    required_chord = CONSTRAINT_TEMPLATE[current_depth]
    
    neighbors = list(CHORD_GRAPH[curr].keys())
    random.seed(42)
    random.shuffle(neighbors)

    for neighbor in neighbors:
        # Jika terdapat akor wajib pada template, potong cabang selain akor wajib tersebut
        if required_chord is not None and neighbor != required_chord:
            continue
            
        # KENDALA 2: Pencegahan stagnasi nada (Tidak boleh 3 akor minor berturut-turut)
        minors = ['Dm', 'Em', 'Am', 'Fm']
        if current_depth >= 2 and path[-1] in minors and path[-2] in minors and neighbor in minors:
            continue
            
        result = backtracking_search(neighbor, path + [neighbor])
        if result:
            return result
            
    return None

def markov_chain_generation(start_chord, transition_matrix):
    """
    Membangkitkan progresi berdasarkan Matriks Probabilitas Rantai Markov (1st-Order).
    """
    random.seed(101)
    path = [start_chord]
    curr = start_chord
    
    for _ in range(TARGET_LENGTH - 1):
        # Mekanisme fallback (mundur/fallback) apabila state saat ini tidak ada di dalam corpus
        if curr not in transition_matrix or not transition_matrix[curr]:
            curr = 'C' # Kembali ke Tonic sebagai default state
            
        population = list(transition_matrix[curr].keys())
        weights = list(transition_matrix[curr].values())
        next_chord = random.choices(population, weights)[0]
        path.append(next_chord)
        curr = next_chord
        
    return path