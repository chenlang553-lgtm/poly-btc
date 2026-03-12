from typing import Literal

from modeling.baseline_z import ZIsotonicBaseline
from modeling.lgbm_model import LgbmIsotonicModel
from modeling.logistic_model import LogisticIsotonicModel

ModelName = Literal["z_isotonic", "logistic_isotonic", "lgbm_isotonic"]


def create_model(name: ModelName) -> object:
    if name == "z_isotonic":
        return ZIsotonicBaseline()
    if name == "logistic_isotonic":
        return LogisticIsotonicModel()
    return LgbmIsotonicModel()
