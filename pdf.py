import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re
import threading
from PIL import Image, ImageFile
import fitz  # PyMuPDF
import sys

ImageFile.LOAD_TRUNCATED_IMAGES = True

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ── 파스텔 카와이 레트로 팔레트 ──────────────────────────────────
BG_DESKTOP   = "#D8C0F0"   # 바탕 라벤더
BG_WINDOW    = "#FDE8F8"   # 창 내부 연핑크
TITLEBAR_BG  = "#C078D8"   # 타이틀바 보라
TITLEBAR_FG  = "#FFFFFF"   # 타이틀바 흰 글씨
BORDER_HI    = "#F8C8EC"   # 밝은 테두리 (highlight)
BORDER_SH    = "#9850B8"   # 어두운 테두리 (shadow)
PANEL_BG     = "#F0D8F8"   # 내부 패널 연보라
TEXT_MAIN    = "#5A2878"   # 메인 텍스트 진보라
BTN1_BG      = "#B8E8C0"   # 버튼1 파스텔 그린
BTN1_FG      = "#2A5030"
BTN1_ACTIVE  = "#D8F8D8"
BTN1_BORDER  = "#70A878"
BTN2_BG      = "#B8D8F8"   # 버튼2 파스텔 블루
BTN2_FG      = "#1A3060"
BTN2_ACTIVE  = "#D8ECFF"
BTN2_BORDER  = "#6890C8"
STATUS_BG    = "#E0C8F0"   # 상태바 연보라
CLOSEBTN_BG  = "#F098C8"   # X 버튼 핑크
# ─────────────────────────────────────────────────────────────────

def _bind_button_fx(btn):
    btn.bind("<ButtonPress-1>",   lambda e: btn.config(relief="sunken"))
    btn.bind("<ButtonRelease-1>", lambda e: btn.config(relief="raised"))

def natural_sort_key(path):
    """자연 정렬 키: '2.png' < '10.png' 순서 보장"""
    name = os.path.basename(path)
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', name)]

# 로딩 상태 관리
status_label = None  # 후에 UI 생성 시 할당
loading_anim_id = None

def show_loading():
    """상태바에 로딩 애니메이션 표시"""
    dots = [0]
    def animate():
        global loading_anim_id
        n = dots[0] % 4
        status_label.config(text=f"  ✦  열심히 작업중!!{'.' * n}")
        dots[0] += 1
        loading_anim_id = root.after(400, animate)
    animate()

def hide_loading():
    """로딩 애니메이션 중지 및 상태 복원"""
    global loading_anim_id
    if loading_anim_id:
        root.after_cancel(loading_anim_id)
        loading_anim_id = None
    status_label.config(text="  ☆  Ready  ☆")

def run_with_loading(task_func):
    """작업을 별도 스레드에서 실행하면서 로딩 표시"""
    show_loading()
    def wrapper():
        try:
            task_func()
        finally:
            root.after(0, hide_loading)
    threading.Thread(target=wrapper, daemon=True).start()

