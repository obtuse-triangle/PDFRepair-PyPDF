from pypdf import PdfWriter
from tqdm import tqdm
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", help="The filename of the PDF to repair. if not specified, all PDF files in the current directory will be repaired.")
parser.add_argument("-c", "--compress", help="Compress the PDF.", action="store_true")


def filename_with_repaired_suffix(filename):
    return filename.replace(".pdf", "_repaired.pdf")

def compressPDF(writer):
  for page in tqdm(writer.pages):
      page.compress_content_streams()
  writer.compress_identical_objects(remove_identicals=True, remove_orphans=True)

def pdfLoad(filename):
    if "_repaired" in filename:
        print("File has already been repaired.")
        return None
    return PdfWriter(clone_from=filename)

def pdfSave(writer, filename):
  with open(filename_with_repaired_suffix(filename), "wb") as file:
      writer.write(file)
  print(f"✅ Repaired file saved as: {filename_with_repaired_suffix(filename)}")

def pdfRepair(filename, compress=False):
  print(f"\033[44mRepairing file: {filename}\033[0m")
  writer = pdfLoad(filename)
  if writer is None:
    return
  if compress:
    compressPDF(writer)
  pdfSave(writer, filename)

if __name__ == "__main__":
  args = parser.parse_args()


  if args.filename:
    if not args.filename.endswith(".pdf"):
      print("\033[41mERROR: File must be a PDF file.\033[0m")
      exit()
    pdfRepair(args.filename, compress=args.compress)
  else:
    print("\033[42mNo file specified. Searching for PDF files in current directory.\033[0m")
    t = False
    for file in os.listdir("."):
      if file.endswith(".pdf"):
        if not t:
          t = True
        pdfRepair(file, compress=args.compress)
    if not t:
      print("\033[43mWARNING: No PDF files found in current directory.\033[0m")
  print("\033[36mDone.\033[0m")

