import os

# How to use the EE cli to ingest images with metadata, band names, and startdate from Google Cloud Storage.
# 
# Assumes:
#   python3 is installed 
#   earthengine cli installed
#   gsutil installed
#   images are being ingested - not tables
#   images are located in a google storage bucket

# note: Quotations are needed when setting the parameters. Depending on your OS you may need double or
# single quotations (on Windows 10 I needed double quotations)
p1 = '-p "(string)R=Radar Volume Index Sentinel-1"'
p2 = '-p "(string)G=Radar Volume Index ALOS2"'
p3 = '-p "(string)B=NDVI Landsat8 SR"'
p4 = '-p "(string)notes=Sentinel-1 is Jun 02, 2020 through Oct 31, 2020, other bands are annual composites"'


# bandnames is a string of band names common to all images that are being ingested and must match 
# the total number of bands.
bandnames = 'R,G,B'
# asset_path is the destination GEE image collection or folder that will hold each image.
asset_path = 'projects/servir-amazonia/para_rgb_2020'


# metadata_dict is a dictionary of where images are and a date. discard if this doesn't work with your format.
metadata_dict = {
    'annual_2020' : {
        # single date of all images in gcs folder
        'start_date' : '2020-01-01',
        'end_date': '2020-12-31',
        # GCS folder with some images
        'cloud' : 'gs://samz/para_rgb/',
    }
}

# which images and metadata to upload
choice = 'annual_2020'
# start date (can be in YYYY-MM-DD srting)
datestr = metadata_dict[choice]['start_date']
end_datestr = metadata_dict[choice]['end_date']

# gets list of files from cloud (loads ALL files)
imglist = os.popen(f'gsutil ls {metadata_dict[choice]["cloud"]}').read().split("\n")

# dryrun print the command that will be called to upload each file if True,
# and runs commands if False.
dryrun = True


for img in imglist:
    # img is a full bucket path.
    # e.g. gs://folder1/folder2/img.tiff

    # get image name by removing spliting on / then on . .tif
    image_name= img.split('/')[-1].split('.')[0]

    # name of the EE asset
    asset_name = image_name

    # skip things that dont have a quad number or are blank
    if len(image_name) == 0 or img == "":
        continue

    if dryrun:
        print(f"earthengine upload image --asset_id={asset_path}/{asset_name} --bands {bandnames} -ts {datestr} -te {end_datestr} {p1} {p2} {p3} {p4} {img}")
    else:
        # upload image
        os.system(f"earthengine upload image --asset_id={asset_path}/{asset_name} --bands {bandnames} {p1} {p2} {p3} {p4} -ts {datestr} -te {end_datestr} {img}")
