import io
import json
import sys
import urllib.error
from http.client import RemoteDisconnected
from unittest.mock import patch

import pytest

from scripts.smoke import main


@pytest.mark.parametrize(
    "error",
    [
        urllib.error.URLError("connection refused"),
        TimeoutError("startup timeout"),
        ConnectionResetError("container port opened before server readiness"),
        RemoteDisconnected("server not ready"),
    ],
)
def test_smoke_retries_startup_transport_errors(monkeypatch, error):
    monkeypatch.setattr(sys, "argv", ["smoke.py"])
    health = io.StringIO(json.dumps({"status": "ok"}))
    prediction = io.StringIO(json.dumps({"cultivar": 1, "probabilities": [0.8, 0.1, 0.1]}))
    with (
        patch(
            "scripts.smoke.urllib.request.urlopen", side_effect=[error, health, prediction]
        ) as open_url,
        patch("scripts.smoke.time.sleep") as sleep,
    ):
        main()
    assert open_url.call_count == 3
    sleep.assert_called_once_with(1)


@pytest.mark.parametrize("error", [urllib.error.URLError("offline"), ConnectionResetError()])
def test_smoke_fails_if_container_never_becomes_ready(monkeypatch, error):
    monkeypatch.setattr(sys, "argv", ["smoke.py"])
    with (
        patch("scripts.smoke.urllib.request.urlopen", side_effect=error) as open_url,
        patch("scripts.smoke.time.sleep"),
        pytest.raises(RuntimeError, match="Service never became ready"),
    ):
        main()
    assert open_url.call_count == 30
