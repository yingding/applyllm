import torch
import os
import subprocess
import re
import sys
import time
from dataclasses import dataclass
import Warnings


@dataclass
class DirectorySetting:
    """set the directory for the model download"""

    home_dir: str = "/home/jovyan/llm-models"
    transformers_cache_home: str = "core-kind/yinwang/models"
    huggingface_token_file: str = "core-kind/yinwang/.cache/huggingface/token"

    def get_cache_home(self):
        """get the cache home"""
        return os.path.join(f"{self.home_dir}", f"{self.transformers_cache_home}")

    def get_token_file(self):
        """get the token file"""
        # use path join for windows and linux compatibility
        return os.path.join(f"{self.home_dir}", f"{self.huggingface_token_file}")


DIR_MODE_MAP = {
    "kf_notebook": DirectorySetting(),
    "mac_local": DirectorySetting(
        home_dir="/Users/yingding",
        transformers_cache_home="MODELS",
        huggingface_token_file="MODELS/.huggingface_token",
    ),
    "win_local": DirectorySetting(
        home_dir="C:\\Users\\yingdingwang",
        transformers_cache_home="MODELS",
        huggingface_token_file="MODELS\\.huggingface_token",
    ),
}


class TokenHelper:
    def __init__(self, dir_setting: DirectorySetting, prefix_list: list = ["llama"]):
        self.prefix_list = prefix_list
        self.dir_setting = dir_setting

    def need_token(self, model_type: str) -> bool:
        """check if the model needs token"""
        # check if the model type startswith a string in the prefix list
        # model_type.startswith(model_name_prefix)
        return any([model_type.startswith(prefix) for prefix in self.prefix_list])

    def get_token(self):
        """get the token from the token file"""
        token_file_path = self.dir_setting.get_token_file()
        with open(token_file_path, "r") as file:
            # file read add a new line to the token, remove it.
            token = file.read().replace("\n", "")
        return token

    def gen_token_kwargs(self, model_type: str):
        """ """
        if self.need_token(model_type):
            # kwargs = {"use_auth_token": get_token(dir_setting)}
            token_kwargs = {
                "token": self.get_token(),
                # "truncation_side": "left",
                # "return_tensors": "pt",
            }
            print("huggingface token loaded")
        else:
            token_kwargs = {}
            print("huggingface token is NOT needed")
        return token_kwargs


class AcceleratorHelper:
    @staticmethod
    def print_container_info() -> None:
        print("-" * 10)
        print(time.strftime("%Y-%m-%d_%H-%M-%S"))
        print(f"python version: {sys.version}")
        print(f"torch version: {torch.__version__}")
        print("-" * 10)

    @staticmethod
    def nvidia_device_info() -> str:
        """get the nvidia MIGs device uuid and GPU uuid"""
        # blocking call
        result = subprocess.run(["nvidia-smi", "-L"], stdout=subprocess.PIPE)
        # decode the byte object, returns string with \n
        cmd_out_str = result.stdout.decode("utf-8")
        return [line.strip() for line in cmd_out_str.split("\n") if len(line) > 0]

    @staticmethod
    def extract_nvidia_device_uuids(input: str):
        """parse the nvidia devices uuid from the nvidia device info str"""
        try:
            # r'' before the search pattern indicates it is a raw string,
            # otherwise "" instead of single quote
            uuid = re.search(r"UUID\:\s(.+?)\)", input).group(1)
        except AttributeError:
            # "UUID\:\s" and "\)" not found
            uuid = ""
        return uuid

    @staticmethod
    def nvidia_device_uuids_filtered_by(
        is_mig: bool = False, log_output: bool = False
    ) -> str:
        """get a comma separated str of nvidia MIGs devices"""
        info_list = AcceleratorHelper.nvidia_device_info()
        if is_mig:
            # skip the first GPU ID, get the MIGs IDS
            uuid_list = [
                AcceleratorHelper.extract_nvidia_device_uuids(e) for e in info_list[1:]
            ]
        else:  # all GPU devices
            uuid_list = [
                AcceleratorHelper.extract_nvidia_device_uuids(e) for e in info_list
            ]
        if log_output is not None and log_output:
            print(uuid_list)

        # if multi gpus need to join the device together for pytorch
        return ",".join(uuid_list)

    @staticmethod
    def _init_cuda_torch(
        uuids: str, dir_setting: DirectorySetting, debug: bool = False
    ) -> None:
        """setup the default env variables for transformers

        Args:
          uuids: a comma separate str of nvidia gpu/mig uuids
        """
        os.environ["WORLD_SIZE"] = "1"
        os.environ["CUDA_VISIBLE_DEVICES"] = uuids
        os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:512"  # 512
        os.environ["XDG_CACHE_HOME"] = dir_setting.get_cache_home()
        # os.environ['XDG_CACHE_HOME'] = f"{data_path}/models"
        if debug:
            # for debugging
            os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
        

    # @staticmethod
    # def init_mps_torch(dir_setting: DirectorySetting) -> None:
    #     """setup the default env variables for transformers"""
    #     # os.environ['TOKENIZERS_PARALLELISM'] = "false"
    #     # https://github.com/huggingface/transformers/issues/5486?ref=assemblyai.com
    #     os.environ["WORLD_SIZE"] = "1"
    #     os.environ["XDG_CACHE_HOME"] = dir_setting.get_cache_home()

    @staticmethod
    def init_torch_env(
        accelerator: str, dir_setting: DirectorySetting, **kwargs
    ) -> None:
        """
        Initializes the PyTorch environment based on the specified accelerator type.

        Args:
            accelerator (str): The type of accelerator to use. Supported values are "mps", "xpu", "npu", "cpu" and "cuda".
            dir_setting (DirectorySetting): An instance of DirectorySetting to manage directory paths.
            kwargs (dict): Additional keyword arguments. For "cuda" accelerator, it can include:
                - "uuids" (str): A string representing the UUIDs.
                - "debug" (bool, optional): A flag to enable or disable debug mode. Defaults to False.

        Raises:
            Warnings.warn: If the specified accelerator is not supported.
        """
        if (
            accelerator == "mps"
            or accelerator == "xpu"
            or accelerator == "npu"
            or accelerator == "cpu"
        ):
            os.environ["WORLD_SIZE"] = "1"
            os.environ["XDG_CACHE_HOME"] = dir_setting.get_cache_home()
        elif accelerator == "cuda":
            if "uuids" in kwargs and isinstance(kwargs["uuids"], str):
                uuids = kwargs["uuids"]
                if "debug" in kwargs and isinstance(kwargs["debug"], bool):
                    debug = kwargs["debug"]
                else:
                    debug = False
                AcceleratorHelper._init_cuda_torch(
                    uuids=uuids, dir_setting=dir_setting, debug=debug
                )
            else:
                # warning with Warnings class
                Warnings.warn("UUIDs not provided for CUDA accelerator")
        else:
            # warning with Warnings class
            Warnings.warn("accelerator not supported")


