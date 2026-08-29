"""File Metadata Viewer - Display detailed file information including size, timestamps, and hashes."""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import hashlib
import threading
import time
from datetime import datetime

MIME_GUESS = {
    ".txt": "text/plain", ".pdf": "application/pdf", ".png": "image/png",
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
    ".bmp": "image/bmp", ".svg": "image/svg+xml", ".mp3": "audio/mpeg",
    ".wav": "audio/wav", ".mp4": "video/mp4", ".avi": "video/x-msvideo",
    ".mkv": "video/x-matroska", ".zip": "application/zip", ".rar": "application/x-rar-compressed",
    ".7z": "application/x-7z-compressed", ".tar": "application/x-tar",
    ".gz": "application/gzip", ".py": "text/x-python", ".js": "text/javascript",
    ".html": "text/html", ".css": "text/css", ".json": "application/json",
    ".xml": "application/xml", ".csv": "text/csv", ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".xls": "application/vnd.ms-excel", ".exe": "application/x-msdownload",
    ".dll": "application/x-msdownload", ".ini": "text/plain", ".log": "text/plain",
}


def create_ui(frame, COLORS, FONTS):
    file_path = ctk.StringVar()
    status_var = ctk.StringVar(value="Ready")

    def human_size(size):
        for unit in ("B", "KB", "MB", "GB", "TB"):
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"

    def browse_file():
        path = filedialog.askopenfilename(title="Select File")
        if path:
            file_path.set(path)
            load_info(path)

    def compute_hashes(path):
        md5_h = hashlib.md5()
        sha256_h = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                md5_h.update(chunk)
                sha256_h.update(chunk)
        return md5_h.hexdigest(), sha256_h.hexdigest()

    def load_info(path):
        status_var.set("Loading file info...")
        info_box.delete("1.0", "end")

        def worker():
            try:
                stat = os.stat(path)
                ext = os.path.splitext(path)[1].lower()
                mime = MIME_GUESS.get(ext, "unknown")
                md5, sha256 = compute_hashes(path)

                lines = [
                    f"{'File Information':^50}",
                    "=" * 50,
                    f"  Filename   : {os.path.basename(path)}",
                    f"  Path       : {path}",
                    f"  Extension  : {ext if ext else '(none)'}",
                    f"  MIME Type  : {mime}",
                    f"  Size       : {human_size(stat.st_size)} ({stat.st_size:,} bytes)",
                    "",
                    f"  Created    : {datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}",
                    f"  Modified   : {datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}",
                    f"  Accessed   : {datetime.fromtimestamp(stat.st_atime).strftime('%Y-%m-%d %H:%M:%S')}",
                    "",
                    f"  MD5        : {md5}",
                    f"  SHA-256    : {sha256}",
                    "=" * 50,
                ]
                frame.after(0, lambda: info_box.replace("1.0", "end", "\n".join(lines)))
                frame.after(0, lambda: status_var.set("Info loaded"))
            except Exception as e:
                frame.after(0, lambda: messagebox.showerror("Error", str(e)))
                frame.after(0, lambda: status_var.set("Error"))

        threading.Thread(target=worker, daemon=True).start()

    # Title
    ctk.CTkLabel(frame, text="File Metadata Viewer", font=FONTS["title"], text_color=COLORS["accent"]).pack(anchor="w", padx=15, pady=(15, 5))
    ctk.CTkLabel(frame, text="View detailed file information", font=FONTS["subtitle"], text_color=COLORS["text_dim"]).pack(anchor="w", padx=15, pady=(0, 10))

    # File selection
    file_frame = ctk.CTkFrame(frame, fg_color="transparent")
    file_frame.pack(fill="x", padx=15, pady=(0, 10))

    ctk.CTkEntry(file_frame, textvariable=file_path, font=FONTS["mono_small"], placeholder_text="No file selected...",
                 fg_color=COLORS["bg_input"], border_color=COLORS["border"], text_color=COLORS["text"],
                 state="disabled").pack(side="left", fill="x", expand=True, padx=(0, 8))
    ctk.CTkButton(file_frame, text="Browse", command=browse_file, font=FONTS["button"],
                  fg_color=COLORS["accent"], hover_color=COLORS["green"], width=100).pack(side="right")

    # Info output
    info_box = ctk.CTkTextbox(frame, font=FONTS["mono"], fg_color=COLORS["bg_input"],
                              border_color=COLORS["border"], border_width=1, text_color=COLORS["text"],
                              wrap="word", height=300)
    info_box.pack(fill="both", expand=True, padx=15, pady=(0, 5))

    # Status
    ctk.CTkLabel(frame, textvariable=status_var, font=FONTS["mono_small"], text_color=COLORS["text_dim"]).pack(anchor="w", padx=15, pady=(5, 15))
