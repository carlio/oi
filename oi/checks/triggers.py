from decimal import Decimal
import operator


class TriggerBase(object):

    def trigger(self, series):
        raise NotImplementedError


class AbsoluteValueTrigger(TriggerBase):

    def __init__(self, accumulator, comparison, threshold):
        self.accumulator = accumulator
        self.comparison = comparison
        self.threshold = threshold

    def trigger(self, series):
        return self.comparison(self.accumulator(series), self.threshold)


def abs_trigger(accumulator, comparison):
    def create(threshold):
        return AbsoluteValueTrigger(accumulator, comparison, threshold)
    return create


class DeviatedByTrigger(TriggerBase):

    def __init__(self, max_deviation):
        self.max_deviation = Decimal(max_deviation)

    def trigger(self, series):
        if len(series) == 0:
            return False

        avg = sum(series) / len(series)
        max_value = max(series)
        min_value = min(series)

        if max_value > (avg + (avg * self.max_deviation)):
            return True

        if min_value < (avg - (avg * self.max_deviation)):
            return True

        return False


TRIGGERS = {
    'deviated': (DeviatedByTrigger,
                 'Triggers if the average value of a series has deviated by more than the (average * argument)'),
    'max_above': (abs_trigger(max, operator.gt),
                  'Triggers if the maximum value is above the argument'),
    'min_above': (abs_trigger(min, operator.gt),
                  'Triggers if the minimum value is above the argument'),
    'max_below': (abs_trigger(max, operator.lt),
                  'Triggers if the maximum value is below the argument'),
    'min_below': (abs_trigger(min, operator.lt),
                  'Triggers if the minimum value is below the argument'),
    'total_above': (abs_trigger(sum, operator.gt),
                    'Triggers if the total of values in the series is above the argument'),
    'total_below': (abs_trigger(sum, operator.lt),
                    'Triggers if the total of values in the series is below the argument')

}
