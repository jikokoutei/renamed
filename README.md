# Batch File Renamer (GUI)

A powerful, lightweight **Python Tkinter** application for batch renaming files with complete control over file order and customizable naming patterns.

Unlike basic file renamers, this tool lets you **drag and reorder files**, preview the output before renaming, and place the increment counter **anywhere** in the filename.

No external libraries are required—Tkinter is included with standard Python.

---

## ✨ Features

* 📁 Rename files in one or multiple folders
* 🔢 Custom numbering with flexible placeholders
* 🔠 Alphabetic sequences (`a`, `b`, `c`, ... `aa`, `ab`, ...)
* 🔡 Prefix support (`a1`, `A01`, etc.)
* 🎯 Place the counter anywhere in the filename
* 👀 Live preview before renaming
* 🖱️ Drag & drop to set the exact rename order
* ⬆️ Move files up/down manually
* 📅 Sort files by:

  * Name (A–Z / Z–A)
  * Date Modified
  * Date Created
* 📋 Queue multiple folders before renaming
* 📝 Detailed rename log
* ⚠️ Built-in validation to prevent invalid filenames
* 🚫 Collision-safe renaming using temporary filenames

---

## Screenshot

<img width="1127" height="898" alt="image" src="https://github.com/user-attachments/assets/4c27ef90-86a1-4a5b-85f1-3bd7c2011327" />


```
screenshot.png
```

---

# Requirements

* Python 3.8 or newer
* Tkinter (included with standard Python)

No additional packages are required.

---

# Installation

Clone the repository:

```bash
git clone https://github.com/jikokoutei/renamed.git
```

Open the project:

```bash
cd renamed
```

---

# Run

```bash
python main.py
```

Windows users may also run:

```bash
py main.py
```

---

# How to Use

## Step 1 — Select Folder

* Click **Browse**
* Choose the folder containing the files
* Select a quick sorting method
* Click **Load Files**

---

## Step 2 — Arrange File Order

Files appear in a list.

You can:

* Drag files up or down
* Use **Move Up**
* Use **Move Down**

The first file in the list receives the first number.

---

## Step 3 — Enter Name Pattern

Type the filename exactly how you want it.

The numbering placeholder must be inside **{}**.

Examples:

```
Photo_{001}
```

Produces

```
Photo_001.jpg
Photo_002.jpg
Photo_003.jpg
```

---

```
Vacation_{01}_Beach
```

Produces

```
Vacation_01_Beach.jpg
Vacation_02_Beach.jpg
```

---

```
IMG-{a1}
```

Produces

```
IMG-a1.png
IMG-a2.png
IMG-a3.png
```

---

```
Document_{A01}
```

Produces

```
Document_A01.pdf
Document_A02.pdf
```

---

```
File_{a}
```

Produces

```
File_a.txt
File_b.txt
File_c.txt
...
File_z.txt
File_aa.txt
```

---

## Supported Placeholders

| Placeholder | Output                  |
| ----------- | ----------------------- |
| `{1}`       | 1, 2, 3, 4...           |
| `{01}`      | 01, 02, 03...           |
| `{001}`     | 001, 002, 003...        |
| `{a1}`      | a1, a2, a3...           |
| `{A01}`     | A01, A02, A03...        |
| `{a}`       | a, b, c... z, aa, ab... |

---

## Live Preview

As you type a pattern, the application shows exactly how the first few filenames will look before anything is renamed.

Example:

```
Preview:

Vacation_001_Beach.jpg
Vacation_002_Beach.jpg
Vacation_003_Beach.jpg
```

---

## Queue Multiple Folders

You can prepare several folders before renaming.

1. Load Folder 1
2. Set its naming pattern
3. Click **Add To Queue**
4. Repeat for additional folders
5. Click **Rename All Queued Folders**

---

## Safety Features

* Detects invalid filename characters
* Prevents malformed placeholders
* Warns if numbering is missing
* Uses temporary filenames to avoid overwrite conflicts
* Shows confirmation before renaming
* Displays a detailed operation log

---

# Example

Original files

```
IMG_5342.jpg
IMG_1234.jpg
IMG_8910.jpg
```

After reordering

```
IMG_8910.jpg
IMG_5342.jpg
IMG_1234.jpg
```

Pattern

```
Vacation_{001}
```

Output

```
Vacation_001.jpg
Vacation_002.jpg
Vacation_003.jpg
```

---

# Project Structure

```
renamed/
│
├── main.py
├── README.md
├── LICENSE
└── screenshot.png
```

---

# Future Improvements

* Undo rename operation
* Rename folders
* Regex rename support
* Presets
* Dark mode
* Metadata-based numbering
* Multi-language support

---

# Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

```
git checkout -b feature-name
```

3. Commit your changes

```
git commit -m "Add feature"
```

4. Push

```
git push origin feature-name
```

5. Open a Pull Request

---

# License

This project is licensed under the MIT License.

---

## Author

* GitHub: https://github.com/jikokoutei

If you find this project useful, consider giving it a ⭐ on GitHub!
