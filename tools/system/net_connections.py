"""
Active Network Connections Tool
Displays active network connections with filtering by status.
"""

import customtkinter as ctk
import psutil
import platform
import os
import threading


def create_ui(frame, COLORS, FONTS):
    status_filter_var = ctk.StringVar(value="All")

    STATUS_COLORS = {
        "ESTABLISHED": COLORS["green"],
        "LISTEN": COLORS["yellow"],
        "TIME_WAIT": COLORS["text_dim"],
        "CLOSE_WAIT": COLORS["red"],
        "SYN_SENT": COLORS["accent"],
        "SYN_RECV": COLORS["accent"],
        "FIN_WAIT1": COLORS["text_dim"],
        "FIN_WAIT2": COLORS["text_dim"],
        "CLOSING": COLORS["red"],
        "LAST_ACK": COLORS["red"],
        "NONE": COLORS["text_dim"],
    }

    def get_connections():
        conns = []
        for c in psutil.net_connections(kind="inet"):
            try:
                local = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else "N/A"
                remote = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else "N/A"
                conns.append({
                    "local_ip": c.laddr.ip if c.laddr else "N/A",
                    "local_port": c.laddr.port if c.laddr else 0,
                    "remote_ip": c.raddr.ip if c.raddr else "N/A",
                    "remote_port": c.raddr.port if c.raddr else 0,
                    "status": c.status or "N/A",
                    "pid": c.pid or "N/A",
                    "local": local,
                    "remote": remote,
                })
            except (AttributeError, OSError):
                continue
        return conns

    def refresh_display():
        for widget in table_frame.winfo_children():
            widget.destroy()

        conns = get_connections()
        filter_val = status_filter_var.get()

        if filter_val != "All":
            conns = [c for c in conns if c["status"] == filter_val]

        header = ctk.CTkFrame(table_frame, fg_color=COLORS["bg_card"], corner_radius=8)
        header.pack(fill="x", padx=5, pady=(5, 2))

        cols = [("Local Address", 180), ("Local Port", 80), ("Remote Address", 180),
                ("Remote Port", 80), ("Status", 110), ("PID", 70)]

        for text, width in cols:
            ctk.CTkLabel(header, text=text, font=FONTS["mono_small"], text_color=COLORS["accent"],
                         width=width, anchor="w").pack(side="left", padx=5, pady=5)

        display_conns = conns[:300]

        for i, conn in enumerate(display_conns):
            bg = COLORS["bg_input"] if i % 2 == 0 else COLORS["bg_card"]
            row = ctk.CTkFrame(table_frame, fg_color=bg, corner_radius=4)
            row.pack(fill="x", padx=5, pady=1)

            status = conn["status"]
            status_color = STATUS_COLORS.get(status, COLORS["text_dim"])

            data = [
                (conn["local_ip"], 180, COLORS["text"]),
                (str(conn["local_port"]), 80, COLORS["text"]),
                (conn["remote_ip"], 180, COLORS["text"]),
                (str(conn["remote_port"]), 80, COLORS["text"]),
                (status, 110, status_color),
                (str(conn["pid"]), 70, COLORS["text"]),
            ]

            for val, width, color in data:
                ctk.CTkLabel(row, text=val, font=FONTS["mono_small"], text_color=color,
                             width=width, anchor="w").pack(side="left", padx=5, pady=3)

        count_label.configure(text=f"Showing {len(display_conns)} / {len(conns)} connections")

        statuses = ["All"] + sorted(set(c["status"] for c in get_connections()))
        status_filter.configure(values=statuses)

    top_bar = ctk.CTkFrame(frame, fg_color="transparent")
    top_bar.pack(fill="x", padx=15, pady=(15, 5))

    ctk.CTkLabel(top_bar, text="Network Connections", font=FONTS["title"], text_color=COLORS["text"]).pack(side="left")

    filter_row = ctk.CTkFrame(frame, fg_color="transparent")
    filter_row.pack(fill="x", padx=15, pady=(0, 5))

    ctk.CTkLabel(filter_row, text="Filter by status:", font=FONTS["body"], text_color=COLORS["text_dim"]).pack(side="left")

    status_filter = ctk.CTkOptionMenu(filter_row, variable=status_filter_var, values=["All"],
                                       font=FONTS["body"], fg_color=COLORS["bg_input"],
                                       button_color=COLORS["border"], button_hover_color=COLORS["accent"],
                                       dropdown_fg_color=COLORS["bg_card"],
                                       dropdown_hover_color=COLORS["border"],
                                       text_color=COLORS["text"], width=150,
                                       command=lambda _: refresh_display())
    status_filter.pack(side="left", padx=10)

    ctk.CTkButton(filter_row, text="Refresh", font=FONTS["button"], fg_color=COLORS["accent"],
                   hover_color=COLORS["border"], text_color=COLORS["text"],
                   command=refresh_display, width=100).pack(side="right")

    count_label = ctk.CTkLabel(frame, text="", font=FONTS["mono_small"], text_color=COLORS["text_dim"])
    count_label.pack(anchor="w", padx=20, pady=(0, 2))

    table_frame = ctk.CTkScrollableFrame(frame, fg_color="transparent", scrollbar_button_color=COLORS["border"])
    table_frame.pack(fill="both", expand=True, padx=5, pady=(0, 15))

    refresh_display()
