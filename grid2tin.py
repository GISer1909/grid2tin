from osgeo import gdal, ogr
import numpy as np
from scipy.spatial import Delaunay
import numpy.ma as ma

class RasterTINProcessor:
    def __init__(self, raster_path, output_shp_path, gradient_threshold):
        self.raster_path = raster_path
        self.output_shp_path = output_shp_path
        self.gradient_threshold = gradient_threshold

    def read_raster(self):
        ds = gdal.Open(self.raster_path)
        band = ds.GetRasterBand(1)
        arr = band.ReadAsArray()
        gt = ds.GetGeoTransform()
        return arr, gt

    def raster_to_points_gradient(self, raster_array, geo_transform):
        grad = np.gradient(raster_array)#计算梯度
        #打印raster_array的shape
        print(raster_array.shape)
        grad_magnitude = np.sqrt(grad[0]**2 + grad[1]**2)

        points = []
        for row in range(raster_array.shape[0]):
            for col in range(raster_array.shape[1]):
                if grad_magnitude[row, col] > self.gradient_threshold:
                    x = geo_transform[0] + col * geo_transform[1]
                    y = geo_transform[3] + row * geo_transform[5]
                    z = raster_array[row, col]
                    points.append((x, y, z))
        #打印点集的数量
        print(len(points))
        return np.array(points)

    def create_tin(self, points):
        return Delaunay(points[:, :2])

    def export_tin_to_shp(self, triangles, points):
        driver = ogr.GetDriverByName('ESRI Shapefile')
        ds = driver.CreateDataSource(self.output_shp_path)
        layer = ds.CreateLayer('', None, ogr.wkbPolygon)

        field_defn = ogr.FieldDefn('Height', ogr.OFTReal)
        layer.CreateField(field_defn)

        for tri in triangles.simplices:
            ring = ogr.Geometry(ogr.wkbLinearRing)
            for idx in tri:
                x, y, z = points[idx]
                ring.AddPoint(x, y, z)

            ring.CloseRings()

            poly = ogr.Geometry(ogr.wkbPolygon)
            poly.AddGeometry(ring)

            feat = ogr.Feature(layer.GetLayerDefn())
            feat.SetGeometry(poly)
            feat.SetField('Height', np.mean(points[tri, 2]))
            layer.CreateFeature(feat)
            feat = None

        ds = None

    def process(self):
        raster_array, geo_transform = self.read_raster()
        points = self.raster_to_points_gradient(raster_array, geo_transform)
        tin = self.create_tin(points)
        self.export_tin_to_shp(tin, points)


# 使用方法
if __name__ == "__main__":
    processor = RasterTINProcessor('./cj.tif', './result.shp', 5)
    processor.process()
