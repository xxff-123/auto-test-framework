import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import re
from ai.client import chat
from ai.generate_cases import generate_cases

SCRIPT_PROMPT = """你是一个 Python 自动化测试工程师。根据下面的接口信息和测试用例，
生成一份可以直接运行的 pytest 测试代码。

要求：
- 使用 requests 库发送请求
- 每条用例写成一个 test_ 开头的函数
- 用 assert 做断言
- 文件顶部 import requests
- 只返回 Python 代码，不要 markdown 标记，不要任何解释
- 函数名必须使用英文小写 + 下划线，严禁中文，
  例如 test_get_post_success、test_post_not_found、test_boundary_id_zero
  
接口信息：
{api_info}

测试用例：
{cases}
"""


def generate_script(api_info, cases):
    prompt = SCRIPT_PROMPT.format(
        api_info=api_info,
        cases=json.dumps(cases, ensure_ascii=False, indent=2),
    )
    code = chat(prompt)
    # 清洗掉可能出现的 markdown 标记
    code = re.sub(r"```python|```", "", code).strip()
    return code


if __name__ == "__main__":
    api_info = """
    - base_url: https://jsonplaceholder.typicode.com
    - 路径: /posts/1
    - 方法: GET
    - 参数: 无
    - 成功: 返回 200 和文章对象（含 userId/id/title/body 字段）
    - 不存在: 返回 404
    """
    cases = generate_cases(api_info)["cases"]
    code = generate_script(api_info, cases)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"api_tests/test_ai_generated_{timestamp}.py"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"已生成 {filename}")