import numpy as np
from sklearn.linear_model import LogisticRegression

from modeling.calibrators import IsotonicCalibrator


class LogisticIsotonicModel:
    def __init__(self) -> None:
        self.model = LogisticRegression(max_iter=200)
        self.calibrator = IsotonicCalibrator()

    def fit(self, x_train: np.ndarray, y_train: np.ndarray, x_cal: np.ndarray, y_cal: np.ndarray) -> None:
        self.model.fit(x_train, y_train)
        raw_cal = self.model.predict_proba(x_cal)[:, 1]
        self.calibrator.fit(raw_cal, y_cal)

    def predict_raw(self, x: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(x)[:, 1]

    def predict_p_cont(self, x: np.ndarray) -> np.ndarray:
        return self.calibrator.predict(self.predict_raw(x))
