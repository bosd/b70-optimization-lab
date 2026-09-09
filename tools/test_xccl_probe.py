"""Exercise the actual health probe without requiring a GPU runtime."""
import os
from pathlib import Path
import runpy
import sys
from types import ModuleType
import unittest
from unittest.mock import Mock, patch


class XcclProbeTest(unittest.TestCase):
    def run_probe(self, result):
        torch = ModuleType("torch")
        dist = ModuleType("torch.distributed")
        torch.distributed = dist
        torch.xpu = Mock()
        torch.float16 = "float16"
        tensor = Mock()
        tensor.cpu.return_value = [result]
        torch.ones = Mock(return_value=tensor)
        dist.init_process_group = Mock()
        dist.barrier = Mock()
        dist.all_reduce = Mock()
        dist.get_world_size = Mock(return_value=2)
        dist.destroy_process_group = Mock()
        with patch.dict(sys.modules, {"torch": torch, "torch.distributed": dist}), \
             patch.dict(os.environ, {"RANK": "1", "LOCAL_RANK": "1"}), \
             patch.object(sys, "argv", ["xccl_probe.py", "allreduce"]):
            module = runpy.run_path(str(Path(__file__).with_name("xccl_probe.py")))
            module["main"]()
        torch.xpu.set_device.assert_called_once_with(1)
        dist.all_reduce.assert_called_once_with(tensor)

    def test_correct_collective_result(self):
        self.run_probe(2)

    def test_unreduced_or_corrupt_result_fails(self):
        for result in (1, 0, float("nan")):
            with self.subTest(result=result), self.assertRaisesRegex(RuntimeError, "allreduce returned"):
                self.run_probe(result)


if __name__ == "__main__":
    unittest.main()
