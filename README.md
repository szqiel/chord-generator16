# Analisis Komparatif Generator Progresi Akor 16 Bar Berbasis Strategi Deterministik dan Stokastik

Repositori ini berisi kode program untuk eksperimen komputasional proyek akhir mata kuliah **Analisis dan Strategi Algoritma (ASA)**, Departemen Informatika, Universitas Diponegoro. Proyek ini membandingkan performa komputasi (kompleksitas waktu eksekusi) dan kualitas estetika musikal dari lima strategi algoritma berbeda dalam membangkitkan progresi akor sepanjang 16 bar untuk genre musik *Alternative Rock* dan *Britpop*.

---

## 🏛️ Desain Permasalahan & Pemodelan Data

Generator ini memodelkan pergerakan progresi akor menggunakan dua representasi utama:

1. **Pemodelan Graf Terarah ($G = (V, E)$)**:
   * **Simpul ($V$)**: Himpunan kosakata akor triad diatonis dasar C Mayor ditambah dengan *borrowed chord* (`Fm`) serta *secondary dominants* (`E7`, `A7`, `D7`).
   * **Sisi ($E$)**: Kemungkinan transisi antar-akor yang dirancang berdasarkan prinsip *voice leading* (efisiensi pergerakan nada) dan jarak kedekatan harmonis dalam *Circle of Fifths*.
   * **Bobot Sisi ($w$)**: Tingkat disonansi musikal ($w \in \{1, 2, 3, 4\}$), di mana bobot $1$ merupakan pergerakan yang paling konsonan (natural) dan $4$ merupakan transisi modal yang lebih disonan.
2. **Pemodelan Stokastik Markov**:
   * Dilatih menggunakan korpus data historis (`CORPUS_DATA`) dari lagu-lagu populer alternative rock untuk mengekstraksi probabilitas transisi empiris musisi manusia ke dalam matriks probabilitas transisi.

---

## 🗂️ Struktur Proyek

Kode program diorganisasikan menggunakan prinsip *Separation of Concerns* ke dalam modul-modul berikut:

