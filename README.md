# Amazon 电商数据分析 Dashboard

本项目针对 `ecommerce_dataset_Amazon.csv` 数据集进行深入分析，使用 Streamlit 构建交互式可视化 Dashboard。

## 📊 功能模块
- **KPI 核心指标**：实时计算筛选后的商品总数、平均价格、平均评分及评论总量。
- **价格与折扣洞察**：分析价格分布及折扣力度与销量的关联。
- **品牌与类别分析**：探索头部品牌的市场占有率及各品类的价值分布。
- **评分质量评估**：通过箱线图展示各品类的用户评分质量。
- **动态交互**：支持按类别、品牌、价格区间和评分进行深度过滤。

## 🚀 快速启动

1. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

2. **启动应用**：
   ```bash
   streamlit run dashboard.py
   ```

## 🛠️ Windows 部署指南
请参考 [dashboard.py](dashboard.py) 所在的文件夹进行部署。

- **使用 NSSM 注册为服务** (推荐)
- **使用 Windows 任务计划程序** (简单快捷)
