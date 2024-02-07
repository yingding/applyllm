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
    def __init__(self, quantized: bool = False, model_config: dict = {}, bnb_config: dict = {}, **kwargs):
        self.quantized = quantized
        self.model_config = model_config
        self.bnb_config = bnb_config
        # self.bnb_config = kwargs.get('bnb_config', None)
        # self.model_config = kwargs.get('model_config', None)

    def __repr__(self):
        # add !r to format the string representation of the object
        return f"LocalCausalLMConfig(quantized={self.quantized!r}, model_config={self.model_config!r}, bnb_config={self.bnb_config!r})"
    
    def __str__(self):
        return repr(self)