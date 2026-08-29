"""
System Information Tool
Displays detailed system information including OS, CPU, memory, and disk usage.
"""

import customtkinter as ctk
import psutil
import platform
import os
import threading


def create_ui(frame, COLORS, FONTS):
    refresh_after_id = None
    auto_refresh_var = None

    def get_system_info():
        info = {}
        try:
            info["os_name"] = platform.system()
            info["os_version"] = platform.platform()
            info["architecture"] = platform.machine()
            info["processor"] = platform.processor() or "N/A"
            info["python_version"] = platform.python_version()
        except Exception as e:
            info["os_name"] = f"Error: {e}"

        try:
            info["cpu_physical"] = psutil.cpu_count(logical=False) or "N/A"
            info["cpu_logical"] = psutil.cpu_count(logical=True) or "N/A"
            info["cpu_percent"] = psutil.cpu_percent(interval=0.5)
            freq = psutil.cpu_freq()
            info["cpu_freq_current"] = f"{freq.current:.0f} MHz" if freq else "N/A"
            info["cpu_freq_max"] = f"{freq.max:.0f} MHz" if freq and freq.max else "N/A"
        except Exception as e:
            info["cpu_percent"] = f"Error: {e}"

        try:
            mem = psutil.virtual_memory()
            info["mem_total"] = f"{mem.total / (1024**3):.2f} GB"
            info["mem_used"] = f"{mem.used / (1024**3):.2f} GB"
            info["mem_available"] = f"{mem.available / (1024**3):.2f} GB"
            info["mem_percent"] = mem.percent
        except Exception as e:
            info["mem_total"] = f"Error: {e}"

        try:
            partitions = []
            for part in psutil.disk_partitions(all=False):
                try:
                    usage = psutil.disk_usage(part.mountpoint)
                    partitions.append({
                        "mount": part.mountpoint,
                        "fstype": part.fstype,
                        "total": f"{usage.total / (1024**3):.2f} GB",
                        "used": f"{usage.used / (1024**3):.2f} GB",
                        "free": f"{usage.free / (1024**3):.2f} GB",
                        "percent": usage.percent,
                    })
                except PermissionError:
                    continue
            info["partitions"] = partitions
        except Exception as e:
            info["partitions"] = []

        return info

    def build_section(parent, title, items):
        card = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], corner_radius=10)
        card.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(card, text=title, font=FONTS["heading"], text_color=COLORS["accent"]).pack(anchor="w", padx=15, pady=(12, 5))

        for label, value in items:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=2)
            ctk.CTkLabel(row, text=label, font=FONTS["body"], text_color=COLORS["text_dim"], width=200, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=str(value), font=FONTS["mono"], text_color=COLORS["text"], anchor="w").pack(side="left", fill="x", expand=True)

        return card

    def build_bar(parent, label, percent, color):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=4)
        ctk.CTkLabel(row, text=label, font=FONTS["body"], text_color=COLORS["text_dim"], width=120, anchor="w").pack(side="left")
        bar_frame = ctk.CTkFrame(row, fg_color=COLORS["bg_input"], height=20, corner_radius=5)
        bar_frame.pack(side="left", fill="x", expand=True, padx=(5, 10))
        bar_frame.pack_propagate(False)
        fill_width = max(1, int(percent))
        bar_fill = ctk.CTkFrame(bar_frame, fg_color=color, corner_radius=5)
        bar_fill.place(relx=0, rely=0, relwidth=percent / 100, relheight=1)
        ctk.CTkLabel(row, text=f"{percent:.1f}%", font=FONTS["mono_small"], text_color=COLORS["text"], width=55).pack(side="right")

    def refresh_display():
        nonlocal refresh_after_id
        info = get_system_info()

        for widget in scroll_frame.winfo_children():
            widget.destroy()

        build_section(scroll_frame, "Operating System", [
            ("System", info.get("os_name", "N/A")),
            ("Platform", info.get("os_version", "N/A")),
            ("Architecture", info.get("architecture", "N/A")),
            ("Processor", info.get("processor", "N/A")),
            ("Python", info.get("python_version", "N/A")),
        ])

        cpu_card = build_section(scroll_frame, "CPU", [
            ("Physical Cores", info.get("cpu_physical", "N/A")),
            ("Logical Cores", info.get("cpu_logical", "N/A")),
            ("Frequency", info.get("cpu_freq_current", "N/A")),
            ("Max Frequency", info.get("cpu_freq_max", "N/A")),
        ])
        build_bar(cpu_card, "Usage", info.get("cpu_percent", 0), COLORS["green"])

        mem_card = build_section(scroll_frame, "Memory", [
            ("Total", info.get("mem_total", "N/A")),
            ("Used", info.get("mem_used", "N/A")),
            ("Available", info.get("mem_available", "N/A")),
        ])
        build_bar(mem_card, "Usage", info.get("mem_percent", 0), COLORS["yellow"])

        disk_card = ctk.CTkFrame(scroll_frame, fg_color=COLORS["bg_card"], corner_radius=10)
        disk_card.pack(fill="x", padx=10, pady=(0, 10))
        ctk.CTkLabel(disk_card, text="Disk Partitions", font=FONTS["heading"], text_color=COLORS["accent"]).pack(anchor="w", padx=15, pady=(12, 5))

        header = ctk.CTkFrame(disk_card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(0, 4))
        for text in ["Mount", "Type", "Total", "Used", "Free"]:
            ctk.CTkLabel(header, text=text, font=FONTS["mono_small"], text_color=COLORS["text_dim"], width=120, anchor="w").pack(side="left", padx=(0, 10))

        for i, part in enumerate(info.get("partitions", [])):
            bg = COLORS["bg_input"] if i % 2 == 0 else COLORS["bg_card"]
            row = ctk.CTkFrame(disk_card, fg_color=bg, corner_radius=4)
            row.pack(fill="x", padx=15, pady=1)
            for key, w in [("mount", 120), ("fstype", 120), ("total", 120), ("used", 120), ("free", 120)]:
                ctk.CTkLabel(row, text=part.get(key, ""), font=FONTS["mono_small"], text_color=COLORS["text"], width=w, anchor="w").pack(side="left", padx=(0, 10))
            build_bar(row, "", part.get("percent", 0), COLORS["yellow"])

        if auto_refresh_var and auto_refresh_var.get():
            refresh_after_id = frame.after(5000, refresh_display)

    def on_refresh():
        nonlocal refresh_after_id
        if refresh_after_id:
            frame.after_cancel(refresh_after_id)
            refresh_after_id = None
        refresh_display()

    header = ctk.CTkFrame(frame, fg_color="transparent")
    header.pack(fill="x", padx=15, pady=(15, 5))
    ctk.CTkLabel(header, text="System Information", font=FONTS["title"], text_color=COLORS["text"]).pack(side="left")

    btn_row = ctk.CTkFrame(header, fg_color="transparent")
    btn_row.pack(side="right")

    auto_refresh_var = ctk.BooleanVar(value=False)
    ctk.CTkSwitch(btn_row, text="Auto-refresh (5s)", variable=auto_refresh_var,
                  font=FONTS["body"], text_color=COLORS["text_dim"],
                  fg_color=COLORS["bg_input"], progress_color=COLORS["accent"],
                  command=on_refresh).pack(side="left", padx=(0, 10))

    ctk.CTkButton(btn_row, text="Refresh", font=FONTS["button"],
                  fg_color=COLORS["accent"], hover_color=COLORS["border"],
                  text_color=COLORS["text"], command=on_refresh, width=100).pack(side="right")

    scroll_frame = ctk.CTkScrollableFrame(frame, fg_color="transparent", scrollbar_button_color=COLORS["border"])
    scroll_frame.pack(fill="both", expand=True, padx=5, pady=(5, 15))

    refresh_display()
