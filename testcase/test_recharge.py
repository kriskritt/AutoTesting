import time
from common.base_test import read_excel,send_request,assert_res,extract_res,dic_evn
from common.handle_encrypt import res_str
from common.handle_path import excel_Path
import pytest

casedata = read_excel(excel_Path,'充值项目测试')

# 获取时间戳
timestamp = int(time.time())
dic_evn['timestamp'] = timestamp
@pytest.mark.parametrize('case',casedata)
def test_recharges(case):
    res = send_request(case)
    assert_res(case,res)
    # 该函数灰提取对应的字段，并且保存到公共的数据容器中
    extract_res(case,res)
    if case['编号'] == 1:
        dic_evn['sign'] = res_str(dic_evn['token'][0:50]+str(timestamp))
