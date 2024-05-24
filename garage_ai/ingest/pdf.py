import fitz  # PyMuPDF
from pathlib import Path

class PdfProcessor:

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def split_pages(self, pdf_path: Path, output_path: Path):
        output_path.mkdir(parents=True, exist_ok=True)
        pdf_path = Path(pdf_path)
        if self.verbose:
            print(f'Splitting pages {pdf_path} to {output_path}')

        try:
            document = fitz.open(pdf_path)
            total_pages = document.page_count

            for page_number in range(total_pages):
                try:
                    if self.verbose:
                        print(f'Processing page {page_number + 1}/{total_pages}')

                    page = document.load_page(page_number)
                    writer = fitz.open()  # Create a new PDF
                    writer.insert_pdf(document, from_page=page_number, to_page=page_number)

                    file_name = f"{page_number + 1}.pdf"
                    output = output_path / pdf_path.parent / pdf_path.name
                    output.mkdir(parents=True, exist_ok=True)

                    if self.verbose:
                        print(f'Writing page to {output}')

                    output_file = output / file_name
                    writer.save(output_file)
                except Exception as e:
                    print(f"Error processing page {page_number + 1} of {pdf_path}: {e}")

        except Exception as e:
            print(f"Error reading {pdf_path}: {e}")

    def extract_text(self, pdf_path: Path) -> str:
        pdf_path = Path(pdf_path)
        if self.verbose:
            print(f'Extracting text from {pdf_path}')

        try:
            document = fitz.open(pdf_path)
            text = ""
            for page_number in range(document.page_count):
                page = document.load_page(page_number)
                text += page.get_text()

            return text
        except Exception as e:
            print(f"Error reading {pdf_path}: {e}")
            return ""