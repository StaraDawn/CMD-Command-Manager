import tkinter as tk  # 用于创建GUI界面
from tkinter import scrolledtext, ttk  # 用于创建滚动文本框和下拉框
import sys  # 用于获取系统信息
import os  # 用于文件路径操作
from 命令管理 import 命令管理  # 导入命令管理模块
from 命令执行 import 命令执行  # 导入命令执行模块

# 设置中文编码，避免CMD输出乱码
if sys.platform == "win32":
    os.system("chcp 65001 >nul")

class 主窗口:
    """主窗口类，负责UI布局和事件绑定"""
    
    def __init__(self):
        """初始化主窗口"""
        # 创建主窗口
        self.主窗口 = tk.Tk()
        self.主窗口.title("CMD命令管理器（带命令管理功能）")
        self.主窗口.geometry("1200x750")
        self.主窗口.minsize(1000, 600)  # 设置最小窗口大小
        
        # 初始化模块
        self.命令管理器 = 命令管理()
        self.命令执行器 = 命令执行()
        
        # 初始化变量
        self.搜索变量 = tk.StringVar()  # 搜索关键词变量
        self.分类变量 = tk.StringVar()  # 分类选择变量
        self.分类变量.set("全部")  # 默认显示全部命令
        
        # 创建UI布局
        self.创建布局()
        # 绑定事件
        self.绑定事件()
        # 初始化数据
        self.初始化数据()
    
    def 创建布局(self):
        """创建UI布局"""
        # ========== 整体布局：分左右两栏 ==========
        self.主框架 = tk.PanedWindow(self.主窗口, orient=tk.HORIZONTAL)
        self.主框架.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # ---------------- 左侧：命令管理区域 ----------------
        self.命令管理框架 = tk.Frame(self.主框架, width=300)
        self.主框架.add(self.命令管理框架, minsize=250)
        
        # 1. 命令管理标题和分类选择
        self.命令管理标题框架 = tk.Frame(self.命令管理框架)
        self.命令管理标题框架.pack(pady=5, fill=tk.X, padx=5)
        
        self.命令管理标题 = tk.Label(
            self.命令管理标题框架, text="常用命令管理", font=("微软雅黑", 12, "bold")
        )
        self.命令管理标题.pack(side=tk.LEFT)
        
        # 分类选择下拉框
        self.分类标签 = tk.Label(
            self.命令管理标题框架, text="分类：", font=("微软雅黑", 9)
        )
        self.分类标签.pack(side=tk.RIGHT, padx=(0, 5))
        
        self.分类下拉框 = ttk.Combobox(
            self.命令管理标题框架, textvariable=self.分类变量, font=("微软雅黑", 9), width=10
        )
        self.分类下拉框.pack(side=tk.RIGHT)
        
        # 2. 搜索功能
        self.搜索框架 = tk.Frame(self.命令管理框架)
        self.搜索框架.pack(pady=5, fill=tk.X, padx=5)
        
        self.搜索标签 = tk.Label(
            self.搜索框架, text="搜索：", font=("微软雅黑", 9)
        )
        self.搜索标签.pack(side=tk.LEFT, padx=(0, 5))
        
        self.搜索输入框 = tk.Entry(
            self.搜索框架, textvariable=self.搜索变量, font=("微软雅黑", 9)
        )
        self.搜索输入框.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.搜索按钮 = tk.Button(
            self.搜索框架, text="搜索", font=("微软雅黑", 9),
            command=self.刷新命令列表框, width=6
        )
        self.搜索按钮.pack(side=tk.RIGHT)
        
        self.清空搜索按钮 = tk.Button(
            self.搜索框架, text="清空", font=("微软雅黑", 9),
            command=self.清空搜索, width=6
        )
        self.清空搜索按钮.pack(side=tk.RIGHT, padx=(0, 5))
        
        # 2. 常用命令列表框
        self.命令列表框架 = tk.Frame(self.命令管理框架)
        self.命令列表框架.pack(pady=5, fill=tk.BOTH, expand=True, padx=5)
        
        # 添加垂直滚动条
        self.命令列表滚动条 = ttk.Scrollbar(self.命令列表框架, orient=tk.VERTICAL)
        
        # 创建列表框
        self.命令列表框 = ttk.Treeview(
            self.命令列表框架, columns=("名称", "命令", "分类"), show="headings", height=15,
            yscrollcommand=self.命令列表滚动条.set
        )
        self.命令列表滚动条.config(command=self.命令列表框.yview)
        
        # 设置列
        self.命令列表框.heading("名称", text="命令名称")
        self.命令列表框.heading("命令", text="命令内容")
        self.命令列表框.heading("分类", text="分类")
        self.命令列表框.column("名称", width=100, minwidth=80)
        self.命令列表框.column("命令", width=180, minwidth=120)
        self.命令列表框.column("分类", width=80, minwidth=60)
        
        # 布局
        self.命令列表滚动条.pack(side=tk.RIGHT, fill=tk.Y)
        self.命令列表框.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 3. 命令管理按钮组
        self.管理按钮框架 = tk.Frame(self.命令管理框架)
        self.管理按钮框架.pack(pady=5, fill=tk.X, padx=5)
        
        self.添加命令按钮 = tk.Button(
            self.管理按钮框架, text="添加常用命令", font=("微软雅黑", 9),
            command=lambda: self.命令管理器.添加常用命令(self.主窗口, self.命令列表框, self.分类变量.get(), self.搜索变量.get()), width=12
        )
        self.添加命令按钮.grid(row=0, column=0, padx=2, pady=2)
        
        self.编辑命令按钮 = tk.Button(
            self.管理按钮框架, text="编辑命令", font=("微软雅黑", 9),
            command=lambda: self.命令管理器.编辑命令(self.主窗口, self.命令列表框, 当前分类=self.分类变量.get(), 搜索关键词=self.搜索变量.get()), width=12
        )
        self.编辑命令按钮.grid(row=0, column=1, padx=2, pady=2)
        
        self.删除命令按钮 = tk.Button(
            self.管理按钮框架, text="删除命令", font=("微软雅黑", 9),
            command=lambda: self.命令管理器.删除常用命令(self.主窗口, self.命令列表框, self.分类变量.get(), self.搜索变量.get()), width=12
        )
        self.删除命令按钮.grid(row=1, column=0, padx=2, pady=2)
        
        self.清空列表按钮 = tk.Button(
            self.管理按钮框架, text="清空列表", font=("微软雅黑", 9),
            command=lambda: self.命令管理器.清空命令列表(self.主窗口, self.命令列表框, self.分类变量.get(), self.搜索变量.get()), width=12
        )
        self.清空列表按钮.grid(row=1, column=1, padx=2, pady=2)
        
        self.管理分类按钮 = tk.Button(
            self.管理按钮框架, text="管理分类", font=("微软雅黑", 9),
            command=lambda: self.命令管理器.管理分类(self.主窗口, self.分类下拉框), width=12
        )
        self.管理分类按钮.grid(row=2, column=0, padx=2, pady=2)
        
        self.导出命令按钮 = tk.Button(
            self.管理按钮框架, text="导出命令", font=("微软雅黑", 9),
            command=lambda: self.命令管理器.导出命令(self.主窗口), width=12
        )
        self.导出命令按钮.grid(row=2, column=1, padx=2, pady=2)
        
        self.导入命令按钮 = tk.Button(
            self.管理按钮框架, text="导入命令", font=("微软雅黑", 9),
            command=lambda: self.命令管理器.导入命令(self.主窗口, self.分类下拉框), width=12
        )
        self.导入命令按钮.grid(row=3, column=0, padx=2, pady=2)
        
        self.导入覆盖按钮 = tk.Button(
            self.管理按钮框架, text="导入覆盖", font=("微软雅黑", 9),
            command=lambda: self.命令管理器.导入命令(self.主窗口, self.分类下拉框, 覆盖=True), width=12
        )
        self.导入覆盖按钮.grid(row=3, column=1, padx=2, pady=2)
        
        # ---------------- 右侧：命令运行区域 ----------------
        self.命令运行框架 = tk.Frame(self.主框架)
        self.主框架.add(self.命令运行框架, minsize=500)
        
        # 1. 命令输入区域
        self.命令输入标签 = tk.Label(
            self.命令运行框架, text="输入/编辑CMD命令：", font=("微软雅黑", 10)
        )
        self.命令输入标签.pack(pady=5)
        
        # 命令名称显示
        self.命令名称标签 = tk.Label(
            self.命令运行框架, text="命令名称：", font=("微软雅黑", 9), fg="#666"
        )
        self.命令名称标签.pack(pady=(0, 2))
        
        self.命令名称显示 = tk.Label(
            self.命令运行框架, text="", font=("微软雅黑", 9, "bold"), fg="#333"
        )
        self.命令名称显示.pack(pady=(0, 5))
        
        # 命令输入框
        self.命令输入框 = tk.Entry(
            self.命令运行框架, font=("微软雅黑", 10)
        )
        self.命令输入框.pack(pady=5, fill=tk.X, padx=5)
        
        # 2. 工作目录设置
        self.工作目录框架 = tk.Frame(self.命令运行框架)
        self.工作目录框架.pack(pady=5, fill=tk.X, padx=5)
        
        self.工作目录标签 = tk.Label(
            self.工作目录框架, text="工作目录：", font=("微软雅黑", 9)
        )
        self.工作目录标签.pack(side=tk.LEFT, padx=(0, 5))
        
        self.工作目录显示 = tk.Entry(
            self.工作目录框架, font=("微软雅黑", 9), state=tk.DISABLED
        )
        self.工作目录显示.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.工作目录显示.config(state=tk.NORMAL)
        self.工作目录显示.insert(0, self.命令执行器.工作目录)
        self.工作目录显示.config(state=tk.DISABLED)
        
        self.浏览工作目录按钮 = tk.Button(
            self.工作目录框架, text="浏览", font=("微软雅黑", 9),
            command=lambda: self.命令执行器.设置工作目录(self.主窗口, self.工作目录显示), width=6
        )
        self.浏览工作目录按钮.pack(side=tk.RIGHT)
        
        self.恢复默认目录按钮 = tk.Button(
            self.工作目录框架, text="默认", font=("微软雅黑", 9),
            command=lambda: self.命令执行器.恢复默认工作目录(self.工作目录显示), width=6
        )
        self.恢复默认目录按钮.pack(side=tk.RIGHT, padx=(0, 5))
        
        # 2. 运行控制按钮组
        self.运行按钮框架 = tk.Frame(self.命令运行框架)
        self.运行按钮框架.pack(pady=5, padx=5)
        
        self.执行按钮 = tk.Button(
            self.运行按钮框架, text="执行命令", font=("微软雅黑", 10),
            command=self.执行命令, width=10, bg="#4CAF50", fg="white"
        )
        self.执行按钮.grid(row=0, column=0, padx=5)
        
        self.停止按钮 = tk.Button(
            self.运行按钮框架, text="停止执行", font=("微软雅黑", 10),
            command=self.停止命令, width=10, state=tk.DISABLED, bg="#f44336", fg="white"
        )
        self.停止按钮.grid(row=0, column=1, padx=5)
        
        self.清空输出按钮 = tk.Button(
            self.运行按钮框架, text="清空输出", font=("微软雅黑", 10),
            command=lambda: self.命令执行器.清空输出(self.输出文本框), width=10
        )
        self.清空输出按钮.grid(row=0, column=2, padx=5)
        
        self.保存到常用按钮 = tk.Button(
            self.运行按钮框架, text="保存到常用", font=("微软雅黑", 10),
            command=self.保存当前命令到常用, width=10
        )
        self.保存到常用按钮.grid(row=0, column=3, padx=5)
        
        # 历史记录按钮
        self.历史记录按钮 = tk.Button(
            self.运行按钮框架, text="查看历史", font=("微软雅黑", 10),
            command=self.显示历史记录, width=10
        )
        self.历史记录按钮.grid(row=0, column=4, padx=5)
        
        self.清空历史按钮 = tk.Button(
            self.运行按钮框架, text="清空历史", font=("微软雅黑", 10),
            command=lambda: self.命令管理器.清空命令历史(self.主窗口), width=10
        )
        self.清空历史按钮.grid(row=0, column=5, padx=5)
        
        # 3. 输出显示区域
        self.输出标签 = tk.Label(
            self.命令运行框架, text="命令执行结果：", font=("微软雅黑", 10)
        )
        self.输出标签.pack(pady=5)
        
        self.输出文本框 = scrolledtext.ScrolledText(
            self.命令运行框架, font=("Consolas", 9)
        )
        self.输出文本框.pack(pady=5, fill=tk.BOTH, expand=True, padx=5)
        self.输出文本框.config(state=tk.DISABLED)
    
    def 绑定事件(self):
        """绑定事件处理函数"""
        # 分类下拉框选择事件
        self.分类下拉框.bind("<<ComboboxSelected>>", lambda event: self.刷新命令列表框())
        # 搜索输入框回车事件
        self.搜索输入框.bind("<Return>", lambda event: self.刷新命令列表框())
        # 双击列表项编辑命令
        self.命令列表框.bind("<Double-1>", lambda event: self.命令管理器.编辑命令(self.主窗口, self.命令列表框, event=event, 当前分类=self.分类变量.get(), 搜索关键词=self.搜索变量.get()))
        # 单击列表项显示到右侧
        self.命令列表框.bind("<Button-1>", lambda event: self.命令管理器.显示命令到右侧(self.命令列表框, self.命令输入框, self.命令名称显示, event))
        # 命令输入框回车执行命令
        self.命令输入框.bind("<Return>", lambda event: self.执行命令())
        # 绑定上下箭头键浏览历史记录
        self.命令输入框.bind("<Up>", lambda event: self.命令管理器.浏览历史记录(self.命令输入框, -1))
        self.命令输入框.bind("<Down>", lambda event: self.命令管理器.浏览历史记录(self.命令输入框, 1))
        
        # ==================== 快捷键绑定 ====================
        # 执行命令 - Ctrl+Enter
        self.命令输入框.bind("<Control-Return>", lambda event: self.执行命令())
        self.主窗口.bind("<Control-Return>", lambda event: self.执行命令())
        
        # 停止执行 - Ctrl+C
        self.主窗口.bind("<Control-c>", lambda event: self.停止命令() if self.命令执行器.命令执行中 else None)
        
        # 清空输出 - Ctrl+L
        self.主窗口.bind("<Control-l>", lambda event: self.命令执行器.清空输出(self.输出文本框))
        
        # 保存到常用 - Ctrl+S
        self.主窗口.bind("<Control-s>", lambda event: self.保存当前命令到常用())
        
        # 显示历史记录 - Ctrl+H
        self.主窗口.bind("<Control-h>", lambda event: self.显示历史记录())
        
        # 清空历史 - Ctrl+Shift+H
        self.主窗口.bind("<Control-H>", lambda event: self.命令管理器.清空命令历史(self.主窗口))
        
        # 添加常用命令 - Ctrl+N
        self.主窗口.bind("<Control-n>", lambda event: self.命令管理器.添加常用命令(self.主窗口, self.命令列表框, self.分类变量.get(), self.搜索变量.get()))
        
        # 编辑常用命令 - Ctrl+E
        self.主窗口.bind("<Control-e>", lambda event: self.命令管理器.编辑命令(self.主窗口, self.命令列表框, 当前分类=self.分类变量.get(), 搜索关键词=self.搜索变量.get()))
        
        # 删除常用命令 - Delete
        self.命令列表框.bind("<Delete>", lambda event: self.命令管理器.删除常用命令(self.主窗口, self.命令列表框, self.分类变量.get(), self.搜索变量.get()))
        
        # 清空命令列表 - Ctrl+Shift+L
        self.主窗口.bind("<Control-L>", lambda event: self.命令管理器.清空命令列表(self.主窗口, self.命令列表框, self.分类变量.get(), self.搜索变量.get()))
        
        # 管理分类 - Ctrl+M
        self.主窗口.bind("<Control-m>", lambda event: self.命令管理器.管理分类(self.主窗口, self.分类下拉框))
        
        # 导出命令 - Ctrl+O
        self.主窗口.bind("<Control-o>", lambda event: self.命令管理器.导出命令(self.主窗口))
        
        # 导入命令 - Ctrl+I
        self.主窗口.bind("<Control-i>", lambda event: self.命令管理器.导入命令(self.主窗口, self.分类下拉框))
        
        # 设置工作目录 - Ctrl+D
        self.主窗口.bind("<Control-d>", lambda event: self.命令执行器.设置工作目录(self.主窗口, self.工作目录显示))
        
        # 恢复默认工作目录 - Ctrl+Shift+D
        self.主窗口.bind("<Control-D>", lambda event: self.命令执行器.恢复默认工作目录(self.工作目录显示))
        
        # 搜索命令 - Ctrl+F
        self.主窗口.bind("<Control-f>", lambda event: self.搜索输入框.focus_set())
        
        # 清空搜索 - Ctrl+Shift+F
        self.主窗口.bind("<Control-F>", lambda event: self.清空搜索())
    
    def 初始化数据(self):
        """初始化数据"""
        # 更新分类下拉框
        self.分类下拉框['values'] = ["全部"] + self.命令管理器.命令分类列表
        # 刷新命令列表
        self.刷新命令列表框()
    
    def 刷新命令列表框(self):
        """刷新常用命令列表框的显示"""
        self.命令管理器.刷新命令列表(self.命令列表框, self.分类变量.get(), self.搜索变量.get())
    
    def 清空搜索(self):
        """清空搜索输入框并重置搜索结果"""
        self.搜索变量.set("")
        self.刷新命令列表框()
    
    def 执行命令(self):
        """执行命令"""
        命令 = self.命令输入框.get()
        # 执行命令前清空输出文本框
        self.命令执行器.清空输出(self.输出文本框)
        
        # 定义回调函数，在命令执行完成后记录历史
        def 命令执行完成回调(执行的命令, 输出内容):
            # 记录命令和输出内容到历史
            self.命令管理器.记录命令到历史(执行的命令, 输出内容)
        
        # 执行命令，传入回调函数
        self.命令执行器.执行命令(命令, self.输出文本框, self.执行按钮, self.停止按钮, 回调=命令执行完成回调)
    
    def 停止命令(self):
        """停止命令"""
        self.命令执行器.停止命令(self.输出文本框, self.执行按钮, self.停止按钮)
    
    def 保存当前命令到常用(self):
        """保存当前命令到常用"""
        命令内容 = self.命令输入框.get()
        self.命令管理器.保存当前命令到常用(self.主窗口, 命令内容)
    
    def 显示历史记录(self):
        """显示历史记录"""
        self.命令管理器.显示历史记录(self.主窗口, self.命令输入框)
    
    def 运行(self):
        """运行主窗口"""
        self.主窗口.mainloop()
