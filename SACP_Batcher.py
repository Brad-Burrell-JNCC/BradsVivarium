import os
import datetime

geomedium_home_dir = r"O:\EAT\EOMonitoringApplications\NorthernIreland2022\NI_Seasonal_Geomedium\SACP_Batch"

s2_gran = r"{}\Test_Data".format(geomedium_home_dir)
mosaic = r"{}\Mosaic".format(geomedium_home_dir)

sacp_batch_command_path = r"{}\SACP_Batch_Commands.txt".format(geomedium_home_dir)
masked_rasters = []


split_set_count = 0
masked_set_count = 0

if os.path.exists(sacp_batch_command_path):
    os.remove(sacp_batch_command_path)
sacp_batch_command = open(sacp_batch_command_path, "a")

for acquisition in os.listdir(s2_gran):
    acquisition_path = r"{}\{}".format(s2_gran, acquisition)
    print(acquisition)
    acquisition_refactor = acquisition.replace('_', '-')
    acquisition_datetime = datetime.datetime.strptime(acquisition.split('_')[1], '%Y%m%d')
    acquisition_date = "{}-{:02d}-{:02d}".format(acquisition_datetime.year,
                                                 acquisition_datetime.month,
                                                 acquisition_datetime.day)
    split_set_count = split_set_count + 1
    source_raster_dir = r"{}\Source".format(acquisition_path)
    split_raster_dir = r"{}\Split".format(acquisition_path)
    mask_raster_dir = r"{}\Mask".format(acquisition_path)

    cloudmask_raster = [x for x in os.listdir(source_raster_dir) if x.endswith('clouds.tif')][0]
    cloudmask_raster_path = r"{}\{}".format(source_raster_dir, cloudmask_raster)
    stdsref_raster = [x for x in os.listdir(source_raster_dir) if x.endswith('stdsref.tif')][0]
    stdsref_raster_path = r"{}\{}".format(source_raster_dir, stdsref_raster)
    stdsref_raster_filename = stdsref_raster.split('.')[0]

    # SPLIT
    sacp_split_raster = """
split_raster_bands;input_raster_path : '{}';output_dir : '{}';output_name_prefix : 'split_{}'""".format(stdsref_raster_path, split_raster_dir, acquisition_refactor)
    sacp_batch_command.write(sacp_split_raster)
    print("{}\n".format(sacp_split_raster))

    if split_set_count == 1:
        pass
    else:
        split_set = '\nadd_new_bandset;band_set : {}'.format(split_set_count)
        sacp_batch_command.write(split_set)
        print("{}\n".format(split_set))

    # SET
    sacp_set_raster = """
create_bandset;raster_path_list : '{}, tif';center_wavelength : 'sentinel-2';wavelength_unit : 1;multiplicative_factor : '1';additive_factor : '0';date : '{}'""".format(split_raster_dir, acquisition_date)
    sacp_batch_command.write(sacp_set_raster)
    print("{}\n".format(sacp_set_raster))

    # MASK
    sacp_mask_raster = """
cloud_masking;band_set : 1;input_raster_path : '{}';class_values : '1';use_buffer : 1;size_in_pixels : 1;nodata_value : 0;output_name_prefix : 'mask_{}';output_dir : '{}'""".format(cloudmask_raster_path, acquisition_refactor, mask_raster_dir)
    sacp_batch_command.write(sacp_mask_raster)
    print("{}\n".format(sacp_mask_raster))
    masked_rasters.append(cloudmask_raster_path)
    remove_bandset = """\nremove_bandset;band_set : 1"""
    print("{}\n".format(remove_bandset))
    sacp_batch_command.write(remove_bandset)


# for i in range(1, split_set_count+1):
#     remove_bandset = """\nremove_bandset;band_set : 1"""
#     print("{}\n".format(remove_bandset))
#     sacp_batch_command.write(remove_bandset)

print(masked_rasters)

for masked_raster in masked_rasters:

    split_masked_raster = masked_raster.split('\\')[-1]
    masked_dir = "{}\\Mask".format(os.path.dirname(os.path.dirname(masked_raster)))
    masked_raster_datetime = datetime.datetime.strptime(split_masked_raster.split('_')[1], '%Y%m%d')
    masked_set_count = masked_set_count + 1
    print(masked_set_count)
    if masked_set_count == 1:
        pass
    else:
        sacp_set_mask_raster = '\nadd_new_bandset;band_set : {}'.format(split_set_count)
        sacp_batch_command.write(sacp_set_mask_raster)
        print("{}\n".format(sacp_set_mask_raster))
    sacp_create_mask_raster = """
create_bandset;raster_path_list : '{}, tif';center_wavelength : 'sentinel-2';wavelength_unit : 1;multiplicative_factor : '1';additive_factor : '0';date : '{}'""".format(masked_dir, masked_set_count, masked_raster_datetime)
    sacp_batch_command.write(sacp_create_mask_raster)
    print("{}\n".format(sacp_create_mask_raster))

# MOSAIC
band_set_list = None
for i in range(1, split_set_count + 1):
    if band_set_list is None:
        band_set_list = "1"
    else:
        band_set_list = "{}, {}".format(band_set_list, i)
sacp_moasic = """
mosaic_bandsets;band_set_list :'{}';use_nodata : 1;nodata_value : 0;virtual_output : 0;output_dir :'{}';output_name_prefix : 'mosaic'""".format(band_set_list, mosaic)
sacp_batch_command.write(sacp_moasic)
print("{}\n".format(sacp_moasic))

# REMOVE
for i in range(1, split_set_count + 1):
    remove_bandset = """
remove_bandset;band_set : 1'""".format(i, band_set_list)
    sacp_batch_command.write(remove_bandset)
    print("{}\n".format(remove_bandset))
sacp_batch_command.close()
