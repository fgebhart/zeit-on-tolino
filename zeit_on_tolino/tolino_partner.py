from enum import Enum

from pydantic import BaseModel
from selenium.webdriver.common.by import By


class SeleniumItem(BaseModel):
    by: str
    value: str


class ShopDetails(BaseModel):
    user: SeleniumItem
    password: SeleniumItem
    login_button: SeleniumItem
    shop_image_keyword: str


thalia = ShopDetails(
    user=SeleniumItem(by=By.ID, value="j_username"),
    password=SeleniumItem(by=By.ID, value="j_password"),
    login_button=SeleniumItem(by=By.CLASS_NAME, value="btn-primary.btn-lg"),
    shop_image_keyword="thalia",
)

hugendubel = ShopDetails(
    user=SeleniumItem(by=By.NAME, value="email"),
    password=SeleniumItem(by=By.NAME, value="password"),
    login_button=SeleniumItem(by=By.CLASS_NAME, value="btn-primary.btn-lg"),
    shop_image_keyword="hugendubel",
)

buecher_de = ShopDetails(
    user=SeleniumItem(by=By.ID, value="form_login"),
    password=SeleniumItem(by=By.ID, value="form_password"),
    login_button=SeleniumItem(by=By.CLASS_NAME, value="btn-primary.pull-right"),
    shop_image_keyword="bucher",
)


class PartnerDetails(Enum):
    thalia: ShopDetails = thalia
    hugendubel: ShopDetails = hugendubel
    buecher_de: ShopDetails = buecher_de
