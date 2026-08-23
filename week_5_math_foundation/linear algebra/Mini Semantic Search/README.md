# 🔍 Mini Semantic Search Engine

> **Learning Project** — Building a semantic search engine from scratch using pure Linear Algebra concepts.  
> Part of the *"Mathematics Behind AI"* learning series.

---

## 📌 What This Project Does

This project implements a **Semantic Search Engine** — a system that finds documents that are *meaningfully similar* to a query, not just keyword matches.

For example, if you search for `"animals that are loyal"`, it will rank **"Dogs are loyal animals."** and **"Puppies are cute animals."** higher than **"Python is a programming language."** — even though none share the exact query words.

---

## 🧠 The Core Idea: Meaning as a Vector

Every sentence is converted into a **vector** (a list of numbers) that represents its meaning in a high-dimensional space. Sentences with similar meanings will have vectors that **point in similar directions**.

```
"Dogs are loyal animals."   → [0.12, -0.45, 0.87, ...]  (384 numbers)
"Puppies are cute animals." → [0.15, -0.40, 0.80, ...]  (close direction!)
"Python is a language."     → [-0.60, 0.30, -0.10, ...]  (very different direction)
```

---

## 📐 The Mathematics — Step by Step

### Step 1 — Encode Sentences into Vectors (Embeddings)

```python
model = SentenceTransformer('all-MiniLM-L6-v2')
doc_emb   = model.encode(documents)   # Shape: (10, 384)
query_emb = model.encode(query)       # Shape: (384,)
```

The model maps each sentence into a **384-dimensional vector**.  
Think of it as coordinates in a 384-dimensional space — each dimension captures some aspect of meaning.

---

### Step 2 — Normalize the Vectors (Unit Vectors)

To compare directions (not magnitudes), we convert every vector to a **unit vector** — a vector with length = 1.

**Formula:**

```
v_hat = v / ||v||     where  ||v|| = sqrt(v1^2 + v2^2 + ... + vn^2)
```

```python
# Normalize the query
norm            = np.sqrt(np.sum(query_emb**2))   # ||query||
query_normalize = query_emb / norm               # unit vector

# Normalize all documents (row-wise)
doc_norm       = np.sqrt(np.sum(doc_emb**2, axis=1, keepdims=True))  # shape: (10,1)
doc_normalize  = doc_emb / doc_norm                                    # shape: (10, 384)
```

**Why normalize?**  
Without normalization, longer sentences produce larger vectors, making them *appear* more similar just because they are bigger. Normalizing puts all vectors on the same unit sphere so we only compare **direction**, not size.

---

### Step 3 — Cosine Similarity via Dot Product

Since both vectors are normalized (length = 1), the dot product **equals the cosine of the angle** between them:

```
similarity(A, B) = A_hat · B_hat = cos(θ)
```

| Angle θ | cos(θ) | Meaning |
|---------|--------|---------|
| 0°      | 1.0    | Identical direction → most similar |
| 90°     | 0.0    | Perpendicular → unrelated |
| 180°    | -1.0   | Opposite direction → most dissimilar |

```python
query_n_transpose = query_normalize.T                      # Shape: (384, 1)
dot_product       = doc_normalize @ query_n_transpose      # Shape: (10, 1)
```

This one matrix multiplication computes the similarity score of **all 10 documents at once** — that's the power of linear algebra!

---

### Step 4 — Rank Results

```python
similarity = np.argsort(-dot_product, axis=0).squeeze()   # sort descending
```

`argsort` returns the **indices** that would sort the array. The `-` makes it sort in descending order (highest similarity first).

---

### Step 5 — Display Results

```python
final = list(zip(f_dot_product[similarity], doc[similarity]))

for score, sentence in final:
    print(f"{score:.2f} --> {sentence}")
```

---

## 🗂️ Project Structure

```
Mini Semantic Search/
│
├── documents.py      # The corpus — 10 sample sentences to search through
├── embedding.py      # Core logic: encode → normalize → dot product → rank
├── app.py            # (Planned) Entry point / UI
├── search.py         # (Planned) Refactored search module
├── .gitignore        # Ignores .venv/ and __pycache__/
└── README.md         # You are here
```

---

## 🔬 Key Linear Algebra Concepts Used

| Concept | Where Used |
|---|---|
| **Vectors** | Each sentence becomes a 384-D vector |
| **Vector Norm (L2)** | `np.sqrt(np.sum(v**2))` — computing vector length |
| **Unit Vectors** | Dividing by norm to get direction-only vectors |
| **Dot Product** | `doc_normalize @ query_n_transpose` — measuring alignment |
| **Matrix Multiplication** | Computing all similarities in one operation |
| **Cosine Similarity** | `dot(unit_A, unit_B) = cos(θ)` |
| **argsort / Ranking** | Sorting indices by similarity score |

---

## ⚙️ Setup & Run

**1. Create a virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
```

**2. Install dependencies**
```bash
pip install sentence-transformers numpy
```

**3. Run the search**
```bash
python embedding.py
```

**4. Try a query**
```
Enter your Sentence : animals that are friendly
```

**Expected output (example):**
```
0.87 --> Dogs are loyal animals.
0.81 --> Puppies are cute animals.
0.45 --> Cats love sleeping.
0.12 --> Machine learning uses data.
...
```

---

## 💡 What's Happening Under the Hood (Intuition)

Imagine every sentence as an **arrow** pointing in some direction in a huge room (384 dimensions). Sentences about similar topics point in similar directions.

When you type a query, its arrow is computed. The search engine then finds which document arrows are **most aligned** (smallest angle) with your query arrow. That's cosine similarity.

```
Query: "loyal animals" ──────────►
Doc 1: "Dogs are loyal" ─────────►  ← small angle = HIGH similarity ✅
Doc 2: "Python language" ──────────────────────────────────────► ← large angle = LOW similarity ❌
```

---

## 🚀 Next Steps to Explore

- [ ] Add more documents to `documents.py` and observe ranking changes
- [ ] Try different queries and see how meaning is captured
- [ ] Implement `search.py` as a reusable function
- [ ] Build a simple CLI or web UI in `app.py`
- [ ] Visualize embeddings in 2D using PCA or t-SNE
- [ ] Try building your own simple TF-IDF embedding from scratch

---

## 📚 Learning Resources

- [3Blue1Brown — Essence of Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab)
- [Cosine Similarity — Wikipedia](https://en.wikipedia.org/wiki/Cosine_similarity)
- [Sentence Transformers Docs](https://www.sbert.net/)

---

*Built while learning the mathematics behind AI — from vectors to meaning.* 🧮
