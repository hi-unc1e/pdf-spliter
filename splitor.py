import os
import PyPDF2
from io import BytesIO


def split_pdf(input_file, output_dir, output_prefix, max_pages=250, max_size=9*1024*1024):
    output_dir = os.path.join(os.path.dirname(input_file), output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'rb') as infile:
        reader = PyPDF2.PdfReader(infile)
        total_pages = len(reader.pages) 
        part_num = 1
        current_page = 0

        while current_page < total_pages:
            writer = PyPDF2.PdfWriter()
            part_size = 0

            while current_page < total_pages and len(writer.pages) < max_pages and part_size < max_size:
                cp = reader.pages[current_page]
                writer.add_page(cp)
                print(f"Processing page {current_page + 1} of {total_pages}")  # 新增的打印语句
                current_page += 1
                
                # Calculate the size of the current part
                temp_buffer = BytesIO()
                writer.write(temp_buffer)
                part_size = temp_buffer.tell()

            output_file = os.path.join(output_dir, f"{output_prefix}_part{part_num}.pdf")
            with open(output_file, 'wb') as outfile:
                writer.write(outfile)

            print(f"Created part {part_num}: {output_file}")  # 新增的打印语句
            part_num += 1

    print("PDF splitting completed.")  # 新增的打印语句

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Split a PDF file into smaller parts.")
    parser.add_argument("input_file", help="Path to the input PDF file.")
    parser.add_argument("--output-dir", default="splited", help="Directory to save the output PDF files.")
    parser.add_argument("--output-prefix", default="s", help="Prefix for the output PDF files.")
    parser.add_argument("--max-pages", type=int, default=250, help="Maximum number of pages per output file.")
    parser.add_argument("--max-size", type=int, default=9*1024*1024, help="Maximum size (in bytes) per output file.")

    args = parser.parse_args()

    split_pdf(args.input_file, args.output_dir, args.output_prefix, args.max_pages, args.max_size)