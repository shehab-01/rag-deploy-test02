import os
import json
from pathlib import Path


def test_1():
    json_data = None
    json_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_ds.json")
    with open(json_path, "rt", encoding="UTF-8") as f:
        json_data = json.load(f)
        # json_text = json.dumps(json_data, indent=4, ensure_ascii=False)
        # print(json_text)

    return None


# 결과
result = test_1()
if result:
    print(result)
