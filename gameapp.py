# import gradio as gr
#
# # 示例功能，这些应该根据你的实际逻辑进行替换
# def create_avatar(file_info):
#     # 这里替换为生成头像的逻辑
#     return file_info
#
# def send_message(message):
#     # 这里替换为处理发送消息的逻辑
#     return "回复: " + message
#
# # 布局和组件
# with gr.Blocks() as demo:
#     with gr.Row():
#         with gr.Column():
#             guest1_image = gr.Image()
#             guest1_dialogue = gr.Textbox(placeholder="嘉宾1发言内容", lines=2)
#         with gr.Column():
#             guest2_image = gr.Image()
#             guest2_dialogue = gr.Textbox(placeholder="嘉宾2发言内容", lines=2)
#         with gr.Column():
#             guest3_image = gr.Image()
#             guest3_dialogue = gr.Textbox(placeholder="嘉宾3发言内容", lines=2)
#     with gr.Row():
#         with gr.Column():
#             guest4_image = gr.Image()
#             guest4_dialogue = gr.Textbox(placeholder="嘉宾4发言内容", lines=2)
#         with gr.Column():
#             guest5_image = gr.Image()
#             guest5_dialogue = gr.Textbox(placeholder="嘉宾5发言内容", lines=2)
#         with gr.Column():
#             guest6_image = gr.Image()
#             guest6_dialogue = gr.Textbox(placeholder="嘉宾6发言内容", lines=2)
#     with gr.Row():
#         host_image = gr.Image()
#         host_dialogue = gr.Textbox(placeholder="主持人发言内容", lines=2)
#     with gr.Row():
#         user_image = gr.File(label="上传您的照片")
#         create_button = gr.Button("生成头像")
#         user_avatar = gr.Image()
#         create_button.click(create_avatar, inputs=user_image, outputs=user_avatar)
#     with gr.Row():
#         user_input = gr.Textbox(label="输入您的对话")
#         send_button = gr.Button("发送")
#         user_dialogue = gr.Textbox()
#         send_button.click(send_message, inputs=user_input, outputs=user_dialogue)
#
# demo.launch()

import gradio as gr

# 示例功能，这些应该根据你的实际逻辑进行替换
def create_avatar(image):
    # 这里替换为生成头像的逻辑
    return image

def send_message(message):
    # 这里替换为处理发送消息的逻辑
    return "回复: " + message

# 布局和组件
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            with gr.Row():
                guest1_image = gr.Image()
                guest1_dialogue = gr.Textbox(placeholder="嘉宾1发言内容", lines=1, min_width=60, scale=1)
            with gr.Row():
                guest2_image = gr.Image()
                guest2_dialogue = gr.Textbox(placeholder="嘉宾2发言内容", lines=1, min_width=60, scale=1)
            with gr.Row():
                guest3_image = gr.Image()
                guest3_dialogue = gr.Textbox(placeholder="嘉宾3发言内容", lines=1, min_width=60, scale=1)
            with gr.Row():
                guest4_image = gr.Image()
                guest4_dialogue = gr.Textbox(placeholder="嘉宾4发言内容", lines=1, min_width=60, scale=1)
            with gr.Row():
                guest5_image = gr.Image()
                guest5_dialogue = gr.Textbox(placeholder="嘉宾5发言内容", lines=1, min_width=60, scale=1)
            with gr.Row():
                guest6_image = gr.Image()
                guest6_dialogue = gr.Textbox(placeholder="嘉宾6发言内容", lines=1, min_width=60, scale=1)

            # 重复上面的行为每个女嘉宾
            # ...
        # 如果你需要在屏幕右上角添加更多内容，可以在这里添加一个Column

    with gr.Row():
        host_image = gr.Image()
        host_dialogue = gr.Textbox(placeholder="主持人发言内容", lines=1)
    # 换行添加用户输入和头像上传
    with gr.Row():
        user_image = gr.File(label="上传您的照片")
        create_button = gr.Button("生成头像")
        user_avatar = gr.Image()

    with gr.Row():
        user_input = gr.Textbox(label="输入您的对话")
        send_button = gr.Button("发送")
        user_dialogue = gr.Textbox()

    # 为按钮设置动作
    create_button.click(create_avatar, inputs=user_image, outputs=user_avatar)
    send_button.click(send_message, inputs=user_input, outputs=user_dialogue)

demo.launch()


