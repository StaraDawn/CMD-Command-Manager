from tkinter import simpledialog, messagebox  # 用于弹出对话框
from 配置管理 import 配置管理  # 导入配置管理模块

class 命令管理:
    """命令管理类，负责常用命令的管理功能"""
    
    def __init__(self):
        """初始化命令管理类"""
        # 从配置文件加载常用命令和分类
        self.常用命令列表, self.命令分类列表 = 配置管理.加载常用命令()
        # 从配置文件加载命令历史
        self.命令历史列表 = 配置管理.加载命令历史()
        self.历史记录最大条数 = 100  # 历史记录最大保存条数
    
    def 刷新命令列表(self, 命令列表框, 当前分类="全部", 搜索关键词=""):
        """刷新常用命令列表框的显示"""
        # 清空原有内容
        for 项 in 命令列表框.get_children():
            命令列表框.delete(项)
        
        # 获取当前选择的分类和搜索关键词
        搜索关键词 = 搜索关键词.strip().lower()
        
        # 添加新内容
        for 命令项 in self.常用命令列表:
            # 检查分类是否匹配
            分类匹配 = (当前分类 == "全部" or 命令项.get("分类", "默认") == 当前分类)
            
            # 检查搜索关键词是否匹配
            搜索匹配 = True
            if 搜索关键词:
                命令名称 = 命令项["名称"].lower()
                命令内容 = 命令项["命令"].lower()
                命令分类 = 命令项.get("分类", "默认").lower()
                搜索匹配 = (搜索关键词 in 命令名称 or 搜索关键词 in 命令内容 or 搜索关键词 in 命令分类)
            
            # 如果分类和搜索都匹配，则显示
            if 分类匹配 and 搜索匹配:
                命令列表框.insert("", "end", values=(命令项["名称"], 命令项["命令"], 命令项.get("分类", "默认")))
    
    def 添加常用命令(self, 主窗口, 命令列表框=None):
        """添加新的常用命令"""
        # 创建添加命令窗口
        from tkinter import Toplevel, Label, Entry, Button, StringVar, ttk
        添加窗口 = Toplevel(主窗口)
        添加窗口.title("添加常用命令")
        添加窗口.geometry("400x250")
        添加窗口.resizable(False, False)
        # 窗口居中
        添加窗口.update_idletasks()
        主窗口_width = 主窗口.winfo_width()
        主窗口_height = 主窗口.winfo_height()
        主窗口_x = 主窗口.winfo_rootx()
        主窗口_y = 主窗口.winfo_rooty()
        窗口_width = 添加窗口.winfo_width()
        窗口_height = 添加窗口.winfo_height()
        x = 主窗口_x + (主窗口_width - 窗口_width) // 2
        y = 主窗口_y + (主窗口_height - 窗口_height) // 2
        添加窗口.geometry(f"400x250+{x}+{y}")
        
        # 名称输入
        Label(添加窗口, text="命令名称：", font=("微软雅黑", 9)).pack(pady=(10, 2))
        名称变量 = StringVar()
        名称输入框 = Entry(添加窗口, textvariable=名称变量, font=("微软雅黑", 9), width=40)
        名称输入框.pack(pady=5)
        
        # 命令内容输入
        Label(添加窗口, text="命令内容：", font=("微软雅黑", 9)).pack(pady=(10, 2))
        命令变量 = StringVar()
        命令输入框 = Entry(添加窗口, textvariable=命令变量, font=("微软雅黑", 9), width=40)
        命令输入框.pack(pady=5)
        
        # 分类选择
        Label(添加窗口, text="命令分类：", font=("微软雅黑", 9)).pack(pady=(10, 2))
        分类变量 = StringVar(value="默认")
        分类下拉框 = ttk.Combobox(添加窗口, textvariable=分类变量, font=("微软雅黑", 9), width=38)
        分类下拉框['values'] = self.命令分类列表
        分类下拉框.pack(pady=5)
        
        def 确认添加():
            新名称 = 名称变量.get().strip()
            新命令 = 命令变量.get().strip()
            新分类 = 分类变量.get()
            
            if not 新名称:
                messagebox.showwarning("警告", "命令名称不能为空！", parent=添加窗口)
                return
            if not 新命令:
                messagebox.showwarning("警告", "命令内容不能为空！", parent=添加窗口)
                return
            
            # 检查重名
            for 项 in self.常用命令列表:
                if 项["名称"] == 新名称:
                    messagebox.showwarning("警告", "该命令名称已存在！", parent=添加窗口)
                    return
            
            # 添加到列表并保存
            self.常用命令列表.append({"名称": 新名称, "命令": 新命令, "分类": 新分类})
            self.保存常用命令()
            添加窗口.destroy()
            messagebox.showinfo("成功", "常用命令添加成功！", parent=主窗口)
            # 刷新命令列表
            if 命令列表框:
                self.刷新命令列表(命令列表框)
        
        # 按钮
        按钮框架 = Label(添加窗口)
        按钮框架.pack(pady=15)
        
        确认按钮 = Button(按钮框架, text="确认", font=("微软雅黑", 9), command=确认添加, width=10)
        确认按钮.pack(side="left", padx=10)
        
        取消按钮 = Button(按钮框架, text="取消", font=("微软雅黑", 9), command=添加窗口.destroy, width=10)
        取消按钮.pack(side="left", padx=10)
        
        添加窗口.transient(主窗口)
        添加窗口.grab_set()
        主窗口.wait_window(添加窗口)
    
    def 编辑命令(self, 主窗口, 命令列表框, 选中索引=None, event=None):
        """编辑命令"""
        # 如果没有提供索引，从选择中获取
        if 选中索引 is None:
            选中项 = 命令列表框.selection()
            if not 选中项:
                # 尝试从事件中获取点击位置的项
                if event:
                    点击项 = 命令列表框.identify_row(event.y)
                    if 点击项:
                        命令列表框.selection_set(点击项)
                        选中项 = [点击项]
                    else:
                        return
                else:
                    messagebox.showwarning("提示", "请先选中要编辑的命令！", parent=主窗口)
                    return
            选中索引 = 命令列表框.index(选中项[0])
        
        原命令项 = self.常用命令列表[选中索引]
        
        # 创建编辑窗口
        from tkinter import Toplevel, Label, Entry, Button, StringVar, ttk
        编辑窗口 = Toplevel(主窗口)
        编辑窗口.title("编辑命令")
        编辑窗口.geometry("400x250")
        编辑窗口.resizable(False, False)
        # 窗口居中
        编辑窗口.update_idletasks()
        主窗口_width = 主窗口.winfo_width()
        主窗口_height = 主窗口.winfo_height()
        主窗口_x = 主窗口.winfo_rootx()
        主窗口_y = 主窗口.winfo_rooty()
        窗口_width = 编辑窗口.winfo_width()
        窗口_height = 编辑窗口.winfo_height()
        x = 主窗口_x + (主窗口_width - 窗口_width) // 2
        y = 主窗口_y + (主窗口_height - 窗口_height) // 2
        编辑窗口.geometry(f"400x250+{x}+{y}")
        
        # 名称输入
        Label(编辑窗口, text="命令名称：", font=("微软雅黑", 9)).pack(pady=(10, 2))
        名称变量 = StringVar(value=原命令项["名称"])
        名称输入框 = Entry(编辑窗口, textvariable=名称变量, font=("微软雅黑", 9), width=40)
        名称输入框.pack(pady=5)
        
        # 命令内容输入
        Label(编辑窗口, text="命令内容：", font=("微软雅黑", 9)).pack(pady=(10, 2))
        命令变量 = StringVar(value=原命令项["命令"])
        命令输入框 = Entry(编辑窗口, textvariable=命令变量, font=("微软雅黑", 9), width=40)
        命令输入框.pack(pady=5)
        
        # 分类选择
        Label(编辑窗口, text="命令分类：", font=("微软雅黑", 9)).pack(pady=(10, 2))
        分类变量 = StringVar(value=原命令项.get("分类", "默认"))
        分类下拉框 = ttk.Combobox(编辑窗口, textvariable=分类变量, font=("微软雅黑", 9), width=38)
        分类下拉框['values'] = self.命令分类列表
        分类下拉框.pack(pady=5)
        
        def 确认修改():
            新名称 = 名称变量.get().strip()
            新命令 = 命令变量.get().strip()
            新分类 = 分类变量.get()
            
            if not 新名称:
                messagebox.showwarning("警告", "命令名称不能为空！", parent=编辑窗口)
                return
            if not 新命令:
                messagebox.showwarning("警告", "命令内容不能为空！", parent=编辑窗口)
                return
            
            # 检查重名（排除自身）
            for i, 项 in enumerate(self.常用命令列表):
                if i != 选中索引 and 项["名称"] == 新名称:
                    messagebox.showwarning("警告", "该命令名称已存在！", parent=编辑窗口)
                    return
            
            # 更新命令
            self.常用命令列表[选中索引] = {"名称": 新名称, "命令": 新命令, "分类": 新分类}
            self.保存常用命令()
            编辑窗口.destroy()
            messagebox.showinfo("成功", "命令编辑成功！", parent=主窗口)
            # 刷新命令列表
            self.刷新命令列表(命令列表框)
        
        # 按钮
        按钮框架 = Label(编辑窗口)
        按钮框架.pack(pady=15)
        
        确认按钮 = Button(按钮框架, text="确认", font=("微软雅黑", 9), command=确认修改, width=10)
        确认按钮.pack(side="left", padx=10)
        
        取消按钮 = Button(按钮框架, text="取消", font=("微软雅黑", 9), command=编辑窗口.destroy, width=10)
        取消按钮.pack(side="left", padx=10)
        
        编辑窗口.transient(主窗口)
        编辑窗口.grab_set()
        主窗口.wait_window(编辑窗口)
    
    def 删除常用命令(self, 主窗口, 命令列表框):
        """删除选中的常用命令"""
        选中项 = 命令列表框.selection()
        if not 选中项:
            messagebox.showwarning("提示", "请先选中要删除的命令！", parent=主窗口)
            return
        
        if messagebox.askyesno("确认删除", "确定要删除选中的命令吗？", parent=主窗口):
            选中索引 = 命令列表框.index(选中项[0])
            del self.常用命令列表[选中索引]
            self.保存常用命令()
            messagebox.showinfo("成功", "常用命令删除成功！", parent=主窗口)
            # 刷新命令列表
            self.刷新命令列表(命令列表框)
    
    def 清空命令列表(self, 主窗口, 命令列表框=None):
        """清空所有常用命令"""
        if not self.常用命令列表:
            messagebox.showinfo("提示", "常用命令列表已为空！", parent=主窗口)
            return
        
        if messagebox.askyesno("确认清空", "确定要清空所有常用命令吗？此操作不可恢复！", parent=主窗口):
            self.常用命令列表 = []
            self.保存常用命令()
            messagebox.showinfo("成功", "常用命令列表已清空！", parent=主窗口)
            # 刷新命令列表
            if 命令列表框:
                self.刷新命令列表(命令列表框)
    
    def 管理分类(self, 主窗口, 分类下拉框):
        """管理命令分类"""
        # 创建分类管理窗口
        from tkinter import Toplevel, Listbox, Button, Label
        分类管理窗口 = Toplevel(主窗口)
        分类管理窗口.title("分类管理")
        分类管理窗口.geometry("400x300")
        # 窗口居中
        分类管理窗口.update_idletasks()
        主窗口_width = 主窗口.winfo_width()
        主窗口_height = 主窗口.winfo_height()
        主窗口_x = 主窗口.winfo_rootx()
        主窗口_y = 主窗口.winfo_rooty()
        窗口_width = 分类管理窗口.winfo_width()
        窗口_height = 分类管理窗口.winfo_height()
        x = 主窗口_x + (主窗口_width - 窗口_width) // 2
        y = 主窗口_y + (主窗口_height - 窗口_height) // 2
        分类管理窗口.geometry(f"400x300+{x}+{y}")
        
        # 分类列表框
        分类列表框 = Listbox(分类管理窗口, font=("微软雅黑", 9), width=40, height=10)
        分类列表框.pack(pady=10, fill="both", expand=True, padx=10)
        
        # 填充分类列表
        for 分类 in self.命令分类列表:
            分类列表框.insert("end", 分类)
        
        # 按钮框架
        按钮框架 = Label(分类管理窗口)
        按钮框架.pack(pady=10, padx=10)
        
        def 添加分类():
            新分类 = simpledialog.askstring("添加分类", "请输入新分类名称：", parent=分类管理窗口)
            if 新分类 and 新分类 not in self.命令分类列表:
                self.命令分类列表.append(新分类)
                分类列表框.insert("end", 新分类)
                # 保存分类列表
                self.保存常用命令()
                # 更新分类下拉框
                分类下拉框['values'] = ["全部"] + self.命令分类列表
                messagebox.showinfo("成功", "分类添加成功！", parent=分类管理窗口)
            elif 新分类 in self.命令分类列表:
                messagebox.showwarning("警告", "该分类名称已存在！", parent=分类管理窗口)
        
        def 编辑分类():
            选中索引 = 分类列表框.curselection()
            if not 选中索引:
                messagebox.showwarning("提示", "请先选中要编辑的分类！", parent=分类管理窗口)
                return
            
            原分类 = 分类列表框.get(选中索引[0])
            if 原分类 == "默认":
                messagebox.showwarning("警告", "默认分类不能编辑！", parent=分类管理窗口)
                return
            
            新分类 = simpledialog.askstring("编辑分类", "请输入新分类名称：", initialvalue=原分类, parent=分类管理窗口)
            if 新分类 and 新分类 not in self.命令分类列表:
                # 更新分类列表
                self.命令分类列表[选中索引[0]] = 新分类
                分类列表框.delete(选中索引[0])
                分类列表框.insert(选中索引[0], 新分类)
                # 更新命令列表中的分类
                for 命令项 in self.常用命令列表:
                    if 命令项.get("分类") == 原分类:
                        命令项["分类"] = 新分类
                # 保存常用命令
                self.保存常用命令()
                # 更新分类下拉框
                分类下拉框['values'] = ["全部"] + self.命令分类列表
                messagebox.showinfo("成功", "分类编辑成功！", parent=分类管理窗口)
            elif 新分类 in self.命令分类列表:
                messagebox.showwarning("警告", "该分类名称已存在！", parent=分类管理窗口)
        
        def 删除分类():
            选中索引 = 分类列表框.curselection()
            if not 选中索引:
                messagebox.showwarning("提示", "请先选中要删除的分类！", parent=分类管理窗口)
                return
            
            要删除的分类 = 分类列表框.get(选中索引[0])
            if 要删除的分类 == "默认":
                messagebox.showwarning("警告", "默认分类不能删除！", parent=分类管理窗口)
                return
            
            # 检查是否有命令使用该分类
            使用该分类的命令数 = 0
            for 命令项 in self.常用命令列表:
                if 命令项.get("分类") == 要删除的分类:
                    使用该分类的命令数 += 1
            
            if 使用该分类的命令数 > 0:
                if not messagebox.askyesno("确认删除", f"该分类下有{使用该分类的命令数}个命令，删除后这些命令将移到默认分类。确定要删除吗？", parent=分类管理窗口):
                    return
            
            # 删除分类
            self.命令分类列表.pop(选中索引[0])
            分类列表框.delete(选中索引[0])
            # 更新命令列表中的分类
            for 命令项 in self.常用命令列表:
                if 命令项.get("分类") == 要删除的分类:
                    命令项["分类"] = "默认"
            # 保存常用命令
            self.保存常用命令()
            # 更新分类下拉框
            分类下拉框['values'] = ["全部"] + self.命令分类列表
            messagebox.showinfo("成功", "分类删除成功！", parent=分类管理窗口)
        
        # 添加分类按钮
        添加按钮 = Button(
            按钮框架, text="添加分类", font=("微软雅黑", 9),
            command=添加分类, width=10
        )
        添加按钮.pack(side="left", padx=5)
        
        # 编辑分类按钮
        编辑按钮 = Button(
            按钮框架, text="编辑分类", font=("微软雅黑", 9),
            command=编辑分类, width=10
        )
        编辑按钮.pack(side="left", padx=5)
        
        # 删除分类按钮
        删除按钮 = Button(
            按钮框架, text="删除分类", font=("微软雅黑", 9),
            command=删除分类, width=10
        )
        删除按钮.pack(side="left", padx=5)
        
        # 关闭按钮
        关闭按钮 = Button(
            按钮框架, text="关闭", font=("微软雅黑", 9),
            command=分类管理窗口.destroy, width=10
        )
        关闭按钮.pack(side="right", padx=5)
        
        分类管理窗口.transient(主窗口)
        分类管理窗口.grab_set()
        主窗口.wait_window(分类管理窗口)
    
    def 导出命令(self, 主窗口):
        """导出常用命令和分类到JSON文件"""
        from tkinter import filedialog
        
        # 打开文件保存对话框
        文件路径 = filedialog.asksaveasfilename(
            title="导出命令配置",
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")],
            parent=主窗口
        )
        
        if not 文件路径:
            return
        
        try:
            # 准备导出数据
            导出数据 = {
                "常用命令": self.常用命令列表,
                "命令分类": self.命令分类列表
            }
            
            # 保存到文件
            import json
            with open(文件路径, "w", encoding="utf-8") as f:
                json.dump(导出数据, f, ensure_ascii=False, indent=2)
            
            messagebox.showinfo("成功", f"命令配置已成功导出到：{文件路径}", parent=主窗口)
        except Exception as 异常信息:
            messagebox.showerror("导出失败", f"导出命令配置出错：{str(异常信息)}", parent=主窗口)
    
    def 导入命令(self, 主窗口, 分类下拉框, 覆盖=False):
        """从JSON文件导入常用命令和分类"""
        from tkinter import filedialog
        
        # 打开文件选择对话框
        文件路径 = filedialog.askopenfilename(
            title="导入命令配置",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")],
            parent=主窗口
        )
        
        if not 文件路径:
            return
        
        try:
            # 读取文件内容
            import json
            with open(文件路径, "r", encoding="utf-8") as f:
                导入数据 = json.load(f)
            
            # 检查数据格式
            if "常用命令" not in 导入数据:
                messagebox.showwarning("导入失败", "无效的命令配置文件：缺少常用命令数据", parent=主窗口)
                return
            
            # 导入命令和分类
            if 覆盖:
                # 完全覆盖
                self.常用命令列表 = 导入数据.get("常用命令", [])
                if "命令分类" in 导入数据:
                    self.命令分类列表 = 导入数据["命令分类"]
                    # 确保默认分类存在
                    if "默认" not in self.命令分类列表:
                        self.命令分类列表.insert(0, "默认")
            else:
                # 追加模式
                新命令 = 导入数据.get("常用命令", [])
                for 命令 in 新命令:
                    # 检查是否重名
                    重名 = False
                    for 现有命令 in self.常用命令列表:
                        if 现有命令["名称"] == 命令["名称"]:
                            重名 = True
                            break
                    if not 重名:
                        self.常用命令列表.append(命令)
                
                # 合并分类
                if "命令分类" in 导入数据:
                    for 分类 in 导入数据["命令分类"]:
                        if 分类 not in self.命令分类列表:
                            self.命令分类列表.append(分类)
            
            # 保存到文件
            self.保存常用命令()
            
            # 更新分类下拉框
            分类下拉框['values'] = ["全部"] + self.命令分类列表
            
            messagebox.showinfo("成功", f"命令配置已成功导入自：{文件路径}", parent=主窗口)
        except Exception as 异常信息:
            messagebox.showerror("导入失败", f"导入命令配置出错：{str(异常信息)}", parent=主窗口)
    
    def 保存当前命令到常用(self, 主窗口, 命令内容):
        """将输入框中的命令保存到常用命令"""
        if not 命令内容.strip():
            messagebox.showwarning("警告", "输入框中无命令可保存！", parent=主窗口)
            return
        
        命令名称 = simpledialog.askstring("输入名称", "请为该命令命名：", parent=主窗口)
        if not 命令名称:
            return
        
        # 选择分类
        from tkinter import Toplevel, Label, Radiobutton, Button, StringVar, Scrollbar, Frame
        分类选择窗口 = Toplevel(主窗口)
        分类选择窗口.title("选择分类")
        分类选择窗口.geometry("300x300")
        分类选择窗口.resizable(True, True)
        # 窗口居中
        分类选择窗口.update_idletasks()
        主窗口_width = 主窗口.winfo_width()
        主窗口_height = 主窗口.winfo_height()
        主窗口_x = 主窗口.winfo_rootx()
        主窗口_y = 主窗口.winfo_rooty()
        窗口_width = 分类选择窗口.winfo_width()
        窗口_height = 分类选择窗口.winfo_height()
        x = 主窗口_x + (主窗口_width - 窗口_width) // 2
        y = 主窗口_y + (主窗口_height - 窗口_height) // 2
        分类选择窗口.geometry(f"300x300+{x}+{y}")
        
        分类标签 = Label(分类选择窗口, text="请选择命令分类：", font=("微软雅黑", 10))
        分类标签.pack(pady=10)
        
        # 创建带滚动条的框架
        滚动框架 = Frame(分类选择窗口)
        滚动框架.pack(fill="both", expand=True, padx=10, pady=5)
        
        # 添加滚动条
        滚动条 = Scrollbar(滚动框架, orient="vertical")
        滚动条.pack(side="right", fill="y")
        
        # 创建内部框架用于放置分类选项
        分类框架 = Frame(滚动框架)
        分类框架.pack(fill="both", expand=True)
        
        # 配置滚动条
        滚动条.config(command=分类框架.yview)
        分类框架.config(yscrollcommand=滚动条.set)
        
        分类变量 = StringVar()
        分类变量.set("默认")
        
        for 分类 in self.命令分类列表:
            分类选项 = Radiobutton(
                分类框架, text=分类, variable=分类变量, value=分类, font=("微软雅黑", 9)
            )
            分类选项.pack(pady=5, anchor="w")
        
        def 确认选择():
            选择的分类 = 分类变量.get()
            分类选择窗口.destroy()
            
            # 检查重名
            for 项 in self.常用命令列表:
                if 项["名称"] == 命令名称:
                    messagebox.showwarning("警告", "该命令名称已存在！", parent=主窗口)
                    return
            
            # 保存
            self.常用命令列表.append({"名称": 命令名称, "命令": 命令内容, "分类": 选择的分类})
            self.保存常用命令()
            messagebox.showinfo("成功", "当前命令已保存到常用！", parent=主窗口)
        
        # 创建按钮框架，确保按钮固定在窗口底部
        按钮框架 = Frame(分类选择窗口)
        按钮框架.pack(fill="x", padx=10, pady=10)
        
        确认按钮 = Button(
            按钮框架, text="确认", font=("微软雅黑", 9),
            command=确认选择, width=10
        )
        确认按钮.pack()
        
        # 确保分类框架可以滚动
        分类框架.update_idletasks()
        分类框架.config(scrollregion=分类框架.bbox("all"))
        
        分类选择窗口.transient(主窗口)
        分类选择窗口.grab_set()
        主窗口.wait_window(分类选择窗口)
    
    def 显示命令到右侧(self, 命令列表框, 命令输入框, 命令名称显示, event=None):
        """单击列表项显示命令到右侧输入框"""
        目标项 = None
        
        # 1. 优先从事件中获取用户点击位置的项
        if event:
            点击项 = 命令列表框.identify_row(event.y)
            if 点击项:
                目标项 = 点击项
        
        # 2. 如果没有从事件中获取到项，再从选择中获取
        if not 目标项:
            选中项 = 命令列表框.selection()
            if 选中项:
                目标项 = 选中项[0]
            else:
                return
        
        # 3. 确保目标项被选中
        命令列表框.selection_set(目标项)
        
        # 4. 从目标项中获取命令名称和内容并显示到右侧
        选中索引 = 命令列表框.index(目标项)
        命令项 = self.常用命令列表[选中索引]
        
        # 显示命令名称
        命令名称显示.config(text=命令项["名称"])
        # 填充到输入框
        命令输入框.delete(0, "end")
        命令输入框.insert(0, 命令项["命令"])
    
    def 记录命令到历史(self, 命令, 输出内容=None):
        """将命令和输出内容添加到历史记录"""
        if 命令:
            # 构建历史记录项，包含命令和输出内容
            历史记录项 = {
                "命令": 命令,
                "输出": 输出内容 or ""
            }
            
            # 直接添加到历史记录，允许重复命令
            self.命令历史列表.append(历史记录项)
            # 限制历史记录条数
            if len(self.命令历史列表) > self.历史记录最大条数:
                self.命令历史列表 = self.命令历史列表[-self.历史记录最大条数:]
            self.保存命令历史()
    
    def 显示历史记录(self, 主窗口, 命令输入框):
        """显示命令历史记录"""
        if not self.命令历史列表:
            messagebox.showinfo("提示", "命令历史记录为空！", parent=主窗口)
            return
        
        # 创建历史记录窗口
        from tkinter import Toplevel, Listbox, Button, Label, scrolledtext
        历史窗口 = Toplevel(主窗口)
        历史窗口.title("命令历史记录")
        历史窗口.geometry("800x500")
        # 窗口居中
        历史窗口.update_idletasks()
        主窗口_width = 主窗口.winfo_width()
        主窗口_height = 主窗口.winfo_height()
        主窗口_x = 主窗口.winfo_rootx()
        主窗口_y = 主窗口.winfo_rooty()
        窗口_width = 历史窗口.winfo_width()
        窗口_height = 历史窗口.winfo_height()
        x = 主窗口_x + (主窗口_width - 窗口_width) // 2
        y = 主窗口_y + (主窗口_height - 窗口_height) // 2
        历史窗口.geometry(f"800x500+{x}+{y}")
        
        # 历史记录列表框
        历史列表框 = Listbox(历史窗口, font=("Consolas", 9), width=80, height=10)
        历史列表框.pack(pady=5, fill="x", padx=5)
        
        # 输出内容显示框
        输出内容标签 = Label(历史窗口, text="输出内容：", font=("微软雅黑", 9))
        输出内容标签.pack(pady=5, padx=5, anchor="w")
        
        输出内容文本框 = scrolledtext.ScrolledText(历史窗口, font=("Consolas", 9), height=15)
        输出内容文本框.pack(pady=5, fill="both", expand=True, padx=5)
        输出内容文本框.config(state="disabled")
        
        # 填充历史记录
        for 历史项 in reversed(self.命令历史列表):  # 最新的命令显示在最上方
            if isinstance(历史项, dict):
                # 新格式：包含命令和输出内容的字典
                命令 = 历史项.get("命令", "")
                历史列表框.insert("end", 命令)
            else:
                # 旧格式：直接是命令字符串
                历史列表框.insert("end", 历史项)
        
        # 显示选中项的输出内容
        def 显示选中项输出(event):
            选中索引 = 历史列表框.curselection()
            if 选中索引:
                # 获取原始历史项
                原始索引 = len(self.命令历史列表) - 1 - 选中索引[0]
                历史项 = self.命令历史列表[原始索引]
                
                # 清空输出内容文本框
                输出内容文本框.config(state="normal")
                输出内容文本框.delete(1.0, "end")
                
                if isinstance(历史项, dict):
                    # 新格式：包含命令和输出内容的字典
                    输出内容 = 历史项.get("输出", "")
                    输出内容文本框.insert("end", 输出内容)
                else:
                    # 旧格式：直接是命令字符串
                    输出内容文本框.insert("end", "无输出内容")
                
                输出内容文本框.config(state="disabled")
        
        # 绑定列表框选择事件
        历史列表框.bind("<<ListboxSelect>>", 显示选中项输出)
        
        # 双击执行历史命令
        def 执行历史命令(event):
            选中索引 = 历史列表框.curselection()
            if 选中索引:
                # 获取原始历史项
                原始索引 = len(self.命令历史列表) - 1 - 选中索引[0]
                历史项 = self.命令历史列表[原始索引]
                
                if isinstance(历史项, dict):
                    # 新格式：包含命令和输出内容的字典
                    选中命令 = 历史项.get("命令", "")
                else:
                    # 旧格式：直接是命令字符串
                    选中命令 = 历史项
                
                命令输入框.delete(0, "end")
                命令输入框.insert(0, 选中命令)
                历史窗口.destroy()
        
        历史列表框.bind("<Double-1>", 执行历史命令)
        
        # 按钮框架
        按钮框架 = Label(历史窗口)
        按钮框架.pack(pady=5, padx=5)
        
        # 清空历史按钮
        清空按钮 = Button(
            按钮框架, text="清空历史", font=("微软雅黑", 9),
            command=lambda: [self.清空命令历史(主窗口), 历史窗口.destroy()]
        )
        清空按钮.pack(side="right", padx=5)
        
        # 关闭按钮
        关闭按钮 = Button(
            按钮框架, text="关闭", font=("微软雅黑", 9),
            command=历史窗口.destroy
        )
        关闭按钮.pack(side="right", padx=5)
        
        # 初始显示第一个历史项的输出内容
        if self.命令历史列表:
            历史列表框.selection_set(0)
            显示选中项输出(None)
    
    def 浏览历史记录(self, 命令输入框, 方向):
        """使用上下箭头键浏览历史记录"""
        当前命令 = 命令输入框.get().strip()
        
        # 如果历史记录为空，直接返回
        if not self.命令历史列表:
            return
        
        # 查找当前命令在历史记录中的位置
        当前索引 = -1
        for i, 历史项 in enumerate(self.命令历史列表):
            if isinstance(历史项, dict):
                # 新格式：包含命令和输出内容的字典
                if 历史项.get("命令") == 当前命令:
                    当前索引 = i
                    break
            else:
                # 旧格式：直接是命令字符串
                if 历史项 == 当前命令:
                    当前索引 = i
                    break
        
        # 计算新索引
        新索引 = 当前索引 + 方向
        if 新索引 < 0:
            新索引 = 0
        elif 新索引 >= len(self.命令历史列表):
            新索引 = len(self.命令历史列表) - 1
        
        # 获取新命令
        历史项 = self.命令历史列表[新索引]
        if isinstance(历史项, dict):
            # 新格式：包含命令和输出内容的字典
            新命令 = 历史项.get("命令", "")
        else:
            # 旧格式：直接是命令字符串
            新命令 = 历史项
        
        # 更新输入框内容
        命令输入框.delete(0, "end")
        命令输入框.insert(0, 新命令)
    
    def 清空命令历史(self, 主窗口):
        """清空命令历史记录"""
        if not self.命令历史列表:
            messagebox.showinfo("提示", "命令历史记录已为空！", parent=主窗口)
            return
        
        if messagebox.askyesno("确认清空", "确定要清空所有命令历史记录吗？此操作不可恢复！", parent=主窗口):
            self.命令历史列表 = []
            self.保存命令历史()
            messagebox.showinfo("成功", "命令历史记录已清空！", parent=主窗口)
    
    def 保存常用命令(self):
        """保存常用命令到配置文件"""
        配置管理.保存常用命令到文件(self.常用命令列表, self.命令分类列表)
    
    def 保存命令历史(self):
        """保存命令历史到配置文件"""
        配置管理.保存命令历史到文件(self.命令历史列表)
