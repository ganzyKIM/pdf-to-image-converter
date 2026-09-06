# Image ↔ PDF Converter

이미지와 PDF를 양방향으로 변환하는 데스크톱 툴. 업로드 없이 로컬에서 처리한다. Windows 98 풍 파스텔 UI.

## 기능

- **이미지 → PDF**: PNG·JPG·JPEG·BMP·GIF를 골라 한 장의 PDF로 이어붙인다.
  파일명은 자연 정렬이라 `2.png`가 `10.png`보다 앞에 온다.
- **PDF → PNG**: 페이지별로 300 DPI PNG로 저장한다.

변환은 별도 스레드에서 돌고, 진행 상황은 상태바에 표시된다.

## 실행

```bash
pip install pillow pymupdf
python pdf.py
```

## exe 빌드

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=app_icon.ico pdf.py
```

## 스택

Python 3 · Tkinter · [Pillow](https://python-pillow.org/)(이미지→PDF) · [PyMuPDF](https://pymupdf.readthedocs.io/)(PDF→PNG)
