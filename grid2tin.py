from osgeo import gdal, ogr, osr
import numpy as np
from scipy.spatial import Delaunay
import numpy.ma as ma

# 读取栅格数据
def read_raster(raster_path):
    ds = gdal.Open(raster_path)
    band = ds.GetRasterBand(1)
    arr = band.ReadAsArray()
    gt = ds.GetGeoTransform()
    return arr, gt

# 生成点集（基于梯度）
def raster_to_points_gradient(raster_array, geo_transform, gradient_threshold):
    # 计算梯度
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

# 创建TIN
def create_tin(points):
    return Delaunay(points[:, :2])

# 导出TIN为矢量格式（如Shapefile）
def export_tin_to_shp(triangles, points, output_path):
    # 创建矢量数据源
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.CreateDataSource(output_path)
    layer = ds.CreateLayer('', None, ogr.wkbPolygon)

    # 添加字段
    field_defn = ogr.FieldDefn('Height', ogr.OFTReal)
    layer.CreateField(field_defn)

    # 创建多边形特征
    for tri in triangles.simplices:
        ring = ogr.Geometry(ogr.wkbLinearRing)
        for idx in tri:
            x, y, z = points[idx]
            ring.AddPoint(x, y, z)

        # 封闭多边形
        ring.CloseRings()

        # 创建几何特征
        poly = ogr.Geometry(ogr.wkbPolygon)
        poly.AddGeometry(ring)

        # 创建要素
        feat = ogr.Feature(layer.GetLayerDefn())
        feat.SetGeometry(poly)
        feat.SetField('Height', np.mean(points[tri, 2])) # 取三角形顶点高度的平均值
        layer.CreateFeature(feat)
        feat = None

    # 清理
    ds = None


# 主函数
def main():
    raster_path = '路径/到/您的/栅格.tif'  # 替换为你的栅格文件路径
    output_shp_path = './result.shp'  # 替换为输出Shapefile的路径
    gradient_threshold = 20  # 设定梯度阈值，根据需要调整

    raster_array, geo_transform = read_raster(raster_path)
    points = raster_to_points_gradient(raster_array, geo_transform, gradient_threshold)
    tin = create_tin(points)
    export_tin_to_shp(tin, points, output_shp_path)

if __name__ == "__main__":
    main()
