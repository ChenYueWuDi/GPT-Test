import sys
from dataclasses import dataclass
from typing import Dict, List

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSplitter,
    QStatusBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


@dataclass
class ModuleItem:
    key: str
    title: str
    content: str


MODULES: List[ModuleItem] = [
    ModuleItem(
        "A",
        "A. 专家角色模块（可替换）",
        """你是一位领域顶级专家，在以下方向具备长期、系统、可验证的研究经验：\n\n"
        "主领域：{主领域，如 等离子体物理 / 光学 / 加速器物理 / 机械工程 / 控制理论}\n\n"
        "次领域（可多选）：{相关分支}\n\n"
        "研究方法覆盖：\n"
        "- 理论建模\n"
        "- 数值模拟\n"
        "- 实验设计与数据分析\n\n"
        "你的回答应体现：\n"
        "- 清晰的物理/工程图像\n"
        "- 严格的假设与适用边界\n"
        "- 可复现、可验证、可扩展的思路""",
    ),
    ModuleItem(
        "B",
        "B. 用户背景模块（稳定）",
        """我是一名受过严格训练的专业研究人员（博士及以上水平），具备良好的数学、物理和工程基础。\n\n"
        "你可以默认我能够理解：\n"
        "- 方程、量纲分析、无量纲参数\n"
        "- 常见近似、数值方法、实验不确定性\n\n"
        "但请你：\n"
        "- 把关键逻辑与物理因果链讲清楚\n"
        "- 明确指出常见误区与失效条件""",
    ),
    ModuleItem(
        "C",
        "C. 回答总原则（强约束）",
        """- 先框架，后细节\n"
        "  - 先给最小自洽模型 / 控制方程 / 系统结构\n"
        "  - 再展开推导、对比与结论\n"
        "- 明确假设与边界\n"
        "  - 所有近似必须说明：何时成立、何时失效\n"
        "- 不确定性显式化\n"
        "  - 无数据 ≠ 猜测\n"
        "  - 请给出区间、主导不确定源、需要的补充信息\n"
        "- 前沿问题给证据链\n"
        "  - 教材 / 综述 / 原始论文 / 实验报告\n"
        "  - 给出处、作者、年份（必要时给 DOI 或 arXiv）\n"
        "- 科研导向\n"
        "  - 不只回答“是什么”\n"
        "  - 还要回答“如何验证 / 如何测量 / 如何模拟 / 如何反证”""",
    ),
    ModuleItem(
        "D",
        "D. 标准输出结构模块（默认开启）",
        """若无特殊说明，请按以下结构输出：\n\n"
        "1️⃣ 结论速览（Executive Summary）\n"
        "- 3–6 条核心结论\n"
        "- 给出物理或工程上的“为什么”\n\n"
        "2️⃣ 物理 / 工程图像\n"
        "- 核心机制\n"
        "- 主导过程\n"
        "- 因果关系\n\n"
        "3️⃣ 模型与关键方程\n"
        "- 控制方程\n"
        "- 主要无量纲参数\n"
        "- 主导项 vs 次要项\n\n"
        "4️⃣ 对比表格（核心）\n"
        "方案 / 机制\t基本原理\t关键参数\t典型量级\t优点\t局限\t适用条件\t可观测量\n\n"
        "5️⃣ 核心计算 / 数量级估算\n"
        "- 明确步骤\n"
        "- 明确单位\n"
        "- 给出合理数量级或区间\n\n"
        "6️⃣ 验证与预测\n"
        "- 实验可测量量\n"
        "- 参数扫描建议\n"
        "- 诊断/数值/工程验证路径\n\n"
        "7️⃣ 参考资料\n"
        "- 教材\n"
        "- 综述\n"
        "- 原始论文\n"
        "- 数据/实验来源""",
    ),
    ModuleItem(
        "E",
        "E. 推导 / 计算 / 模拟规范（按需）",
        """当问题涉及计算或模拟时：\n\n"
        "- 明确采用方法：\n"
        "  - 解析 / 数值 / 半经验\n"
        "- 若是模拟，说明：\n"
        "  - 模型类型（流体 / PIC / MHD / FEM / 控制模型等）\n"
        "  - 边界条件\n"
        "  - 时间与空间分辨率限制\n"
        "  - 常见数值陷阱""",
    ),
    ModuleItem(
        "F",
        "F. 问题定义模块（每次只填这里）",
        """问题陈述：\n{用一句话描述问题}\n\n"
        "目标量 / 关注指标：\n{如 能量约束时间 / 诊断信噪比 / 稳定性阈值 / 精度 / 成本}\n\n"
        "希望解决的核心矛盾：\n{效率 vs 稳定性 / 精度 vs 成本 / 理论 vs 实验}""",
    ),
    ModuleItem(
        "G",
        "G. 已知条件模块（可选填）",
        """几何/结构参数：\n\n"
        "场/边界条件：\n\n"
        "时间尺度 / 空间尺度：\n\n"
        "已知实验或模拟结果：\n\n"
        "可用诊断 / 计算资源：\n\n"
        "若未给出，请你采用物理上合理的默认假设并明确说明。""",
    ),
    ModuleItem(
        "H",
        "H. 输出控制开关（每次可改）",
        """深度级别：科普 / 研究生 / 论文级（默认：研究生）\n"
        "数学强度：低 / 中 / 高（默认：中-高）\n"
        "对比强度：单方案 / 多方案对比 / 全景对比\n"
        "计算程度：\n- 不需要\n- 数量级估算\n- 推导 + 估算\n- 推导 + 估算 + 不确定性分析\n"
        "输出长度：短 / 中 / 长""",
    ),
]


class PromptBuilderWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Prompt 模板生成器")
        self.resize(1180, 760)

        self.module_data: Dict[str, str] = {m.key: m.content for m in MODULES}
        self.module_titles: Dict[str, str] = {m.key: m.title for m in MODULES}
        self.include_flags: Dict[str, bool] = {m.key: True for m in MODULES}
        self.syncing = False

        self._build_ui()
        self._connect_signals()
        self.refresh_preview_from_modules()

    def _build_ui(self) -> None:
        tabs = QTabWidget(self)
        tabs.setDocumentMode(True)
        self.setCentralWidget(tabs)

        # TAB 1
        tab1 = QWidget()
        tab1_layout = QVBoxLayout(tab1)

        splitter = QSplitter(Qt.Horizontal)
        tab1_layout.addWidget(splitter)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QLabel("模块列表（勾选后会参与最终 Prompt）"))

        self.module_list = QListWidget()
        for m in MODULES:
            item = QListWidgetItem(f"[{m.key}] {m.title}")
            item.setCheckState(Qt.Checked)
            item.setData(Qt.UserRole, m.key)
            self.module_list.addItem(item)
        left_layout.addWidget(self.module_list)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.current_module_label = QLabel("当前模块：")
        right_layout.addWidget(self.current_module_label)

        self.module_editor = QPlainTextEdit()
        self.module_editor.setPlaceholderText("在这里编辑当前模块内容...")
        right_layout.addWidget(self.module_editor)

        actions_row = QHBoxLayout()
        self.reset_current_btn = QPushButton("重置当前模块")
        self.preview_now_btn = QPushButton("同步到预览")
        actions_row.addWidget(self.reset_current_btn)
        actions_row.addStretch(1)
        actions_row.addWidget(self.preview_now_btn)
        right_layout.addLayout(actions_row)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([370, 810])

        tabs.addTab(tab1, "模块查看与编辑")

        # TAB 2
        tab2 = QWidget()
        tab2_layout = QVBoxLayout(tab2)

        check_wrap = QWidget()
        form = QFormLayout(check_wrap)
        self.deep_check = QCheckBox("检查模块标题完整性")
        self.empty_check = QCheckBox("检查内容为空的模块")
        self.deep_check.setChecked(True)
        self.empty_check.setChecked(True)
        form.addRow("检查项：", self.deep_check)
        form.addRow("", self.empty_check)
        tab2_layout.addWidget(check_wrap)

        tab2_layout.addWidget(QLabel("预览与即时修改（这里修改会同步到模块编辑页）"))
        self.preview_editor = QPlainTextEdit()
        self.preview_editor.setPlaceholderText("生成的完整 Prompt 会显示在这里，可直接编辑...")
        tab2_layout.addWidget(self.preview_editor)

        bottom_row = QHBoxLayout()
        self.validate_btn = QPushButton("执行检查")
        self.export_btn = QPushButton("导出为 TXT")
        self.copy_btn = QPushButton("复制到剪贴板")
        bottom_row.addWidget(self.validate_btn)
        bottom_row.addStretch(1)
        bottom_row.addWidget(self.copy_btn)
        bottom_row.addWidget(self.export_btn)
        tab2_layout.addLayout(bottom_row)

        tabs.addTab(tab2, "检查、预览与导出")

        status = QStatusBar()
        self.setStatusBar(status)

        export_action = QAction("导出", self)
        export_action.triggered.connect(self.export_prompt)
        self.menuBar().addAction(export_action)

        self.module_list.setCurrentRow(0)
        self._load_current_module_editor()

    def _connect_signals(self) -> None:
        self.module_list.currentRowChanged.connect(self._load_current_module_editor)
        self.module_list.itemChanged.connect(self._on_module_checked_changed)
        self.module_editor.textChanged.connect(self._on_module_text_changed)
        self.preview_editor.textChanged.connect(self._on_preview_text_changed)
        self.reset_current_btn.clicked.connect(self._reset_current_module)
        self.preview_now_btn.clicked.connect(self.refresh_preview_from_modules)
        self.validate_btn.clicked.connect(self.validate_preview)
        self.export_btn.clicked.connect(self.export_prompt)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)

    def _active_key(self) -> str:
        item = self.module_list.currentItem()
        return item.data(Qt.UserRole) if item else "A"

    def _load_current_module_editor(self) -> None:
        key = self._active_key()
        self.syncing = True
        self.current_module_label.setText(f"当前模块：[{key}] {self.module_titles.get(key, '')}")
        self.module_editor.setPlainText(self.module_data.get(key, ""))
        self.syncing = False

    def _on_module_checked_changed(self, item: QListWidgetItem) -> None:
        key = item.data(Qt.UserRole)
        self.include_flags[key] = item.checkState() == Qt.Checked
        self.refresh_preview_from_modules()

    def _on_module_text_changed(self) -> None:
        if self.syncing:
            return
        key = self._active_key()
        self.module_data[key] = self.module_editor.toPlainText()
        self.refresh_preview_from_modules()

    def _compose_prompt(self) -> str:
        sections = []
        for m in MODULES:
            if self.include_flags.get(m.key, True):
                title = self.module_titles[m.key]
                body = self.module_data[m.key].strip()
                sections.append(f"### 【{title}】\n{body}\n")
        return "\n".join(sections).strip() + "\n"

    def refresh_preview_from_modules(self) -> None:
        if self.syncing:
            return
        self.syncing = True
        self.preview_editor.setPlainText(self._compose_prompt())
        self.syncing = False
        self.statusBar().showMessage("预览已同步", 1800)

    def _parse_preview_back(self, preview_text: str) -> bool:
        marker_map = {f"### 【{self.module_titles[m.key]}】": m.key for m in MODULES}
        chunks: Dict[str, List[str]] = {}
        current_key = None

        for line in preview_text.splitlines():
            stripped = line.strip()
            if stripped in marker_map:
                current_key = marker_map[stripped]
                chunks[current_key] = []
                continue
            if current_key:
                chunks[current_key].append(line)

        if not chunks:
            return False

        for m in MODULES:
            key = m.key
            if key in chunks:
                self.module_data[key] = "\n".join(chunks[key]).strip()
                self.include_flags[key] = True
            else:
                self.include_flags[key] = False

        self.syncing = True
        for i in range(self.module_list.count()):
            item = self.module_list.item(i)
            key = item.data(Qt.UserRole)
            item.setCheckState(Qt.Checked if self.include_flags.get(key, False) else Qt.Unchecked)
        self.syncing = False

        self._load_current_module_editor()
        return True

    def _on_preview_text_changed(self) -> None:
        if self.syncing:
            return
        ok = self._parse_preview_back(self.preview_editor.toPlainText())
        if ok:
            self.statusBar().showMessage("预览修改已同步到模块", 1800)
        else:
            self.statusBar().showMessage("未识别到标准模块标题，暂未同步", 2200)

    def _reset_current_module(self) -> None:
        key = self._active_key()
        template = next((m.content for m in MODULES if m.key == key), "")
        self.module_data[key] = template
        self._load_current_module_editor()
        self.refresh_preview_from_modules()

    def validate_preview(self) -> None:
        warnings = []
        if self.deep_check.isChecked():
            for m in MODULES:
                if self.include_flags.get(m.key, True):
                    header = f"### 【{self.module_titles[m.key]}】"
                    if header not in self.preview_editor.toPlainText():
                        warnings.append(f"缺少标题: {header}")

        if self.empty_check.isChecked():
            for m in MODULES:
                if self.include_flags.get(m.key, True) and not self.module_data[m.key].strip():
                    warnings.append(f"模块 [{m.key}] 内容为空")

        if warnings:
            QMessageBox.warning(self, "检查结果", "\n".join(warnings))
            self.statusBar().showMessage("检查完成：存在问题", 2600)
        else:
            QMessageBox.information(self, "检查结果", "检查通过：模块结构完整。")
            self.statusBar().showMessage("检查通过", 1800)

    def export_prompt(self) -> None:
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "导出 Prompt",
            "prompt_template.txt",
            "Text Files (*.txt)",
        )
        if not file_path:
            return
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.preview_editor.toPlainText().strip() + "\n")
        self.statusBar().showMessage(f"已导出：{file_path}", 2200)

    def copy_to_clipboard(self) -> None:
        QApplication.clipboard().setText(self.preview_editor.toPlainText())
        self.statusBar().showMessage("已复制到剪贴板", 1800)


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("Prompt 模板生成器")
    win = PromptBuilderWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
