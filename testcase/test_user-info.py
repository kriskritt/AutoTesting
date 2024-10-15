from common.handle_path import excel_Path
import pytest
from common.base_test import read_excel, send_request
from common.base_test import assert_res, dic_evn
from common.base_test import extract_res

# 读取Excel中的测试用例数据
casedatas = read_excel(excel_Path, '修改用户头像流程')

# 从casedatas中逐条执行用例
@pytest.mark.parametrize('case',casedatas)
def test_modify_user(case):
    res = send_request(case)
    extract_res(case,res)
    print(f'接口关联的数据容器：{dic_evn}')
    assert_res(case,res)
