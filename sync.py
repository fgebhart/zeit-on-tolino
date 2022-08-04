import logging
from pathlib import Path

from zeit_on_tolino import epub, tolino, web, zeit

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


if __name__ == "__main__":
    log.info("logging into ZEIT premium...")
    webdriver = web.get_webdriver()

    # download ZEIT
    log.info("downloading most recent ZEIT e-paper...")
    e_paper_name = zeit.download_e_paper(webdriver)
    e_paper_path = Path(web.DOWNLOAD_PATH) / e_paper_name
    e_paper_title = epub.get_epub_info(e_paper_path)["title"]
    assert e_paper_path.is_file()
    log.info(f"successfully finished download of '{e_paper_title}'")

    # upload to tolino cloud
    log.info("upload ZEIT e-paper to tolino cloud...")
    tolino.upload_e_paper(webdriver, file_path=e_paper_path)
    log.info("successfully uploaded ZEIT e-paper to tolino cloud.")

    webdriver.quit()
    log.info("done.")
