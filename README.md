# Batch File Renamer (GUI)

A powerful, lightweight **Python Tkinter** application for batch renaming files with complete control over file order and customizable naming patterns.

Unlike basic file renamers, this tool lets you **drag and reorder files**, preview the output before renaming, and place the increment counter **anywhere** in the filename.

No external libraries are required—Tkinter is included with standard Python.

---

## 📑 Table of Contents

- [✨ Features](#-features)
- [🖼️ Screenshot](#-screenshot)
- [📋 Requirements](#-requirements)
- [⬇️ Installation](#️-installation)
- [▶️ Run](#️-run)
- [📖 How to Use](#-how-to-use)
- [🔢 Supported Placeholders](#-supported-placeholders)
- [👀 Live Preview](#-live-preview)
- [📂 Queue Multiple Folders](#-queue-multiple-folders)
- [🛡️ Safety Features](#️-safety-features)
- [💡 Example](#-example)
- [📁 Project Structure](#-project-structure)
- [🚀 Future Improvements](#-future-improvements)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👤 Author](#-author)

---

# ✨ Features

- 📁 Rename files in one or multiple folders
- 🔢 Custom numbering with flexible placeholders
- 🔠 Alphabetic sequences (`a`, `b`, `c`, ..., `aa`, `ab`, ...)
- 🔡 Prefix support (`a1`, `A01`, etc.)
- 🎯 Place the counter anywhere in the filename
- 👀 Live preview before renaming
- 🖱️ Drag & Drop to arrange file order
- ⬆️ Move files up or down manually
- 📅 Sort by:
  - Name (A–Z / Z–A)
  - Date Modified
  - Date Created
- 📋 Queue multiple folders
- 📝 Detailed operation log
- ⚠️ Filename validation
- 🚫 Collision-safe renaming using temporary filenames

---

# 🖼️ Screenshot

<p align="center">
<img src="https://github.com/user-attachments/assets/4c27ef90-86a1-4a5b-85f1-3bd7c2011327" width="900">
</p>

---

# 📋 Requirements

- Python **3.8+**
- Tkinter (comes with Python)
- Windows / Linux / macOS

Check your Python version:

```bash
python --version
```

or

```bash
py --version
```

---

# ⬇️ Installation

Clone the repository

```bash
git clone https://github.com/jikokoutei/renamed.git
```

Open the project

```bash
cd renamed
```

(Optional but Recommended) Create a virtual environment

```bash
python -m venv .venv
```

Activate it

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

No additional dependencies are required.

---

# ▶️ Run

```bash
python main.py
```

or

```bash
py main.py
```

---

# 📖 How to Use

## Step 1 — Select Folder

- Click **Browse**
- Choose the folder containing your files
- Select a quick sort option
- Click **Load Files**

---

## Step 2 — Arrange File Order

Drag files into the exact order you want.

You can also use:

- Move Up
- Move Down

The first file receives the first number.

---

## Step 3 — Enter Name Pattern

Place the numbering placeholder inside **{}**

Example

```text
Photo_{001}
```

Output

```text
Photo_001.jpg
Photo_002.jpg
Photo_003.jpg
```

---

```text
Vacation_{01}_Beach
```

Output

```text
Vacation_01_Beach.jpg
Vacation_02_Beach.jpg
```

---

```text
IMG-{a1}
```

Output

```text
IMG-a1.png
IMG-a2.png
IMG-a3.png
```

---

```text
Document_{A01}
```

Output

```text
Document_A01.pdf
Document_A02.pdf
```

---

```text
File_{a}
```

Output

```text
File_a.txt
File_b.txt
File_c.txt
...
File_z.txt
File_aa.txt
File_ab.txt
```

---

# 🔢 Supported Placeholders

| Placeholder | Output |
|-------------|--------|
| `{1}` | 1,2,3... |
| `{01}` | 01,02,03... |
| `{001}` | 001,002,003... |
| `{a1}` | a1,a2,a3... |
| `{A01}` | A01,A02,A03... |
| `{a}` | a,b,c...z,aa,ab... |

---

# 👀 Live Preview

The application automatically previews the first few output filenames before any files are renamed.

Example

```text
Vacation_001_Beach.jpg
Vacation_002_Beach.jpg
Vacation_003_Beach.jpg
```

---

# 📂 Queue Multiple Folders

You can rename several folders in one operation.

1. Load Folder
2. Arrange files
3. Enter pattern
4. Click **Add To Queue**
5. Repeat
6. Click **Rename All Queued Folders**

---

# 🛡️ Safety Features

- Prevents invalid filenames
- Detects malformed placeholders
- Warns when numbering is omitted
- Uses temporary filenames to avoid conflicts
- Confirmation dialog before renaming
- Detailed operation log

---

# 💡 Example

Original

```text
IMG_5342.jpg
IMG_1234.jpg
IMG_8910.jpg
```

After arranging

```text
IMG_8910.jpg
IMG_5342.jpg
IMG_1234.jpg
```

Pattern

```text
Vacation_{001}
```

Result

```text
Vacation_001.jpg
Vacation_002.jpg
Vacation_003.jpg
```

---

# 📁 Project Structure

```text
renamed/
│
├── main.py
├── README.md
├── LICENSE
└── screenshot.png
```

---

# 🚀 Future Improvements

- Undo Rename
- Folder Renaming
- Regex Rename
- Naming Presets
- Dark Mode
- Metadata-Based Numbering
- Multi-language Support

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository

2. Create a new branch

```bash
git checkout -b feature-name
```

3. Commit changes

```bash
git commit -m "Add feature"
```

4. Push

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📄 License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

# 👤 Author

**Khileshwar Sahu**

- GitHub: https://github.com/jikokoutei

If this project helped you, please consider giving it a ⭐ on GitHub!
