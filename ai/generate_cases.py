import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import re
from ai.client import chat
PROMPT = """你是一个软件测试专家。请针对下面这个接口设计测试用例，
必须覆盖三类：正常场景、异常场景、边界场景。

要求：
1. 必须使用我提供的 base_url，不要自己编地址
2. 每条用例的输入参数必须真正符合用例名称（名称说 N 字符，参数就要真是 N 字符）
3. 状态码要符合语义：参数校验错误用 400，认证失败用 401，成功用 200
4. 函数名用英文小写+下划线（如 test_get_post_success）
5. 只返回合法 JSON/Python 代码，不要解释
6. 函数名必须使用英文小写 + 下划线，严禁中文，
  例如 test_get_post_success、test_post_not_found、test_boundary_id_zero

接口信息：
{api_info}

只返回 JSON，不要多余文字，格式：
{{
  "cases": [
    {{"name": "用例名称", "type": "正常/异常/边界", "params": {{}}, "expected": "预期结果"}}
  ]
}}
"""


def generate_cases(api_info):
    text = chat(PROMPT.format(api_info=api_info), json_mode=True)
    # 清洗：模型有时会用 ```json ``` 包裹，去掉再解析
    text = re.sub(r"```json|```", "", text).strip()
    return json.loads(text)


if __name__ == "__main__":
    api_info = """
    - base_url: https://jsonplaceholder.typicode.com
    - 路径: /posts/1
    - 方法: GET
    - 参数: 无
    - 成功: 返回 200 和文章对象（含 userId/id/title/body 字段）
    - 不存在: 返回 404
    """
    result = generate_cases(api_info)
    for case in result["cases"]:
        print(f"[{case['type']}] {case['name']}  →  预期: {case['expected']}")
