import typing as t

import pandas as pd

from my_model import __version__ as _version
from my_model.config.core import config
from my_model.processing.data_manager import load_pipeline
from my_model.processing.validation import validate_inputs

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
_genero_pipe = load_pipeline(file_name=pipeline_file_name)


def make_prediction(
    input_data: pd.DataFrame,
):
    """Make a prediction using a saved model pipeline."""
    # HAY UN BUG EN EL DATAFRAME
    data = pd.DataFrame(input_data)
    #validated_data, errors = validate_inputs(input_data=data)
    #results = {"predictions": None, "version": _version, "errors": errors}
    #predictions = _genero_pipe.predict(data)
    #if not errors:
    #    predictions = _genero_pipe.predict(
    #        X=validated_data[config.model_config.features]
    #    )
    #    results = {
    #        "predictions": predictions,
    #        "version": _version,
    #        "errors": errors,
    #    }

    return _genero_pipe.predict(data)
