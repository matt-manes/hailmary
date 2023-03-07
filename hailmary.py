import argparse
from pathlib import Path
from hailmary_client import HailmaryClient

root = Path(__file__).parent


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "paths",
        type=str,
        nargs="*",
    )

    parser.add_argument("-w", "--write_dir", type=str, default=Path.cwd())

    parser.add_argument(
        "-i",
        "--includes",
        type=str,
        nargs="*",
        default=[],
        help=""" List of glob patterns to use when including files to be transferred. """,
    )

    parser.add_argument(
        "-e",
        "--excludes",
        type=str,
        nargs="*",
        default=[],
        help=""" List of glob patterns to use when excluding files to be transferred. """,
    )

    parser.add_argument(
        "-s",
        "--serving_directory",
        action="store_true",
        help=""" Contact the server and return the serving directory. """,
    )

    args = parser.parse_args()
    args.write_dir = Path(args.write_dir)

    return args


def main(args: argparse.Namespace):
    client = HailmaryClient()
    if args.serving_directory:
        print(client.get_serving_directory())
    else:
        files = client.get_content(args.paths, args.includes, args.excludes)
        for file in files:
            path = args.write_dir / file
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(files[file])
            client.logger.info(f"Wrote file to '{path}'")


if __name__ == "__main__":
    main(get_args())
