# Image ↔ PDF Converter

Windows 98 감성의 파스텔 카와이 UI로 만든 이미지 ↔ PDF 변환 데스크톱 툴입니다. 별도 서버나 온라인 업로드 없이 로컬에서 즉시 변환됩니다.

## 기능

- **여러 이미지 → PDF 합치기**: PNG/JPG/JPEG/BMP/GIF 여러 장을 선택하면 파일명을 자연 정렬(`2.png` < `10.png`)해서 순서대로 이어붙인 PDF 한 장으로 저장합니다.
- **PDF → PNG 분할**: PDF 파일을 페이지별로 300 DPI 고화질 PNG로 저장합니다.
- 변환 작업은 별도 스레드에서 돌아가 UI가 멈추지 않고, 상태바에 진행 애니메이션이 표시됩니다.

## 스크린샷

*(추가 예정)*

## 실행 방법

```bash
pip install pillow pymupdf
python pdf.py
```

## exe로 빌드하기

PyInstaller로 아이콘 포함 단일 실행 파일을 만들 수 있습니다.

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=app_icon.ico pdf.py
```

## 기술 스택

- Python 3 + Tkinter (GUI)
- [Pillow](https://python-pillow.org/) — 이미지 → PDF 변환
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) — PDF → PNG 렌더링
