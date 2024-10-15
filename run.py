# 所有测试用例收集执行入口
import os

import pytest
from loguru import logger

# 通过日志记录接口运行信息（持续化储存）
from common.handle_path import log_path

logger.add(log_path,
           encoding="utf8",
           level='INFO',
           rotation='10MB',
           retention=20)


pytest.main(['-s','-v','--alluredir=outputs/allure-results','--clean-alluredir'])
# 此时运行当前py文件，那么会以当前py文件作为基准的路径Path().cwd()-->获取的就是当前py文件对应文件夹路径（E:\daily\fengzhuang_test）
# print(Path(__file__))
# print(Path().cwd()/'datas'/'casedata.xlsx')

# 后续自动生成图形化的Allure报告，python代码执行cmd报告，python代码执行cmd命令 -allure serve allure-results
# os.system('allure serve E:\\daily\\fengzhuang_test\\outputs\\allure-results')

