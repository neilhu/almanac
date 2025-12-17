import io
import os
import contextlib
from unittest import mock
from datetime import date

# Helper to dynamically load the getTimes function from almanac.py
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def load_getTimes():
    path = os.path.join(BASE_DIR, "almanac.py")
    with open(path, "r") as f:
        source = f.read()
    start = source.index("def getTimes")
    end = source.index("def weather")
    func_code = source[start:end]
    namespace = {"date": date, "Astral": object}
    exec(func_code, namespace)
    return namespace["getTimes"]

getTimes = load_getTimes()

class DummyCity:
    def sun(self, date=None, local=True):
        return {
            "dawn": "2023-01-01 06:00:00-04:00",
            "sunrise": "2023-01-01 07:00:00-04:00",
            "noon": "2023-01-01 12:00:00-04:00",
            "sunset": "2023-01-01 18:00:00-04:00",
            "dusk": "2023-01-01 19:00:00-04:00",
        }

    def moon_phase(self, date=None):
        return 21

class DummyAstral:
    def __init__(self):
        self.solar_depression = None

    def __getitem__(self, name):
        return DummyCity()


def test_last_quarter_output():
    with mock.patch.dict(getTimes.__globals__, {"Astral": DummyAstral}):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            getTimes("Boston")
        output = buf.getvalue()
    assert "Moon:    Last quarter" in output
