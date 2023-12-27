# Grid2TIN

Grid2TIN 是一个 Python 仓库，提供了一组函数，用于将GRID转换为三角不规则网络 (TIN)，并将其导出为 Shapefile 格式的矢量文件。这个工具特别适用于将高程或其他连续栅格数据转换为 TIN 表示，以便进一步分析或可视化。下面是如何使用 Grid2TIN 仓库及其主要功能的说明。

## 目录
- [Grid2TIN](#grid2tin)
  - [目录](#目录)
  - [先决条件](#先决条件)
  - [安装](#安装)
  - [使用方法](#使用方法)
    - [读取栅格数据](#读取栅格数据)
    - [生成点集（基于梯度）](#生成点集基于梯度)
    - [创建 TIN](#创建-tin)
    - [导出 TIN 为 Shapefile](#导出-tin-为-shapefile)
  - [示例](#示例)
  - [贡献](#贡献)
  - [许可证](#许可证)

## 先决条件
在使用 Grid2TIN 之前，请确保已安装以下先决条件：
- Python（>= 3.6）
- GDAL（地理空间数据抽象库）
- NumPy
- SciPy
- OGR（GDAL 的一部分）

## 安装
要安装所需的 Python 库，您可以使用以下 pip 命令：

```bash
pip install numpy scipy gdal osgeo
```

## 使用方法
要使用 Grid2TIN，请按照以下步骤进行：

### 读取栅格数据
`read_raster` 函数读取栅格文件并返回栅格数组和地理空间转换信息。

```python
from osgeo import gdal

raster_path = '路径/到/您的/栅格.tif'
raster_array, geo_transform = read_raster(raster_path)
```

### 生成点集（基于梯度）
`raster_to_points_gradient` 函数根据梯度阈值从栅格数据生成点集。

```python
gradient_threshold = 20  # 根据需要进行调整
points = raster_to_points_gradient(raster_array, geo_transform, gradient_threshold)
```

### 创建 TIN
`create_tin` 函数从生成的点集创建三角不规则网络 (TIN)。

```python
tin = create_tin(points)
```

### 导出 TIN 为 Shapefile
`export_tin_to_shp` 函数将 TIN 数据导出为 Shapefile。

```python
output_shp_path = '路径/到/输出/result.shp'
export_tin_to_shp(tin, points, output_shp_path)
```

## 示例
提供了一个完整的 Grid2TIN 使用示例，位于提供的代码的 `main` 函数中。将 `raster_path` 和 `output_shp_path` 替换为您自己的文件路径，并根据需要调整 `gradient_threshold`。然后，运行 `main` 函数生成 TIN 并将其导出为 Shapefile。

```python
if __name__ == "__main__":
    main()
```

## 贡献
欢迎对 Grid2TIN 仓库进行贡献。如果您有建议或改进意见，请创建拉取请求或在 GitHub 仓库中提出问题。

## 许可证
此项目根据 MIT 许可证许可。有关详细信息，请参阅 [LICENSE](LICENSE) 文件。