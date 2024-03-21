import os
import shutil
import yaml
DEFAULT_AGENT_DIR = "E:/机器学习NLP/agent/LoveStory/game/config"
DEFAULT_CFG_DIR = os.path.join(DEFAULT_AGENT_DIR, "config")
CUSTOMER_CFG_NAME = "customer_config.yaml"
PLOT_CFG_NAME = "plot_config.yaml"
SIGNATURE_DIR = os.path.join(DEFAULT_AGENT_DIR, "signature")
SUFFIX = '.zip'

def get_user_dir(uuid=""):
    user_dir = DEFAULT_CFG_DIR
    user_dir = user_dir.replace("config", "config/user")
    if uuid != "":
        user_dir = user_dir.replace("user", uuid)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir