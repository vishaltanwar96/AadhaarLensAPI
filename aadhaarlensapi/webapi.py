from aadhaar.secure_qr import extract_data
from aadhaar.secure_qr.exceptions import MalformedDataReceived
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/api/extract/", methods=["POST"])
def extract_api():
    data = request.json.get("data")
    if not data:
        return jsonify({"status": "fail", "error": "Please send the data"}), 400
    try:
        data = int(data)
    except ValueError:
        return (
            jsonify(
                {
                    "status": "fail",
                    "error": "Conversion to int not possible, Please send valid data",
                }
            ),
            400,
        )
    try:
        extracted_data = extract_data(data)
    except MalformedDataReceived:
        return jsonify({"status": "fail", "error": "Please send valid data"}), 400
    return jsonify({"status": "ok", "response": extracted_data.to_dict()}), 200


if __name__ == "__main__":
    app.run()
