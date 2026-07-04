"""
Batch File Renamer (GUI) - v4
--------------------------------
A Tkinter GUI to rename all files in one or more folders using a custom
name pattern with a user-defined increment placed anywhere via {}.

NAME PATTERN
------------
Type any file name pattern and put the increment sample inside curly
braces {} anywhere you like. The sample tells the tool how to count:

    {1}     -> 1, 2, 3, 4 ...            (no padding)
    {01}    -> 01, 02, 03 ... 10, 11 ...  (2-digit padding)
    {001}   -> 001, 002 ... 010 ... 100   (3-digit padding)
    {a1}    -> a1, a2, a3 ... a10 ...     (letter prefix + counting number)
    {A01}   -> A01, A02 ... A10 ...       (upper letter prefix + padded number)
    {a}     -> a, b, c ... z, aa, ab ...  (pure letter sequence, Excel-style)

The rest of the pattern is kept exactly as typed, e.g.:
    "Vacation_{001}_beach"  ->  Vacation_001_beach.jpg, Vacation_002_beach.jpg ...
    "IMG-{a1}"              ->  IMG-a1.png, IMG-a2.png ...

If you don't include any {}, "_{1}" is added automatically at the end
(so it behaves like the classic name_1, name_2 ... style) - but the app
will always warn you first, so a typo in your {} never goes unnoticed.

A live PREVIEW below the pattern box always shows exactly what the first
few output file names will look like, before you commit to anything.

ORDER OF FILES
--------------
  1. Browse to a folder, pick a quick sort to get a sensible starting order.
  2. Click "Load Files" - files appear in a list.
  3. Drag files up/down (or use Move Up / Move Down) to set the EXACT
     order you want. Top of the list = first number in the sequence.
  4. Type the name pattern and click "Add To Queue".
  5. Repeat for other folders, then click "Rename All Queued Folders".

Run with:  python rename_files_gui.py
(Tkinter ships with standard Python - no pip install needed.)
"""

import os
import re
import platform
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

QUICK_SORTS = [
    "Name (A-Z)",
    "Name (Z-A)",
    "Date Modified (Oldest first)",
    "Date Modified (Newest first)",
    "Date Created (Oldest first)",
    "Date Created (Newest first)",
]

ILLEGAL_CHARS = re.compile(r'[<>:"/\\|?*]')

# Matches a {...} placeholder. We intentionally allow surrounding
# whitespace INSIDE the braces (e.g. "{ 01 }") since that's a very easy
# typo to make and previously caused the whole placeholder to be missed
# silently.
PLACEHOLDER_RE = re.compile(r'\{\s*([^{}]*?)\s*\}')


# ---------------------------------------------------------------------------
# Increment / pattern helpers
# ---------------------------------------------------------------------------

def _alpha_to_num(s: str) -> int:
    """Convert a letter sequence ('a'->0, 'z'->25, 'aa'->26 ...), Excel-style."""
    s = s.lower()
    num = 0
    for ch in s:
        num = num * 26 + (ord(ch) - ord('a') + 1)
    return num - 1


def _num_to_alpha(n: int) -> str:
    n += 1
    result = ""
    while n > 0:
        n, rem = divmod(n - 1, 26)
        result = chr(97 + rem) + result
    return result


def generate_increment_sequence(token: str, count: int):
    """Generate `count` increment strings based on a sample token such as
    '001', '01', '1', 'a1', 'A01', 'a', 'A'."""
    token = token.strip()
    match = re.match(r'^(.*?)(\d+)$', token)
    if match is not None:
        prefix, digits = match.group(1), match.group(2)
        width = len(digits)
        start = int(digits)
        return [f"{prefix}{str(start + i).zfill(width)}" for i in range(count)]

    if token.isalpha():
        is_upper = token.isupper()
        start_val = _alpha_to_num(token)
        seq = []
        for i in range(count):
            letters = _num_to_alpha(start_val + i)
            seq.append(letters.upper() if is_upper else letters)
        return seq

    # fallback for symbols with no digits, e.g. "--"
    return [f"{token}{i + 1}" for i in range(count)]


