import builtins
import importlib
import sys
import unittest
from unittest import mock


class WhisperImportTest(unittest.TestCase):
    def test_missing_whisper_does_not_crash_module_import(self):
        original_import = builtins.__import__

        def fake_import(name, *args, **kwargs):
            if name == "whisper":
                raise ImportError("DLL load failed while importing numba")
            return original_import(name, *args, **kwargs)

        with mock.patch("builtins.__import__", side_effect=fake_import):
            sys.modules.pop("services.whisper_service", None)
            module = importlib.import_module("services.whisper_service")

        self.assertTrue(hasattr(module, "transcribir_audio"))
        self.assertIsNone(module.whisper)


if __name__ == "__main__":
    unittest.main()
