import concurrent.futures
from pathlib import Path
import os
from tqdm import tqdm
from garage_ai.walker import Walker
from garage_ai.pdf import PdfProcessor

class PageSplitter:

    def __init__(self, source_folder: Path, output_root: Path, num_threads: int = os.cpu_count(), verbose: bool = False):
        self.walker = Walker(source_folder, verbose=verbose)
        self.processor = PdfProcessor(output_root, verbose=verbose)
        self.num_threads = num_threads
        self.verbose = verbose

    def _process_pdf(self, pdf: Path):
        if self.walker.metadata(pdf)["processed"]:
            if self.verbose:
                print(f"Skipping {pdf}")
        else:
            if self.verbose:
                print(f"Processing {pdf}")
            try:
                self.processor.split_pages(pdf)
                self.walker.set_metadata(pdf, "processed", True)
            except Exception as e:
                print(f"Error processing {pdf}: {e}")

    def split(self):
        pdfs = self.walker.walk()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            executor.map(self._process_pdf, pdfs)

