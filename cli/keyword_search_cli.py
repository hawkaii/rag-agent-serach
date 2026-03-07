#!/usr/bin/env python3

import argparse
import json
import string
from pathlib import Path
from nltk.stem import PorterStemmer

BASE_DIR = Path(__file__).parent.parent
data_path = BASE_DIR / "data" / "movies.json"
stop_words_path = BASE_DIR / "data" / "stopwords.txt"

with open(data_path, "r", encoding="utf-8") as f:
    data = json.load(f)
movies = data["movies"]

with open(stop_words_path, "r", encoding="utf-8") as f:
    stop_words = f.read().splitlines()

stemmer = PorterStemmer()


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

    args = parser.parse_args()

    match args.command:
        case "search":
            # print the search query here
            query = args.query

            results = []
            for movie in movies:
                title_clean = remove_punc(movie["title"]).lower()
                query_tokens = split_word(query.lower())
                title_tokens = split_word(title_clean)
                query_filtered = remove_stop_words_stem(query_tokens)
                title_filtered = remove_stop_words_stem(title_tokens)
                if matches_query(query_filtered, title_filtered):
                    results.append(movie)

            results = results[:5]

            print(f"Searching for: {query}")
            for i, movie in enumerate(results, 1):
                print(f"{i}. {movie['title']}")

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
