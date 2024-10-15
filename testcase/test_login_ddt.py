import json
import pytest
from requests import request
from common.handle_path import excel_Path
from common.base_test import read_excel, send_request
# 读取Excel中的测试用例数据
from common.base_test import assert_res

casedatas = read_excel(excel_Path, '登录')

# 从casedatas中逐条执行用例
@pytest.mark.parametrize('case',casedatas)
def test_login(case):
    res = send_request(case)
    assert_res(case,res)

