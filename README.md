# Image ↔ PDF Converter

이미지와 PDF를 서로 바꾸는 데스크톱 툴입니다.
파일은 내 컴퓨터 안에서만 처리합니다.

## 기능

- 이미지 여러 장을 PDF 한 개로 합치기. PNG, JPG, BMP, GIF 지원
- PDF를 페이지마다 300 DPI PNG로 나누기

이미지를 합칠 때는 파일 이름을 자연 정렬합니다.
`2.png`가 `10.png`보다 앞에 옵니다.
나눈 PNG는 `원본이름_1.png`, `원본이름_2.png` 순서로 저장됩니다.
변환은 별도 스레드에서 돌고, 진행 중에는 상태바에 표시가 뜹니다.

## 실행

Python 3가 필요합니다. Tkinter는 Python에 포함돼 있습니다.

```bash
pip install -r requirements.txt
python pdf.py
```

창 아이콘은 현재 폴더의 `app_icon.ico`를 읽습니다.
저장소 폴더에서 실행하지 않으면 아이콘 없이 뜹니다.

## exe 빌드

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=app_icon.ico pdf.py
```

결과물은 `dist/pdf.exe`입니다.

## 파일

| 파일 | 내용 |
|---|---|
| `pdf.py` | 앱 전체 |
| `app_icon.ico` | 창과 exe 아이콘 |
| `requirements.txt` | 필요한 패키지. 이미지 합치기는 Pillow, PDF 나누기는 PyMuPDF |
