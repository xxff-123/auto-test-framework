# 自动化测试框架（接口 + UI）

## 项目简介

基于 Python 搭建的自动化测试框架，同时覆盖接口测试和 Web UI 测试：

- 接口层：Requests + Pytest，测试 JSONPlaceholder 公开 API
- UI 层：Playwright + Pytest，测试 SauceDemo 电商站

框架采用 POM（页面对象模式）与配置分离，实现「测试逻辑」与「页面操作」解耦——页面改版时只需修改页面对象，不用动测试用例。

## 技术栈

| 技术       | 用途           |
| ---------- | -------------- |
| Python 3   | 开发语言       |
| Pytest     | 用例管理与执行 |
| Requests   | 接口请求       |
| Playwright | 浏览器自动化   |
| POM        | 页面对象模式   |

## 项目结构

    auto-test-framework/
    ├── config/                 配置目录
    │   └── settings.py         集中管理 URL、账号
    ├── api_tests/              接口测试
    │   └── test_posts.py       接口用例
    ├── ui_tests/               UI 测试
    │   ├── pages/              页面对象（POM）
    │   │   ├── login_page.py
    │   │   └── inventory_page.py
    │   └── test_ui.py          UI 用例
    ├── conftest.py             公共 fixture（登录复用）
    ├── pytest.ini              pytest 配置
    ├── requirements.txt        依赖清单
    └── README.md

## 用例覆盖

### 接口测试（7 条）

| 用例           | 说明                                 |
| -------------- | ------------------------------------ |
| 查询文章列表   | GET /posts，验证返回 100 条          |
| 查询单篇文章   | GET /posts/1，验证字段完整           |
| 查询不存在资源 | GET /posts/999，验证返回 404         |
| 创建文章       | POST /posts，验证返回 201            |
| 删除文章       | DELETE /posts/1，验证返回 200/204    |
| 参数过滤校验   | GET /comments?postId=1，验证数据归属 |
| 响应耗时校验   | 验证响应时间小于 2 秒                |

### UI 测试（9 条）

| 用例         | 说明                        |
| ------------ | --------------------------- |
| 登录成功     | 正常账号登录，跳转商品页    |
| 登录失败     | 错误密码，提示错误信息      |
| 锁定用户登录 | 锁定账号，提示已被锁定      |
| 加入购物车   | 加购商品，角标显示 1        |
| 移除商品     | 加购后移除，角标消失        |
| 加入多个商品 | 加购两件，角标显示 2        |
| 完整下单流程 | 加购→结算→填写信息→完成下单 |
| 价格排序     | 按价格从低到高排序并校验    |
| 退出登录     | 退出后回到登录页            |

## 框架亮点

1. **POM 分层**：页面元素和操作封装成类，页面改版只改一处
2. **配置分离**：URL、账号集中在 config/settings.py，不写死在用例里
3. **公共 fixture**：登录动作抽到 conftest.py，用例通过 logged_in_page 直接获得登录态，消除重复代码
4. **异常场景覆盖**：不只测正常流程，还覆盖 404、错误密码、锁定用户等异常情况

## 如何运行

    pip install -r requirements.txt
    playwright install chromium
    pytest -v

