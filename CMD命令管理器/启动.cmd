@echo off

:: 设置中文编码，确保中文显示正常
chcp 65001

:: 进入当前目录
cd /d "%~dp0"

:: 启动CMD命令管理器，使用pythonw.exe来避免显示命令窗口
start "CMD命令管理器" "%PYTHON_HOME%\pythonw.exe" "%~dp0命令行管理程序.py"

:: 如果PYTHON_HOME环境变量未设置，尝试使用系统路径中的pythonw
if %errorlevel% neq 0 (
    start "CMD命令管理器" pythonw "%~dp0命令行管理程序.py"
)

:: 退出批处理文件，不等待用户输入
exit
