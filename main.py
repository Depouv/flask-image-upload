from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import ollama
# from PIL import Image
import io
import base64

app = Flask(__name__, template_folder="templates")


# Dossier où les uploads seront stockées
upload_folder = os.path.join('static', 'images')
 
app.config['UPLOAD_FOLDER'] = upload_folder

@app.route("/", methods=["GET"])
def home():
    # renvoie le fichier templates/image_render.html
    return render_template("image_render.html")

@app.route("/", methods=["POST"])
def upload_file():
    if "img" not in request.files:
        return "Aucune image reçue", 400

    file = request.files['img']

    if file.filename == "":
        return "Nom de fichier non valide", 400

    # Sécurisation du nom de fichier
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    # Sauvegarde de l'image
    file.save(filepath)



    # Appel à Ollama → génération de l’histoire
    
    
    with open(filepath, "rb") as img :
        response = ollama.chat(
        model='gemma3:4b',
        messages=[{
            'role': 'user',
            'content': "Tu es expert en histoire pour les enfants. Raconte une brève histoire de 100 mots pour enfants inspirée de cette image",
            'images': [img.read()],
            },],
        )
    app.logger.info(response)
    story = response['message']['content']
    # return render_template("image_render.html", img=filepath, story=story)


    # # On renvoie la même page mais avec l'image
    # # Flask sert automatiquement static/ donc on met le bon chemin
    # img_url = "/" + filepath

    return render_template("image_render.html", story=story)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



