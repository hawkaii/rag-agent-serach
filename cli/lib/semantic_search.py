from sentence_transformers import SentenceTransformer


class SemanticSearch:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def generate_embedding(self, text):
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty or whitespace")
        result = self.model.encode([text])
        return result[0]


def embed_text(text):
    sem_search = SemanticSearch()
    embedding = sem_search.generate_embedding(text)
    print(f"Text: {text}")
    print(f"First 3 dimensions: {embedding[:3]}")
    print(f"Dimensions: {embedding.shape[0]}")


def verify_model():
    sem_search = SemanticSearch()
    model = sem_search.model

    print(f"Model loaded: {model}")
    print(f"Max sequence length: {model.max_seq_length}")
