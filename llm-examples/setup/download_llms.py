"""
Before run this script, need to generate a token from huggingface
To login, `huggingface_hub` requires a token generated from https://huggingface.co/settings/tokens
-> user profile -> settings -> Access Tokens -> New token
name: llama2
role: read

Then call
huggingface-cli

use 
echo "<my_token>" > token
to create a token instead of using vi, which will add a new line char to token automatically.

"""
import os
import click
# import argpass


'''set the model download cache directory'''
# set the home directory for the models

from dataclasses import dataclass
@dataclass
class DirectorySetting:
    """set the directory for the model download"""
    home_dir: str="/home/jovyan/llm-models"
    transformers_cache_home: str="core-kind/yinwang/models"
    huggingface_token_file: str="core-kind/yinwang/.cache/huggingface/token"

    def get_cache_home(self):
        """get the cache home"""
        return f"{self.home_dir}/{self.transformers_cache_home}"
    
    def get_token_file(self):
        """get the token file"""
        return f"{self.home_dir}/{self.huggingface_token_file}"

model_map = {
    "llama7B-chat":     "meta-llama/Llama-2-7b-chat-hf",
    "llama13B-chat" :   "meta-llama/Llama-2-13b-chat-hf",
    "llama70B-chat" :   "meta-llama/Llama-2-70b-chat-hf",
    # "70B" : "meta-llama/Llama-2-70b-hf"
    "mistral7B-01":     "mistralai/Mistral-7B-v0.1",
    "mistral7B-inst02": "mistralai/Mistral-7B-Instruct-v0.2",
    "mixtral8x7B-01":   "mistralai/Mixtral-8x7B-v0.1",
    "mixtral8x7B-inst01":   "mistralai/Mixtral-8x7B-Instruct-v0.1", 
}

dir_mode_map = {
    "kf_notebook": DirectorySetting(),
    "mac_local": DirectorySetting(home_dir="/Users/yingding", transformers_cache_home="MODELS", huggingface_token_file="MODELS/.huggingface_token"),
}

default_model_type = "mistral7B-01"
default_dir_mode = "kf_notebook"


def need_token(model_type: str, model_name_prefix: str="llama"):
    """check if the model needs token"""
    return model_type.startswith(model_name_prefix)


def get_token(dir_setting: DirectorySetting):
    """get the token from the token file"""
    token_file_path = dir_setting.get_token_file()
    with open(token_file_path, "r") as file:
        # file read add a new line to the token, remove it.
        token = file.read().replace('\n', '')
    return token

# print the raw string to see if there is new line in the token
# print(r'{}'.format(token))

# Reference: https://click.palletsprojects.com/en/8.1.x/quickstart/
# @click.option(..., is_flag=True, ...) set the option to be boolean
# call with download_llms --help
# https://www.geeksforgeeks.org/argparse-vs-docopt-vs-click-comparing-python-command-line-parsing-libraries/
# https://click.palletsprojects.com/en/8.1.x/quickstart/
# https://click.palletsprojects.com/en/8.1.x/options/
# https://www.youtube.com/watch?v=kNke39OZ2k0
@click.command()
@click.option('-t','--model-type', 'model_type', default=default_model_type, type=str, required=False, help=f"set the llm type to download:\n{', '.join(model_map.keys())}, default is {default_model_type}")
@click.option('-m','--mode', 'dir_mode', default=default_dir_mode, type=str, required=False, help=f"set the directory settings to use:\n{', '.join(dir_mode_map.keys())}, default is {default_dir_mode}")
def download(model_type: str=default_model_type, dir_mode: str=default_dir_mode):
    """
    This method will download the llm model. If cache exists, the cached model will be used.
    
    get help:
    python3 download_llms.py --help

    valid call:
    python3 download_llms.py -t mistral7B-01
    python3 download_llms.py --model-type mistral7B-01
    
    invalid call:
    python3 download_llms.py -t=mistral7B-01
    python3 download_llms.py --model-type=mistral7B-01

    set directory:
    python3 download_llms.py -t mistral7B-01 -m kf_notebook
    
    Args:
      model_type: "llama7B-chat", "llama13B-chat", "llama70B-chat", "mistral7B-01", "mistral7B-inst02", "mistral8x7B-01"
      dir_mode: "kf_notebook", "mac_local"
    """
 
    dir_setting=dir_mode_map.get(dir_mode, dir_mode_map[default_dir_mode])
    os.environ['XDG_CACHE_HOME']=dir_setting.get_cache_home()
    print("-"*10)
    print(f"download dir: {os.environ['XDG_CACHE_HOME']}")

    from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

    model_name = model_map.get(model_type, model_map[default_model_type])
    
    print("-"*10)
    print(f"model_type: {model_type}")
    print(f"model_name: {model_name}")
    print("-"*10)
    
    if need_token(model_type):
        # kwargs = {"use_auth_token": get_token(dir_setting)}
        kwargs = {"token": get_token(dir_setting)}
        print("huggingface token loaded")
    else:
        kwargs = {}
        print("huggingface token is NOT needed")
    print("-"*10)
    tokenizer = AutoTokenizer.from_pretrained(model_name, **kwargs)
    model = AutoModelForCausalLM.from_pretrained(model_name, **kwargs)
    
if __name__ == '__main__':
    """
    uses default for click
    https://stackoverflow.com/questions/49011223/python-correct-use-of-click-with-main-and-init
    """
#    parser = argparse.ArgumentParser()
#    parser.add_argument('--model-type', dest='model-type',
#                        default=os.environ['model-type'], type=str, help='the llama2 type to download: 7B, 13B')
    
#    args = parser.parse_args()
#    params_dict = args.__dict__
    
#    print(params_dict)
    download()