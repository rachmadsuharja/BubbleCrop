# Chat Bubble Auto Cropper

A **cross-platform desktop application (Arch Linux & Windows)** for **automatically detecting and cropping chat bubbles** from a single conversation image using **YOLO (Object Detection)**.

This app is designed specifically for **comic workflows, chat stories, dataset generation, and creative content**, producing **cumulative (step-by-step) crops**.

---

## Key Features

- Automatic detection of chat elements using YOLO

  - Text bubbles
  - Stickers
  - Photos

- **Cumulative Crop**

  - `bubble1.jpg` → first bubble only
  - `bubble2.jpg` → bubble 1 + 2
  - and so on

- Full-width image preserved (no horizontal cropping)
- Easy configuration via `config.json`
- AI model separated from application logic (easy to upgrade)
- Desktop GUI (PySide6)
- Ready to be bundled into a standalone binary (no Python required for users)

---

## Project Structure

```
BubbleCrop/
├── src/
│   ├── app.py          # GUI entry point
│   └── inference.py    # YOLO logic + cropping
├── models/
│   └── best.pt         # Trained YOLO model
├── assets/             # Icons / UI assets
├── config.json         # Runtime configuration
├── classes.json        # YOLO class mapping
├── requirements.txt    # Dependencies (DEV only)
└── README.md
```

---

## How It Works

1. The user selects a chat screenshot or a zip (must include some screenshots inside)
2. YOLO detects chat bubble positions
3. Bubbles are sorted from top to bottom
4. The app performs **vertical cumulative cropping**
5. Outputs are saved as:

single image

```
bubble_1.jpg
bubble_2.jpg
bubble_3.jpg
...
```

or (zip)

```
DirName_bubble1.jpg
DirName_bubble2.jpg
DirName_bubble1.jpg
DirName_bubble2.jpg
...
```

---

## Configuration (`config.json`)

```json
{
  "confidence": 0.4,
  "padding": 8,
  "output_format": "jpg"
}
```

| Key           | Description              |
| ------------- | ------------------------ |
| confidence    | YOLO detection threshold |
| padding       | Extra crop margin (px)   |
| output_format | jpg / png                |

---

## Class Mapping (`classes.json`)

⚠️ **MUST match the class order used during YOLO training**

```json
{
  "0": "bubble",
  "1": "sticker",
  "2": "image"
}
```

---

## Development Setup (DEV Mode)

> For developers only — **not required for end users**

### 1. Create Virtual Environment

```bash
python -m venv venv
source ./venv/bin/activate      # Linux
venv\Scripts\activate           # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python ./src/app.py
```

---

## Application Bundling

### 🔹 Windows (EXE)

```bash
pyinstaller \
  --windowed \
  --add-data "models/best.pt;models" \
  src/app.py
```

Output:

```
dist/app.exe
```

---

### 🔹 Linux (Arch)

```bash
pyinstaller ./src/app.py --name BubbleCrop
```

Output:

```
dist/BubbleCrop/BubbleCrop
```

---

## Not Included in the Application

- Training dataset
- `runs/` directory
- YOLO label files
- Virtual environment (`venv`)

The application ships **only the trained model and inference logic**.

---

## Model Upgrade

YOLO models can be replaced without rebuilding the application:

```
models/
├── best_v1.pt
├── best_v2.pt
```

Update the path in `config.json` or code if needed.

---

## Tested On

- Arch Linux (x86_64)
- Windows 10 / 11

---

## Important Notes

- Builds **must be done on the target OS**
- Cross-compilation is not supported
- GPU is optional (CPU-only inference supported)

---

## License

MIT License

---

## Contributing

Pull requests and issues are welcome.

---

> Built for creative workflows and AI-assisted content generation.
