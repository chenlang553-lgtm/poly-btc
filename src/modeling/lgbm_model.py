import numpy as np
from lightgbm import LGBMClassifier

from modeling.calibrators import IsotonicCalibrator


class LgbmIsotonicModel:
    def __init__(self) -> None:
        self.model = LGBMClassifier(n_estimators=200, learning_rate=0.05, num_leaves=31)
        self.calibrator = IsotonicCalibrator()

    def fit(self, x_train: np.ndarray, y_train: np.ndarray, x_cal: np.ndarray, y_cal: np.ndarray) -> None:
        self.model.fit(x_train, y_train)
        raw_cal = self.model.predict_proba(x_cal)[:, 1]
        self.calibrator.fit(raw_cal, y_cal)

    def predict_p_cont(self, x: np.ndarray) -> np.ndarray:
        raw = self.model.predict_proba(x)[:, 1]
        return self.calibrator.predict(raw)
