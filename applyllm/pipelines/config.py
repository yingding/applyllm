"""
Class for configuration of the pipeline, models and experiments for better tracking in one place.
"""

class ExperimentConfig:
    pass


class PipelineConfig:
    pass


class ModelConfig:
    """
    Example:

    kwargs = {
        "model_config": {
            "pretrained_model_name_or_path": model_name,
            "device": "cpu",
            # "device_map": "auto", # put to GPU if GPU is available
            "max_position_embeddings": MAX_LENGTH,
            "max_length": MAX_LENGTH,
        },
    }
    tokenizer_config = ModelConfig(**kwargs)
    tokenizer = AutoTokenizer.from_pretrained(
        **tokenizer_config.get_config(), 
        **token_kwargs,
    )
    """
    def __init__(self, model_config: dict = {}, **kwargs):
        self.model_config = model_config

    def get_config(self) -> dict:
        return self.model_config

    def __repr__(self):
        # add !r to format the string representation of the object
        return f"ModelConfig(model_config={self.model_config!r})"
    
    def __str__(self):
        return repr(self)
    

class LocalCausalLMConfig:
    """
    Example:
    base_lm_config = ModelConfig(
        model_config = {
            "pretrained_model_name_or_path": model_name,
            "device_map": "auto",
            # "max_memory": f"{int(torch.cuda.mem_get_info()[0]/1024**3)-2}GB",
        }
    )
    kwargs = {
        "quantized": True,
        "model_config": base_lm_config.get_config(),
        "quantization_config": {
            "quantization_config": transformers.BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type='nf4',
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=bfloat16
            )
        }
    }

    lm_config = LocalCausalLMConfig(**kwargs)

    model = AutoModelForCausalLM.from_pretrained(
      **lm_config.get_config(),
      **token_kwargs,  
    )
    """
    def __init__(self, quantized: bool = False, model_config: dict = {},  quantization_config: dict = {}, **kwargs):
        self.quantized = quantized
        self.model_config = model_config
        self.quantization_config = quantization_config

    def get_config(self) -> dict:
        if self.quantized:
            return {**self.model_config, **self.quantization_config}
        else:
            return self.model_config

    def __repr__(self):
        # add !r to format the string representation of the object
        return f"LocalCausalLMConfig(quantized={self.quantized!r}, model_config={self.model_config!r}, quantization_config={self.quantization_config!r})"
    
    def __str__(self):
        return repr(self)