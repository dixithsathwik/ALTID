from deepface import DeepFace

def match_faces(id_image_path, selfie_image_path):
    try:
        result = DeepFace.verify(id_image_path, selfie_image_path, enforce_detection=False)
        return result.get('verified', False)
    except Exception as e:
        print(f"Face match error: {e}")
        return False 