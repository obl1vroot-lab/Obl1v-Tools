"""Password Strength Analyzer - Evaluate password strength with detailed scoring."""

import customtkinter as ctk
import secrets
import string
import math
import re


def _analyze(password):
    if not password:
        return {"score": 0, "length": 0, "varieties": 0, "entropy": 0, "label": "Empty"}

    length = len(password)
    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_symbol = bool(re.search(r"[^a-zA-Z0-9]", password))
    varieties = sum([has_lower, has_upper, has_digit, has_symbol])

    charset = 0
    if has_lower:
        charset += 26
    if has_upper:
        charset += 26
    if has_digit:
        charset += 10
    if has_symbol:
        charset += 33
    entropy = length * math.log2(charset) if charset else 0

    repeats = sum(password.count(c) - 1 for c in set(password)) / max(length, 1)
    sequential = 0
    for i in range(length - 2):
        if ord(password[i + 1]) - ord(password[i]) == 1 and ord(password[i + 2]) - ord(password[i + 1]) == 1:
            sequential += 1
    seq_ratio = sequential / max(length, 1)

    score = 0
    score += min(length * 3, 30)
    score += varieties * 15
    score += min(entropy / 2, 30)
    score -= repeats * 15
    score -= seq_ratio * 20
    score = max(0, min(100, int(score)))

    if score < 25:
        label = "Weak"
    elif score < 50:
        label = "Fair"
    elif score < 75:
        label = "Good"
    else:
        label = "Strong"

    return {"score": score, "length": length, "varieties": varieties,
            "entropy": round(entropy, 1), "label": label,
            "char_types": (has_lower, has_upper, has_digit, has_symbol)}


def create_ui(frame, COLORS, FONTS):
    input_var = ctk.StringVar()
    score_var = ctk.StringVar(value="0")
    label_var = ctk.StringVar(value="")
    detail_var = ctk.StringVar(value="")

    ctk.CTkLabel(frame, text="Password Strength Analyzer", font=FONTS["heading"],
                 text_color=COLORS["text"], anchor="w").pack(fill="x", padx=16, pady=(16, 8))

    inp_frame = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=10)
    inp_frame.pack(fill="x", padx=16, pady=(0, 8))

    inp = ctk.CTkEntry(inp_frame, textvariable=input_var, placeholder_text="Enter password...",
                       font=FONTS["mono"], fg_color=COLORS["bg_input"], text_color=COLORS["text"],
                       border_color=COLORS["border"], height=36, show="*")
    inp.pack(fill="x", padx=12, pady=10)

    def analyze(_=None):
        data = _analyze(input_var.get())
        score_var.set(str(data["score"]))
        color = COLORS["red"] if data["score"] < 25 else COLORS["yellow"] if data["score"] < 75 else COLORS["green"]
        label_var.set(f'{data["label"]}  ({data["score"]}/100)')
        type_names = ["Lowercase", "Uppercase", "Digits", "Symbols"]
        types_str = ", ".join(n for n, v in zip(type_names, data["char_types"]) if v) if data["varieties"] else "None"
        detail_var.set(
            f"Length: {data['length']}   |   Char types: {data['varieties']}/4 ({types_str})\n"
            f"Entropy: {data['entropy']} bits"
        )

    ctk.CTkButton(frame, text="Analyze", font=FONTS["button"], fg_color=COLORS["accent"],
                  hover_color=COLORS["green"], command=analyze).pack(fill="x", padx=16, pady=(0, 8))

    result_frame = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=10)
    result_frame.pack(fill="x", padx=16, pady=(0, 16))

    bar_frame = ctk.CTkFrame(result_frame, fg_color=COLORS["bg_input"], corner_radius=8, height=28)
    bar_frame.pack(fill="x", padx=12, pady=(12, 4))
    bar_frame.pack_propagate(False)
    bar_fill = ctk.CTkFrame(bar_frame, fg_color=COLORS["accent"], corner_radius=8, width=0)
    bar_fill.place(relx=0, rely=0, relheight=1.0, relwidth=0.0)

    ctk.CTkLabel(result_frame, textvariable=label_var, font=FONTS["heading"],
                 text_color=COLORS["text"], anchor="w").pack(fill="x", padx=12, pady=(8, 0))

    ctk.CTkLabel(result_frame, textvariable=detail_var, font=FONTS["mono_small"],
                 text_color=COLORS["text_dim"], anchor="w", justify="left").pack(fill="x", padx=12, pady=(4, 12))

    def on_input(*_):
        data = _analyze(input_var.get())
        fraction = data["score"] / 100
        color = COLORS["red"] if data["score"] < 25 else COLORS["yellow"] if data["score"] < 75 else COLORS["green"]
        bar_fill.configure(fg_color=color)
        bar_fill.place_configure(relwidth=fraction)
        analyze()

    input_var.trace_add("write", on_input)
