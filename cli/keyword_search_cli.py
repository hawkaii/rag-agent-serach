#!/usr/bin/env python3

import argparse
import json
import string
from pathlib import Path
from nltk.stem import PorterStemmer
import pickle

BASE_DIR = Path(__file__).parent.parent
data_path = BASE_DIR / "data" / "movies.json"
stop_words_path = BASE_DIR / "data" / "stopwords.txt"
cache_dir = BASE_DIR / "cache"

with open(data_path, "r", encoding="utf-8") as f:
    data = json.load(f)
movies = data["movies"]

with open(stop_words_path, "r", encoding="utf-8") as f:
    stop_words = f.read().splitlines()

stemmer = PorterStemmer()


class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.docmap = {}

    def __add_document(self, doc_id, text):
        text_clean = remove_punc(text.lower())
        tokens = remove_stop_words_stem(split_word(text_clean))
        for token in tokens:
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(doc_id)

    def get_documents(self, term):
        term = term.lower()
        doc_ids = self.index.get(term, set())
        return sorted(doc_ids)

    def build(self, movies):
        for doc_id, movie in enumerate(movies):
            tit_desc = f"{movie['title']} {movie['description']}"
            # print(tit_desc)
            self.__add_document(doc_id, tit_desc)
            self.docmap[doc_id] = movie

    def save(self):
        cache_dir.mkdir(parents=True, exist_ok=True)

        with open(cache_dir / "index.pkl", "wb") as f:
            pickle.dump(self.index, f)
        with open(cache_dir / "docmap.pkl", "wb") as f:
            pickle.dump(self.docmap, f)

    def load(self):
        import os

        if not os.path.exists(cache_dir / "index.pkl"):
            raise FileNotFoundError("Index Not Found")
        with open(cache_dir / "index.pkl", "rb") as f:
            self.index = pickle.load(f)
        with open(cache_dir / "docmap.pkl", "rb") as f:
            self.docmap = pickle.load(f)


def remove_stop_words_stem(tokens: list[str]) -> list[str]:
    """Remove stop words from a list of tokens."""
    filtered_ls = [token for token in tokens if token not in stop_words]
    res = []
    for token in filtered_ls:
        res.append(stemmer.stem(token))
    return res


def remove_punc(text: str) -> str:
    """Remove all punctuation from text."""
    return text.translate(str.maketrans("", "", string.punctuation))


def split_word(text: str) -> list[str]:
    """Split text into tokens, removing empty tokens."""
    return [token for token in text.split() if token]


def matches_query(query_tokens: list[str], title_tokens: list[str]) -> bool:
    """Check if at least one query token matches any part of a title token."""
    for q_token in query_tokens:
        for t_token in title_tokens:
            if q_token in t_token:
                return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    build_parser = subparsers.add_parser("build", help="Build the parser index")

    args = parser.parse_args()

    match args.command:
        case "search":
            # print the search query here
            query = args.query

            inverted_index = InvertedIndex()
            inverted_index.load()
            results = []
            query_tokens = split_word(query.lower())
            query_filtered = remove_stop_words_stem(query_tokens)
            for token in query_filtered:
                doc_ids = inverted_index.get_documents(token)
                for doc_id in doc_ids:
                    if doc_id not in results:
                        results.append(doc_id)
                    if len(results) >= 5:
                        break
                if len(results) >= 5:
                    break

            print(f"Searching for: {query}")
            for i, doc_id in enumerate(results, 1):
                movie = inverted_index.docmap[doc_id]
                print(f"{i}. {movie['title']} (id : {doc_id})")
        case "build":
            index = InvertedIndex()
            index.build(movies)
            index.save()

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
