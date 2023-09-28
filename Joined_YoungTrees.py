import csv

csv_file = "J:\\GISprojects\\YoungTrees\\NFI048 - NB - results by component group - c2 or c3 latest survey.csv"

from osgeo import ogr
import os

shapefile = "J:\\GISprojects\\YoungTrees\\wetransfer_young_trees_results_2021_22032023_nfi2020_restock-geojson_2023-06-27_1158\\Young_Trees_Results_2021_22032023_NFI2020_Restock.geojson"
driver = ogr.GetDriverByName("GeoJSON")
dataSource = driver.Open(shapefile, 0)
layer = dataSource.GetLayer()
shapefile_list =[]
headers = ['SOURCE',
           'CATEGORY',
           'IFT_IOA',
           'REASON_FOR',
           'AP_YEAR',
           'GRANT_YEAR',
           'ORIGIN',
           'COUNTRY',
           'GS_REFEREN',
           'COMMENTS',
           'QA',
           'NFI2020_UN',
           'ORIG_FID',
           'AP_UPDATE',
           'Shape_Leng',
           'Shape_Area',
           'Area_ha',
           'class_2021',
           'prob_2021',
           'model_2021',]
for feature in layer:
    orig_fid = feature.GetField("ORIG_FID")
    geom = feature.GetGeometryRef()
    geom_wkt = geom.ExportToWkt()
    source = feature.GetField("SOURCE")
    category = feature.GetField("CATEGORY")
    ift_ioa = feature.GetField("IFT_IOA")
    reason_for = feature.GetField("REASON_FOR")
    ap_year = feature.GetField("AP_YEAR")
    grant_year = feature.GetField("GRANT_YEAR")
    origin = feature.GetField("ORIGIN")
    country = feature.GetField("COUNTRY")
    gs_referen = feature.GetField("GS_REFEREN")
    comments = feature.GetField("COMMENTS")
    qa = feature.GetField("QA")
    nfi2020_un = feature.GetField("NFI2020_UN")
    ap_update = feature.GetField("AP_UPDATE")
    shape_leng = feature.GetField("Shape_Leng")
    shape_area = feature.GetField("Shape_Area")
    area_ha = feature.GetField("Area_ha")
    class_2021 = feature.GetField("class_2021")
    prob_2021 = feature.GetField("prob_2021")
    model_2021 = feature.GetField("model_2021")
    merged = [orig_fid, source, category, ift_ioa, reason_for, ap_year, grant_year, origin, country,
              gs_referen, comments, qa, nfi2020_un, orig_fid, ap_update, shape_leng, shape_area,
              area_ha, class_2021, prob_2021, model_2021, geom_wkt]
    shapefile_list.append(merged)

row_count = 0

with open("Joined_Young_Tress.csv", 'w') as out:
    writer = csv.writer(out, delimiter=",")
    with open(csv_file, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            ogid = row[1]
            if ogid == 'ORIG_FI':
                writer.writerow(row + headers)
            else:
                for item in shapefile_list:
                    ls_orig_fid = item[0]
                    if int(ogid) == int(ls_orig_fid):
                        merge = row + item
                        print(merge)
                        writer.writerow(merge)




