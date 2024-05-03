import nltk
nltk.download('punkt')

from datasketch import MinHash, MinHashLSH
from nltk.tokenize import word_tokenize
from collections import defaultdict

# Глобальные настройки проекта
NUM_PERM = 128  # Длина MinHash сигнатуры
THRESHOLD = 0.3  # Порог для LSH

# Функция токенизации текста
def tokenize_text(text):
    return word_tokenize(text.lower())

# Генерация списка вхождений для каждого "слова"
def generate_word_entries(documents):
    word_entries = defaultdict(list)
    for doc_id, text in documents.items():
        tokens = tokenize_text(text)
        for token in tokens:
            word_entries[token].append(doc_id)
    return word_entries

# Генерация MinHash сигнатур
def generate_minhash_signatures(documents, num_perm=NUM_PERM):
    minhash_signatures = {}
    for doc_id, text in documents.items():
        tokens = tokenize_text(text)
        minhash = MinHash(num_perm=num_perm)
        for token in tokens:
            minhash.update(token.encode('utf-8'))
        minhash_signatures[doc_id] = minhash
    return minhash_signatures

# Поиск похожих документов
def find_similar_documents(minhash_signatures, threshold=THRESHOLD, num_perm=NUM_PERM):
    lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)
    for doc_id, minhash in minhash_signatures.items():
        lsh.insert(doc_id, minhash)
    similar_documents = {}
    for doc_id, minhash in minhash_signatures.items():
        similar_docs = lsh.query(minhash)
        similar_docs.remove(doc_id)
        similar_documents[doc_id] = similar_docs
    return similar_documents

documents = {
    "doc1": "The sun rises in the east and sets in the west",
    "doc2": "Stars twinkle in the night sky",
    "doc3": "The moon orbits around the earth",
    "doc4": "The earth revolves around the sun",
    "doc5": "The sun is a star in the Milky Way galaxy",
    "doc6": "The night sky is full of stars and galaxies",
    "doc7": "The Milky Way is just one of billions of galaxies",
    "doc8": "The universe is vast and infinite",
    "doc9": "The speed of light is approximately 299,792 kilometers per second",
    "doc10": "The universe is constantly expanding"
}

word_entries = generate_word_entries(documents)
minhash_signatures = generate_minhash_signatures(documents)
similar_documents = find_similar_documents(minhash_signatures)

for doc_id, similar_docs in similar_documents.items():
    print(f"Similar documents for {doc_id}: {similar_docs}")
