import pymupdf
import sys

def extract_pages_from_pdf(master_document, page_num_start, page_num_end):
    # Create a new PDF document and insert the specified pages from the master document
    new_pdf = pymupdf.open()
    new_pdf.insert_pdf(master_document, from_page=page_num_start, to_page=page_num_end)
    return new_pdf

def process_master_pdf(master_pdf_path):
    """Process the master PDF file and extract individual invoices as separate PDF files."""
    # Open the master PDF invoice file
    master_document = pymupdf.open(master_pdf_path)

    seen_invoice_nums = set()
    from_page_index = 0
    to_page_index = 0

    for curr_page_index in range(len(master_document)):
        # Get the invoice number for the current page and the next page
        curr_page_invoice_num = get_invoice_num_from_page(master_document[curr_page_index])
        next_page_invoice_num = get_invoice_num_from_page(master_document[curr_page_index + 1]) if curr_page_index + 1 < len(master_document) else None

        # If the current page's invoice number is equal to the next page's index number, continue to the next page
        if curr_page_invoice_num == next_page_invoice_num:
            print(f"Page {curr_page_index} has the same invoice number as the next page. Continuing to next page.")
            if curr_page_invoice_num in seen_invoice_nums:
                # If the invoice number has already been seen, only increment to_page_index
                to_page_index += 1
            else:
                from_page_index = curr_page_index
                to_page_index = curr_page_index + 1
                seen_invoice_nums.add(curr_page_invoice_num)
        else:
            # Save page/s as new PDF file and reset from_page and to_page indices
            new_pdf = extract_pages_from_pdf(master_document, from_page_index, to_page_index)
            new_pdf.save(f'{curr_page_invoice_num}.pdf')
            new_pdf.close()
            
            # Reset the from_page_index and to_page_index for the next invoice
            from_page_index = curr_page_index + 1
            to_page_index = curr_page_index + 1

    master_document.close()


def get_invoice_num_from_page(page):
    # Get all of the text of the current page as a list of strings
    curr_page_text_as_list = page.get_text().split("\n")
    
    # Extract the invoice number from the text
    invoice_number = curr_page_text_as_list[curr_page_text_as_list.index("Invoice #") + 1]
    
    return invoice_number

def main():
    args = sys.argv[1:] 

    if len(args) > 0:
        # Check if the first argument is a valid PDF file
        master_pdf_path = args[0]
        try:
            # Attempt to open the PDF file to check if it exists and is valid
            with pymupdf.open(master_pdf_path) as _:
                pass
            process_master_pdf(master_pdf_path)
        except Exception as e:
            print(f"Error: {e}")
            print("Please provide a valid PDF file.")
    else:
        print("No arguments provided.")

if __name__ == "__main__":
    main()



"""
TO DO:
# It should be able to handle invoices that contain multiple pages. (Consider 2 pointer approach + "seen set")
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
"""