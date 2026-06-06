"""
main.py
Titik masuk utama (entry point) dari sistem generator progresi akor.
Melakukan inisialisasi lingkungan pengujian, merangkum fungsi, dan mencetak laporan waktu komputasi.
"""

import time
from music_data import CORPUS_DATA, CONSTRAINT_TEMPLATE
from trainer import train_first_order_markov
from algorithms import (
    greedy_search, 
    dfs_search, 
    bfs_search, 
    backtracking_search, 
    markov_chain_generation
)

def run_experiment():
    # 1. Melatih Model Stokastik
    print("Menganalisis korpus dataset dan melatih Matriks Markov...")
    markov_matrix = train_first_order_markov(CORPUS_DATA)
    
    # 2. Mendefinisikan Skenario Pengujian (Entry Nodes)
    START_CHORD_GRAF = 'G'
    START_CHORD_BACKTRACKING = CONSTRAINT_TEMPLATE[0] # Mengikuti aturan wajib dari user ('Am')
    
    algorithms = {
        "Greedy": lambda: greedy_search(START_CHORD_GRAF),
        "DFS": lambda: dfs_search(START_CHORD_GRAF),
        "BFS": lambda: bfs_search(START_CHORD_GRAF),
        "Backtracking": lambda: backtracking_search(START_CHORD_BACKTRACKING, [START_CHORD_BACKTRACKING]),
        "Markov Chain": lambda: markov_chain_generation(START_CHORD_GRAF, markov_matrix)
    }

    # 3. Mengeksekusi Benchmarking
    print("\n" + "=" * 115)
    print(f"{'HASIL PENGUJIAN KOMPUTASIONAL GENERATOR AKOR (16 BAR)':^115}")
    print("=" * 115)
    print(f"{'Metode Algoritma':<16} | {'Waktu (ms)':<10} | {'Keluaran Progresi (Output)'}")
    print("-" * 115)

    for name, func in algorithms.items():
        start_time = time.perf_counter_ns()
        result = func()
        end_time = time.perf_counter_ns()
        
        # Konversi resolusi nanodetik ke milidetik untuk pelaporan presisi
        elapsed_ms = (end_time - start_time) / 1_000_000
        
        if result:
            progression = " - ".join(result)
        else:
            progression = "[GAGAL] Tidak ditemukan jalur yang memenuhi kendala (constraint)."
            
        print(f"{name:<16} | {elapsed_ms:<10.4f} | {progression}")
        
    print("=" * 115)

if __name__ == "__main__":
    run_experiment()