* **[`music_data.py`](file:///c:/Users/SYAIR/Documents/PRAKTIKUM%20AJG!/Praktikum%20ASA/ChordProgression/chord-generator16/music_data.py)**: Berisi basis pengetahuan musikal, meliputi adjacency list graf akor (`CHORD_GRAPH`), korpus latih musik (`CORPUS_DATA`), dan template kendala Backtracking (`CONSTRAINT_TEMPLATE`).
* **[`trainer.py`](file:///c:/Users/SYAIR/Documents/PRAKTIKUM%20AJG!/Praktikum%20ASA/ChordProgression/chord-generator16/trainer.py)**: Modul untuk melatih model probabilitas stokastik, mendukung pembuatan matriks probabilitas Rantai Markov Orde-1 (`train_first_order_markov`) dan Orde-2 (`train_second_order_markov`).
* **[`algorithms.py`](file:///c:/Users/SYAIR/Documents/PRAKTIKUM%20AJG!/Praktikum%20ASA/ChordProgression/chord-generator16/algorithms.py)**: Berisi implementasi logika pencarian graf dan pembangkitan probabilistik:
  * `greedy_search`
  * `dfs_search`
  * `bfs_search`
  * `backtracking_search`
  * `markov_chain_generation`
* **[`main.py`](file:///c:/Users/SYAIR/Documents/PRAKTIKUM%20AJG!/Praktikum%20ASA/ChordProgression/chord-generator16/main.py)**: Titik masuk utama (*entry point*) program yang menguji kelima algoritma secara simultan, mengukur waktu eksekusi aktual menggunakan *high-resolution performance counter* (`time.perf_counter_ns()`), dan menyajikan hasil pengujian dalam bentuk tabel.

---

## 🧠 Implementasi Algoritma

### 1. Greedy Search (Deterministik - Heuristik Lokal)

Algoritma Greedy melakukan pemilihan akor secara sekuensial dengan mengambil keputusan optimal secara lokal pada setiap langkah. Algoritma ini mengevaluasi simpul tetangga dari akor saat ini dan memilih akor berikutnya dengan bobot sisi (disonansi) terkecil ($w_{min}$).

* **Kompleksitas Waktu**: $\mathcal{O}(V)$ per pencarian, di mana $V$ adalah jumlah simpul tetangga.
* **Karakteristik Musikal**: Pergerakan nada sangat monoton, repetitif (misal: `C - G - C - G`), dan mudah terjebak pada optimal lokal tanpa memori jangka panjang.

### 2. Depth-First Search / DFS (Deterministik - traversal Mendalam)

DFS menelusuri graf sedalam mungkin hingga kedalaman 16 bar. Agar luaran tidak bersifat kaku dan deterministik, urutan simpul tetangga diacak (*shuffled*) pada setiap langkah. Pengujian menggunakan *random seed* tetap untuk menjaga konsistensi perbandingan performa.

* **Kompleksitas Waktu**: $\mathcal{O}(V + E)$
* **Karakteristik Musikal**: Menghasilkan variasi progresi yang sangat luas, namun sering kali menghasilkan lompatan nada yang tidak natural atau melenceng terlalu jauh ke akor minor yang terlampau gelap.

### 3. Breadth-First Search / BFS (Deterministik - Traversal Melebar)

BFS menelusuri graf tingkat demi tingkat (lebar). Karena BFS murni pada graf siklik akan memicu ledakan ruang keadaan (*state-space explosion*) dengan kompleksitas ruang eksponensial $\mathcal{O}(b^d)$ (di mana $b$ adalah branching factor dan $d=16$), diimplementasikan teknik **Level-State Deduplication**. Teknik ini membatasi hanya satu status akor unik yang disimpan dalam queue pada setiap tingkat kedalaman (bar).

* **Kompleksitas Waktu**: Dioptimasi menjadi $\mathcal{O}(V \cdot d)$
* **Karakteristik Musikal**: Menjamin rute terpendek secara matematis, namun setara kaku dan repetitifnya dengan Greedy karena sifat jalur-terpendek yang dimilikinya.

### 4. Backtracking (Deterministik - Constraint Satisfaction Problem / CSP)

Algoritma Backtracking menyelesaikan progresi akor dengan memperlakukannya sebagai CSP. Algoritma melakukan traversal mendalam dengan menerapkan dua kendala (*constraints*):

1. **Kendala Dinamis (*Pruning*)**: Mencegah stagnasi musikal yang terlalu gelap dengan melarang kemunculan tiga akor minor berturut-turut (`Dm`, `Em`, `Am`, `Fm`).
2. **Kendala Absolut (*Template Alignment*)**: Memaksa progresi akor untuk mematuhi template absolut: bar ke-1 wajib `Am`, bar ke-8 wajib `F`, dan bar ke-16 wajib `E7`.
   Jika penugasan akor melanggar salah satu kendala, algoritma akan memangkas cabang (*pruning*) dan melakukan runut balik (*backtrack*).

* **Kompleksitas Waktu**: Batas atas terburuk $\mathcal{O}(b^N)$ di mana $b$ adalah branching factor dan $N=16$ (bar).
* **Karakteristik Musikal**: Sangat terstruktur, mematuhi kaidah harmoni tonal dengan ketat, dan berhasil memenuhi struktur wajib lagu populer.

### 5. Rantai Markov Orde-1 (Stokastik - Probabilistik)

Berbeda dengan pencarian graf di atas, Rantai Markov beroperasi secara stokastik menggunakan matriks probabilitas transisi yang dilatih dari data historis. Keadaan berikutnya $X_{t+1}$ dipilih menggunakan *weighted random selection* berdasarkan probabilitas kondisional $P(X_{t+1} \mid X_t)$. Jika sistem menemui keadaan yang tidak didefinisikan dalam data latih, algoritma secara otomatis menggunakan mekanisme *fallback* kembali ke akor dasar Tonic (`C`).

* **Kompleksitas Waktu**: $\mathcal{O}(1)$ per transisi
* **Karakteristik Musikal**: Menghasilkan progresi paling dinamis dan natural yang menyerupai pola ciptaan musisi manusia, berhasil mereplikasi gaya (*style imitation*) khas alternatif rock seperti pergerakan modal `F` ke `Fm` mayor-minor.

---

## ⚡ Hasil Eksperimen Komputasional

Eksperimen benchmarking dijalankan menggunakan Python 3.12 pada perangkat keras yang seragam dengan mencatat waktu eksekusi dalam satuan milidetik (ms).

Berikut adalah hasil ringkasan pengujian (Skenario dimulai dari akor **G Major**):

| Metode Algoritma       | Waktu Eksekusi (ms) | Keluaran Progresi Akor (16 Bar)                                           |
| :--------------------- | :-----------------: | :------------------------------------------------------------------------ |
| **Greedy**       |      0.0249 ms      | G - C - G - C - G - C - G - C - G - C - G - C - G - C - G - C             |
| **DFS**          |      0.0693 ms      | G - E7 - Am - Em - Am - F - C - F - G - C - Fm - G - Am - Dm - G - Am     |
| **BFS**          |      0.0870 ms      | G - C - G - C - G - C - G - C - G - C - G - C - G - C - G - C             |
| **Backtracking** |      0.1213 ms      | Am - Em - A7 - F - Dm - G7 - Am - F - Dm - G7 - Am - Em - A7 - F - G - E7 |
| **Markov Chain** |      0.0491 ms      | G - Am - F - E7 - Am - F - Fm - C - G - Am - F - Em - Am - F - Fm - C     |

### Analisis Kritis *Trade-Off*:

* **Algoritma Pencarian Graf Tradisional (Greedy & BFS)** tidak cocok untuk penulisan karya seni musik yang kreatif karena kecenderungannya mencari rute terpendek yang memicu repitisi kaku.
* **Backtracking** merupakan pilihan terbaik untuk skenario yang membutuhkan struktur harmoni yang ketat (seperti mematuhi penempatan bagian verse/chorus), namun memiliki overhead komputasi yang paling tinggi karena tumpukan rekursif dan proses validasi kendala.
* **Markov Chain** menawarkan keseimbangan (*trade-off*) paling optimal karena memberikan waktu eksekusi yang sangat cepat ($\mathcal{O}(1)$ per langkah) sekaligus kualitas estetika musikal tertinggi berdasarkan kebiasaan komposisi musisi manusia.

---

## 🚀 Cara Menjalankan Program

### Persyaratan Sistem

Program ini murni menggunakan pustaka bawaan standar (*standard library*) Python 3.x, sehingga **tidak membutuhkan** instalasi dependensi pihak ketiga (`pip`).

### Langkah Eksekusi

1. Clone repositori ini ke komputer Anda:
   ```bash
   git clone https://github.com/szqiel/chord-generator16.git
   cd chord-generator16
   ```
2. Jalankan berkas utama:
   ```bash
   python main.py
   ```

---

## 📚 Referensi Akademik

1. D. Tymoczko, "The Geometry of Musical Chords," *Science*, vol. 313, no. 5783, pp. 72-74, 2006.
2. J. S. Vassallo, Ö. Sandred, and J. Vincenot, "NeuralConstraints: integrating a neural generative model with constraint-based composition," *Frontiers in Computer Science*, vol. 7, 2025.
3. T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein, *Introduction to Algorithms*, 4th ed. Cambridge, MA: MIT Press, 2022.
4. MusMat Research Group, "An Introduction to Markov Chains in Music Composition and Analysis," *Journal MusMat*, vol. III, no. 2, pp. 19-42, Dec. 2019.
5. S. J. Russell and P. Norvig, *Artificial Intelligence: A Modern Approach*, 3rd ed. Upper Saddle River, NJ: Prentice Hall, 2010.
6. S. Kostka, D. Payne, and B. Almén, *Tonal Harmony*, 8th ed. New York: McGraw-Hill Education, 2017.
7. H. Tsushima, E. Nakamura, K. Itoyama, and K. Yoshii, "Function- and Rhythm-Aware Melody Harmonization Based on Tree-Structured Parsing and Split-Merge Sampling of Chord Sequences," in *Proc. 18th Int. Soc. Music Inf. Retr. Conf. (ISMIR)*, 2017.
