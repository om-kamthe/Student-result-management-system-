import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

FILE = "student_result.csv"

COLORS = {
    "navy",     
    "blue",       
    "blue_dark",
    "bg",         
    "surface",
    "surface_alt",
    "text" ,       
    "muted",      
    "border",     
    "success",
    "danger",
    "input",
}

SUBJECTS = ["Physics", "Mathematics", "Computer Science", "Chemistry", "English"]
HEADERS = ["Name", "Roll No", "Class"] + SUBJECTS
RESULT_COLUMNS = ("Name", "Roll No", "Class", "Total Marks", "Percentage", "Result")


def ensure_csv():
    """Create the CSV file with the correct header if it does not exist."""
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(HEADERS)


ensure_csv()



root = tk.Tk()
root.title("Student Result Management System")
root.geometry("1100x720")
root.minsize(950, 650)
root.configure(bg=COLORS["bg"])



style = ttk.Style(root)
try:
    style.theme_use("clam")
except tk.TclError:
    pass

style.configure(
    "Treeview",
    background=COLORS["surface"],
    foreground=COLORS["text"],
    fieldbackground=COLORS["surface"],
    rowheight=34,
    font=("Segoe UI", 10),
    borderwidth=0,
)
style.configure(
    "Treeview.Heading",
    background=COLORS["navy"],
    foreground="white",
    font=("Segoe UI", 10, "bold"),
    padding=(8, 8),
)
style.map(
    "Treeview",
    background=[("selected", "#DBEAFE")],
    foreground=[("selected", COLORS["text"])],
)
style.configure(
    "TEntry",
    padding=8,
    fieldbackground=COLORS["input"],
)
style.configure(
    "TScrollbar",
    background=COLORS["surface_alt"],
    troughcolor=COLORS["bg"],
    bordercolor=COLORS["bg"],
)


def make_button(parent, text, command, primary=True, width=18):
    """Create consistently styled application buttons."""
    bg = COLORS["blue"] if primary else COLORS["surface_alt"]
    fg = "white" if primary else COLORS["navy"]
    active_bg = COLORS["blue_dark"] if primary else "#DCE5F0"

    button = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", 10, "bold"),
        bg=bg,
        fg=fg,
        activebackground=active_bg,
        activeforeground=fg,
        relief="flat",
        bd=0,
        cursor="hand2",
        width=width,
        padx=8,
        pady=9,
    )

    # Simple hover treatment without changing the overall palette.
    button.bind("<Enter>", lambda _e: button.configure(bg=active_bg))
    button.bind("<Leave>", lambda _e: button.configure(bg=bg))
    return button


def make_label(parent, text, size=11, bold=False, color=None):
    return tk.Label(
        parent,
        text=text,
        font=("Segoe UI", size, "bold" if bold else "normal"),
        bg=parent.cget("bg"),
        fg=color or COLORS["text"],
    )


# -------------------- HEADER --------------------
header = tk.Frame(root, bg=COLORS["navy"], height=92)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="STUDENT RESULT MANAGEMENT SYSTEM",
    font=("Segoe UI", 23, "bold"),
    bg=COLORS["navy"],
    fg="white",
).pack(pady=(17, 2))

tk.Label(
    header,
    text="Manage student records • Calculate results • View performance",
    font=("Segoe UI", 10),
    bg=COLORS["navy"],
    fg="#D7E3F4",
).pack()


# -------------------- NAVIGATION --------------------
button_frame = tk.Frame(root, bg=COLORS["bg"])
button_frame.pack(pady=18)

# -------------------- CONTENT CONTAINER --------------------
content = tk.Frame(root, bg=COLORS["bg"])
content.pack(fill="both", expand=True, padx=28, pady=(0, 24))


# -------------------- FRAME 1 / ADD STUDENT --------------------
frame1 = tk.Frame(
    content,
    bg=COLORS["surface"],
    highlightbackground=COLORS["border"],
    highlightthickness=1,
)

