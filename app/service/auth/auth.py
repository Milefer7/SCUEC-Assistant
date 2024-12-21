import base64
import hashlib
import hmac
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

from app.models import llm_model


def create_auth_url() -> str:
    """
    生成 Authorization 字段及请求 URL，用于 API 鉴权
    """
    # 获取当前时间并转换为HTTP格式
    cur_time = datetime.now()
    date = format_date_time(mktime(cur_time.timetuple()))

    # 拼接 HTTP 请求头的各个部分
    tmp = f"host: {llm_model.host}\n"
    tmp += f"date: {date}\n"
    tmp += "GET /v1.1/chat HTTP/1.1"

    # print(tmp)

    """上方拼接生成的tmp字符串如下
    host: spark-api.xf-yun.com
    date: Fri, 05 May 2023 10:43:39 GMT
    GET /v1.1/chat HTTP/1.1
    """

    # 使用 HMAC-SHA256 进行加密
    tmp_sha = hmac.new(llm_model.APISecret.encode('utf-8'), tmp.encode('utf-8'), digestmod=hashlib.sha256).digest()

    # 对加密结果进行 base64 编码
    signature = base64.b64encode(tmp_sha).decode(encoding='utf-8')

    # 拼接 Authorization 头部的字符串
    authorization_origin = f"api_key='{llm_model.APIKey}', algorithm='hmac-sha256', headers='host date request-line', signature='{signature}'"

    # 对 Authorization 字符串进行 base64 编码
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

    # 构建请求 URL
    v = {
        "authorization": authorization,  # 鉴权生成的 authorization
        "date": date,  # 当前时间的 HTTP 格式
        "host": llm_model.host  # 请求的主机名
    }

    # 生成最终的 URL
    url = llm_model.url + urlencode(v)

    # print(authorization)
    print(url)

    return url


create_auth_url()