def find_placeholders(pattern: str):
    """Return all {...} placeholders found in the raw, as-typed pattern."""
    return PLACEHOLDER_RE.findall(pattern)


def parse_pattern(pattern: str, auto_append_ok: bool = True):
    """Validate a name pattern and return (full_pattern, token_full, token).

    full_pattern  - pattern guaranteed to contain exactly one {token}
    token_full    - the placeholder text including braces, e.g. '{001}'
    token         - the sample text inside the braces, e.g. '001'

    Raises ValueError with a human-readable message on problems, including
    when the person clearly *tried* to use a placeholder (there's a "{" or
    "}" in the text) but it wasn't a valid one - e.g. unmatched brace or an
    empty {}. That case is never silently "fixed" for the user.
    """
    working = pattern
    matches = list(PLACEHOLDER_RE.finditer(working))

    if len(matches) == 0:
        if ("{" in working or "}" in working):
            raise ValueError(
                "Found a '{' or '}' in your pattern, but it isn't a valid "
                "placeholder (check for a missing brace or empty {}). "
                "Fix it or remove the braces entirely."
            )
        if not auto_append_ok:
            raise ValueError("NO_PLACEHOLDER")
        working = working + "_{1}"
        matches = list(PLACEHOLDER_RE.finditer(working))

    if len(matches) > 1:
        raise ValueError("Only one {increment} placeholder is supported in the name pattern.")

    m = matches[0]
    token_full = m.group(0)
    token = m.group(1)
    if not token.strip():
        raise ValueError("The {} placeholder cannot be empty.")

    literal_only = working.replace(token_full, "", 1)
    if ILLEGAL_CHARS.search(literal_only):
        raise ValueError('Name pattern contains characters not allowed in file names: < > : " / \\ | ? *')

    return working, token_full, token


# ---------------------------------------------------------------------------
# Renaming logic
# ---------------------------------------------------------------------------

