import dashscope
dashscope.api_key="your dashscope api key"
import os
import requests
from http import HTTPStatus
from config_utils import get_user_dir
import uuid


LOGO_PROMPT = """根据下面人物背景:{desc}，为这个人物生成一张画像。越接近真人越好。"""


def generate_user_logo_file(desc, name, uuid_str):
    logo_path = get_user_dir(uuid_str)
    logo_file = os.path.join(logo_path, name + '.png')
    logo_file = logo_file.replace("\\", "/")
    print(logo_file)
    generate_logo_file(desc, logo_file)
    return logo_file if os.path.exists(logo_file) else None


def generate_logo_file(desc, logo_file):
    from dashscope.common.error import InvalidTask
    dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY") or dashscope.api_key
    assert dashscope.api_key

    prompt = LOGO_PROMPT.format(desc=desc)
    try:
        rsp = dashscope.ImageSynthesis.call(
            model='wanx-lite',
            prompt=prompt,
            n=1,
            size='768*768')

        # save file to current directory
        if rsp.status_code == HTTPStatus.OK:
            # if os.path.exists(logo_file):
            #     os.remove(logo_file)
            print("ok")
            for result in rsp.output.results:
                with open(logo_file, 'wb+') as f:
                    f.write(requests.get(result.url).content)

        else:
            print('Failed, status_code: %s, code: %s, message: %s' %
                  (rsp.status_code, rsp.code, rsp.message))
    except InvalidTask as e:
        print(e)

if __name__ == '__main__':
    desc = "干活超勤快的黑奴"  # 描述人物背景
    name = "路易十四"  # 人物名称
    uuid_str = "f47ac10b-58cc-4372-a567-0e02b2c3d471"  # 假设的UUID

    # 调用函数生成头像文件
    logo_file = generate_user_logo_file(desc, name, uuid_str)

    if logo_file:
        print(f"头像文件已生成，位置：{logo_file}")
    else:
        print("生成头像文件失败。")
