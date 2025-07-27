from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import replicate
import os

load_dotenv()

app = Flask(__name__)
replicate_client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    image = request.files.get("image")
    if not image:
        return jsonify({"error": "image is not uploaded."}), 400

    try:
        image_path = "input.png"
        image.save(image_path)

        output = replicate_client.run(
            "lucataco/anime-character-generator:1531004ee4c98894ab11f8a4ce6206099e732c1da15121987a8eef54828f0663",
            input={
                "image": open(image_path, "rb"),
                "prompt": "dog turned into anime girl"
            }
        )

        return jsonify({"result_url": output})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
