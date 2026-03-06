#!/usr/bin/env python3

import argparse
import json
import string
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
data_path = BASE_DIR / "data" / "movies.json"

with open(data_path, "r", encoding="utf-8") as f:
    data = json.load(f)
movies = data["movies"]


def remove_punc(text: str) -> str:
    """Remove all punctuation from text."""
    return text.translate(str.maketrans("", "", string.punctuation))


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
            for movie in data["movies"]:
                title_clean = remove_punc(movie["title"]).lower()
                if query.lower() in title_clean:
                    results.append(movie)

            results = results[:5]

            print(f"Searching for: {query}")
            for i, movie in enumerate(results, 1):
                print(f"{i}. {movie['title']}")

            pass
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
