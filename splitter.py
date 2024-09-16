#!/usr/bin/env /Users/dpdu/.pyenv/versions/3.8.18/bin/python3
import os
import pymupdf  # PyMuPDF
import multiprocessing
import tempfile

def process_part(args):
    input_file, output_dir, output_prefix, start_page, end_page, part_num, max_size = args
    doc = pymupdf.open(input_file)
    writer = pymupdf.open()
    current_size = 0
    part_count = 1

    for page_num in range(start_page, min(end_page, len(doc))):
        writer.insert_pdf(doc, from_page=page_num, to_page=page_num)
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', dir=output_dir, delete=True) as tmp_file:
            writer.save(tmp_file.name)
            current_size = os.path.getsize(tmp_file.name)
        
        if current_size > max_size:
            # Save the current part and start a new one
            output_file = os.path.join(output_dir, f"{output_prefix}_part{part_num}_{part_count}.pdf")
            writer.save(output_file)
            print(f"Created part {part_num}_{part_count}: {output_file}")
            
            # Reset for next part
            writer = pymupdf.open()
            current_size = 0
            part_count += 1

    # Save any remaining pages
    if writer.page_count > 0:
        output_file = os.path.join(output_dir, f"{output_prefix}_part{part_num}_{part_count}.pdf")
        writer.save(output_file)
        print(f"Created part {part_num}_{part_count}: {output_file}")

    writer.close()


def split_pdf(input_file, output_dir, output_prefix, max_pages=290, max_size=9*1024*1024):
    output_dir = os.path.join(os.path.dirname(input_file), output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    doc = pymupdf.open(input_file)
    total_pages = len(doc)

    num_parts = (total_pages + max_pages - 1) // max_pages
    pool = multiprocessing.Pool()
    # for i in range(num_parts):
    #     args = (input_file, output_dir, output_prefix, i * max_pages, (i + 1) * max_pages, i + 1, max_size)
    #     process_part(args)

    args_list = [
        (input_file, output_dir, output_prefix, i * max_pages, (i + 1) * max_pages, i + 1, max_size)
        for i in range(num_parts)
    ]
    pool.map(process_part, args_list)
    pool.close()
    pool.join()

    print("PDF splitting completed.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Split a PDF file into smaller parts.")
    parser.add_argument("input_file", help="Path to the input PDF file.")
    parser.add_argument("--output-dir", default="splited", help="Directory to save the output PDF files.")
    parser.add_argument("--output-prefix", default="s", help="Prefix for the output PDF files.")
    parser.add_argument("--max-pages", type=int, default=280, help="Maximum number of pages per output file.")
    parser.add_argument("--max-size", type=int, default=9*1024*1024, help="Maximum size (in bytes) per output file.")

    args = parser.parse_args()

    split_pdf(args.input_file, args.output_dir, args.output_prefix, args.max_pages, args.max_size)