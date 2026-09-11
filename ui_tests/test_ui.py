from playwright.sync_api import expect
from config.settings import UI_BASE_URL
from ui_tests.pages.login_page import LoginPage
from ui_tests.pages.inventory_page import InventoryPage


def test_login_success(page):
    login = LoginPage(page)
    login.open()
    login.login()
    expect(page).to_have_url(UI_BASE_URL + "inventory.html")
    expect(page.locator(".inventory_item")).to_have_count(6)


def test_login_wrong_password(page):
    login = LoginPage(page)
    login.open()
    login.login(password="wrong_password")
    expect(login.error).to_be_visible()
    expect(page).to_have_url(UI_BASE_URL)


def test_login_locked_out_user(page):
    login = LoginPage(page)
    login.open()
    login.login(username="locked_out_user")
    expect(login.error).to_contain_text("Sorry, this user has been locked out")


def test_add_to_cart(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    inventory.add_to_cart("sauce-labs-fleece-jacket")
    expect(inventory.cart_badge).to_have_text("1")


def test_remove_from_cart(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    inventory.add_to_cart("sauce-labs-fleece-jacket")
    expect(inventory.cart_badge).to_have_text("1")
    inventory.remove_from_cart("sauce-labs-fleece-jacket")
    expect(inventory.cart_badge).to_have_count(0)


def test_add_multiple_items(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    inventory.add_to_cart("sauce-labs-backpack")
    inventory.add_to_cart("sauce-labs-fleece-jacket")
    expect(inventory.cart_badge).to_have_text("2")


def test_complete_checkout_flow(logged_in_page):
    page = logged_in_page
    inventory = InventoryPage(page)
    inventory.add_to_cart("sauce-labs-backpack")
    page.click("[data-test='shopping-cart-badge']")
    page.click("[data-test='checkout']")
    page.fill("[data-test='firstName']", "John")
    page.fill("[data-test='lastName']", "Doe")
    page.fill("[data-test='postalCode']", "12345")
    page.click("[data-test='continue']")
    page.click("[data-test='finish']")
    expect(page.locator("[data-test='complete-header']")).to_have_text("Thank you for your order!")


def test_sort_by_price(logged_in_page):
    inventory = InventoryPage(logged_in_page)
    inventory.sort_by("lohi")
    prices = inventory.item_prices()
    assert prices[0] <= prices[-1]


def test_logout(logged_in_page):
    page = logged_in_page
    page.click("#react-burger-menu-btn")
    page.click("#logout_sidebar_link")
    expect(page).to_have_url(UI_BASE_URL)