def images_to_pdf():
    image_paths = filedialog.askopenfilenames(
        title="PDF로 변환할 이미지 파일들을 선택하세요",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
    )
    if not image_paths:
        return

    # 자연 정렬: 1, 2, 3, ... 10, 11 순서 보장
    image_paths = sorted(image_paths, key=natural_sort_key)

    save_path = filedialog.asksaveasfilename(
        title="PDF를 저장할 위치와 이름을 지정하세요",
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if not save_path:
        return

    def task():
        try:
            images = [Image.open(p).convert('RGB') for p in image_paths]
            images[0].save(save_path, save_all=True, append_images=images[1:])
            root.after(0, lambda: messagebox.showinfo(
                "✿ 완료 ✿", "PDF 파일이 파일명 순서대로\n성공적으로 생성되었습니다!  ♡"))
        except Exception as e:
            root.after(0, lambda: messagebox.showerror(
                "× 오류 ×", f"PDF 생성 중 문제가 발생했습니다:\n{e}"))

    run_with_loading(task)

def pdf_to_pngs():
    pdf_path = filedialog.askopenfilename(
        title="PNG로 분해할 PDF 파일을 선택하세요",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if not pdf_path:
        return

    save_dir = filedialog.askdirectory(title="이미지들을 저장할 폴더를 선택하세요")
    if not save_dir:
        return

    def task():
        try:
            pdf_document = fitz.open(pdf_path)
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            total = len(pdf_document)

            for page_num in range(total):
                page = pdf_document.load_page(page_num)
                pix  = page.get_pixmap(dpi=300)
                output_path = os.path.join(save_dir, f"{base_name}_{page_num + 1}.png")
                pix.save(output_path)

            pdf_document.close()
            root.after(0, lambda: messagebox.showinfo(
                "✿ 완료 ✿", f"총 {total}장의 PNG 이미지가\n저장되었습니다!  ♡"))
        except Exception as e:
            root.after(0, lambda: messagebox.showerror(
                "× 오류 ×", f"PDF 분할 중 문제가 발생했습니다:\n{e}"))

    run_with_loading(task)


# ══════════════════════════════════════════════════════════════════
#  메인 창 구성
# ══════════════════════════════════════════════════════════════════
root = tk.Tk()
root.title("Image ↔ PDF Converter")
root.geometry("420x340")
root.resizable(False, False)
root.configure(bg=BG_DESKTOP)

try:
    root.iconbitmap(resource_path("app_icon.ico"))
except Exception:
    pass

# ── 바탕화면 격자 패턴 (Win9x 바탕화면 느낌) ─────────────────────
canvas_bg = tk.Canvas(root, width=420, height=340, bg=BG_DESKTOP,
                      highlightthickness=0)
canvas_bg.place(x=0, y=0)
for x in range(0, 420, 12):
    canvas_bg.create_line(x, 0, x, 340, fill="#CDB8E8", width=1)
for y in range(0, 340, 12):
    canvas_bg.create_line(0, y, 420, y, fill="#CDB8E8", width=1)

# ── 외부 창 프레임 (Win9x 입체 테두리) ───────────────────────────
outer = tk.Frame(root, bg=BORDER_HI, bd=0)
outer.place(x=14, y=14, width=392, height=312)

# 3D 테두리 효과: 밝은 외곽 → 어두운 내곽
tk.Frame(outer, bg=BORDER_HI, height=2).pack(side="top",    fill="x")
tk.Frame(outer, bg=BORDER_HI, width=2).pack(side="left",   fill="y")
tk.Frame(outer, bg=BORDER_SH, height=2).pack(side="bottom", fill="x")
tk.Frame(outer, bg=BORDER_SH, width=2).pack(side="right",  fill="y")

window_frame = tk.Frame(outer, bg=BG_WINDOW, bd=2, relief="groove")
window_frame.pack(fill="both", expand=True, padx=2, pady=2)

# ── 타이틀 바 ────────────────────────────────────────────────────
titlebar = tk.Frame(window_frame, bg=TITLEBAR_BG, height=28)
titlebar.pack(fill="x")
titlebar.pack_propagate(False)

tk.Label(titlebar,
         text="  ✦  Image  ↔  PDF  Converter  ✦",
         bg=TITLEBAR_BG, fg=TITLEBAR_FG,
         font=("MS Sans Serif", 9, "bold")).pack(side="left", pady=5)

for sym, clr in [("■", "#A0D0A0"), ("×", CLOSEBTN_BG)]:
    tk.Label(titlebar, text=f" {sym} ", bg=clr, fg="white",
             font=("MS Sans Serif", 8, "bold"),
             relief="raised", bd=2, padx=1
             ).pack(side="right", padx=2, pady=4)

# ── 창 본문 ──────────────────────────────────────────────────────
body = tk.Frame(window_frame, bg=BG_WINDOW, padx=16, pady=10)
body.pack(fill="both", expand=True)

# 안내 패널 (sunken 인셋 박스)
info_panel = tk.Frame(body, bg=PANEL_BG, bd=2, relief="sunken")
info_panel.pack(fill="x", pady=(0, 10))

tk.Label(info_panel,
         text="♡   원하시는 기능을 선택해주세요   ♡",
         bg=PANEL_BG, fg=TEXT_MAIN,
         font=("MS Sans Serif", 10, "bold"),
         pady=7).pack()

# ── 기능 버튼 ────────────────────────────────────────────────────
def make_button(parent, text, command, bg, fg, active_bg, shadow):
    wrap = tk.Frame(parent, bg=shadow, bd=1)
    wrap.pack(fill="x", pady=6)

    btn = tk.Button(wrap,
                    text=text,
                    command=command,
                    bg=bg, fg=fg,
                    activebackground=active_bg,
                    activeforeground=fg,
                    font=("MS Sans Serif", 9, "bold"),
                    relief="raised", bd=3,
                    cursor="hand2",
                    height=2)
    btn.pack(fill="x")
    _bind_button_fx(btn)
    return btn

make_button(
    body,
    text="  ✦  여러 이미지를 →  PDF 로 합치기\n        ( 파일명 순서대로 자동 정렬 )",
    command=images_to_pdf,
    bg=BTN1_BG, fg=BTN1_FG,
    active_bg=BTN1_ACTIVE,
    shadow=BTN1_BORDER
)

make_button(
    body,
    text="  ✦  PDF 파일을  →  여러 PNG 로 분할\n        ( 300 DPI  고화질 저장 )",
    command=pdf_to_pngs,
    bg=BTN2_BG, fg=BTN2_FG,
    active_bg=BTN2_ACTIVE,
    shadow=BTN2_BORDER
)

# ── 상태바 ───────────────────────────────────────────────────────
statusbar = tk.Frame(window_frame, bg=STATUS_BG, height=22, bd=1, relief="sunken")
statusbar.pack(fill="x", side="bottom")
statusbar.pack_propagate(False)

status_label = tk.Label(statusbar,
         text="  ☆  Ready  ☆",
         bg=STATUS_BG, fg=TEXT_MAIN,
         font=("MS Sans Serif", 7)
         )
status_label.pack(side="left", padx=6)

tk.Label(statusbar,
         text="v2.0  ♡  ",
         bg=STATUS_BG, fg=TEXT_MAIN,
         font=("MS Sans Serif", 7)
         ).pack(side="right", padx=6)

root.mainloop()
