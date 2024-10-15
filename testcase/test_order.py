from common.handle_path import excel_Path
import pytest
from common.base_test import read_excel, send_request
from common.base_test import assert_res,dic_evn
from common.base_test import extract_res,assert_db

# 读取Excel中的测试用例数据
casedatas = read_excel(excel_Path, '下单支付流程')

# 从casedatas中逐条执行用例
@pytest.mark.parametrize('case',casedatas)
def test_order(case):
    res = send_request(case)
    print(f'接口关联的数据容器：{dic_evn}')
    assert_res(case,res)
    extract_res(case, res)
    assert_db(case)
