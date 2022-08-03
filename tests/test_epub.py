from zeit_on_tolino import epub


def test_get_epub_info(test_epub_path, test_epub_title) -> None:
    info = epub.get_epub_info(test_epub_path)
    assert info["title"] == test_epub_title
