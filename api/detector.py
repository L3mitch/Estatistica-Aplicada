import os
import pickle # Lê e armazena a lista de encodings
from collections import Counter # Conta o número de ocorrências de um valor
from pathlib import Path # Manipula caminhos de arquivos

import face_recognition # Reconhece faces em imagens
from PIL import Image, ImageDraw # Cria e edita imagens

api_path = ""
if os.environ.get("FLASK_DEBUG") == '1':
    api_path = "api/"

DEFAULT_ENCODINGS_PATH = Path(api_path + "output/encodings.pkl")
BOUNDING_BOX_COLOR = "blue"
TEXT_COLOR = "white"

# Create directories if they don't already exist
Path(api_path + "training").mkdir(exist_ok=True)
Path(api_path + "output").mkdir(exist_ok=True)
Path(api_path + "match").mkdir(exist_ok=True)


def encode_new_face(
    name: str,
    model: str = "hog",
    encodings_location: Path = DEFAULT_ENCODINGS_PATH,
) -> None:
    """
    Given a new face, add it to the known encodings.
    """
    if encodings_location.exists() and encodings_location.stat().st_size > 0:
        with encodings_location.open(mode="rb") as f:
            loaded_encodings = pickle.load(f)
    else:
        loaded_encodings = {"names": [], "encodings": []}
    
    names = loaded_encodings["names"]
    encodings = loaded_encodings["encodings"]

    for filepath in Path(api_path + "training").glob(f"{name}/*"):
        name = filepath.parent.name
        image = face_recognition.load_image_file(filepath)
        face_locations = face_recognition.face_locations(image, model=model)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        for encoding in face_encodings:
            names.append(name)
            encodings.append(encoding)
    
    name_encodings = {"names": names, "encodings": encodings}
    with encodings_location.open(mode="wb") as f:
        pickle.dump(name_encodings, f)
    return True
 
def match_face(
    match_name: str,
    image_id: str,
    model: str = "hog",
    encodings_location: Path = DEFAULT_ENCODINGS_PATH,
) -> None:
    """
    Given an image and a name, checks if the face in the image matches the name.
    """
    with encodings_location.open(mode="rb") as f:
        loaded_encodings = pickle.load(f)
    filepath = Path(api_path + "match") / f"{image_id}.jpg"
    input_image = face_recognition.load_image_file(filepath)

    input_face_locations = face_recognition.face_locations(
        input_image, model=model
    )
    input_face_encodings = face_recognition.face_encodings(
        input_image, input_face_locations
    )

    #pillow_image = Image.fromarray(input_image)
    #draw = ImageDraw.Draw(pillow_image)

    for bounding_box, unknown_encoding in zip(
        input_face_locations, input_face_encodings
    ):
        name = _recognize_face(unknown_encoding, loaded_encodings)
        os.remove(filepath)
        if name == match_name:
            return True
        elif name == None:
            return False
        else:
            # _display_face(draw, bounding_box, name + "não é " + match_name)
            return False

    #del draw
    #pillow_image.show()

def recognize_face(
    image_id: str,
    model: str = "hog",
    encodings_location: Path = DEFAULT_ENCODINGS_PATH,
) -> None:
    """
    Given an image and a name, checks if the face in the image matches the name.
    """
    with encodings_location.open(mode="rb") as f:
        loaded_encodings = pickle.load(f)
    filepath = Path(api_path + "match") / f"{image_id}.jpg"
    input_image = face_recognition.load_image_file(filepath)

    input_face_locations = face_recognition.face_locations(
        input_image, model=model
    )
    input_face_encodings = face_recognition.face_encodings(
        input_image, input_face_locations
    )

    pillow_image = Image.fromarray(input_image)
    draw = ImageDraw.Draw(pillow_image)

    for bounding_box, unknown_encoding in zip(
        input_face_locations, input_face_encodings
    ):
        name = _recognize_face(unknown_encoding, loaded_encodings)
        if not name:
            name = "Unknown"
        if not bounding_box:
            _display_face(draw, bounding_box, name)

    os.remove(filepath)
    print(image_id," É a foto do " , name)
    del draw
    pillow_image.show()
    return name

def _recognize_face(unknown_encoding, loaded_encodings):
    """
    Given an unknown encoding and all known encodings, find the known
    encoding with the most matches.
    """
    boolean_matches = face_recognition.compare_faces(
        loaded_encodings["encodings"], unknown_encoding
    )
    votes = Counter(
        name
        for match, name in zip(boolean_matches, loaded_encodings["names"])
        if match
    )
    if votes:
        return votes.most_common(1)[0][0]


def _display_face(draw, bounding_box, name):
    """
    Draws bounding boxes around faces, a caption area, and text captions.
    """
    top, right, bottom, left = bounding_box
    draw.rectangle(((left, top), (right, bottom)), outline=BOUNDING_BOX_COLOR)
    text_left, text_top, text_right, text_bottom = draw.textbbox(
        (left, bottom), name
    )
    draw.rectangle(
        ((text_left, text_top), (text_right, text_bottom)),
        fill=BOUNDING_BOX_COLOR,
        outline=BOUNDING_BOX_COLOR,
    )
    draw.text(
        (text_left, text_top),
        name,
        fill=TEXT_COLOR,
    )



# Encode new face
# Precisa que seja adicionado um diretório com o nome da pessoa na pasta training
# Exemplo: /training/michel_jackson
# Recebe o nome da pessoa a ser adicionada
# Adiciona a pessoa na lista de encodings

# encode_new_face("michel_jackson", model="hog")

# Match Face
# Precisa que seja adicionada a imagem a testar na pasta match, com o nome igual ao id que será passado
# Exemplo: /match/86.jpg
# Recebe o nome da pessoa a ser comparada e o id da imagem a ser comparada
# Retorna True se a pessoa na imagem é a mesma que a pessoa passada
# Retorna False se a pessoa na imagem não é a mesma que a pessoa passada

# print(match_face("michel_jackson", "86", model="hog"))



