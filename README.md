# Prompt 模板生成器（桌面版）

这是一个基于 **PySide6** 的桌面工具，用于按模块组合并编辑 Prompt 模板，最终导出文本。

## 功能

- 两页 Tab：
  - **模块查看与编辑**：查看模块、勾选启用、编辑当前模块。
  - **检查、预览与导出**：检查结构、预览完整 Prompt、直接编辑预览并回写同步、导出 TXT。
- 模块 A-H 已内置。
- 预览页修改后，可同步回第一页模块内容。
- 支持复制到剪贴板和导出文本。

## 本地运行

```bash
python -m venv .venv
source .venv/bin/activate  # Windows 用 .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## 打包 EXE（Windows）

在 Windows 命令行执行：

```bat
build_exe.bat
```

产物路径：

- `dist\PromptTemplateBuilder.exe`

## 说明

如果你当前在 Linux 环境中开发，本仓库提供的是 Windows 打包脚本；请在 Windows 环境执行 `build_exe.bat` 生成可下载的 `.exe`。
