
_embedding_model = None

def get_embedding_model():
    """
    A lazy-loading function to get the sentence-transformer model.
    It loads the model only once, the first time it is called.
    """
    from sentence_transformers import SentenceTransformer
    global _embedding_model
    
    if _embedding_model is None:
        print("--- LAZY LOADING: Loading sentence-transformer model for the first time... ---")
        _embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("--- LAZY LOADING: Model loaded successfully. ---")
        
    return _embedding_model