class AcceleratorStatus:
    # Reference: https://stackoverflow.com/questions/58216000/get-total-amount-of-free-gpu-memory-and-available-using-pytorch
    # from typing import Tuple
    def byte_gb_info(self, byte_mem) -> str:
        """calculate the byte size to GB size for better human readable"""
        # format the f string float with :.2f to decimal digits
        # https://zetcode.com/python/fstring/
        return f"{(byte_mem/1024**3):4f} GB"

    def gpu_usage(self) -> None:
        pass

    # factory method to create the correct accelerator status class
    @staticmethod
    def create_accelerator_status() -> "AcceleratorStatus":
        # check if the MPS is enabled
        if torch.backends.mps.is_available():
            return MpsAcceleratorStatus()
        elif torch.cuda.is_available():
            return CudaAcceleratorStatus()
        else:
            return AcceleratorStatus()


class MpsAcceleratorStatus(AcceleratorStatus):
    def __init__(self):
        pass

    def accelerator_mem_info(self):
        # allocated
        a = torch.mps.driver_allocated_memory()
        print(f"Allocated memory : {self.byte_gb_info(a)}")

    def gpu_usage(self) -> None:
        print("-" * 20)
        self.accelerator_mem_info()
        print("-" * 20)


class CudaAcceleratorStatus(AcceleratorStatus):
    def __init__(self):
        pass

    def accelerator_mem_info(self, device_idx: int):
        # total
        t = torch.cuda.get_device_properties(device_idx).total_memory
        # usable
        r = torch.cuda.memory_reserved(device_idx)
        # allocated
        a = torch.cuda.memory_allocated(device_idx)
        # still free
        f = r - a
        # unit = "GB"
        print(  # "GPU memory info:\n" +
            f"Physical  memory : {self.byte_gb_info(t)}\n"
            + f"Reserved  memory : {self.byte_gb_info(r)}\n"
            + f"Allocated memory : {self.byte_gb_info(a)}\n"
            + f"Free      memory : {self.byte_gb_info(f)}"
        )

    def accelerator_compute_info(self, device_idx: int) -> None:
        name = torch.cuda.get_device_properties(device_idx).name
        count = torch.cuda.get_device_properties(device_idx).multi_processor_count
        print(
            f"Device name      : {name} \n"
            + f"Device idx       : {device_idx} \n"
            + f"No. of processors: {count}"
        )

    def gpu_usage(self) -> None:
        num_of_gpus = torch.cuda.device_count()
        # this shows only the gpu device, not the MIG
        print(f"num_of_gpus: {num_of_gpus}")
        for device_idx in range(torch.cuda.device_count()):
            print("-" * 20)
            self.accelerator_compute_info(device_idx)
            self.accelerator_mem_info(device_idx)
            print("-" * 20)
