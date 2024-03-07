# DEM到TIN转换工具

这是一个基于Python和GDAL库的工具，用于将数字高程模型（DEM）转换为三角剖分不规则网络（TIN）。

## 特性

- **读取DEM数据**：该工具能够读取GeoTiff格式的DEM数据。

- **基于梯度生成点集**：工具会根据DEM数据生成点集，只有当地形的梯度超过设定的阈值时，该点才会被纳入点集。

- **生成Delaunay三角网**：利用生成的点集，工具会进一步生成Delaunay三角网，即TIN。

- **保存结果**：工具将TIN数据保存为文本文件，同时生成一个表示DEM数据边界的GeoJSON文件。

## 使用方法

1. 在`main()`函数中，将`raster_path`变量修改为你的DEM文件的路径。

2. 将`output_txt_path`变量修改为你希望保存TIN数据的文本文件的路径。

3. 将`output_geojson_path`变量修改为你希望保存边界数据的GeoJSON文件的路径。

4. 将`gradient_threshold`变量设定为你期望的梯度阈值。

5. 运行脚本。

## 注意

本项目生成的txt格式可以适用于[DEM可视化软件](https://github.com/GISer1909/dem_show)。通过该软件，你可以直观地查看和分析TIN数据。

## 依赖

- Python
- GDAL
- NumPy
- SciPy

## 许可

该项目采用MIT许可。