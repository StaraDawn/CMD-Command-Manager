import subprocess  # 用于执行CMD命令
import threading  # 用于创建线程，避免界面卡死
import os  # 用于文件路径操作
from tkinter import messagebox  # 用于弹出消息框

class 命令执行:
    """命令执行类，负责命令的执行和输出处理"""
    
    def __init__(self):
        """初始化命令执行类"""
        self.命令执行中 = False  # 命令执行状态
        self.子进程 = None  # 存储子进程对象
        self.工作目录 = os.getcwd()  # 默认工作目录为当前目录
        self.输出内容 = ""  # 存储命令的输出内容
    
    def 执行命令(self, 命令, 输出文本框, 执行按钮, 停止按钮, 回调=None):
        """执行输入的CMD命令（线程执行避免卡死）"""
        输入的命令 = 命令.strip()
        if not 输入的命令:
            messagebox.showwarning("警告", "请输入要执行的CMD命令！")
            return
        
        # 清空输出内容
        self.输出内容 = ""
        
        # 更新按钮状态
        执行按钮.config(state="disabled")
        停止按钮.config(state="normal")
        self.命令执行中 = True
        
        # 记录执行的命令
        命令执行信息 = f">>> 执行命令：{输入的命令}"
        self.追加输出内容(输出文本框, 命令执行信息)
        self.输出内容 += 命令执行信息 + "\n"
        
        # 线程执行命令
        def 命令执行线程():
            try:
                self.子进程 = subprocess.Popen(
                    输入的命令,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",
                    errors="ignore",
                    cwd=self.工作目录
                )
                
                # 实时读取输出
                while self.命令执行中 and self.子进程.poll() is None:
                    输出行 = self.子进程.stdout.readline()
                    if 输出行:
                        输出内容 = 输出行.strip()
                        self.追加输出内容(输出文本框, 输出内容)
                        self.输出内容 += 输出内容 + "\n"
                
                # 读取剩余输出
                剩余输出 = self.子进程.communicate()[0]
                if 剩余输出:
                    剩余输出内容 = 剩余输出.strip()
                    self.追加输出内容(输出文本框, 剩余输出内容)
                    self.输出内容 += 剩余输出内容 + "\n"
                
                # 输出执行结果
                退出码 = self.子进程.returncode
                if 退出码 == 0:
                    执行结果 = f">>> 命令执行完成（退出码：{退出码}"
                    self.追加输出内容(输出文本框, 执行结果)
                    self.输出内容 += 执行结果 + "\n"
                else:
                    执行结果 = f">>> 命令执行失败（退出码：{退出码}"
                    self.追加输出内容(输出文本框, 执行结果)
                    self.输出内容 += 执行结果 + "\n"
            
            except Exception as 异常信息:
                错误信息 = f">>> 执行出错：{str(异常信息)}"
                self.追加输出内容(输出文本框, 错误信息)
                self.输出内容 += 错误信息 + "\n"
            
            finally:
                self.命令执行中 = False
                执行按钮.config(state="normal")
                停止按钮.config(state="disabled")
                # 执行回调函数，传递命令和输出内容
                if 回调:
                    回调(输入的命令, self.输出内容)
        
        threading.Thread(target=命令执行线程, daemon=True).start()
    
    def 停止命令(self, 输出文本框, 执行按钮, 停止按钮):
        """停止正在执行的命令"""
        if self.子进程 and self.命令执行中:
            try:
                self.子进程.terminate()
                self.追加输出内容(输出文本框, ">>> 命令已手动停止")
            except Exception as 异常信息:
                self.追加输出内容(输出文本框, f">>> 停止命令失败：{str(异常信息)}")
            finally:
                self.命令执行中 = False
                执行按钮.config(state="normal")
                停止按钮.config(state="disabled")
    
    def 追加输出内容(self, 输出文本框, 内容):
        """向输出框追加内容（线程安全）"""
        输出文本框.config(state="normal")
        输出文本框.insert("end", 内容 + "\n")
        输出文本框.see("end")  # 自动滚动到末尾
        输出文本框.config(state="disabled")
    
    def 清空输出(self, 输出文本框):
        """清空输出文本框"""
        输出文本框.config(state="normal")
        输出文本框.delete(1.0, "end")
        输出文本框.config(state="disabled")
    
    def 设置工作目录(self, 主窗口, 工作目录显示):
        """设置命令执行的工作目录"""
        from tkinter import filedialog
        
        # 打开目录选择对话框
        选择的目录 = filedialog.askdirectory(title="选择工作目录", parent=主窗口)
        
        if 选择的目录:
            self.工作目录 = 选择的目录
            # 更新工作目录显示
            工作目录显示.config(state="normal")
            工作目录显示.delete(0, "end")
            工作目录显示.insert(0, self.工作目录)
            工作目录显示.config(state="disabled")
            messagebox.showinfo("成功", f"工作目录已设置为：{self.工作目录}", parent=主窗口)
    
    def 恢复默认工作目录(self, 工作目录显示):
        """恢复默认工作目录"""
        self.工作目录 = os.getcwd()
        # 更新工作目录显示
        工作目录显示.config(state="normal")
        工作目录显示.delete(0, "end")
        工作目录显示.insert(0, self.工作目录)
        工作目录显示.config(state="disabled")
        messagebox.showinfo("成功", f"工作目录已恢复为默认目录：{self.工作目录}")
