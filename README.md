# grid2tin

## 简介

`grid2tin`是一个基于Python的工具，用于将栅格数据转换为TIN（三角不规则网络）并导出为Shapefile格式。该工具适用于地理信息系统（GIS）数据处理，特别是在地形建模、地理空间分析等领域中非常有用。

## 功能

- 读取栅格数据（如DEM，数字高程模型）
- 根据栅格数据的梯度生成点集
- 创建TIN
- 将TIN导出为Shapefile格式

## 安装

本工具依赖于多个Python库，包括GDAL、NumPy和SciPy等。请按照以下步骤安装：

1. 克隆仓库到本地：
   ```
   git clone https://github.com/GISer1909/grid2tin.git
   ```
2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

## 使用方法

1. 确保您的Python环境已安装所有依赖。
2. 编辑`grid2tin.py`文件，设置栅格文件路径、输出Shapefile路径和梯度阈值。
3. 运行脚本：
   ```
   python grid2tin.py
   ```

## 示例

假设您有一个名为`example.tif`的栅格文件，并希望将其输出为`output.shp`，您可以按照以下步骤操作：

1. 设置栅格文件路径为`example.tif`。
2. 设置输出Shapefile路径为`output.shp`。
3. 设置梯度阈值（根据您的数据特性自行决定）。
4. 运行`grid2tin.py`。

## 贡献

欢迎对本项目作出贡献！如果您有任何改进建议或功能请求，请通过Issue或Pull Request与我联系。

## 许可证

本项目遵循MIT License许可证。有关更多信息，请参阅LICENSE文件。
