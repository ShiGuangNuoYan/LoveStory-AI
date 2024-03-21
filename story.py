from functools import partial
from agentscope.message import Msg
from agentscope.msghub import msghub
import agentscope
from agentscope.agents import UserAgent
from prompt import Prompts
import uuid
import dashscope
dashscope.api_key="your dashscope api key"
import os
import requests
from http import HTTPStatus
from config_utils import get_user_dir

LOGO_PROMPT = """根据下面人物背景:{desc}，为这个人物生成一张画像。越接近真人越好。"""
lighting=[True,True,True,True,True,True]
keywords = ["不愿意", "不同意", "否","退出","算了","不喜欢","没感觉","不合适","不般配"]

def generate_user_logo_file(desc, name, uuid_str):
    logo_path = get_user_dir(uuid_str)
    logo_file = os.path.join(logo_path, name + '.png')
    logo_file = logo_file.replace("\\", "/")
    # print(logo_file)
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
            size='784*784')

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

def personalise():
    # 生成一个随机UUID
    desc=input("请输入你对自己的描述:")
    name=input("请输入你的名字:")
    random_uuid = uuid.uuid4()
    logo_file=generate_user_logo_file(desc=desc,name=name,uuid_str=random_uuid)
    if logo_file:
        print(f"头像文件已生成，位置：{logo_file}")
    else:
        print("生成头像文件失败。")

def main(name) -> None:
    HostMsg = partial(Msg, name="系统", echo=False)
    user_agent = UserAgent(name=name)
    participants = agentscope.init(
        model_configs="E:/机器学习NLP/agent/LoveStory/config/model_configs.json",
        agent_configs="E:/机器学习NLP/agent/LoveStory/config/agent_configs.json",
    )
    f_guests,host=participants[:6],participants[-1]
    with msghub([user_agent] + f_guests + [host]) as hub:
        welcome_message = HostMsg(content=Prompts.welcome_user.format(user_agent.name))
        print(welcome_message)
        reply1=host(welcome_message)
        hub.broadcast(reply1)

        for guest in f_guests:
            guest.reply(welcome_message)

        #自我介绍
        intro_message=HostMsg(content=Prompts.to_user_intro.format(**{"user_name":user_agent.name}))
        reply2=host(intro_message)
        hub.broadcast(reply2)
        introduction_hint = user_agent()
        hub.broadcast(introduction_hint)
        for index, guest in enumerate(f_guests):
            if lighting[index]:
                hint = HostMsg(
                    content=Prompts.to_f_guest_intro.format_map(
                        {
                            "fguest_name": guest.name,
                            "user_name": user_agent.name,
                        },
                    ),
                )
                response=guest(hint)
                # print(response)
                src_str=response['content']
                # print(response['content'])
                condition_result1 = "灭灯" in src_str
                condition_result2 = "留灯" in src_str
                # print(condition_result)
                hub.broadcast(response)
                if condition_result1 and not condition_result2:
                    lighting[index]=False
                    hint2=HostMsg(content=Prompts.pity.format(**{"fguest_name":guest.name}))
                    hub.broadcast(host(hint2))
                    if not any(lighting):
                        host(HostMsg(content=Prompts.over()))
                        return

        hint3=HostMsg(content=Prompts.experience)
        reply3=host.reply(hint3)
        hub.broadcast(reply3)
        #恋爱经历
        experience_hint=user_agent()
        hub.broadcast(experience_hint)
        for index,guest in enumerate(f_guests):
            if lighting[index]:
                hint =HostMsg(
                    content=Prompts.to_f_guest_ex.format_map(
                        {
                            "fguest_name": guest.name,
                            "user_name": user_agent.name,
                        },
                    ),
                )
                response1 = guest(hint)
                # print(response)
                src_str = response1['content']
                # print(response['content'])
                condition_result1 = "灭灯" in src_str
                condition_result2 = "留灯" in src_str
                hub.broadcast(response1)
                if condition_result1 and not condition_result2:
                    lighting[index] = False
                    hint4 = HostMsg(content=Prompts.pity.format(**{"fguest_name": guest.name}))
                    hub.broadcast(host(hint4))
                    if not any(lighting):
                        host(HostMsg(content=Prompts.over()))
                        return
        #自身优势
        hint5 = HostMsg(content=Prompts.advantage)
        reply4=host.reply(hint5)
        hub.broadcast(reply4)

        advantage_hint = user_agent()
        hub.broadcast(advantage_hint)
        for index,guest in enumerate(f_guests):
            if lighting[index]:
                hint =HostMsg(
                    content=Prompts.to_f_guest_ad.format_map(
                        {
                            "fguest_name": guest.name,
                            "user_name": user_agent.name,
                        },
                    ),
                )
                response2 = guest(hint)
                # print(response)
                src_str = response2['content']
                # print(response['content'])
                condition_result1 = "灭灯" in src_str
                condition_result2 = "留灯" in src_str
                # print(condition_result)
                hub.broadcast(response2)
                if condition_result1 and not condition_result2:
                    lighting[index] = False
                    hint6 = HostMsg(content=Prompts.pity.format(**{"fguest_name": guest.name}))
                    hub.broadcast(host(hint6))
                    if not any(lighting):
                        host(HostMsg(content=Prompts.over()))
                        return

        if any(lighting):
            hint7=HostMsg(content=Prompts.to_user_light)
            hub.broadcast(host(hint7))
            choose_or_not=user_agent()
            hub.broadcast(choose_or_not)
            for keyword in keywords:
                if keyword in choose_or_not['content']:
                    hint8 = HostMsg(content=Prompts.to_user_quit.format(**{"user_name": user_agent.name}))
                    host(hint8)
                    return


        hint10 = HostMsg(content=Prompts.to_f_guest_suc.format(**{"user_name": user_agent.name}))
        hub.broadcast(host(hint10))
        # 最终牵手成功
        user_love = user_agent()
        if   "6号" in choose_or_not['content']:
            guest_love = participants[5](user_love)
            return
        elif "5号" in choose_or_not['content']:
            guest_love = participants[4](user_love)
            return
        elif "4号" in choose_or_not['content']:
            guest_love = participants[3](user_love)
            return
        elif "3号" in choose_or_not['content']:
            guest_love = participants[2](user_love)
            return
        elif "2号" in choose_or_not['content']:
            guest_love = participants[1](user_love)
            return
        elif "1号" in choose_or_not['content']:
            guest_love = participants[0](user_love)
            return

if __name__ == '__main__':
    # personalise()
    main(name="xxx")


