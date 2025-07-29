# IPPOG Ressource database formatting tool

<p align="center">
  <a href="https://ippog-resources-portal.web.cern.ch/">
    <img src="media/IPPOG_logo.png" alt="IPPOG logo">
  </a>
</p>

## Database formatting

The goal of this code is to facilitate the work of the IPPOG core team in uploading projects to the Wordpress [IPPOG Resource Portal](https://ippog-resources-portal.web.cern.ch/).

The aim is to let the community submit their projects through a simple and explicit [google form](https://forms.gle/tp2t45JroU8sFffH9).

The [Google Sheet extracted from it](https://docs.google.com/spreadsheets/d/1x_SdxdlHwG8chH77WqrTAAgijY2XBY3nPIi2p3TKqzs/edit?usp=sharing) is already formatted to be added to the Resource Database (*minus the first column that needs to be replaced by the ID of the project*).

The user can either export the database as a csv file (see `exemple_file.csv`) and run `run_local.py` or enable the Google API to directly work with the online database and run `run_online.py`. The code produces, for each line of the database, one markdown file in a directory named `output_markdown`. These files are already mostly formatted to be copy/pasted into the WordPress website.

The flowchart detailing the upload process is as follows :

![Flowchart](media/Flowchart.svg)

## Dependencies
*WIP*

## Running
*WIP*

## Uploading
![Uploading](media/How_to_upload.mp4)

<iframe width="1680" height="736" src="https://www.youtube.com/embed/OQ6QYBG_MYU" title="How to upload project" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## What needs to be done manually on the WordPress website
What needs to be done manually appears in the markdown file as `[draft]`
- Create a "media & text" block with the title and the featured image
- Upload the "Featured image"
- Update the "excerpt"
- Add the categories and tag to the post properties
- Add the "categories" and "tag" blocks
- Remove the unnecessary parts

Categories and tags work in the following way:

| ![Topics category](media/Topics_category.svg) | ![Types category](media/Types_category.svg) |
| - | - |

## Work in progress
- Documentation document
- Git Repository

## Data
Some data about the projects currently on the website: 

For more details, see `data_analysis_local.py` and `data_analysis_online.py`

![Related members data](media/data/Related_members.svg)
![Topics data](media/data/topics.svg)
![Types data](media/data/types.svg)

## Contact
If you see any problem, don't hesitate to contact me at hector.pillot [at] proton.me