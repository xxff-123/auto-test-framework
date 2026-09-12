import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.client import chat

PROMPT = """你是一个软件测试专家。下面是失败的 pytest 测试输出。
请用简洁的中文回答两点：
1. 失败的根本原因
2. 具体的修复建议

测试输出：
{output}
"""


def analyze_failure(output):
    return chat(PROMPT.format(output=output))


def run_and_analyze(test_file):
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_file, "-v", "--tb=short"],
        capture_output=True, text=True,
        encoding="utf-8", errors="replace",
        env=env,
    )
    output = result.stdout + result.stderr

    if result.returncode != 0:
        print("测试有失败，AI 正在分析...\n")
        print(analyze_failure(output))
    else:
        print("全部通过，无需分析")


if __name__ == "__main__":
    run_and_analyze("api_tests")
