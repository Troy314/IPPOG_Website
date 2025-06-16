# IPPOG_Website
## Master project for database formatting to upload on the IPPOG resource portal 

The goal of this project is to facilitate the work of the IPPOG core team in uploading projects to the https://ippog-resources-portal.web.cern.ch/ 

The idea is to let the community submit their projects through a [google form](https://forms.gle/tp2t45JroU8sFffH9)

The [Google Sheet extracted from it](https://docs.google.com/spreadsheets/d/1x_SdxdlHwG8chH77WqrTAAgijY2XBY3nPIi2p3TKqzs/edit?usp=sharing) is already formatted to be added to the complete database (*minus the first column that needs to be replaced by the ID of the project*)

The database.csv is then run through the `run.py` code to produce markdown files in a directory named `output_markdown`. Each line of the database produces a markdown file already mostly formatted for the WordPress website.

## Dependancies

## Running

## What need to be done manually on the wordpress website
- Add the "Featured image"
- Create a "media & text" block with the title(s) and the featured image
- Add the abstract
- Add the categories and tag
- Add the "categories" and "tag" blocks
- Remove the unnecessary parts