def quick_sorted_files(folder_path: str, sort_option: str):
    files = [
        f for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    def full(f):
        return os.path.join(folder_path, f)

    if sort_option == "Name (A-Z)":
        files.sort(key=lambda f: f.lower())
    elif sort_option == "Name (Z-A)":
        files.sort(key=lambda f: f.lower(), reverse=True)
    elif sort_option == "Date Modified (Oldest first)":
        files.sort(key=lambda f: os.path.getmtime(full(f)))
    elif sort_option == "Date Modified (Newest first)":
        files.sort(key=lambda f: os.path.getmtime(full(f)), reverse=True)
    elif sort_option == "Date Created (Oldest first)":
        files.sort(key=lambda f: os.path.getctime(full(f)))
    elif sort_option == "Date Created (Newest first)":
        files.sort(key=lambda f: os.path.getctime(full(f)), reverse=True)

    return files


def build_preview_names(pattern: str, count: int, auto_append_ok: bool = True):
    """Return (names, error). names is a list of up to `count` example
    output stems (no extension). error is None on success, or a message."""
    try:
        full_pattern, token_full, token = parse_pattern(pattern, auto_append_ok=auto_append_ok)
    except ValueError as e:
        return None, str(e)

    seq = generate_increment_sequence(token, count)
    return [full_pattern.replace(token_full, s, 1) for s in seq], None


def rename_files_in_order(folder_path: str, pattern: str, ordered_files, log):
    """Rename files in folder_path following ordered_files sequence, using
    the increment pattern (e.g. 'Photo_{001}_trip')."""

    if not os.path.isdir(folder_path):
        log(f"  [SKIP] Folder does not exist: {folder_path}")
        return

    existing = [f for f in ordered_files if os.path.isfile(os.path.join(folder_path, f))]
    if not existing:
        log(f"  [SKIP] No valid files to rename in: {folder_path}")
        return

    try:
        full_pattern, token_full, token = parse_pattern(pattern)
    except ValueError as e:
        log(f"  [ERROR] {e}")
        return

    sequence = generate_increment_sequence(token, len(existing))

    # Step 1: temp rename to avoid collisions
    temp_names = []
    for i, filename in enumerate(existing, start=1):
        old_path = os.path.join(folder_path, filename)
        temp_path = os.path.join(folder_path, f"__temp_rename_{i}__")
        os.rename(old_path, temp_path)
        ext = os.path.splitext(filename)[1]
        temp_names.append((temp_path, ext))

    # Step 2: final rename using the pattern + generated sequence
    for i, (temp_path, ext) in enumerate(temp_names):
        new_stem = full_pattern.replace(token_full, sequence[i], 1)
        new_name = f"{new_stem}{ext}"
        os.rename(temp_path, os.path.join(folder_path, new_name))
        log(f"  -> {new_name}")

    log(f"  Done: {len(temp_names)} file(s) renamed in '{folder_path}'\n")


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------

class RenamerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Batch File Renamer")
        self.geometry("900x780")
        # Raised from 700x520: below this, the file-order list (the part
        # you actually need to see and drag rows in) was getting squeezed
        # down to just a couple of visible rows.
        self.minsize(760, 640)

        self.jobs = []            # list of dicts: path, pattern, ordered_files
        self.current_folder = None
        self._log_line_count = 0

        # Root grid: everything is resizable. Rows that hold lists get
        # weight so they grow/shrink with the window; fixed-height rows
        # (controls) get weight 0. minsize on each list row is a hard
        # floor - it stops that row being squeezed to uselessness even
        # if the window is dragged smaller than is really comfortable.
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=4, minsize=170)   # order section (most important - protect it most)
        self.rowconfigure(3, weight=2, minsize=90)    # jobs table
        self.rowconfigure(5, weight=2, minsize=90)    # log

        self._build_add_job_section()
        self._build_order_section()
        self._build_queue_section()
        self._build_jobs_table()
        self._build_action_section()
        self._build_log_section()

    # ---------- UI sections ----------

    def _build_add_job_section(self):
        frame = ttk.LabelFrame(self, text="Step 1: Choose a folder")
        frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Folder:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.folder_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.folder_var).grid(row=0, column=1, columnspan=2, sticky="ew", padx=5, pady=5)
        ttk.Button(frame, text="Browse...", command=self.browse_folder).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame, text="Quick sort:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.sort_var = tk.StringVar(value=QUICK_SORTS[0])
        ttk.Combobox(
            frame, textvariable=self.sort_var, values=QUICK_SORTS,
            state="readonly", width=28
        ).grid(row=1, column=1, sticky="w", padx=5, pady=5)
        ttk.Button(frame, text="Load Files", command=self.load_files).grid(row=1, column=3, padx=5, pady=5)

    def _build_order_section(self):
        frame = ttk.LabelFrame(self, text="Step 2: Drag files to set the exact rename order (top = first)")
        frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        list_frame = ttk.Frame(frame)
        list_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self.order_listbox = tk.Listbox(list_frame, height=8, selectmode="single", activestyle="none")
        self.order_listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(list_frame, command=self.order_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.order_listbox.config(yscrollcommand=scrollbar.set)

        # drag-and-drop reorder (only triggers when the target row actually changes)
        self.order_listbox.bind("<Button-1>", self._drag_start)
        self.order_listbox.bind("<B1-Motion>", self._drag_motion)
        self.order_listbox.bind("<<ListboxSelect>>", lambda e: self._update_preview())

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=0, column=1, sticky="n", padx=5, pady=5)
        ttk.Button(btn_frame, text="Move Up", command=self.move_up, width=12).pack(pady=2)
        ttk.Button(btn_frame, text="Move Down", command=self.move_down, width=12).pack(pady=2)

    def _build_queue_section(self):
        frame = ttk.LabelFrame(self, text="Step 3: Set the name pattern and add to queue")
        frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Name pattern:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.pattern_var = tk.StringVar()
        self.pattern_var.trace_add("write", lambda *a: self._update_preview())
        ttk.Entry(frame, textvariable=self.pattern_var).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ttk.Button(frame, text="Add To Queue", command=self.add_job).grid(row=0, column=2, padx=10, pady=5)

        help_text = (
            "Put the increment sample inside {}  -  anywhere in the name.\n"
            "{1}\u21921,2,3   {01}\u219201,02,03   {001}\u2192001,002,003   {a1}\u2192a1,a2,a3   {a}\u2192a,b,c...\n"
            "Example: \"Vacation_{001}_beach\"  \u2192  Vacation_001_beach.jpg, Vacation_002_beach.jpg ..."
        )
        ttk.Label(frame, text=help_text, foreground="#555555", font=("", 8), justify="left").grid(
            row=1, column=0, columnspan=3, sticky="w", padx=5, pady=(0, 3)
        )

        # Live preview - this is what catches a mistyped {} before it ever
        # touches your files.
        self.preview_var = tk.StringVar(value="Preview: (load files and type a pattern to see example output names)")
        ttk.Label(
            frame, textvariable=self.preview_var, foreground="#1a6b1a",
            font=("", 9, "bold"), justify="left", wraplength=820
        ).grid(row=2, column=0, columnspan=3, sticky="w", padx=5, pady=(0, 5))

    def _build_jobs_table(self):
        frame = ttk.LabelFrame(self, text="Queued folders")
        frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        columns = ("path", "pattern", "file_count")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=5)
        self.tree.heading("path", text="Folder Path")
        self.tree.heading("pattern", text="Name Pattern")
        self.tree.heading("file_count", text="Files")
        self.tree.column("path", width=340)
        self.tree.column("pattern", width=220)
        self.tree.column("file_count", width=60, anchor="center")
        self.tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        tree_scroll = ttk.Scrollbar(frame, command=self.tree.yview)
        tree_scroll.grid(row=0, column=1, sticky="ns")
        self.tree.config(yscrollcommand=tree_scroll.set)

        ttk.Button(frame, text="Remove Selected", command=self.remove_selected).grid(
            row=1, column=0, sticky="e", padx=5, pady=(0, 5)
        )

    def _build_action_section(self):
        frame = ttk.Frame(self)
        frame.grid(row=4, column=0, sticky="ew", padx=10, pady=(0, 5))
        ttk.Button(frame, text="Rename All Queued Folders", command=self.run_rename).pack(side="left")
        ttk.Label(frame, text="\u26a0 This renames files in place.").pack(side="left", padx=10)

    def _build_log_section(self):
        frame = ttk.LabelFrame(self, text="Log")
        frame.grid(row=5, column=0, sticky="nsew", padx=10, pady=(0, 10))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        self.log_text = tk.Text(frame, height=8, state="disabled", wrap="word")
        self.log_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        log_scroll = ttk.Scrollbar(frame, command=self.log_text.yview)
        log_scroll.grid(row=0, column=1, sticky="ns")
        self.log_text.config(yscrollcommand=log_scroll.set)

    # ---------- live preview ----------

    def _update_preview(self):
        pattern = self.pattern_var.get().strip()
        if not pattern:
            self.preview_var.set("Preview: (type a pattern to see example output names)")
            return

        count = self.order_listbox.size() or 3
        count = min(count, 3)
        names, error = build_preview_names(pattern, count, auto_append_ok=True)

        if error:
            self.preview_var.set(f"Preview: \u26a0 {error}")
            return

        # Warn (without blocking) if there was no real {} in what they typed,
        # since that means a counter gets silently appended.
        if not find_placeholders(pattern):
            joined = ", ".join(f"{n}.<ext>" for n in names)
            self.preview_var.set(
                f"Preview: {joined}  \u26a0 No {{}} found - a counter (_1, _2, ...) will be added automatically."
            )
        else:
            joined = ", ".join(f"{n}.<ext>" for n in names)
            self.preview_var.set(f"Preview: {joined} ...")

    # ---------- drag-and-drop reorder handlers ----------

    def _drag_start(self, event):
        self._drag_index = self.order_listbox.nearest(event.y)

    def _drag_motion(self, event):
        new_index = self.order_listbox.nearest(event.y)
        if new_index != self._drag_index and 0 <= new_index < self.order_listbox.size():
            item = self.order_listbox.get(self._drag_index)
            self.order_listbox.delete(self._drag_index)
            self.order_listbox.insert(new_index, item)
            self.order_listbox.selection_clear(0, "end")
            self.order_listbox.selection_set(new_index)
            self._drag_index = new_index

    def move_up(self):
        sel = self.order_listbox.curselection()
        if not sel or sel[0] == 0:
            return
        i = sel[0]
        item = self.order_listbox.get(i)
        self.order_listbox.delete(i)
        self.order_listbox.insert(i - 1, item)
        self.order_listbox.selection_set(i - 1)

    def move_down(self):
        sel = self.order_listbox.curselection()
        if not sel or sel[0] == self.order_listbox.size() - 1:
            return
        i = sel[0]
        item = self.order_listbox.get(i)
        self.order_listbox.delete(i)
        self.order_listbox.insert(i + 1, item)
        self.order_listbox.selection_set(i + 1)

    # ---------- actions ----------

    def browse_folder(self):
        path = filedialog.askdirectory(title="Select folder")
        if path:
            self.folder_var.set(path)

    def load_files(self):
        path = self.folder_var.get().strip()
        if not path or not os.path.isdir(path):
            messagebox.showerror("Invalid folder", "Please choose a valid, existing folder.")
            return

        files = quick_sorted_files(path, self.sort_var.get())
        if not files:
            messagebox.showinfo("No files", "This folder has no files to rename.")
            return

        self.current_folder = path
        self.order_listbox.delete(0, "end")
        for f in files:
            self.order_listbox.insert("end", f)
        self._update_preview()

    def add_job(self):
        if not self.current_folder:
            messagebox.showerror("No folder loaded", "Click 'Load Files' for a folder first.")
            return

        pattern = self.pattern_var.get().strip()
        if not pattern:
            messagebox.showerror("Missing name pattern", "Please enter a name pattern (e.g. Photo_{001}).")
            return

        try:
            parse_pattern(pattern)
        except ValueError as e:
            messagebox.showerror("Invalid name pattern", str(e))
            return

        # If the person didn't actually include a {} placeholder, make sure
        # they know a counter will be appended automatically - don't let
        # that happen silently.
        if not find_placeholders(pattern):
            proceed = messagebox.askyesno(
                "No {} placeholder found",
                "Your pattern doesn't contain a {} counter, so '_1', '_2', "
                "'_3' ... will be appended automatically to the end of every "
                "file name.\n\nIs that what you want?",
            )
            if not proceed:
                return

        ordered_files = list(self.order_listbox.get(0, "end"))
        if not ordered_files:
            messagebox.showerror("No files", "The order list is empty.")
            return

        self.jobs.append({
            "path": self.current_folder,
            "pattern": pattern,
            "ordered_files": ordered_files,
        })
        self.tree.insert("", "end", values=(self.current_folder, pattern, len(ordered_files)))

        # reset for next folder
        self.folder_var.set("")
        self.pattern_var.set("")
        self.order_listbox.delete(0, "end")
        self.current_folder = None
        self._update_preview()

    def remove_selected(self):
        selected = self.tree.selection()
        for item in selected:
            index = self.tree.index(item)
            self.tree.delete(item)
            del self.jobs[index]

    def log(self, message: str, force_refresh: bool = False):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.configure(state="disabled")

        self._log_line_count += 1
        # Only force a UI refresh periodically (or when told to) - keeps
        # things responsive instead of redrawing on every single line.
        if force_refresh or self._log_line_count % 20 == 0:
            self.log_text.see("end")
            self.update_idletasks()

    def run_rename(self):
        if not self.jobs:
            messagebox.showwarning("No folders queued", "Add at least one folder before renaming.")
            return

        confirm = messagebox.askyesno(
            "Confirm rename",
            f"This will rename files in {len(self.jobs)} folder(s). Continue?"
        )
        if not confirm:
            return

        self.log("=== Starting rename process ===\n", force_refresh=True)
        for job in self.jobs:
            self.log(f"Processing: {job['path']}  (pattern: '{job['pattern']}')", force_refresh=True)
            rename_files_in_order(job["path"], job["pattern"], job["ordered_files"], self.log)

        self.log("=== All folders processed ===", force_refresh=True)
        messagebox.showinfo("Done", "Renaming complete. Check the log for details.")


if __name__ == "__main__":
    app = RenamerApp()
    app.mainloop()
