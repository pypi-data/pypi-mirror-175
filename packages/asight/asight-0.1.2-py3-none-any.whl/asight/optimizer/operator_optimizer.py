"""
operator optimizer module
"""
from asight.datasets.profiling_dataset import ProfilingDataset
from asight.optimizer.optimizer import Optimizer
from asight.result.result import DetailRecord, OptimizeResult, Result
from asight.util.common import load_module


class OperatorOptimizer(Optimizer):
    """
    operator optimizer
    """

    def __init__(self) -> None:
        self.checker = load_module("optimizer/operator_checker")
        self.result = None

    @Optimizer.check_data((ProfilingDataset.get_key(), ))
    def optimize(self, data) -> Result:
        """
        optimize operator
        :param data: input datasets
        :return: result
        """
        self.result = OptimizeResult()
        profiling_data = data[ProfilingDataset.get_key()]
        self._check(profiling_data)
        return self.result

    def _check(self, profiling_data):
        for _, checker in self.checker.items():
            if checker.check(profiling_data):
                # add record
                record = checker.make_record(profiling_data)
                self.result.add(record)
                # add details
                details = checker.get_details()
                if details:
                    for detail in details:
                        self.result.add_detail(checker.get_name(), DetailRecord(detail))
                # add tune op list
                tune_op_list = checker.get_tune_op_list()
                if tune_op_list:
                    self.result.add_tune_op_list(tune_op_list)


def register(optimizers):
    """
    register operator optimizer to optimizers
    :param optimizer: optimizer
    """
    optimizers[OperatorOptimizer] = OperatorOptimizer()
