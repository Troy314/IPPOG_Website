# IPPOG Ressource database formatting tool
## Database formatting

The goal of this code is to facilitate the work of the IPPOG core team in uploading projects to the Wordpress [IPPOG Ressource Portal](https://ippog-resources-portal.web.cern.ch/).

The aims is to let the community submit their projects through a simple an explicit [google form](https://forms.gle/tp2t45JroU8sFffH9).

The [Google Sheet extracted from it](https://docs.google.com/spreadsheets/d/1x_SdxdlHwG8chH77WqrTAAgijY2XBY3nPIi2p3TKqzs/edit?usp=sharing) is already formatted to be added to the Ressource Database (*minus the first column that needs to be replaced by the ID of the project*).

The database.csv is then ran through the `run.py` code to produce markdown files in a directory named `output_markdown`. Each line of the database produces a markdown file already mostly formatted for the WordPress website.

The format of the database is the following : 

| ID | Name of the project in English | Name of the project in it's original language | Featured Image | Credit of the featured image | Abstract | Author names,affiliation | Supporting entities | Related IPPOG member | Public contact | Private contact | Name of the conference | Year of the conference | Presentation Documents | Project Status | Type | Topics | Audiences | Langage | Sub Type | Sub Topics | Wordpress page | State |
| - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |


## Dependancies

## Running

## What need to be done manually on the wordpress website
- Add the "Featured image"
- Create a "media & text" block with the title(s) and the featured image
- Add the abstract
- Add the categories and tag
- Add the "categories" and "tag" blocks
- Remove the unnecessary parts

Categories and tags works in the following way
