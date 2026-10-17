"""Poll readiness, then check real model inference. No third-party dependency."""

import argparse
import json
import time
import urllib.error
import urllib.request


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment")
    args = parser.parse_args()
    for attempt in range(30):
        try:
            with urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=2) as response:
                health = json.load(response)
            break
        except (urllib.error.URLError, TimeoutError, ConnectionError) as error:
            print(f"Waiting for service ({attempt + 1}/30): {type(error).__name__}: {error}")
            time.sleep(1)
    else:
        raise RuntimeError("Service never became ready")
    if args.environment:
        assert health["environment"] == args.environment
    payload = json.dumps(
        {"values": [14.23, 1.71, 2.43, 15.6, 127, 2.8, 3.06, 0.28, 2.29, 5.64, 1.04, 3.92, 1065]}
    ).encode()
    request = urllib.request.Request(
        "http://127.0.0.1:8000/predict", data=payload, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(request, timeout=5) as response:
        prediction = json.load(response)
    assert prediction["cultivar"] in [1, 2, 3]
    assert abs(sum(prediction["probabilities"]) - 1) < 1e-6
    print(json.dumps({"health": health, "prediction": prediction}, indent=2))


if __name__ == "__main__":
    main()
