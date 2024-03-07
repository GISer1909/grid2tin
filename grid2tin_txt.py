from osgeo import gdal, osr, ogr
import numpy as np
from scipy.spatial import Delaunay
import numpy.ma as ma
import json

# 读取栅格数据
def read_raster(raster_path):
    ds = gdal.Open(raster_path)
    band = ds.GetRasterBand(1)
    arr = band.ReadAsArray()
    gt = ds.GetGeoTransform()
    return arr, gt, ds.RasterYSize, ds.RasterXSize

# 生成点集（基于梯度）
def raster_to_points_gradient(raster_array, geo_transform, gradient_threshold):
    grad = np.gradient(raster_array)
    grad_magnitude = np.sqrt(grad[0]**2 + grad[1]**2)

    points = []
    for row in range(raster_array.shape[0]):
        for col in range(raster_array.shape[1]):
            if grad_magnitude[row, col] > gradient_threshold:
                x = geo_transform[0] + col * geo_transform[1]
                y = geo_transform[3] + row * geo_transform[5]
                z = raster_array[row, col]
                points.append((x, y, z))
    return np.array(points)

# 计算矩形边界的四个角点
def calculate_rectangle_corners(gt, width, height):
    corners = [
        (gt[0], gt[3]),  # 左上角
        (gt[0] + width * gt[1], gt[3]),  # 右上角
        (gt[0] + width * gt[1], gt[3] + height * gt[5]),  # 右下角
        (gt[0], gt[3] + height * gt[5])  # 左下角
    ]
    return corners

# 坐标转换
def convert_coord(x, y):
    source = osr.SpatialReference()
    source.ImportFromEPSG(4326)
    target = osr.SpatialReference()
    target.ImportFromEPSG(3857)
    transform = osr.CoordinateTransformation(source, target)
    x, y, _ = transform.TransformPoint(y, x)
    return x, y

# 生成 Delaunay 三角网
def delaunay_triangles(points):
    tri = Delaunay(points[:, :2])
    return points[tri.simplices]

# 保存结果到文本文件
def save_to_txt(triangles,corners, output_filename):
    with open(output_filename, 'w') as file:
        #第一行写入左下角坐标和右上角坐标
        #找出左下角和右上角坐标
        left_down = corners[3]
        right_up = corners[1]
        corners_data = ';'.join([','.join(map(str, point)) for point in [left_down,right_up]])
        file.write(corners_data + '\n')
        for triangle in triangles:
            triangle_data = ';'.join([','.join(map(str, point)) for point in triangle])
            file.write(triangle_data + '\n')
            

# 创建 GeoJSON 文件
def create_geojson_polygon(corners, output_path):
    # 准备 GeoJSON 结构
    geojson = {
        "type": "FeatureCollection",
        "crs": {
            "type": "name",
            "properties": {
                "name": "EPSG:3857"
            }
        },
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [corners]
                }
            }
        ]
    }

    # 写入文件
    with open(output_path, 'w') as file:
        json.dump(geojson, file)

# 主程序
def main():
    raster_path = "./cj.tif"  # 输入栅格文件路径
    output_txt_path = 'output_triangles.txt'  # 输出文本文件路径
    output_geojson_path = 'boundary.geojson'  # 输出 GeoJSON 文件路径
    gradient_threshold = 3  # 梯度阈值

    raster_array, geo_transform, raster_height, raster_width = read_raster(raster_path)

    # 计算矩形边界的角点并转换坐标
    corners = calculate_rectangle_corners(geo_transform, raster_width, raster_height)
    converted_corners = [convert_coord(x, y) for x, y in corners]

    # 创建并保存 GeoJSON 文件
    create_geojson_polygon(converted_corners + [converted_corners[0]], output_geojson_path)  # 添加第一个点以闭合多边形
    print(f"边界已保存至 {output_geojson_path}")

    points = raster_to_points_gradient(raster_array, geo_transform, gradient_threshold)
    points = np.array([convert_coord(x, y) + (z,) for x, y, z in points])

    triangles = delaunay_triangles(points)
    save_to_txt(triangles,converted_corners, output_txt_path)
    print(f"三角网数据已保存到 {output_txt_path}")

if __name__ == "__main__":
    main()
