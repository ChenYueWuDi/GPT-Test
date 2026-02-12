import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSplitter,
    QStatusBar,
    QTabWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
)


@dataclass
class ModuleItem:
    key: str
    title: str
    content: str
    enabled: bool = True


DEFAULT_MODULES: List[ModuleItem] = [
    ModuleItem("A", "专家角色模块（可替换）", """你是一位领域顶级专家，在以下方向具备长期、系统、可验证的研究经验：

主领域：{主领域，如 等离子体物理 / 光学 / 加速器物理 / 机械工程 / 控制理论}
次领域（可多选）：{相关分支}

研究方法覆盖：
- 理论建模
- 数值模拟
- 实验设计与数据分析

你的回答应体现：
- 清晰的物理/工程图像
- 严格的假设与适用边界
- 可复现、可验证、可扩展的思路"""),
    ModuleItem("B", "用户背景模块（稳定）", """我是一名受过严格训练的专业研究人员（博士及以上水平），具备良好的数学、物理和工程基础。

你可以默认我能够理解：
- 方程、量纲分析、无量纲参数
- 常见近似、数值方法、实验不确定性

但请你：
- 把关键逻辑与物理因果链讲清楚
- 明确指出常见误区与失效条件"""),
    ModuleItem("C", "回答总原则（强约束）", """- 先框架，后细节
  - 先给最小自洽模型 / 控制方程 / 系统结构
  - 再展开推导、对比与结论
- 明确假设与边界
  - 所有近似必须说明：何时成立、何时失效
- 不确定性显式化
  - 无数据 ≠ 猜测
  - 请给出区间、主导不确定源、需要的补充信息
- 前沿问题给证据链
  - 教材 / 综述 / 原始论文 / 实验报告
  - 给出处、作者、年份（必要时给 DOI 或 arXiv）
- 科研导向
  - 不只回答“是什么”
  - 还要回答“如何验证 / 如何测量 / 如何模拟 / 如何反证”"""),
    ModuleItem("D", "标准输出结构模块（默认开启）", """若无特殊说明，请按以下结构输出：

1️⃣ 结论速览（Executive Summary）
- 3–6 条核心结论
- 给出物理或工程上的“为什么”

2️⃣ 物理 / 工程图像
- 核心机制
- 主导过程
- 因果关系

3️⃣ 模型与关键方程
- 控制方程
- 主要无量纲参数
- 主导项 vs 次要项

4️⃣ 对比表格（核心）
方案 / 机制	基本原理	关键参数	典型量级	优点	局限	适用条件	可观测量

5️⃣ 核心计算 / 数量级估算
- 明确步骤
- 明确单位
- 给出合理数量级或区间

6️⃣ 验证与预测
- 实验可测量量
- 参数扫描建议
- 诊断/数值/工程验证路径

7️⃣ 参考资料
- 教材
- 综述
- 原始论文
- 数据/实验来源"""),
    ModuleItem("E", "推导 / 计算 / 模拟规范（按需）", """当问题涉及计算或模拟时：

- 明确采用方法：
  - 解析 / 数值 / 半经验
- 若是模拟，说明：
  - 模型类型（流体 / PIC / MHD / FEM / 控制模型等）
  - 边界条件
  - 时间与空间分辨率限制
  - 常见数值陷阱"""),
    ModuleItem("F", "问题定义模块（每次只填这里）", """问题陈述：
{用一句话描述问题}

目标量 / 关注指标：
{如 能量约束时间 / 诊断信噪比 / 稳定性阈值 / 精度 / 成本}

希望解决的核心矛盾：
{效率 vs 稳定性 / 精度 vs 成本 / 理论 vs 实验}"""),
    ModuleItem("G", "已知条件模块（可选填）", """几何/结构参数：
场/边界条件：
时间尺度 / 空间尺度：
已知实验或模拟结果：
可用诊断 / 计算资源：

若未给出，请你采用物理上合理的默认假设并明确说明。"""),
    ModuleItem("H", "输出控制开关（每次可改）", """深度级别：科普 / 研究生 / 论文级（默认：研究生）
数学强度：低 / 中 / 高（默认：中-高）
对比强度：单方案 / 多方案对比 / 全景对比
计算程度：
- 不需要
- 数量级估算
- 推导 + 估算
- 推导 + 估算 + 不确定性分析
输出长度：短 / 中 / 长"""),
]


