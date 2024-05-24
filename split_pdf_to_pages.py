import argparse
from pathlib import Path
from garage_ai.page_splitter import PageSplitter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recursively split PDFs into individual pages.")
    parser.add_argument("pdf_folder", type=Path, help="Path to the root folder containing PDFs.")
    parser.add_argument("output_folder", type=Path, help="Path to the output folder.")
    args = parser.parse_args()

    # Use the provided paths
    pdf_folder = args.pdf_folder
    output_folder = args.output_folder

    splitter = PageSplitter(pdf_folder, output_folder, verbose=True)
    splitter.split()