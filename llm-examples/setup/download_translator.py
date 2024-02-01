"""
Run this script to download a T5 family translator model

Example: 
>> python3 download_translator.py --help 
"""
import os
import click

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


# from transformers import T5Tokenizer, T5ForConditionalGeneration

# T5 model family info on huggingface
# https://huggingface.co/docs/transformers/model_doc/t5
# Note: T5 can only translate from "translate_en_to_de" but not de_to_en
# need to use mt5 

# model_map = {
#    "small": "t5-small",
#    "base" : "t5-base",
#    "large" : "t5-large",
#    "3B" : "t5-3b", # 11.4 GB
#    "11B" : "t5-11b" # 45.2 GB
# }

model_map = {
   "small": "google/mt5-small", # 1.2 GB
   "base" : "google/mt5-base", # 2.33 GB
   "large" : "google/mt5-large", # 4.9 GB,
   "xl" : "google/mt5-xl", # 15 GB
   "xxl" : "google/mt5-xxl" # 51.7 GB
}

dir_mode_map = {
    "kf_notebook": DirectorySetting(),
    "mac_local": DirectorySetting(home_dir="/Users/yingding", transformers_cache_home="MODELS", huggingface_token_file="MODELS/.huggingface_token"),
}

default_model_type = "small"
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

# token_file_path = f"{DATA_ROOT}/core-kind/yinwang/.cache/huggingface/token"
# file = open(token_file_path, "r")

# file read add a new line to the token, remove it.
# token = file.read().replace('\n', '')

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
@click.option('-t','--model-type', 'model_type', default=default_model_type, type=str, required=False, help=f"set the translator type to download:\n{', '.join(model_map.keys())}, default is {default_model_type}")
@click.option('-m','--mode', 'dir_mode', default=default_dir_mode, type=str, required=False, help=f"set the directory settings to use:\n{', '.join(dir_mode_map.keys())}, default is {default_dir_mode}")
def download(model_type: str=default_model_type, dir_mode: str=default_dir_mode):
    """
    This method will download a T5 translator model. If cache exists, the cached model will be used.

    get help:
    python3 download_translator.py --help

    valid call:
    python3 download_translator.py -t small
    python3 download_translator.py --model-type small
    
    
    set directory:
    python3 download_translator.py -t small -m kf_notebook
    
    Args:
      model_type: "small", ..., "3B", "11B"
    """
    # model_type = params.get("model-type", os.environ['model-type'])
    dir_setting=dir_mode_map.get(dir_mode, dir_mode_map[default_dir_mode])
    os.environ['XDG_CACHE_HOME']=dir_setting.get_cache_home()
    print("-"*10)
    print(f"download dir: {os.environ['XDG_CACHE_HOME']}")
    
    from transformers import MT5Model, MT5ForConditionalGeneration, MT5TokenizerFast, MT5Config

    # model_name = model_map.get(model_type, model_map[os.environ['model-type']])
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
    
    tokenizer = MT5TokenizerFast.from_pretrained(model_name)
    model = MT5ForConditionalGeneration.from_pretrained(model_name)
    
    # tokenizer = T5Tokenizer.from_pretrained(model_name)
    # model = T5ForConditionalGeneration.from_pretrained(model_name)
    
    
if __name__ == '__main__':
    """
    uses default for click
    https://stackoverflow.com/questions/49011223/python-correct-use-of-click-with-main-and-init
    
    translator on huggingface: 
    https://huggingface.co/learn/nlp-course/chapter7/4?fw=tf
    
    Inference and Fine-tuning T5 model
    https://huggingface.co/docs/transformers/model_doc/t5
    """
    download()