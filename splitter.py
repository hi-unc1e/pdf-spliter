#!/usr/bin/env /Users/dpdu/.pyenv/versions/3.8.18/bin/python3
import os
import pymupdf  # PyMuPDF
import multiprocessing

def process_part(args):
    input_file, output_dir, output_prefix, start_page, end_page, part_num = args
    doc = pymupdf.open(input_file)
    writer = pymupdf.open()

    for page_num in range(start_page, min(end_page, len(doc))):
        writer.insert_pdf(doc, from_page=page_num, to_page=page_num)
        print(f"Processing page {page_num + 1} of {len(doc)}")

    output_file = os.path.join(output_dir, f"{output_prefix}_part{part_num}.pdf")
    writer.save(output_file)
    writer.close()

    print(f"Created part {part_num}: {output_file}")

def split_pdf(input_file, output_dir, output_prefix, max_pages=250, max_size=9*1024*1024):
    output_dir = os.path.join(os.path.dirname(input_file), output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    doc = pymupdf.open(input_file)
    total_pages = len(doc)

    num_parts = (total_pages + max_pages - 1) // max_pages
    pool = multiprocessing.Pool()

    args_list = [
        (input_file, output_dir, output_prefix, i * max_pages, (i + 1) * max_pages, i + 1)
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
    parser.add_argument("--max-pages", type=int, default=250, help="Maximum number of pages per output file.")
    parser.add_argument("--max-size", type=int, default=9*1024*1024, help="Maximum size (in bytes) per output file.")

    args = parser.parse_args()

    split_pdf(args.input_file, args.output_dir, args.output_prefix, args.max_pages, args.max_size)