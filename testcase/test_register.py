from common.handle_path import excel_Path
import pytest
from common.base_test import read_excel, send_request,assert_db
from common.base_test import assert_res,dic_evn
from common.base_test import extract_res
from common.handle_data import query_db,get_unregister_phone,get_unregister_username

# 读取Excel中的测试用例数据
casedatas = read_excel(excel_Path, '注册流程')
phone = get_unregister_phone()
dic_evn['mobile_phone'] = phone
dic_evn['user_name'] = get_unregister_username()

# 从casedatas中逐条执行用例
@pytest.mark.parametrize('case',casedatas)
def test_order(case):
    res = send_request(case)
    extract_res(case,res)
    assert_res(case,res)
    assert_db(case)
    # 要求：在第一条接口请求结束之后查询数据库
    if case['编号'] == 1:
        sql = f"select mobile_code from tz_sms_log where user_phone='{phone}' order by rec_date desc limit 1"
        code = query_db(sql,'one')[0]
        dic_evn['code'] = code
