# Prompt 模板生成器 Pro（桌面版）

一个可视化、现代化的 Prompt 模板编辑器。支持模块化管理、双页签工作流、预设导入导出、实时预览同步，并可打包为 Windows EXE。

## 核心特性

- **双 Tab 工作流**
  - Tab1：模块查看 + 勾选启用 + 模块编辑（合并流程）
  - Tab2：检查 + 预览 + 导出
- **模块能力增强**
  - 模块改名
  - 新增/删除模块
  - 预览编辑反向同步到模块
- **预设管理**
  - 导入预设（JSON）
  - 导出预设（JSON）
  - 一键恢复默认预设
- **更现代 UI**
  - 深色/浅色主题切换
  - 卡片式布局 + 圆角控件 + 更清晰排版
- **实用增强功能**
  - 模块筛选
  - 占位符检查、空内容检查、标题完整性检查
  - 字符数统计
  - 一键复制 / 导出 TXT

## 本地运行

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## 在 Windows 打包 EXE（本地）

```bat
build_exe.bat
```

打包结果：

- `dist\PromptTemplateBuilder.exe`

## 如何下载 EXE（推荐）

本仓库已提供 GitHub Actions 自动构建工作流：

1. 打开仓库 `Actions` 页面。
2. 选择 **Build Windows EXE**。
3. 点击 **Run workflow**。
4. 任务完成后，在该次运行的 **Artifacts** 下载：
   - `PromptTemplateBuilder-windows-exe`

下载后解压即可得到 `PromptTemplateBuilder.exe`。

## 预设文件格式（JSON）

```json
{
  "version": 1,
  "modules": [
    {
      "key": "A",
      "title": "专家角色模块",
      "content": "...",
      "enabled": true
    }
  ]
}
```