def modern_stylesheet(dark: bool = True) -> str:
    if dark:
        return """
        QMainWindow { background: #161B22; }
        QWidget { color: #E6EDF3; font-size: 13px; }
        QTabWidget::pane { border: 1px solid #30363D; border-radius: 10px; background: #0D1117; }
        QTabBar::tab { background: #21262D; border: 1px solid #30363D; padding: 10px 16px; border-top-left-radius: 8px; border-top-right-radius: 8px; margin-right: 5px; }
        QTabBar::tab:selected { background: #2F81F7; color: white; border-color: #2F81F7; }
        QPlainTextEdit, QListWidget, QLineEdit { background: #0D1117; border: 1px solid #30363D; border-radius: 8px; padding: 8px; selection-background-color: #2F81F7; }
        QPushButton { background: #238636; border: none; border-radius: 8px; padding: 8px 14px; color: white; }
        QPushButton:hover { background: #2EA043; }
        QPushButton:pressed { background: #1A7F37; }
        QStatusBar { background: #0D1117; border-top: 1px solid #30363D; }
        QToolBar { background: #0D1117; border-bottom: 1px solid #30363D; spacing: 8px; }
        QFrame#Card { background: #0D1117; border: 1px solid #30363D; border-radius: 10px; }
        """
    return """
    QMainWindow { background: #F6F8FA; }
    QWidget { color: #24292F; font-size: 13px; }
    QTabWidget::pane { border: 1px solid #D0D7DE; border-radius: 10px; background: white; }
    QTabBar::tab { background: #EAEEF2; border: 1px solid #D0D7DE; padding: 10px 16px; border-top-left-radius: 8px; border-top-right-radius: 8px; margin-right: 5px; }
    QTabBar::tab:selected { background: #0969DA; color: white; border-color: #0969DA; }
    QPlainTextEdit, QListWidget, QLineEdit { background: white; border: 1px solid #D0D7DE; border-radius: 8px; padding: 8px; selection-background-color: #0969DA; }
    QPushButton { background: #1A7F37; border: none; border-radius: 8px; padding: 8px 14px; color: white; }
    QPushButton:hover { background: #2DA44E; }
    QStatusBar { background: white; border-top: 1px solid #D0D7DE; }
    QToolBar { background: white; border-bottom: 1px solid #D0D7DE; spacing: 8px; }
    QFrame#Card { background: white; border: 1px solid #D0D7DE; border-radius: 10px; }
    """


class PromptBuilderWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Prompt 模板生成器 Pro")
        self.resize(1280, 820)
        self.modules: List[ModuleItem] = [ModuleItem(**asdict(m)) for m in DEFAULT_MODULES]
        self.syncing = False
        self.dark_theme = True

        self._build_ui()
        self._connect_signals()
        self.apply_theme()
        self.refresh_module_list()
        self.module_list.setCurrentRow(0)
        self.refresh_preview_from_modules()

    def _build_ui(self) -> None:
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        self.new_action = QAction("新建预设", self)
        self.import_action = QAction("导入预设", self)
        self.export_preset_action = QAction("导出预设", self)
        self.theme_action = QAction("切换主题", self)
        self.theme_action.setCheckable(True)
        self.theme_action.setChecked(True)

        toolbar.addAction(self.new_action)
        toolbar.addAction(self.import_action)
        toolbar.addAction(self.export_preset_action)
        toolbar.addSeparator()
        toolbar.addAction(self.theme_action)

        tabs = QTabWidget(self)
        tabs.setDocumentMode(True)
        self.setCentralWidget(tabs)

        tab1 = QWidget()
        tab1_layout = QVBoxLayout(tab1)
        splitter = QSplitter(Qt.Horizontal)
        tab1_layout.addWidget(splitter)

        left_card = QFrame()
        left_card.setObjectName("Card")
        left_layout = QVBoxLayout(left_card)
        left_layout.addWidget(QLabel("模块中心"))
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("筛选模块（按名称）...")
        left_layout.addWidget(self.filter_input)

        self.module_list = QListWidget()
        left_layout.addWidget(self.module_list)

        left_buttons = QHBoxLayout()
        self.add_btn = QPushButton("新增")
        self.delete_btn = QPushButton("删除")
        left_buttons.addWidget(self.add_btn)
        left_buttons.addWidget(self.delete_btn)
        left_layout.addLayout(left_buttons)

        right_card = QFrame()
        right_card.setObjectName("Card")
        right_layout = QVBoxLayout(right_card)

        self.current_module_label = QLabel("当前模块")
        label_font = QFont()
        label_font.setPointSize(14)
        label_font.setBold(True)
        self.current_module_label.setFont(label_font)
        right_layout.addWidget(self.current_module_label)

        rename_row = QHBoxLayout()
        self.rename_input = QLineEdit()
        self.rename_input.setPlaceholderText("修改模块标题...")
        self.apply_rename_btn = QPushButton("保存标题")
        rename_row.addWidget(self.rename_input)
        rename_row.addWidget(self.apply_rename_btn)
        right_layout.addLayout(rename_row)

        self.module_editor = QPlainTextEdit()
        self.module_editor.setPlaceholderText("编辑模块内容...")
        right_layout.addWidget(self.module_editor)

        row = QHBoxLayout()
        self.reset_current_btn = QPushButton("重置当前模块")
        self.sync_preview_btn = QPushButton("同步到预览")
        row.addWidget(self.reset_current_btn)
        row.addStretch(1)
        row.addWidget(self.sync_preview_btn)
        right_layout.addLayout(row)

        splitter.addWidget(left_card)
        splitter.addWidget(right_card)
        splitter.setSizes([360, 880])
        tabs.addTab(tab1, "模块查看与编辑")

        tab2 = QWidget()
        tab2_layout = QVBoxLayout(tab2)

        check_card = QFrame()
        check_card.setObjectName("Card")
        check_layout = QFormLayout(check_card)
        self.header_check = QCheckBox("检查模块标题完整性")
        self.empty_check = QCheckBox("检查空内容")
        self.placeholder_check = QCheckBox("检查占位符（{...}）")
        self.header_check.setChecked(True)
        self.empty_check.setChecked(True)
        self.placeholder_check.setChecked(False)
        check_layout.addRow("检查规则", self.header_check)
        check_layout.addRow("", self.empty_check)
        check_layout.addRow("", self.placeholder_check)
        tab2_layout.addWidget(check_card)

        self.preview_editor = QPlainTextEdit()
        self.preview_editor.setPlaceholderText("预览 / 即时修改最终 Prompt（可回写）")
        tab2_layout.addWidget(self.preview_editor)

        bottom = QHBoxLayout()
        self.validate_btn = QPushButton("执行检查")
        self.copy_btn = QPushButton("复制")
        self.export_txt_btn = QPushButton("导出TXT")
        self.word_count_label = QLabel("字符数: 0")
        bottom.addWidget(self.validate_btn)
        bottom.addWidget(self.copy_btn)
        bottom.addWidget(self.export_txt_btn)
        bottom.addStretch(1)
        bottom.addWidget(self.word_count_label)
        tab2_layout.addLayout(bottom)

        tabs.addTab(tab2, "检查、预览与导出")

        self.setStatusBar(QStatusBar())

    def _connect_signals(self) -> None:
        self.new_action.triggered.connect(self.reset_all_modules)
        self.import_action.triggered.connect(self.import_preset)
        self.export_preset_action.triggered.connect(self.export_preset)
        self.theme_action.triggered.connect(self.toggle_theme)

        self.filter_input.textChanged.connect(self.refresh_module_list)
        self.module_list.currentRowChanged.connect(self.load_current_module)
        self.module_list.itemChanged.connect(self.on_checked_changed)

        self.module_editor.textChanged.connect(self.on_module_text_changed)
        self.preview_editor.textChanged.connect(self.on_preview_text_changed)

        self.apply_rename_btn.clicked.connect(self.rename_current_module)
        self.add_btn.clicked.connect(self.add_module)
        self.delete_btn.clicked.connect(self.delete_current_module)
        self.reset_current_btn.clicked.connect(self.reset_current_module)
        self.sync_preview_btn.clicked.connect(self.refresh_preview_from_modules)

        self.validate_btn.clicked.connect(self.validate_preview)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.export_txt_btn.clicked.connect(self.export_prompt_txt)

    def apply_theme(self) -> None:
        self.setStyleSheet(modern_stylesheet(self.dark_theme))

    def toggle_theme(self) -> None:
        self.dark_theme = self.theme_action.isChecked()
        self.apply_theme()

    def refresh_module_list(self) -> None:
        keyword = self.filter_input.text().strip().lower() if hasattr(self, "filter_input") else ""
        selected_key = self.active_key()

        self.syncing = True
        self.module_list.clear()
        for module in self.modules:
            if keyword and keyword not in module.title.lower() and keyword not in module.key.lower():
                continue
            item = QListWidgetItem(f"[{module.key}] {module.title}")
            item.setData(Qt.UserRole, module.key)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked if module.enabled else Qt.Unchecked)
            self.module_list.addItem(item)
        self.syncing = False

        if self.module_list.count() > 0:
            row = self.find_row_by_key(selected_key) if selected_key else 0
            self.module_list.setCurrentRow(max(0, row))

    def find_row_by_key(self, key: Optional[str]) -> int:
        if not key:
            return 0
        for i in range(self.module_list.count()):
            if self.module_list.item(i).data(Qt.UserRole) == key:
                return i
        return 0

    def active_key(self) -> Optional[str]:
        item = self.module_list.currentItem()
        return item.data(Qt.UserRole) if item else None

    def get_module(self, key: str) -> Optional[ModuleItem]:
        return next((m for m in self.modules if m.key == key), None)

    def load_current_module(self) -> None:
        key = self.active_key()
        if not key:
            return
        module = self.get_module(key)
        if not module:
            return
        self.syncing = True
        self.current_module_label.setText(f"当前模块: [{module.key}] {module.title}")
        self.rename_input.setText(module.title)
        self.module_editor.setPlainText(module.content)
        self.syncing = False

    def on_checked_changed(self, item: QListWidgetItem) -> None:
        if self.syncing:
            return
        key = item.data(Qt.UserRole)
        module = self.get_module(key)
        if module:
            module.enabled = item.checkState() == Qt.Checked
            self.refresh_preview_from_modules()

    def on_module_text_changed(self) -> None:
        if self.syncing:
            return
        key = self.active_key()
        if not key:
            return
        module = self.get_module(key)
        if module:
            module.content = self.module_editor.toPlainText()
            self.refresh_preview_from_modules()

    def rename_current_module(self) -> None:
        key = self.active_key()
        title = self.rename_input.text().strip()
        if not key or not title:
            return
        module = self.get_module(key)
        if module:
            module.title = title
            self.refresh_module_list()
            self.refresh_preview_from_modules()
            self.statusBar().showMessage("模块标题已更新", 1800)

    def next_key(self) -> str:
        existing = {m.key for m in self.modules}
        for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if c not in existing:
                return c
        return f"M{len(self.modules) + 1}"

    def add_module(self) -> None:
        key = self.next_key()
        module = ModuleItem(key=key, title=f"新模块 {key}", content="请输入模块内容...", enabled=True)
        self.modules.append(module)
        self.refresh_module_list()
        self.module_list.setCurrentRow(self.find_row_by_key(key))
        self.refresh_preview_from_modules()

    def delete_current_module(self) -> None:
        key = self.active_key()
        if not key:
            return
        if len(self.modules) <= 1:
            QMessageBox.warning(self, "提示", "至少保留一个模块。")
            return
        self.modules = [m for m in self.modules if m.key != key]
        self.refresh_module_list()
        self.refresh_preview_from_modules()

    def reset_current_module(self) -> None:
        key = self.active_key()
        if not key:
            return
        default = next((m for m in DEFAULT_MODULES if m.key == key), None)
        module = self.get_module(key)
        if module:
            module.content = default.content if default else ""
            if default:
                module.title = default.title
            self.load_current_module()
            self.refresh_module_list()
            self.refresh_preview_from_modules()

    def reset_all_modules(self) -> None:
        self.modules = [ModuleItem(**asdict(m)) for m in DEFAULT_MODULES]
        self.refresh_module_list()
        self.module_list.setCurrentRow(0)
        self.refresh_preview_from_modules()
        self.statusBar().showMessage("已恢复默认预设", 1800)

    def compose_prompt(self) -> str:
        sections = []
        for module in self.modules:
            if module.enabled:
                sections.append(f"### [{module.key}] {module.title}\n{module.content.strip()}\n")
        return "\n".join(sections).strip() + "\n"

    def refresh_preview_from_modules(self) -> None:
        if self.syncing:
            return
        self.syncing = True
        text = self.compose_prompt()
        self.preview_editor.setPlainText(text)
        self.word_count_label.setText(f"字符数: {len(text)}")
        self.syncing = False

    def parse_preview_back(self, text: str) -> bool:
        lines = text.splitlines()
        parsed: List[ModuleItem] = []
        current: Optional[ModuleItem] = None

        for line in lines:
            if line.startswith("### [") and "] " in line:
                if current:
                    current.content = current.content.strip()
                    parsed.append(current)
                marker = line[5:]
                key, title = marker.split("] ", 1)
                current = ModuleItem(key=key, title=title.strip(), content="", enabled=True)
            elif current:
                current.content += line + "\n"

        if current:
            current.content = current.content.strip()
            parsed.append(current)

        if not parsed:
            return False

        existing_map: Dict[str, ModuleItem] = {m.key: m for m in self.modules}
        new_modules: List[ModuleItem] = []
        for p in parsed:
            enabled = existing_map.get(p.key).enabled if p.key in existing_map else True
            p.enabled = enabled
            new_modules.append(p)

        self.modules = new_modules
        self.refresh_module_list()
        self.module_list.setCurrentRow(0)
        return True

    def on_preview_text_changed(self) -> None:
        if self.syncing:
            return
        ok = self.parse_preview_back(self.preview_editor.toPlainText())
        self.word_count_label.setText(f"字符数: {len(self.preview_editor.toPlainText())}")
        if ok:
            self.load_current_module()
            self.statusBar().showMessage("预览修改已同步回模块", 1800)
        else:
            self.statusBar().showMessage("预览格式未匹配，暂未同步", 2200)

    def validate_preview(self) -> None:
        warnings: List[str] = []
        preview = self.preview_editor.toPlainText()

        if self.header_check.isChecked():
            for m in self.modules:
                if m.enabled and f"### [{m.key}] {m.title}" not in preview:
                    warnings.append(f"缺少标题：[{m.key}] {m.title}")
        if self.empty_check.isChecked():
            for m in self.modules:
                if m.enabled and not m.content.strip():
                    warnings.append(f"模块 [{m.key}] 内容为空")
        if self.placeholder_check.isChecked() and "{" in preview and "}" in preview:
            warnings.append("检测到未替换的占位符，请确认是否需要保留。")

        if warnings:
            QMessageBox.warning(self, "检查结果", "\n".join(warnings))
            self.statusBar().showMessage("检查完成：有待处理项", 2500)
        else:
            QMessageBox.information(self, "检查结果", "检查通过，结构与内容均正常。")
            self.statusBar().showMessage("检查通过", 1500)

    def export_prompt_txt(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "导出 Prompt", "prompt_template.txt", "Text Files (*.txt)")
        if not path:
            return
        Path(path).write_text(self.preview_editor.toPlainText().strip() + "\n", encoding="utf-8")
        self.statusBar().showMessage(f"已导出 TXT：{path}", 2200)

    def export_preset(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "导出预设", "prompt_preset.json", "JSON Files (*.json)")
        if not path:
            return
        payload = {"version": 1, "modules": [asdict(m) for m in self.modules]}
        Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        self.statusBar().showMessage(f"预设已导出：{path}", 2200)

    def import_preset(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "导入预设", "", "JSON Files (*.json)")
        if not path:
            return
        try:
            payload = json.loads(Path(path).read_text(encoding="utf-8"))
            modules = [ModuleItem(**m) for m in payload.get("modules", [])]
            if not modules:
                raise ValueError("未读取到模块")
        except Exception as exc:
            QMessageBox.critical(self, "导入失败", f"导入预设失败：{exc}")
            return

        self.modules = modules
        self.refresh_module_list()
        self.module_list.setCurrentRow(0)
        self.refresh_preview_from_modules()
        self.statusBar().showMessage(f"已导入预设：{path}", 2200)

    def copy_to_clipboard(self) -> None:
        QApplication.clipboard().setText(self.preview_editor.toPlainText())
        self.statusBar().showMessage("已复制到剪贴板", 1500)


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("Prompt 模板生成器 Pro")
    window = PromptBuilderWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
