"""
Running Processes Tool
Displays a list of running processes with sorting, filtering, and kill capability.
"""

import customtkinter as ctk
import psutil
import platform
import os
import threading


def create_ui(frame, COLORS, FONTS):
    sort_column = "cpu"
    sort_reverse = True
    selected_pid = None

    def get_processes():
        procs = []
        for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "status", "username"]):
            try:
                info = p.info
                procs.append({
                    "pid": info["pid"],
                    "name": info["name"] or "N/A",
                    "cpu": info["cpu_percent"] or 0.0,
                    "memory": info["memory_percent"] or 0.0,
                    "status": info["status"] or "N/A",
                    "user": info["username"] or "N/A",
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return procs

    def sort_key(proc):
        col = sort_column
        if col == "pid":
            return proc["pid"]
        elif col == "name":
            return proc["name"].lower()
        elif col == "cpu":
            return proc["cpu"]
        elif col == "memory":
            return proc["memory"]
        elif col == "status":
            return proc["status"].lower()
        elif col == "user":
            return proc["user"].lower()
        return proc["pid"]

    def refresh_display():
        for widget in table_frame.winfo_children():
            widget.destroy()

        search_text = search_var.get().lower().strip()
        procs = get_processes()

        if search_text:
            procs = [p for p in procs if search_text in p["name"].lower() or search_text in str(p["pid"]) or search_text in p["user"].lower()]

        procs.sort(key=sort_key, reverse=sort_reverse)

        header = ctk.CTkFrame(table_frame, fg_color=COLORS["bg_card"], corner_radius=8)
        header.pack(fill="x", padx=5, pady=(5, 2))

        columns = [("PID", "pid", 70), ("Name", "name", 200), ("CPU%", "cpu", 70),
                    ("Mem%", "memory", 70), ("Status", "status", 100), ("User", "user", 150)]

        for text, col_id, width in columns:
            indicator = ""
            if sort_column == col_id:
                indicator = " ▼" if sort_reverse else " ▲"
            btn = ctk.CTkButton(
                header, text=text + indicator, font=FONTS["mono_small"],
                fg_color="transparent", hover_color=COLORS["border"],
                text_color=COLORS["accent"], width=width, anchor="w",
                command=lambda c=col_id: toggle_sort(c)
            )
            btn.pack(side="left", padx=5, pady=5)

        display_procs = procs[:200]

        for i, proc in enumerate(display_procs):
            bg = COLORS["bg_input"] if i % 2 == 0 else COLORS["bg_card"]
            row = ctk.CTkFrame(table_frame, fg_color=bg, corner_radius=4)
            row.pack(fill="x", padx=5, pady=1)

            pid_val = str(proc["pid"])
            status_color = COLORS["green"] if proc["status"] == "running" else (
                COLORS["yellow"] if proc["status"] == "sleeping" else COLORS["text_dim"]
            )

            data = [
                (pid_val, 70), (proc["name"], 200),
                (f"{proc['cpu']:.1f}", 70), (f"{proc['memory']:.1f}", 70),
                (proc["status"], 100), (proc["user"], 150)
            ]

            for (val, w), (_, col_id, _) in zip(data, columns):
                color = status_color if col_id == "status" else COLORS["text"]
                ctk.CTkLabel(row, text=val, font=FONTS["mono_small"], text_color=color, width=w, anchor="w").pack(side="left", padx=5, pady=3)

            select_btn = ctk.CTkButton(row, text="●", font=FONTS["mono_small"],
                                        fg_color="transparent", hover_color=COLORS["red"],
                                        text_color=COLORS["red"], width=20,
                                        command=lambda p=proc["pid"]: select_process(p))
            select_btn.pack(side="right", padx=5)

        count_label.configure(text=f"Showing {len(display_procs)} / {len(procs)} processes")

    def toggle_sort(col):
        nonlocal sort_column, sort_reverse
        if sort_column == col:
            sort_reverse = not sort_reverse
        else:
            sort_column = col
            sort_reverse = True
        refresh_display()

    def select_process(pid):
        nonlocal selected_pid
        selected_pid = pid
        kill_btn.configure(state="normal")
        selected_label.configure(text=f"Selected PID: {pid}")

    def kill_process():
        nonlocal selected_pid
        if selected_pid is None:
            return

        confirm = ctk.CTkToplevel(frame)
        confirm.title("Confirm Kill")
        confirm.geometry("350x150")
        confirm.configure(fg_color=COLORS["bg_dark"])
        confirm.transient(frame)
        confirm.grab_set()

        ctk.CTkLabel(confirm, text=f"Kill process {selected_pid}?", font=FONTS["heading"], text_color=COLORS["red"]).pack(pady=(20, 10))
        ctk.CTkLabel(confirm, text="This action cannot be undone.", font=FONTS["body"], text_color=COLORS["text_dim"]).pack(pady=(0, 15))

        btn_row = ctk.CTkFrame(confirm, fg_color="transparent")
        btn_row.pack()

        def confirm_kill():
            try:
                p = psutil.Process(selected_pid)
                p.kill()
            except psutil.NoSuchProcess:
                pass
            except psutil.AccessDenied:
                pass
            confirm.destroy()
            refresh_display()

        ctk.CTkButton(btn_row, text="Cancel", font=FONTS["button"], fg_color=COLORS["bg_input"],
                       text_color=COLORS["text"], hover_color=COLORS["border"],
                       command=confirm.destroy, width=80).pack(side="left", padx=5)
        ctk.CTkButton(btn_row, text="Kill", font=FONTS["button"], fg_color=COLORS["red"],
                       text_color=COLORS["text"], hover_color="#8B0000",
                       command=confirm_kill, width=80).pack(side="left", padx=5)

    top_bar = ctk.CTkFrame(frame, fg_color="transparent")
    top_bar.pack(fill="x", padx=15, pady=(15, 5))

    ctk.CTkLabel(top_bar, text="Running Processes", font=FONTS["title"], text_color=COLORS["text"]).pack(side="left")

    search_var = ctk.StringVar()
    search_entry = ctk.CTkEntry(top_bar, textvariable=search_var, placeholder_text="Search by name, PID, or user...",
                                 font=FONTS["body"], fg_color=COLORS["bg_input"], border_color=COLORS["border"],
                                 text_color=COLORS["text"], width=300)
    search_entry.pack(side="left", padx=10)
    search_var.trace_add("write", lambda *_: refresh_display())

    ctk.CTkButton(top_bar, text="Refresh", font=FONTS["button"], fg_color=COLORS["accent"],
                   hover_color=COLORS["border"], text_color=COLORS["text"],
                   command=refresh_display, width=90).pack(side="right", padx=(5, 0))

    control_bar = ctk.CTkFrame(frame, fg_color="transparent")
    control_bar.pack(fill="x", padx=15, pady=(0, 5))

    selected_label = ctk.CTkLabel(control_bar, text="No process selected", font=FONTS["body"], text_color=COLORS["text_dim"])
    selected_label.pack(side="left")

    kill_btn = ctk.CTkButton(control_bar, text="Kill Process", font=FONTS["button"], fg_color=COLORS["red"],
                              text_color=COLORS["text"], hover_color="#8B0000",
                              command=kill_process, width=110, state="disabled")
    kill_btn.pack(side="right")

    count_label = ctk.CTkLabel(frame, text="", font=FONTS["mono_small"], text_color=COLORS["text_dim"])
    count_label.pack(anchor="w", padx=20)

    table_frame = ctk.CTkScrollableFrame(frame, fg_color="transparent", scrollbar_button_color=COLORS["border"])
    table_frame.pack(fill="both", expand=True, padx=5, pady=(0, 15))

    refresh_display()
