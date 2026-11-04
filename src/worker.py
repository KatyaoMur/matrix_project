"""Расчётный процесс для обработки файлового задания."""

import argparse

from src.matrix_sin import process_request


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("request_path")
    parser.add_argument("result_path")
    args = parser.parse_args()
    process_request(args.request_path, args.result_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
