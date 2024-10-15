import json
from common.handle_path import excel_Path
import pytest
from requests import request
from common.base_test import read_excel, send_request
from common.base_test import assert_res

# 读取Excel中的测试用例数据
casedatas = read_excel(excel_Path, '搜索')

# 从casedatas中逐条执行用例
@pytest.mark.parametrize('case',casedatas)
def test_search(case):
    res = send_request(case)
    assert_res(case,res)
