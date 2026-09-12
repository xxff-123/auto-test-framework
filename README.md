# AI 驱动的自动化测试框架（接口 + UI）

## 项目简介

基于 Python 搭建的自动化测试框架，覆盖接口测试和 Web UI 测试，并接入大模型实现**测试用例生成、脚本转换、失败归因**：

- **接口层**：Requests + Pytest，测试 JSONPlaceholder 公开 API
- **UI 层**：Playwright + Pytest，测试 SauceDemo 电商站
- **AI 层**：接入大模型，实现测试用例自动生成、脚本自动转换、失败自动归因

框架采用 POM（页面对象模式）与配置分离，实现「测试逻辑」与「页面操作」解耦；AI 模块独立封装模型调用，切换模型只需改一个文件。

## 技术栈

| 技术       | 用途                              |
| ---------- | --------------------------------- |
| Python 3   | 开发语言                          |
| Pytest     | 用例管理与执行                    |
| Requests   | 接口请求                          |
| Playwright | 浏览器自动化                      |
| POM        | 页面对象模式                      |
| 大模型 API | 用例生成 / 脚本转换 / 失败归因    |

## 项目结构

    auto-test-framework/
    ├── config/
    │   └── settings.py         集中管理 URL、账号
    ├── api_tests/              接口测试
    │   └── test_posts.py       接口用例
    ├── ui_tests/               UI 测试
    │   ├── pages/              页面对象（POM）
    │   │   ├── login_page.py
    │   │   └── inventory_page.py
    │   └── test_ui.py          UI 用例
    ├── ai/                     AI 能力
    │   ├── client.py           封装大模型调用
    │   ├── generate_cases.py   根据接口信息生成测试用例
    │   ├── generate_script.py  把用例转成 pytest 脚本
    │   └── analyze_failure.py  测试失败时自动分析原因
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

## AI 能力（核心亮点）

| 能力        | 说明                                                             |
| ----------- | ---------------------------------------------------------------- |
| AI 生成用例 | 输入接口信息，大模型自动生成覆盖正常 / 异常 / 边界的测试用例     |
| AI 转脚本   | 把生成的用例自动转成可运行的 pytest 代码                         |
| AI 失败归因 | 测试失败时，自动把报错交给大模型分析根本原因并给出修复建议       |

**完整闭环**：丢接口信息 → AI 生成用例 → AI 转脚本 → 跑测试 → 失败了 AI 分析原因。

> 实践中发现 AI 产出需要人工校对（例如可能编造接口地址、混淆 400/401 状态码语义），因此在实际使用中对 prompt 加入了约束，并保留人工 review 环节——「会用 AI，但不盲信 AI」。

## 框架亮点

1. **POM 分层**：页面元素和操作封装成类，页面改版只改一处
2. **配置分离**：URL、账号集中在 config/settings.py，不写死在用例里
3. **公共 fixture**：登录动作抽到 conftest.py，用例通过 logged_in_page 直接获得登录态，消除重复代码
4. **异常场景覆盖**：不只测正常流程，还覆盖 404、错误密码、锁定用户等异常情况
5. **AI 增强**：接入大模型实现用例生成、脚本转换、失败归因；模型调用独立封装，便于切换

## 如何运行

    pip install -r requirements.txt
    playwright install chromium
    pytest -v

### 使用 AI 能力

在项目根目录创建 `.env` 文件（该文件已被 .gitignore 忽略，不会上传）：

    AI_API_KEY=你的大模型APIKey

然后：

    python ai/generate_cases.py     # 生成测试用例
    python ai/generate_script.py    # 生成 pytest 脚本
    python ai/analyze_failure.py    # 跑测试并自动分析失败原因
