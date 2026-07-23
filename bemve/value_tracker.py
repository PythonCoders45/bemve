class ValueTracker:
    """Stores a scalar float value that can be animated or tracked by updaters."""

    def __init__(self, value: float = 0.0):
        self._value = float(value)

    def get_value(self) -> float:
        return self._value

    def set_value(self, value: float):
        self._value = float(value)
        return self

    def increment_value(self, delta: float):
        self._value += delta
        return self


class TrackerAnimation:
    """Animates a ValueTracker from its current value to a target value."""

    def __init__(self, tracker: ValueTracker, target_value: float, duration: float = 1.0):
        self.tracker = tracker
        self.start_value = tracker.get_value()
        self.target_value = target_value
        self.duration = duration

    def update(self, alpha: float):
        new_val = self.start_value + (self.target_value - self.start_value) * alpha
        self.tracker.set_value(new_val)
