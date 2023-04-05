import logging

from zeit_on_tolino import env_vars, epub, tolino, web, zeit

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


if __name__ == "__main__":
    env_vars.verify_env_vars_are_set()
    env_vars.verify_configured_partner_shop_is_supported()

    log.info("logging into ZEIT premium...")
    webdriver = web.get_webdriver()

    # download ZEIT
    log.info("downloading most recent ZEIT e-paper...")
    e_paper_path = zeit.download_e_paper(webdriver)
    e_paper_title = epub.get_epub_info(e_paper_path)["title"]
    assert e_paper_path.is_file()
    log.info(f"successfully finished download of '{e_paper_title}'")

    # upload to tolino cloud
    log.info("upload ZEIT e-paper to tolino cloud...")
    tolino.login_and_upload(webdriver, e_paper_path, e_paper_title)

    webdriver.quit()
    log.info("done.")
