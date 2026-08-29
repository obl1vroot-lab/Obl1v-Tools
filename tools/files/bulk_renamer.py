"""Bulk File Renamer - Rename multiple files using patterns, prefixes, and suffixes."""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import re
import threading


def create_ui(frame, COLORS, FONTS):
    folder_path = ctk.StringVar()
    pattern_var = ctk.StringVar(value="{n}")
    prefix_var = ctk.StringVar()
    suffix_var = ctk.StringVar()
    ext_filter_var = ctk.StringVar(value="*.*")
    counter_start_var = ctk.StringVar(value="1")
    status_var = ctk.StringVar(value="Ready")

    def browse_folder():
        path = filedialog.askdirectory(title="Select Folder")
        if path:
            folder_path.set(path)
            status_var.set(f"Selected: {path}")

    def get_filtered_files(path, ext_filter):
        ext_filter = ext_filter.strip()
        files = []
        for f in sorted(os.listdir(path)):
            fpath = os.path.join(path, f)
            if os.path.isfile(fpath):
                if ext_filter == "*.*" or ext_filter == "*" or not ext_filter:
                    files.append(f)
                else:
                    pattern = ext_filter.replace("*", ".*")
                    if re.match(f"^{pattern}$", f, re.IGNORECASE):
                        files.append(f)
        return files

    def build_renames(files, pattern, prefix, suffix, start):
        renames = []
        for i, fname in enumerate(files):
            name, ext = os.path.splitext(fname)
            n = start + i
            new_name = pattern.replace("{n}", str(n)).replace("{name}", name).replace("{ext}", ext.lstrip("."))
            new_name = f"{prefix}{new_name}{suffix}"
            if not os.path.splitext(new_name)[1] and ext:
                new_name += ext
            renames.append((fname, new_name))
        return renames

    def preview():
        path = folder_path.get()
        if not path or not os.path.isdir(path):
            messagebox.showerror("Error", "Please select a valid folder.")
            return

        files = get_filtered_files(path, ext_filter_var.get())
        if not files:
            preview_box.delete("1.0", "end")
            preview_box.insert("end", "No matching files found.")
            return

        try:
            start = int(counter_start_var.get())
        except ValueError:
            messagebox.showerror("Error", "Counter start must be a number.")
            return

        renames = build_renames(files, pattern_var.get(), prefix_var.get(), suffix_var.get(), start)

        lines = [f"{'Before':<40} ->  {'After'}", "-" * 80]
        for old, new in renames:
            lines.append(f"  {old:<38} ->  {new}")
        lines.append(f"\n{len(renames)} file(s) will be renamed.")

        preview_box.delete("1.0", "end")
        preview_box.insert("end", "\n".join(lines))
        status_var.set(f"Preview: {len(renames)} files")

    def do_rename():
        path = folder_path.get()
        if not path or not os.path.isdir(path):
            messagebox.showerror("Error", "Please select a valid folder.")
            return

        files = get_filtered_files(path, ext_filter_var.get())
        if not files:
            messagebox.showinfo("Info", "No matching files found.")
            return

        try:
            start = int(counter_start_var.get())
        except ValueError:
            messagebox.showerror("Error", "Counter start must be a number.")
            return

        renames = build_renames(files, pattern_var.get(), prefix_var.get(), suffix_var.get(), start)

        if not messagebox.askyesno("Confirm Rename", f"Rename {len(renames)} file(s)?\nThis cannot be undone."):
            return

        status_var.set("Renaming...")
        rename_btn.configure(state="disabled")

        def worker():
            try:
                errors = []
                for old, new in renames:
                    old_path = os.path.join(path, old)
                    new_path = os.path.join(path, new)
                    try:
                        if os.path.exists(new_path):
                            errors.append(f"Skipped (exists): {old}")
                            continue
                        os.rename(old_path, new_path)
                    except Exception as e:
                        errors.append(f"Error: {old} - {e}")

                def done():
                    if errors:
                        messagebox.showwarning("Rename Complete", f"Completed with {len(errors)} issue(s).\n\n" + "\n".join(errors[:10]))
                    else:
                        messagebox.showinfo("Rename Complete", f"Successfully renamed {len(renames)} file(s).")
                    status_var.set("Rename complete")
                    rename_btn.configure(state="normal")

                frame.after(0, done)
            except Exception as e:
                frame.after(0, lambda: messagebox.showerror("Error", str(e)))
                frame.after(0, lambda: rename_btn.configure(state="normal"))

        threading.Thread(target=worker, daemon=True).start()

    # Title
    ctk.CTkLabel(frame, text="Bulk File Renamer", font=FONTS["title"], text_color=COLORS["accent"]).pack(anchor="w", padx=15, pady=(15, 5))
    ctk.CTkLabel(frame, text="Rename multiple files using patterns", font=FONTS["subtitle"], text_color=COLORS["text_dim"]).pack(anchor="w", padx=15, pady=(0, 10))

    # Folder selection
    folder_frame = ctk.CTkFrame(frame, fg_color="transparent")
    folder_frame.pack(fill="x", padx=15, pady=(0, 10))

    ctk.CTkEntry(folder_frame, textvariable=folder_path, font=FONTS["mono_small"], placeholder_text="No folder selected...",
                 fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["text"],
                 state="disabled").pack(side="left", fill="x", expand=True, padx=(0, 8))
    ctk.CTkButton(folder_frame, text="Browse", command=browse_folder, font=FONTS["button"],
                  fg_color=COLORS["accent"], hover_color=COLORS["green"], width=100).pack(side="right")

    # Pattern row
    pattern_frame = ctk.CTkFrame(frame, fg_color="transparent")
    pattern_frame.pack(fill="x", padx=15, pady=(0, 5))

    ctk.CTkLabel(pattern_frame, text="Pattern:", font=FONTS["body"], text_color=COLORS["text"], width=80).pack(side="left")
    ctk.CTkEntry(pattern_frame, textvariable=pattern_var, font=FONTS["mono_small"], placeholder_text="{n}",
                 fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["text"], width=200).pack(side="left", padx=(0, 15))
    ctk.CTkLabel(pattern_frame, text="Ext Filter:", font=FONTS["body"], text_color=COLORS["text"], width=80).pack(side="left")
    ctk.CTkEntry(pattern_frame, textvariable=ext_filter_var, font=FONTS["mono_small"], placeholder_text="*.jpg",
                 fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["text"], width=150).pack(side="left")

    # Prefix / Suffix / Counter
    mod_frame = ctk.CTkFrame(frame, fg_color="transparent")
    mod_frame.pack(fill="x", padx=15, pady=(0, 5))

    ctk.CTkLabel(mod_frame, text="Prefix:", font=FONTS["body"], text_color=COLORS["text"], width=80).pack(side="left")
    ctk.CTkEntry(mod_frame, textvariable=prefix_var, font=FONTS["mono_small"], placeholder_text="",
                 fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["text"], width=150).pack(side="left", padx=(0, 15))
    ctk.CTkLabel(mod_frame, text="Suffix:", font=FONTS["body"], text_color=COLORS["text"], width=80).pack(side="left")
    ctk.CTkEntry(mod_frame, textvariable=suffix_var, font=FONTS["mono_small"], placeholder_text="",
                 fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["text"], width=150).pack(side="left", padx=(0, 15))
    ctk.CTkLabel(mod_frame, text="Start #:", font=FONTS["body"], text_color=COLORS["text"], width=80).pack(side="left")
    ctk.CTkEntry(mod_frame, textvariable=counter_start_var, font=FONTS["mono_small"], placeholder_text="1",
                 fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["text"], width=80).pack(side="left")

    # Buttons
    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.pack(fill="x", padx=15, pady=(5, 10))

    ctk.CTkButton(btn_frame, text="Preview", command=preview, font=FONTS["button"],
                  fg_color=COLORS["bg_card"], border_color=COLORS["border"], border_width=1,
                  text_color=COLORS["text"], hover_color=COLORS["accent"]).pack(side="left", padx=(0, 8))
    rename_btn = ctk.CTkButton(btn_frame, text="Rename", command=do_rename, font=FONTS["button"],
                               fg_color=COLORS["red"], hover_color="#cc0000")
    rename_btn.pack(side="left")

    # Preview output
    preview_box = ctk.CTkTextbox(frame, font=FONTS["mono_small"], fg_color=COLORS["bg_input"],
                                 border_color=COLORS["border"], border_width=1, text_color=COLORS["text"],
                                 wrap="word", height=200)
    preview_box.pack(fill="both", expand=True, padx=15, pady=(0, 5))

    # Status
    ctk.CTkLabel(frame, textvariable=status_var, font=FONTS["mono_small"], text_color=COLORS["text_dim"]).pack(anchor="w", padx=15, pady=(5, 15))
