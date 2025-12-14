from src.inference import BubbleCropper

cropper = BubbleCropper(
    model_path="models/best.pt",
    config_path="config.json",
    classes_path="classes.json"
)

cropper.process(
    input_path="file.zip"
)
