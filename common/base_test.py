import json
from string import Template
from common.handle_data import query_db
from loguru import logger
import openpyxl
from requests import request
import jsonpath

# 数据容器-字典格式，用来保存接口之间要关联的字段
dic_evn = {}

#读取excel中的数据
def read_excel(file_path,sheet_name):
    # 加载工作簿
    wb = openpyxl.load_workbook(file_path)
    # 得到sheet
    sh = wb[sheet_name]
    # 通过sheet获取所有数据
    datas = list(sh.values)
    header = datas[0]
    new_li = []
    for i in datas[1:]:
        result = dict(zip(header,i))
        new_li.append(result)
    return new_li


def assert_res(case,res):
    # 响应断言
    # 相当于所有的用例检查响应状态码都为200
    # assert res.status_code == 200
    # 代码需要处理所有的断言场景:
    # 1、响应状态码断言
    # 2、响应体字段断言(jsonpath表达式)
    # 3、响应体文本断言
    # case['期望结果']
    # 没有写的话，case['期望结果']返回结果是None,这里的if用来判断期望结果这列数据是否为空
    # 以下的代码是针对所有用例的断言场景进行统一的设计，不管是什么类型的断言，下面的代码都可以兼容
    if case['期望结果']:
        logger.info('-----------------------断言日志----------------------------')
        # 将json格式的字符串转换为字典类型
        dic = json.loads(case['期望结果'])
        for k, v in dic.items():
            # k(键)：status_code 或者 $..nickName 或者text
            # v(值)
            if k == 'status_code':
                assert res.status_code == v
                logger.info(f'响应状态码断言，期望值：{v}，实际值：{res.status_code}')
            elif k == 'text':
                assert res.text == v
                logger.info(f'响应体文本断言，期望值：{v}，实际值：{res.text}')
            # 通过判断第一个字符是不是$，如果这里是$开头，就说明这里为jsonpath表达式，我们需要进行响应体字段断言
            elif k[0] == '$':
                assert jsonpath.jsonpath(res.json(), k)[0] == v
                logger.info(f'响应体字段断言，期望值：{v}，实际值：{jsonpath.jsonpath(res.json(), k)[0]}')
            # 后续如果有新的断言场景，我们可以通过elif再补充

def assert_db(case):
 # 数据库断言
    if case['数据库断言']:
        db_info = case['数据库断言']
        db_info = Template(db_info).safe_substitute(dic_evn)
        dic = json.loads(db_info)
        for k,v in dic.items():
            # k代表我们要去执行的SQL语句， v:代表的就是期望值
            result = query_db(k,option='one')[0]
            logger.info(f'数据库断言，期望值：{v}，实际值：{result}，执行的SQL语句：{k}')
            assert result == v


# 通过将requests请求部分的代码封装成统一的函数，目的是为了能够处理所有不同的类型接口请求，get/post/put/delete
# 并且还可以处理不同传参类型，post为例：json表单传参/文件上传
def send_request(case):
    method = case['请求方法']
    url = case['请求地址']
    params = case['请求参数']
    headers = case['请求头']
    # 在请求发送&记录请求日志之前做标记识别替换的动作，需要参数替换有请求地址、请求参数、请求头
    url = Template(url).safe_substitute(dic_evn)
    if params:
        params = Template(params).safe_substitute(dic_evn)
    if headers:
        headers = Template(headers).safe_substitute(dic_evn)
    logger.info('-----------------------请求日志----------------------------')
    logger.info(f'请求方法：{method}')
    logger.info(f'请求地址：{url}')
    logger.info(f'请求头：{headers}')
    logger.info(f'请求参数：{params}')
    dic_header = None
    res = None
    if headers:
        dic_header = json.loads(headers)
    if method.lower() == 'get' or method.lower() == 'delete':
        # 为了去兼容get请求参数为空的情况
        if params:
            res = request(method,url,params=json.loads(params),headers=dic_header)
        else:
            res = request(method, url,headers=dic_header)
    elif method.lower() == 'post'or method.lower() == 'put':
        # 判断传参类型 - 如果Content-Type字段的值是application/json,表明json传参
        if 'application/json' in dic_header['Content-Type']:
            res = request(method,url,json=json.loads(params),headers=dic_header)
        elif 'application/x-www-form-urlencoded' in dic_header['Content-Type']:
            res = request(method,url,data=json.loads(params),headers=dic_header)
        elif 'multipart/form-data' in dic_header['Content-Type']:
            # 为什么Content-Type之后，默认把requests加的boundary字段的值进行覆盖，实际上传递给后端就没有boundary字段，最终会导致500的问题，所以要去掉Content-Type
            dic_header.pop('Content-Type')
            res = request(method,url,files=eval(params),headers=dic_header)

    logger.info('-----------------------响应日志----------------------------')
    logger.info(f'响应状态码:{res.status_code}')
    logger.info(f'响应时间:{res.elapsed.total_seconds()}s')
    logger.info(f'响应头:{res.headers}')
    logger.info(f'响应体:{res.text}')
    return res


def extract_res(case,res):
    # 提取响应字段
    extract_info = case['提取响应字段']
    if extract_info:
        extract_dict = json.loads(extract_info)
        # for 循环处理字典{"token":"$..access_token","nickname":"$..nickname"}
        for k, v in extract_dict.items():
            # 两种情况：jsonpath提取响应字段的值 / 整个响应文本数据提取
            if v == 'text':
                value = res.text
            else:
                value = jsonpath.jsonpath(res.json(),v)[0]
            # 通过jsonpath表达式提取实际的值
            # 关联字段的值需要保存到一个数据容器中（可能会有多组，比如prid_id:116 sku_id: 150 token:XXX...）
            dic_evn[k] = value

