from pathlib import Path
from garage_ai.ingest.pdf import PdfProcessor

processor = PdfProcessor(verbose=True)
processor.split_pages(
    pdf_path=Path("data/fsm/subaru/2002-2007 FSM/Forester_2002_USDM/ENGINE SECTION/Fuel Injection Fuel Systems/Fuel Delivery Return and Evaporation Lines.pdf"),
    output_path=Path("tmp/output")
)