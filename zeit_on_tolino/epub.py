import zipfile
from pathlib import Path
from typing import Dict

from lxml import etree


def get_epub_info(file_path: Path) -> Dict[str, str]:
    def xpath(element, path):
        return element.xpath(
            path,
            namespaces={
                "n": "urn:oasis:names:tc:opendocument:xmlns:container",
                "pkg": "http://www.idpf.org/2007/opf",
                "dc": "http://purl.org/dc/elements/1.1/",
            },
        )[0]

    # prepare to read from the .epub file
    zip_content = zipfile.ZipFile(file_path)

    # find the contents metafile
    cfname = xpath(
        etree.fromstring(zip_content.read("META-INF/container.xml")),
        "n:rootfiles/n:rootfile/@full-path",
    )

    # grab the metadata block from the contents metafile
    metadata = xpath(etree.fromstring(zip_content.read(cfname)), "/pkg:package/pkg:metadata")

    # repackage the data
    return {s: xpath(metadata, f"dc:{s}/text()") for s in ("title", "language", "creator", "date", "identifier")}
