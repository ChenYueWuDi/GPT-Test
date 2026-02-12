@echo off
setlocal

if not exist .venv (
  python -m venv .venv
)

call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

pyinstaller --noconfirm --windowed --onefile --name PromptTemplateBuilder app.py

echo.
echo Build complete. EXE path:
echo dist\PromptTemplateBuilder.exe
pause
