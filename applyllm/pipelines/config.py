"""
Class for configuration of the pipeline, models and experiments for better tracking in one place.
"""

class ExperimentConfig:
    pass

class ModelConfig:
    pass

class PipelineConfig:
    pass 


class LocalCausalLMConfig:
    def __init__(self, quantized: bool = False, model_config: dict = {},  quantization_config = None, **kwargs):
        self.quantized = quantized
        self.model_config = model_config
        self.quantization_config = quantization_config
        # self.bnb_config = kwargs.get('bnb_config', None)
        # self.model_config = kwargs.get('model_config', None)

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