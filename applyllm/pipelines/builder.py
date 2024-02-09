class KwargsBuilder:
    """
    merge the kwargs from the list of kwargs for the Transformer model or pipeline
    """

    def __init__(self, args_list: list = []):
        self.kwargs = {}
        self.args_list = args_list

    def override(self, kwargs: dict):
        self.args_list.append(kwargs)
        return self

    def build(self) -> dict:
        """
        during the build, merge the kwargs from the list of args_list,
        the later kwargs always override the prevous kwargs during the merge.
        """
        # https://peps.python.org/pep-0584/
        # https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression-in-python
        # merge dictionary python 3.9 |= operator, python 3.8 {**d1, **d2}
        for kwargs in self.args_list:
            # kwargs override the previous self.kwargs
            self.kwargs = {**self.kwargs, **kwargs}
        return self.kwargs

    def __repr__(self) -> str:
        return self.kwargs

    def __str__(self) -> str:
        return self.__repr__()


class ModelInfo:
    def __init__(self, model_family: str, inst_msg_begin: str, inst_msg_end: str):
        self.model_family = model_family
        self.inst_msg_begin = inst_msg_begin
        self.inst_msg_end = inst_msg_end

    def __repr__(self) -> str:
        # output the raw string of the object
        # {value!r} calls the repr() method of the value to show the raw string inside the f string method
        return f"ModelInfo(model_family={self.model_family!r}, inst_msg_begin={self.inst_msg_begin!r}, inst_msg_end={self.inst_msg_end!r})"

    def __str__(self) -> str:
        return self.__repr__()


class ModelCatalog:
    """
    mistral instruction example:
    https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2
    llama2 instruction examples:
    https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF
    """

    META_FAMILY = "meta-llama"
    MISTRAL_FAMILY = "mistralai"
    INST_MSG_MAP = {
        MISTRAL_FAMILY: """<s>[INST] You are a helpful, respectful and honest assistant.
Always answer as helpfully as possible using the context text provided.
Your answers should only answer the question once and not have any text after the answer is done.\n
If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.
If you don't know the answer to a question, please don't share false information. Just return \"</s>\"
""",
        META_FAMILY: """[INST]<<SYS>>You are a helpful, respectful and honest assistant.
Always answer as helpfully as possible using the context text provided.
Your answers should only answer the question once and not have any text after the answer is done.\n
If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.
If you don't know the answer to a question, please don't share false information.<</SYS>>
""",
    }
    INST_MSG_ENDING = "[/INST]"

    @classmethod
    def get_model_info(cls, model_name) -> "ModelInfo":
        """
        Args:
            model_name: the model name such as mistralai/Mistral-7B-Instruct-v0.2 from huggingface
        """
        if model_name.startswith(cls.META_FAMILY):
            model_info = ModelInfo(
                cls.META_FAMILY, cls.INST_MSG_MAP[cls.META_FAMILY], cls.INST_MSG_ENDING
            )
        elif model_name.startswith(cls.MISTRAL_FAMILY):
            model_info = ModelInfo(
                cls.MISTRAL_FAMILY,
                cls.INST_MSG_MAP[cls.MISTRAL_FAMILY],
                cls.INST_MSG_ENDING,
            )
        else:
            model_info = ModelInfo("", "", "")
        return model_info


class PromptHelper:
    def __init__(
        self,
        model_info: ModelInfo = ModelCatalog.get_model_info(
            ModelCatalog.MISTRAL_FAMILY
        ),
    ):
        self.model_info = model_info

    def gen_prompt(self, query: str) -> str:
        if query is not None or len(query) > 0:
            prompt = f"""{self.model_info.inst_msg_begin}\n{query}\n{self.model_info.inst_msg_end}"""
        else:
            prompt = (
                f"""{self.model_info.inst_msg_begin}{self.model_info.inst_msg_end}"""
            )
        return prompt

    def get_inst_msg(self) -> str:
        return self.gen_prompt("")
