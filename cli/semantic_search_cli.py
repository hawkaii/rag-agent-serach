#!/usr/bin/env python3

import argparse

from cli.lib.semantic_search import verify_model, embed_text


def main():
    parser = argparse.ArgumentParser(description="Semantic Search CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    embed_parser = subparsers.add_parser(
        "embed_text", help="generated embedding given a text"
    )
    embed_parser.add_argument("text", type=str, help="Text to embed")

    subparsers.add_parser("verify")

    args = parser.parse_args()

    match args.command:
        case "verify":
            return verify_model()
        case "embed_text":
            return embed_text(args.text)
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
