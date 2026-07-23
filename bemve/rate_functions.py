import numpy as np


def linear(t: float) -> float:
    return t


def smooth(t: float) -> float:
    # Smooth step (S-curve interpolation)
    return 3 * t**2 - 2 * t**3


def there_and_back(t: float) -> float:
    return 2 * t if t < 0.5 else 2 * (1 - t)


def bounce(t: float) -> float:
    # Simple bounce effect
    return abs(np.sin(t * np.pi * 3)) * t