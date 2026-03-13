import numpy as np

from modeling.calibrators import IsotonicCalibrator


class ZIsotonicBaseline:
    def __init__(self) -> None:
        self.calibrator = IsotonicCalibrator()

    def fit(self, z: np.ndarray, y_cont: np.ndarray) -> None:
        self.calibrator.fit(z, y_cont)

    def predict_p_cont(self, z: np.ndarray) -> np.ndarray:
        return self.calibrator.predict(z)