tk.Label(
    frame1,
    text="ADD STUDENT",
    font=("Segoe UI", 18, "bold"),
    bg=COLORS["surface"],
    fg=COLORS["navy"],
).grid(row=0, column=0, columnspan=2, pady=(22, 16))

entries = {}


def add_entry(row, label_text, key):
    tk.Label(
        frame1,
        text=label_text,
        font=("Segoe UI", 10, "bold"),
        bg=COLORS["surface"],
        fg=COLORS["text"],
        anchor="w",
    ).grid(row=row, column=0, padx=(40, 18), pady=7, sticky="w")

    entry = ttk.Entry(frame1, width=34)
    entry.grid(row=row, column=1, padx=(0, 40), pady=7, sticky="ew")
    entries[key] = entry


add_entry(1, "Name", "name")
add_entry(2, "Roll No", "roll")
add_entry(3, "Class", "class_name")
add_entry(4, "Physics", "physics")
add_entry(5, "Mathematics", "mathematics")
add_entry(6, "Computer Science", "computer")
add_entry(7, "Chemistry", "chemistry")
add_entry(8, "English", "english")

frame1.columnconfigure(1, weight=1)


def clear_entries():
    for entry in entries.values():
        entry.delete(0, tk.END)


def save_student():
    name = entries["name"].get().strip()
    roll = entries["roll"].get().strip()
    class_name = entries["class_name"].get().strip()

    if not name or not roll or not class_name:
        messagebox.showwarning(
            "Missing Information",
            "Please enter Name, Roll No and Class.",
        )
        return

    marks = {}
    for subject, key in zip(SUBJECTS, ["physics", "mathematics", "computer", "chemistry", "english"]):
        value = entries[key].get().strip()
        try:
            mark = int(value)
        except ValueError:
            messagebox.showerror(
                "Invalid Marks",
                f"{subject}: please enter a whole number.",
            )
            return

        if not 0 <= mark <= 100:
            messagebox.showerror(
                "Invalid Marks",
                f"{subject}: marks must be between 0 and 100.",
            )
            return

        marks[subject] = mark

    # Prevent accidental duplicate student records for the same roll number.
    try:
        with open(FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if any(row.get("Roll No", "").strip() == roll for row in reader):
                messagebox.showwarning(
                    "Duplicate Roll No",
                    f"Roll No {roll} already exists.",
                )
                return
    except FileNotFoundError:
        ensure_csv()

    with open(FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            name,
            roll,
            class_name,
            marks["Physics"],
            marks["Mathematics"],
            marks["Computer Science"],
            marks["Chemistry"],
            marks["English"],
        ])

    messagebox.showinfo("Success", "Student record saved successfully.")
    clear_entries()


make_button(frame1, "SAVE STUDENT", save_student, primary=True, width=20).grid(
    row=9, column=0, columnspan=2, pady=(18, 24)
)


# -------------------- FRAME 2 / GET RESULT --------------------
frame2 = tk.Frame(
    content,
    bg=COLORS["surface"],
    highlightbackground=COLORS["border"],
    highlightthickness=1,
)

tk.Label(
    frame2,
    text="GET STUDENT RESULT",
    font=("Segoe UI", 18, "bold"),
    bg=COLORS["surface"],
    fg=COLORS["navy"],
).pack(pady=(24, 14))

search_area = tk.Frame(frame2, bg=COLORS["surface"])
search_area.pack(pady=4)

tk.Label(
    search_area,
    text="Enter Roll No",
    font=("Segoe UI", 10, "bold"),
    bg=COLORS["surface"],
    fg=COLORS["text"],
).pack(side="left", padx=(0, 10))

result_roll_entry = ttk.Entry(search_area, width=25)
result_roll_entry.pack(side="left", padx=5)

result_tree = ttk.Treeview(
    frame2,
    columns=RESULT_COLUMNS,
    show="hea
    
    
    
    
    
    
    
