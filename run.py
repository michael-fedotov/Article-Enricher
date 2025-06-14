from llm_enrich import enrich_with_llm
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Process an article and enrich it with media/links."
    )

    parser.add_argument(
        "article_path",
        type=str,
        help="Path to the markdown article"

    )

    parser.add_argument(
        "keywords_path",
        type=str,
        help="Path to the file containing keywords."
    )

    args = parser.parse_args()

    print(args.article_path)
    print(args.keywords_path)


if __name__ == "__main__":
    main()