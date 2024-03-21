# -*- coding: utf-8 -*-
"""run web ui"""
import argparse
import os
import sys
import threading
import time
from collections import defaultdict
from typing import Optional, Callable
import traceback
import dashscope
import requests
from http import HTTPStatus
import uuid

global username
username=None
dashscope.api_key="your dashscope api key"
DEFAULT_AGENT_DIR = "E:/机器学习NLP/agent/LoveStory/game/config"
DEFAULT_CFG_DIR = os.path.join(DEFAULT_AGENT_DIR, "config")
CUSTOMER_CFG_NAME = "customer_config.yaml"
PLOT_CFG_NAME = "plot_config.yaml"
SIGNATURE_DIR = os.path.join(DEFAULT_AGENT_DIR, "signature")
SUFFIX = '.zip'
LOGO_PROMPT = """根据下面人物背景:{desc}，为这个人物生成一张画像。越接近真人越好。"""
color_images =[ "E:/img/jiangxi.jpg","E:/img/shandong.jpg","E:/img/jilin.jpg",
                "E:/img/henan.jpg","E:/img/sichuan.jpg","E:/img/jiangsu.jpg"]
names=["悠然","蓝心","雪琳","梓萱","思琪","诗涵"]

def get_user_dir(uuid=""):
    user_dir = DEFAULT_CFG_DIR
    user_dir = user_dir.replace("config", "config/user")
    if uuid != "":
        user_dir = user_dir.replace("user", uuid)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

def generate_user_logo_file(desc):
    #uuid_str=uuid.uuid4()
    uuid_=uuid.uuid4()
    logo_path = get_user_dir(str(uuid_))
    logo_file = os.path.join(logo_path + '.png')
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

try:
    import gradio as gr
except ImportError:
    gr = None

try:
    import modelscope_studio as mgr
except ImportError:
    mgr = None

from agentscope.web.studio.utils import (
    send_player_input,
    get_chat_msg,
    SYS_MSG_PREFIX,
    ResetException,
    check_uuid,
    send_msg,
    generate_image_from_name,
    audio2text,
    send_reset_msg,
    thread_local_data,
)

MAX_NUM_DISPLAY_MSG = 20
FAIL_COUNT_DOWN = 30


def init_uid_list() -> list:
    """Initialize an empty list for storing user IDs."""
    return []


glb_history_dict = defaultdict(init_uid_list)
glb_signed_user = []


def reset_glb_var(uid: str) -> None:
    """Reset global variables for a given user ID."""
    global glb_history_dict
    glb_history_dict[uid] = init_uid_list()


def get_chat(uid: str) -> list[list]:
    """Retrieve chat messages for a given user ID."""
    uid = check_uuid(uid)
    global glb_history_dict
    line = get_chat_msg(uid=uid)
    # TODO: Optimize the display effect, currently there is a problem of
    #  output display jumping
    if line:
        glb_history_dict[uid] += [line]
    dial_msg = []
    for line in glb_history_dict[uid]:
        _, msg = line
        if isinstance(msg, dict):
            dial_msg.append(line)
        else:
            # User chat, format: (msg, None)
            dial_msg.append(line)
    return dial_msg[-MAX_NUM_DISPLAY_MSG:]


def send_audio(audio_term: str, uid: str) -> None:
    """Convert audio input to text and send as a chat message."""
    uid = check_uuid(uid)
    content = audio2text(audio_path=audio_term)
    send_player_input(content, uid=uid)
    msg = f"""{content}
    <audio src="{audio_term}"></audio>"""
    send_msg(msg, is_player=True, role="Me", uid=uid, avatar=None)


def send_image(image_term: str, uid: str) -> None:
    """Send an image as a chat message."""
    uid = check_uuid(uid)
    send_player_input(image_term, uid=uid)

    msg = f"""<img src="{image_term}"></img>"""
    avatar = generate_image_from_name("Me")
    send_msg(msg, is_player=True, role="Me", uid=uid, avatar=avatar)


def send_message(msg: str, uid: str) -> str:
    """Send a generic message to the player."""
    uid = check_uuid(uid)
    send_player_input(msg, uid=uid)
    avatar = generate_image_from_name("Me")
    send_msg(msg, is_player=True, role="Me", uid=uid, avatar=avatar)
    return ""


def fn_choice(data: gr.EventData, uid: str) -> None:
    """Handle a selection event from the chatbot interface."""
    uid = check_uuid(uid)
    # pylint: disable=protected-access
    send_player_input(data._data["value"], uid=uid)
def submit_name(name: str) -> None:
    """处理提交的名称"""
    print(f"接收到的名称：{name}")
    # 这里调用你的main函数或其他逻辑
    # 假设main函数现在可以接受一个名称作为参数
    global username
    username=name
    return


def import_function_from_path(
    module_path: str,
    function_name: str,
    module_name: Optional[str] = None,
) -> Callable:
    """Import a function from the given module path."""
    import importlib.util

    script_dir = os.path.dirname(os.path.abspath(module_path))

    # Temporarily add a script directory to sys.path
    original_sys_path = sys.path[:]
    sys.path.insert(0, script_dir)

    try:
        # If a module name is not provided, you can use the filename (
        # without extension) as the module name
        if module_name is None:
            module_name = os.path.splitext(os.path.basename(module_path))[0]
        # Creating module specifications and loading modules
        spec = importlib.util.spec_from_file_location(
            module_name,
            module_path,
        )
        if spec is not None:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            # Getting a function from a module
            function = getattr(module, function_name)
        else:
            raise ImportError(
                f"Could not find module spec for {module_name} at"
                f" {module_path}",
            )
    except AttributeError as exc:
        raise AttributeError(
            f"The module '{module_name}' does not have a function named '"
            f"{function_name}'. Please put your code in the main function, "
            f"read README.md for details.",
        ) from exc
    finally:
        # Restore the original sys.path
        sys.path = original_sys_path

    return function


