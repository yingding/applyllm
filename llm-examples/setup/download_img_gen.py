"""
Download the Img Gen model from Hugging Face
"""
import os
import click


'''set the model download cache directory'''

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

# https://huggingface.co/runwayml/stable-diffusion-v1-5
model_map = {
    "diffusion-v1.5":     "runwayml/stable-diffusion-v1-5",
}

dir_mode_map = {
    "kf_notebook": DirectorySetting(),
    "mac_local": DirectorySetting(home_dir="/Users/yingding", transformers_cache_home="MODELS", huggingface_token_file="MODELS/.huggingface_token"),
}

default_model_type = "diffusion-v1.5"
default_dir_mode = "kf_notebook"


def need_token(model_type: str, model_name_prefix: list=["llama", "gemma"]):
    """check if the model needs token"""
    return any([model_type.startswith(prefix) for prefix in model_name_prefix])


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
    
    get help:\n
    python3 download_img_gen.py --help

    valid call:\n
    python3 download_img_gen.py -t diffusion-v1.5\n
    python3 download_img_gen.py --model-type diffusion-v1.5\n
    
    invalid call:\n
    python3 download_img_gen.py -t=diffusion-v1.5\n
    python3 download_img_gen.py --model-type=diffusion-v1.5\n

    set directory:\n
    python3 download_img_gen.py -t diffusion-v1.5 -m kf_notebook
    
    Args:\n
      model_type: "diffusion-v1.5"\n
      dir_mode: "kf_notebook", "mac_local"\n
    """
 
    dir_setting=dir_mode_map.get(dir_mode, dir_mode_map[default_dir_mode])
    os.environ['XDG_CACHE_HOME']=dir_setting.get_cache_home()
    print("-"*10)
    print(f"download dir: {os.environ['XDG_CACHE_HOME']}")

    from diffusers import StableDiffusionPipeline
    import torch

    model_name = model_map.get(model_type, model_map[default_model_type])
    
    print("-"*10)
    print(f"model_type: {model_type}")
    print(f"model_name: {model_name}")
    print("-"*10)
    
    if need_token(model_type):
        # kwargs = {"use_auth_token": get_token(dir_setting)}
        kwargs = {
            "torch_dtype": torch.float16,
            "token": get_token(dir_setting)
        }
        print("huggingface token loaded")
    else:
        kwargs = {
            "torch_dtype": torch.float16
        }
        print("huggingface token is NOT needed")
    print("-"*10)

    model = StableDiffusionPipeline.from_pretrained(model_name, **kwargs)
    
if __name__ == '__main__':
    """
    uses default for click
    https://stackoverflow.com/questions/49011223/python-correct-use-of-click-with-main-and-init
    """
    download()