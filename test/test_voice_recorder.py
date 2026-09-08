import unittest
from unittest import mock

from services import voice_recorder


class VoiceRecorderDeviceSelectionTest(unittest.TestCase):
    def test_selects_first_real_input_device(self):
        devices = [
            {"name": "Speakers", "max_input_channels": 0},
            {"name": "Micrófono USB", "max_input_channels": 1},
            {"name": "Headset", "max_input_channels": 1},
        ]

        with mock.patch("services.voice_recorder.sd.query_devices", return_value=devices):
            self.assertEqual(voice_recorder._seleccionar_dispositivo_entrada(), 1)


if __name__ == "__main__":
    unittest.main()
