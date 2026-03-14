from flask import Flask, render_template, request, jsonify, send_file
from deepface import DeepFace
from rembg import remove
from PIL import Image
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    file = request.files["image"]
    remove_bg = request.form.get("remove_bg")

    filename = str(uuid.uuid4()) + ".png"
    upload_path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(upload_path)

    try:

        result = DeepFace.analyze(
            img_path=upload_path,
            actions=["age"],
            enforce_detection=True
        )

        age = result[0]["age"]

        output_path = upload_path

        if remove_bg == "true":

            img = Image.open(upload_path).convert("RGBA")
            output = remove(img)

            new_name = "processed_" + filename
            output_path = os.path.join(OUTPUT_FOLDER, new_name)

            output.save(output_path)

        return jsonify({
            "age": age,
            "image": output_path
        })

    except Exception:
        return jsonify({"error": "No face detected"})


@app.route("/download")
def download():

    path = request.args.get("file")

    if not os.path.exists(path):
        return "File not found"

    response = send_file(path, as_attachment=True)

    try:
        os.remove(path)
    except:
        pass

    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    