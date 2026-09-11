import pytest
import os
import sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from ui_tests.pages.login_page import LoginPage

@pytest.fixture
def logged_in_page(page):
    login=LoginPage(page)
    login.open()
    login.login()
    return page