from common.base_test import read_excel, send_request, assert_res,dic_evn
from common.handle_path import excel_Path,log_path
import pytest
from common.handle_encrypt import md5_str

casedatas = read_excel(excel_Path,'erp项目测试')
# 最开始进行密码加密，并且保存到公共的数据容器
dic_evn['encypt_password'] = md5_str('123456')

# 从casedatas中逐条执行用例
@pytest.mark.parametrize('case',casedatas)
def test_login_erp(case):
    res = send_request(case)
    assert_res(case,res)
