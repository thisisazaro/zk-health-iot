from flask import Flask, request, jsonify
import json, subprocess

app = Flask(__name__)

@app.route("/pulse", methods=["POST"])
def receive_pulse():
    data = request.json
    pulse = int(data.get("pulse"))
    threshold = 80
    alert = 1 if pulse > threshold else 0

    with open("../circom/input.json", "w") as f:
        json.dump({"pulse": pulse, "threshold": threshold, "alert": alert}, f)

    subprocess.run(["bash", "generate_proof.sh"], cwd="../circom")

    return jsonify({"status": "proof generated", "pulse": pulse, "alert": alert})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
