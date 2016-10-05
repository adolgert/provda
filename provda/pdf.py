import collections
import os
import tempfile
from PyPDF2 import PdfFileWriter, PdfFileReader


logger = logging.getLogger("provda.pdf")


def add_keys(pdf_file, kv):
    """
    Add a dictionary of key-value pairs to a pdf file.
    Adds metadata to PDF files so you can know how they were generated.

    :param pdf_file: Either an iterable of files or a filename.
    :param kv: A readable mapping (dict).
    """
    try:
        pdf_file = iter(pdf_file)
    except TypeError:
        pdf_file = [pdf_file]
    assert isinstance(keydict, collections.Mapping)

    for orig in pdf_file:
        logger.debug("Adding keys to {}".format(orig))
        out_file = tempfile.NamedTemporaryFile(mode="wb", delete=False)
        pdfDict = {u"/{0}".format(k): v for (k, v) in kv.items()}
        in_file = PdfFileReader(orig)
        out_obj = PdfFileWriter()
        out_obj.addMetadata(pdfDict)
        for page in range(in_file.getNumPages()):
            out_obj.addPage(in_file.getPage(page))
        out_obj.write(out_file)
        out_file.close()
        shutil.copy(out_file.name, orig)
        os.remove(out_file)
