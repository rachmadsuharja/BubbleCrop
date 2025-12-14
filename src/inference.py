import cv2
import os
import json
import zipfile
import shutil
import tempfile
from pathlib import Path
from ultralytics import YOLO

class BubbleCropper:
    def __init__(
        self,
        model_path="../models/best.pt",
        config_path="../config.json",
        classes_path="../classes.json",
    ):
        self.model = YOLO(model_path)

        with open(config_path, "r") as f:
            self.config = json.load(f)

        with open(classes_path, "r") as f:
            self.classes = json.load(f)

        self.bubble_class_id = None
        for k, v in self.classes.items():
            if v == "bubble":
                self.bubble_class_id = int(k)
                break

        if self.bubble_class_id is None:
            raise ValueError("'Bubble' class not found in classes file")

    def get_default_output_dir(self):
        try:
            documents_path = Path.home() / "Documents"
            default_dir = documents_path / "BubbleCrop"
            
            default_dir.mkdir(parents=True, exist_ok=True)
            return str(default_dir)
        except Exception as e:
            print(f"Warning: Could not set default output to Documents/BubbleCrop. Using './output'. Error: {e}")
            return "output"


    def process(self, input_path, output_dir=None):
        if output_dir is None:
            output_dir = self.get_default_output_dir()
            
        if not os.path.exists(input_path):
            raise ValueError(f"Input path not found: {input_path}")

        if input_path.lower().endswith(".zip"):
            print(f"Processing ZIP file: {input_path}")
            self._process_zip(input_path, output_dir)
        else:
            print(f"Processing single image: {input_path}")
            self._process_single_image(input_path, output_dir)

    def _process_zip(self, zip_path, main_output_dir):
        zip_name = Path(zip_path).stem
        
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.webp')
            image_files = []

            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.startswith('.') or '__MACOSX' in root:
                        continue
                        
                    if file.lower().endswith(valid_extensions):
                        full_path = os.path.join(root, file)
                        image_files.append(full_path)
            
            image_files.sort(key=lambda x: os.path.basename(x))

            if not image_files:
                print(f"--- Warning: No valid images found in ZIP: {zip_path} ---")
                return

            print(f"--- Found {len(image_files)} images. Starting processing... ---")

            processed_count = 0
            
            for file_path in image_files:
                filename = os.path.basename(file_path)
                
                page_name = Path(filename).stem
                zip_output_dir = os.path.join(main_output_dir, zip_name)

                self._process_single_image(
                    file_path,
                    zip_output_dir,
                    prefix = f"{Path(file_path).parent.name}_{Path(filename).stem}"
                )

                processed_count += 1

            print(f"--- Finished. Total {processed_count} images processed from this ZIP. ---")

    def _process_single_image(self, image_path, output_dir, prefix=None):
        img = cv2.imread(image_path)
        if img is None:
            print(f"Warning: Failed to read image: {image_path}")
            return

        h, w, _ = img.shape

        results = self.model(
            img,
            conf=self.config.get("confidence", 0.4),
            device="cpu",
            verbose=False
        )[0]

        boxes = []
        for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
            if int(cls) == self.bubble_class_id:
                x1, y1, x2, y2 = map(int, box)
                boxes.append((x1, y1, x2, y2))

        if not boxes:
            print(f"No bubbles detected in {os.path.basename(image_path)}")
            return

        boxes.sort(key=lambda b: b[1])

        os.makedirs(output_dir, exist_ok=True)

        padding = self.config.get("padding", 0)
        
        top_y = max(0, boxes[0][1] - padding) 

        for i, box in enumerate(boxes):
            bottom_y = min(h, box[3] + padding)
            
            if top_y >= bottom_y:
                continue

            crop = img[top_y:bottom_y, 0:w]

            output_format = self.config.get('output_format', 'jpg')
            if prefix:
                output_filename = f"{prefix}_bubble_{i + 1}.{output_format}"
            else:
                output_filename = f"bubble_{i + 1}.{output_format}"

            output_path = os.path.join(output_dir, output_filename)
            
            cv2.imwrite(output_path, crop)

        print(f"Saved {len(boxes)} bubbles to '{output_dir}'")