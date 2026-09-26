import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


KNOWLEDGE_BASE_DIR = "knowledge_base"


def load_knowledge_base():
    """
    Load all text files from the knowledge_base directory.
    """

    documents = []

    for filename in os.listdir(KNOWLEDGE_BASE_DIR):

        if filename.endswith(".txt"):

            file_path = os.path.join(
                KNOWLEDGE_BASE_DIR,
                filename
            )

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read()

                documents.append({
                    "source": filename,
                    "content": content
                })

    return documents


def create_chunks(documents):
    """
    Split knowledge-base documents into topic-based chunks.
    """

    chunks = []

    for document in documents:

        sections = document["content"].split("\n\n")

        current_chunk = ""

        for section in sections:

            section = section.strip()

            if not section:
                continue

            # Combine smaller related sections
            if len(current_chunk) < 400:
                current_chunk += "\n\n" + section

            else:
                chunks.append({
                    "source": document["source"],
                    "content": current_chunk.strip()
                })

                current_chunk = section

        # Add the final remaining chunk
        if current_chunk.strip():

            chunks.append({
                "source": document["source"],
                "content": current_chunk.strip()
            })

    return chunks

def retrieve_relevant_context(query, top_k=4):
    """
    Retrieve the most relevant knowledge-base chunks
    for the user's network problem.
    """

    documents = load_knowledge_base()
    chunks = create_chunks(documents)

    if not chunks:
        return []

    chunk_texts = [
        chunk["content"]
        for chunk in chunks
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(
        chunk_texts + [query]
    )

    chunk_vectors = vectors[:-1]
    query_vector = vectors[-1]

    similarities = cosine_similarity(
        query_vector,
        chunk_vectors
    ).flatten()

    ranked_indices = similarities.argsort()[::-1]

    results = []

    for index in ranked_indices[:top_k]:

        if similarities[index] > 0:

            results.append({
                "source": chunks[index]["source"],
                "content": chunks[index]["content"],
                "score": float(similarities[index])
            })

    return results