from config.settings import UI_BASE_URL,UI_USERNAME,UI_PASSWORD
class LoginPage:
    #登入页面：把登入相关的元素封装到一起
    def __init__(self,page):
        self.page=page
        self.username=page.locator("#user-name")
        self.password=page.locator("#password")
        self.login_button=page.locator("#login-button")
        self.error=page.locator("[data-test='error']")

    def open(self):
        self.page.goto(UI_BASE_URL)

    def login(self,username=UI_USERNAME,password=UI_PASSWORD):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()
