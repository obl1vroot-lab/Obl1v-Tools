"""Password Hasher - Hash passwords with multiple algorithms."""

import customtkinter as ctk
import secrets
import string
import hashlib

try:
    import bcrypt
except ImportError:
    bcrypt = None


def _hash_pw(password, algorithm):
    if algorithm == "bcrypt":
        if bcrypt is None:
            return ("bcrypt module not installed. Run: pip install bcrypt", "")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return (hashed.decode(), salt.decode())
    elif algorithm == "MD5":
        return (hashlib.md5(password.encode()).hexdigest(), "")
    elif algorithm == "SHA256":
        return (hashlib.sha256(password.encode()).hexdigest(), "")
    elif algorithm == "SHA512":
        return (hashlib.sha512(password.encode()).hexdigest(), "")
    return ("", "")


def create_ui(frame, COLORS, FONTS):
    input_var = ctk.StringVar()
    output_var = ctk.StringVar()
    salt_var = ctk.StringVar()
    algo_var = ctk.StringVar(value="SHA256")

    ctk.CTkLabel(frame, text="Password Hasher", font=FONTS["heading"],
                 text_color=COLORS["text"], anchor="w").pack(fill="x", padx=16, pady=(16, 8))

    inp_frame = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=10)
    inp_frame.pack(fill="x", padx=16, pady=(0, 8))

    ctk.CTkLabel(inp_frame, text="Password", font=FONTS["body"],
                 text_color=COLORS["text_dim"]).pack(anchor="w", padx=12, pady=(8, 0))
    ctk.CTkEntry(inp_frame, textvariable=input_var, placeholder_text="Enter password...",
                 font=FONTS["mono"], fg_color=COLORS["bg_input"], text_color=COLORS["text"],
                 border_color=COLORS["border"], height=36, show="*").pack(fill="x", padx=12, pady=(4, 10))

    algo_frame = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=10)
    algo_frame.pack(fill="x", padx=16, pady=(0, 8))
    ctk.CTkLabel(algo_frame, text="Algorithm", font=FONTS["body"],
                 text_color=COLORS["text_dim"]).pack(anchor="w", padx=12, pady=(8, 0))
    ctk.CTkOptionMenu(algo_frame, variable=algo_var, values=["MD5", "SHA256", "SHA512", "bcrypt"],
                      fg_color=COLORS["bg_input"], button_color=COLORS["accent"],
                      button_hover_color=COLORS["green"], font=FONTS["body"],
                      dropdown_fg_color=COLORS["bg_card"]
                      ).pack(fill="x", padx=12, pady=(4, 10))

    def hash_pw():
        pw = input_var.get()
        if not pw:
            output_var.set("Enter a password first")
            salt_var.set("")
            return
        result, salt = _hash_pw(pw, algo_var.get())
        output_var.set(result)
        salt_var.set(f"Salt: {salt}" if salt else "")

    ctk.CTkButton(frame, text="Hash", font=FONTS["button"], fg_color=COLORS["accent"],
                  hover_color=COLORS["green"], command=hash_pw).pack(fill="x", padx=16, pady=(0, 8))

    out_frame = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=10)
    out_frame.pack(fill="x", padx=16, pady=(0, 16))

    ctk.CTkLabel(out_frame, text="Hash Output", font=FONTS["body"],
                 text_color=COLORS["text_dim"]).pack(anchor="w", padx=12, pady=(8, 0))

    row = ctk.CTkFrame(out_frame, fg_color="transparent")
    row.pack(fill="x", padx=12, pady=(4, 4))
    ctk.CTkEntry(row, textvariable=output_var, font=FONTS["mono_small"],
                 fg_color=COLORS["bg_input"], text_color=COLORS["text"],
                 border_color=COLORS["border"], state="readonly", height=36
                 ).pack(side="left", fill="x", expand=True, padx=(0, 8))

    def copy():
        frame.clipboard_clear()
        frame.clipboard_append(output_var.get())

    ctk.CTkButton(row, text="Copy", font=FONTS["button"], width=60,
                  fg_color=COLORS["border"], hover_color=COLORS["accent"],
                  command=copy).pack(side="right", ipady=2)

    ctk.CTkLabel(out_frame, textvariable=salt_var, font=FONTS["mono_small"],
                 text_color=COLORS["text_dim"], anchor="w").pack(fill="x", padx=12, pady=(0, 10))

    if bcrypt is None:
        warn = ctk.CTkLabel(frame, text="Note: Install bcrypt for bcrypt support (pip install bcrypt)",
                            font=FONTS["body"], text_color=COLORS["yellow"])
        warn.pack(fill="x", padx=16, pady=(0, 8))
