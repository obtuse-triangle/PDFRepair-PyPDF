from pypdf import PdfWriter
from tqdm import tqdm
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("FILEPATH", help="The PDF file or directory to repair.")
parser.add_argument("--compress", "-c",
                    help="Compress the PDF.", action="store_true")


def filename_with_repaired_suffix(filename):
  return filename.replace(".pdf", "_repaired.pdf")


def pdfLoad(filename):
  if "_repaired" in filename:
    print("File has already been repaired.")
    return None
  return PdfWriter(clone_from=filename)


def pdfSave(writer, filename):
  with open(filename_with_repaired_suffix(filename), "wb") as file:
    writer.write(file)
  print(f"✅ Repaired file saved as: {filename_with_repaired_suffix(filename)}")


def compressPDF(writer):
  for page in tqdm(writer.pages):
    page.compress_content_streams()
  writer.compress_identical_objects(
    remove_identicals=True, remove_orphans=True)


def pdfRepair(filename, compress=False):
  print(f"\033[44mRepairing file: {filename}\033[0m")
  writer = pdfLoad(filename)
  if writer is None:
    return
  if compress:
    compressPDF(writer)
  pdfSave(writer, filename)


def main():
  args = parser.parse_args()
  if args.FILEPATH:
    if not os.path.exists(args.FILEPATH):
      print("\033[41mERROR: File does not exist.\033[0m")
    elif os.path.isdir(args.FILEPATH):
      t = False
      for file in os.listdir(args.FILEPATH):
        if file.endswith(".pdf"):
          t = True
          pdfRepair(file, compress=args.compress)
      if not t:
        print("\033[41mERROR: No PDF files found in directory.\033[0m")
    elif not args.FILEPATH.endswith(".pdf"):
      print("\033[41mERROR: File must be a PDF file.\033[0m")
    else:
      pdfRepair(args.FILEPATH, compress=args.compress)
  else:
    print("\033[41mNo file specified.\033[0m")


if __name__ == "__main__":
  main()
