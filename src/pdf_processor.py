import pymupdf
import os
import ctypes

def extract_pages_from_pdf(input_pdf: pymupdf.Document, page_num_start: int, page_num_end: int) -> pymupdf.Document:
    """
    Extract the specified pages from the input PDF and return a new PDF document. page_num_end inclusive.
    """
    new_pdf = pymupdf.open()
    new_pdf.insert_pdf(input_pdf, from_page=page_num_start, to_page=page_num_end)
    return new_pdf

def save_pdf_file(pdf: pymupdf.Document, file_name: str) -> None:
    output_dir = os.getenv("OUTPUT_DIR")
    pdf.save(f'{output_dir}/{file_name}.pdf')
    pdf.close()
    return None

def process_input_pdf():
    """Process the master PDF file and extract individual invoices as separate PDF files."""
    # Open the master PDF invoice file
    input_pdf_path = os.getenv("INPUT_PATH")
    input_invoices_pdf = pymupdf.open(input_pdf_path)

    seen_invoice_nums = set()

    # Extraction range variables
    # These variables will be used to track the start and end of the page range for each invoice
    from_page_index = 0
    to_page_index = 0

    for curr_page_index in range(len(input_invoices_pdf)):
        # Get the invoice number for the current page and the next page
        curr_page_invoice_num = get_invoice_num_from_page(input_invoices_pdf[curr_page_index])
        next_page_invoice_num = get_invoice_num_from_page(input_invoices_pdf[curr_page_index + 1]) if curr_page_index + 1 < len(input_invoices_pdf) else None

        # If the current page's and next page's invoice numbers are equal, set up or update the range of pages to extract
        if curr_page_invoice_num == next_page_invoice_num:
            if curr_page_invoice_num in seen_invoice_nums:
                # If the invoice number has already been seen, only increment to_page_index
                to_page_index += 1
            else:
                from_page_index = curr_page_index
                to_page_index = curr_page_index + 1
                seen_invoice_nums.add(curr_page_invoice_num)
        else:
            # Save page/s as new PDF file and reset from_page and to_page indices
            new_pdf = extract_pages_from_pdf(input_invoices_pdf, from_page_index, to_page_index)
            save_pdf_file(new_pdf, curr_page_invoice_num)

            
            # Reset the extraction range variables for the next invoice
            from_page_index = curr_page_index + 1
            to_page_index = curr_page_index + 1

    input_invoices_pdf.close()


def get_invoice_num_from_page(page):
    # Get all of the text of the current page as a list of strings
    curr_page_text_as_list = page.get_text().split("\n")
    
    # Extract the invoice number from the text
    invoice_number = curr_page_text_as_list[curr_page_text_as_list.index("Invoice #") + 1]
    
    return invoice_number

def main():
    process_input_pdf()
    ctypes.windll.user32.MessageBoxW(0, f'Processed invoices saved to directory: {os.getenv("OUTPUT_DIR")}', "Processing Complete", 64)


if __name__ == "__main__":
    main()



"""
TO DO:
# It should be able to give an option of where to save the new PDF files.
# Determine that an executable can be created from this script using PyInstaller or similar tools.


ERRORS:
It should be able to handle cases where the master PDF file is empty or does not exist.
It should be able to handle cases where the invoice number is not found on the page.

EDGE CASES:
Master invoices document is empty or does not exist.
Master Invoice document is not a valid PDF file.
Invoice number is not found or cannot be extracted from the page.
Master invoice document is 1 page long.


DONE:
# It should be able to handle invoices that contain multiple pages. (Consider 2 pointer approach + "seen set")
"""