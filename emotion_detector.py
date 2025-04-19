from transformers import pipeline

# Load the emotion classification model once at startup
def load_emotion_classifier(device=0):
    """
    Load the pre-trained emotion classification model.

    Args:
    - device (int): The device to run the model on. Defaults to GPU (device=0).
      Falls back to CPU if GPU is not available.

    Returns:
    - pipeline: The pre-trained emotion classification pipeline.
    """
    return pipeline(
        "text-classification",
        model="nateraw/bert-base-uncased-emotion",
        device=device  # Use GPU if available, otherwise fallback to CPU
    )

# Initialize the emotion classifier at the start
emotion_classifier = load_emotion_classifier()

def detect_emotion(text):
    """
    Detect the emotion in the given text using the pre-trained model.
    
    Args:
    - text (str): The input text to classify the emotion of.
    
    Returns:
    - tuple: A tuple containing the detected emotion and the confidence score.
      The emotion is returned as a lowercase string, and the confidence score as a float.
    """
    if not text or not text.strip():
        return "unknown", 0.0  # Return default if the text is empty or just whitespace
    
    try:
        # Get the emotion and confidence score from the classifier
        result = emotion_classifier(text)[0]
        emotion = result['label'].lower()
        confidence = float(result['score'])
        return emotion, confidence
    except Exception as e:
        print(f"Error detecting emotion: {e}")
        return "unknown", 0.0  # Default in case of error

# Example usage:
# emotion, confidence = detect_emotion("I feel so happy today!")
# print(f"Detected emotion: {emotion} with confidence: {confidence}")
