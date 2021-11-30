import subprocess

# A script to use the EE cli to ingest images with metadata, band names, and startdate from Google Cloud Storage.
# 
# Assumes:
#   python3 is installed 
#   earthengine cli installed
#   gsutil installed
#   images are being ingested - not tables
#   images are located in a google storage bucket


# bandnames is a string of band names common to all images that are being ingested and must match 
# the total number of bands.
bandnames = 'C-VV,C-VH,C-INC,L-HH,L-HV,L-INC,Landsat_NDVI,MODIS_Tree_Cover,PRODES'
# asset_path is the destination GEE image collection or folder that will hold each image.
asset_path = 'projects/servir-amazonia/para_stacks'


# datestr is the start date to be associated with each image. If your images have different dates,
# you will need to find another method to assign them for each image.
datestr = '2020-06-01'

# base_cloud_path is the google storage bucket or sub directory with the images to ingest into EE.
base_cloud_path = 'gs://samz/para/'


# get a list of  tif files from the base cloud path.
imglist = subprocess.run(['gsutil', 'ls', f'{base_cloud_path.strip("/")}/*.tif'],
    text=True, shell=True, capture_output=True).stdout.split('\n')

# dryrun prints the command that will be called to upload each file if True,
# and runs commands if False.
dryrun = False


for img in imglist:
    # img is a full bucket object path (e.g. img = "gs://folder1/folder2/img.tif")

    # Get the full image name by removing the path string (e.g. image_name = "img.tif")
    image_name= img.split('/')[-1]
    # Create the asset name by removing .tif file extention (e.g. asset_name = "img")
    asset_name = image_name.split('.')[0]

    command = ["earthengine", 'upload', 'image', f'--asset_id={asset_path}/{asset_name}', '--bands', bandnames, '-ts', datestr, img]
    # skip blank items
    if img == "":
        continue

    if dryrun:
        print(f'DRY RUN {" ".join(command)}')
    else:
        # upload image
        subprocess.run(command)
