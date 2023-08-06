"""
check mte2 bound optimization
"""
import logging
from typing import List

from asight.common.profiling.summary import OpInfo
from asight.optimizer.operator_checker.operator_checker import OperatorChecker

logger = logging.getLogger()


class Mte2BoundChecker(OperatorChecker):
    """
    mte2 bound checker
    """
    _CHECKER = "mte2 bound"
    _PROBLEM = "mte2 bound"
    _description = "mte2 ratio is more than 80%"
    _SUGGESTION = [OperatorChecker.SUB_GRAPH_TUNE_SUGGESTION]
    _MIN_TOTAL_DURATION_RATIO = 0.3
    _MIN_TASK_DURATION_RATIO = 0.1
    _MIN_TASK_DURATION = float('inf')
    _ITEMS = [
        "op_name", "op_type", "task_type", "task_duration", "mte2_ratio", "block_dim", "input_shapes",
        "input_data_types", "input_formats", "output_shapes", "output_data_types", "output_formats"
    ]

    _op_list: List[OpInfo] = []
    _tune_op_list: List[str] = []

    def _check_data(self, data):
        if not self._check_summary(data):
            return False
        summary = data.summary
        op_info = summary.op_list[0]
        if not op_info.has_attr("mte2_ratio"):
            logger.warning(self.SKIP_CHECK_MSG, self._CHECKER, "mte2_ratio in op summary")
            return False
        return True

    def _check_operator(self, op_info) -> bool:
        if op_info.task_type == "AI_CPU":
            return False
        ratio = self.get_ratio(op_info, "mte2_ratio")
        if not ratio:
            return False
        if ratio >= 0.8:
            return True
        return False

    def get_tune_op_list(self):
        return None


def register(checker):
    """
    register mte2 bound checker to operator checker
    :param checker: checker
    """
    checker[Mte2BoundChecker] = Mte2BoundChecker()
