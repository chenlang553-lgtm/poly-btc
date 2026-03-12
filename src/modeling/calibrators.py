import numpy as np
from sklearn.isotonic import IsotonicRegression


class IsotonicCalibrator:
    def __init__(self) -> None:
        self.model = IsotonicRegression(y_min=0.0, y_max=1.0, out_of_bounds="clip")

    def fit(self, score: np.ndarray, y: np.ndarray) -> None:
        self.model.fit(score, y)

    def predict(self, score: np.ndarray) -> np.ndarray:
        return self.model.predict(score)
