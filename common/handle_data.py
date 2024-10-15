import pymysql
from faker import Faker


def query_db(sql, option, many_num=1):
    """
    数据库查询操作的统一封装
    :param sql: 要执行的SQL语句
    :param option: 要进行的操作，one代表查询一条数据，many代表查询多条数据（mang_num参数指定查询的条数），all代表的查询所有的数据
    :param many_num: 参数指定查询的条数
    :return: 执行的结果
    """
    conn = pymysql.connect(
        host='mall.lemonban.com',
        port=3306,
        user='lemon_auto',
        password='lemon!@123',
        database='yami_shops',
        charset='utf8'
    )
    cur = conn.cursor()
    cur.execute(sql)
    if option == 'one':
        result = cur.fetchone()
    elif option =='many':
        result = cur.fetchmany(many_num)
    elif option == 'all':
        result = cur.fetchall()
    else:
        result = "option参数不符合要求"
    conn.close()
    return result


def get_unregister_phone():
    """
    构造生成没有使用过的手机号码，满足注册使用
    :return: 满足要求的手机号码
    """
    f = Faker(locale="zh-CN")
    while True:
        phone = f.phone_number()
        # 查询数据库，检查手机号码是否在数据库(用户表)中
        result = query_db(f"select count(*) from tz_user where user_mobile = '{phone}'","one")[0]
        # 如果result为1，代表数据库中有这条数据记录的，需要重新构造新的数据-->查询数据库
        if result == 0:
            break
    return phone

def get_unregister_username():
    """
    构造生成没有使用过的用户名，满足注册使用
    :return: 满足要求的手机号码
    """
    f = Faker(locale="zh-CN")
    while True:
        username = f.pystr(4,16)
        # 查询数据库，检查手机号码是否在数据库(用户表)中
        result = query_db(f"select count(*) from tz_user where user_name = '{username}'", "one")[0]
        # 如果result为1，代表数据库中有这条数据记录的，需要重新构造新的数据-->查询数据库
        if result == 0:
            break
    return username
