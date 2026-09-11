class InventoryPage:
    #商品列表页：封装加购，移除，下单
    def __init__(self,page):
        self.page=page
        self.cart_badge=page.locator("[data-test='shopping-cart-badge']")
        self.sort_dropdown=page.locator(".product_sort_container")
    def add_to_cart(self,item):
        self.page.locator(f"#add-to-cart-{item}").click()

    def remove_from_cart(self,item):
        self.page.locator(f"#remove-{item}").click()

    def sort_by(self,value):
        self.sort_dropdown.select_option(value)

    def item_prices(self):
        text=self.page.locator(".inventory_item_price").all_text_contents()
        return [float(t.replace("$","")) for t in text]