import os  # 用于文件路径操作
import json  # 用于JSON文件的读写

# 常用命令保存路径
命令保存文件 = "常用命令.json"
# 命令历史记录保存路径
历史记录文件 = "命令历史.json"

class 配置管理:
    """配置文件管理类，负责读写配置文件"""
    
    @staticmethod
    def 加载常用命令():
        """从JSON文件加载常用命令和分类"""
        常用命令列表 = []
        命令分类列表 = ["默认", "网络", "文件", "系统", "其他"]  # 默认分类
        
        try:
            if os.path.exists(命令保存文件):
                with open(命令保存文件, "r", encoding="utf-8") as f:
                    加载数据 = json.load(f)
                    
                    # 检查数据格式
                    if isinstance(加载数据, list):
                        # 旧格式：直接是命令数组
                        常用命令列表 = 加载数据
                        # 为旧格式的命令添加分类字段
                        for 命令项 in 常用命令列表:
                            if "分类" not in 命令项:
                                命令项["分类"] = "默认"
                    else:
                        # 新格式：包含常用命令和分类
                        常用命令列表 = 加载数据.get("常用命令", [])
                        
                        # 加载分类列表
                        if "命令分类" in 加载数据:
                            命令分类列表 = 加载数据["命令分类"]
                            # 确保默认分类存在
                            if "默认" not in 命令分类列表:
                                命令分类列表.insert(0, "默认")
                        
                        # 确保所有命令都有分类字段
                        for 命令项 in 常用命令列表:
                            if "分类" not in 命令项:
                                命令项["分类"] = "默认"
                    
                    # 如果是旧格式，转换为新格式并保存
                    if isinstance(加载数据, list):
                        配置管理.保存常用命令到文件(常用命令列表, 命令分类列表)
        except Exception as 异常信息:
            print(f"加载常用命令出错：{str(异常信息)}")
            常用命令列表 = []
        
        return 常用命令列表, 命令分类列表
    
    @staticmethod
    def 保存常用命令到文件(常用命令列表, 命令分类列表):
        """将常用命令和分类保存到JSON文件"""
        try:
            # 准备保存数据
            保存数据 = {
                "常用命令": 常用命令列表,
                "命令分类": 命令分类列表
            }
            with open(命令保存文件, "w", encoding="utf-8") as f:
                json.dump(保存数据, f, ensure_ascii=False, indent=2)
        except Exception as 异常信息:
            print(f"保存常用命令出错：{str(异常信息)}")
    
    @staticmethod
    def 加载命令历史():
        """从JSON文件加载命令历史"""
        命令历史列表 = []
        
        try:
            if os.path.exists(历史记录文件):
                with open(历史记录文件, "r", encoding="utf-8") as f:
                    命令历史列表 = json.load(f)
        except Exception as 异常信息:
            print(f"加载命令历史出错：{str(异常信息)}")
            命令历史列表 = []
        
        return 命令历史列表
    
    @staticmethod
    def 保存命令历史到文件(命令历史列表, 历史记录最大条数=100):
        """将命令历史保存到JSON文件"""
        try:
            # 限制历史记录条数
            if len(命令历史列表) > 历史记录最大条数:
                命令历史列表 = 命令历史列表[-历史记录最大条数:]
            
            with open(历史记录文件, "w", encoding="utf-8") as f:
                json.dump(命令历史列表, f, ensure_ascii=False, indent=2)
        except Exception as 异常信息:
            print(f"保存命令历史出错：{str(异常信息)}")