# pylint: disable=too-many-statements
def run_app() -> None:
    """Entry point for the web UI application."""
    parser = argparse.ArgumentParser()
    parser.add_argument("script", type=str, help="Script file to run")
    args = parser.parse_args()

    # Make sure script_path is an absolute path
    script_path = os.path.abspath(args.script)

    # Get the directory where the script is located
    script_dir = os.path.dirname(script_path)
    # Save the current working directory
    # Change the current working directory to the directory where
    os.chdir(script_dir)

    def start_game(uid: str) -> None:
        """Start the main game loop."""
        thread_local_data.uid = uid
        main = import_function_from_path(script_path, "main")

        while True:
            try:
                if username!=None:
                    main(username)
            except ResetException:
                print(f"Reset Successfully：{uid} ")
            except Exception as e:
                trace_info = "".join(
                    traceback.TracebackException.from_exception(e).format(),
                )
                for i in range(FAIL_COUNT_DOWN, 0, -1):
                    send_msg(
                        f"{SYS_MSG_PREFIX} error {trace_info}, reboot "
                        f"in {i} seconds",
                        uid=uid,
                    )
                    time.sleep(1)
            reset_glb_var(uid)

    def check_for_new_session(uid: str) -> None:
        """
        Check for a new user session and start a game thread if necessary.
        """
        uid = check_uuid(uid)
        if uid not in glb_signed_user and username!=None:
            glb_signed_user.append(uid)
            print("==========Signed User==========")
            print(f"Total number of users: {len(glb_signed_user)}")
            run_thread = threading.Thread(
                target=start_game,
                args=(uid,),
            )
            run_thread.start()

    with gr.Blocks() as demo:
        warning_html_code = """
                        <div class="hint" style="text-align:
                        center;background-color: rgba(255, 255, 0, 0.15);
                        padding: 10px; margin: 10px; border-radius: 5px;
                        border: 1px solid #ffcc00;">
                        <p>If you want to start over, please click the
                        <strong>reset</strong>
                        button and <strong>refresh</strong> the page</p>
                        </div>
                        """
        gr.HTML(warning_html_code)
        uuid = gr.Textbox(label="modelscope_uuid", visible=False)
        with gr.Row():
            image_components = [gr.Image(value=img_path, label=names[i]) for i, img_path in enumerate(color_images)]
        with gr.Row():
            chatbot = mgr.Chatbot(
                label="Dialog",
                show_label=False,
                bubble_full_width=False,
                visible=True,
            )

        with gr.Column():
            name_input = gr.Textbox(label="请输入您的名称")
            submit_name_button = gr.Button(value="😆提交名称")
            user_chat_input = gr.Textbox(
                label="user_chat_input",
                placeholder="首先输入你英俊潇洒的名字,然后就可以和女嘉宾对话了!",
                show_label=False,
            )
            send_button = gr.Button(value="📣发送")
        # with gr.Row():
        #     audio = gr.Accordion("Audio input", open=False)
        #     with audio:
        #         audio_term = gr.Audio(
        #             visible=True,
        #             type="filepath",
        #             format="wav",
        #         )
        #         submit_audio_button = gr.Button(value="Send Audio")
        with gr.Row():
            text= gr.Accordion("你的形象", open=True)
            with text:
                text_term=gr.Textbox(
                    label="快来自创你自己的形象吧！",
                    placeholder="快来描述一下你的形象吧...",
                    show_label = False
                )
                send_text_button = gr.Button(value="🤖一键生成")

            image = gr.Accordion("查看你的形象", open=True)
            with image:
                image_term = gr.Image(
                    visible=True,
                    height=784,
                    width=784,
                    interactive=True,
                    type="filepath",
                )
                # submit_image_button = gr.Button(value="Send Image")
        with gr.Column():
            reset_button = gr.Button(value="重新开始")

        # submit message
        send_button.click(
            send_message,
            [user_chat_input, uuid],
            user_chat_input,
        )
        user_chat_input.submit(
            send_message,
            [user_chat_input, uuid],
            user_chat_input,
        )

        # submit_audio_button.click(
        #     send_audio,
        #     inputs=[audio_term, uuid],
        #     outputs=[audio_term],
        # )

        # submit_image_button.click(
        #     send_image,
        #     inputs=[image_term, uuid],
        #     outputs=[image_term],
        # )
        submit_name_button.click(
            submit_name,
            inputs=name_input,
            outputs=[]
        )
        send_text_button.click(
            generate_user_logo_file,
            inputs=text_term,
            outputs=image_term,
        )

        reset_button.click(send_reset_msg, inputs=[uuid])

        chatbot.custom(fn=fn_choice, inputs=[uuid])

        demo.load(
            check_for_new_session,
            inputs=[uuid],
            every=0.5,
        )

        demo.load(
            get_chat,
            inputs=[uuid],
            outputs=[chatbot],
            every=0.5,
        )
    demo.queue()
    demo.launch()


if __name__ == "__main__":
    run_app()
