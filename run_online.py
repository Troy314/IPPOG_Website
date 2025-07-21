import csv
import os
from datetime import datetime
import pathlib

from member_dictionary import members_dico

import gspread
from google.oauth2.service_account import Credentials

def json_to_md(output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load Google Sheets API credentials
    SERVICE_ACCOUNT_FILE = "ippog-466111-e8e5130144ad.json"  # Update with your JSON file
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    # Authenticate and create the client
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)

    # Open the Google Sheet by ID
    SHEET_ID = "1x_SdxdlHwG8chH77WqrTAAgijY2XBY3nPIi2p3TKqzs"  # Replace with your actual sheet ID
    sheet = client.open_by_key(SHEET_ID).get_worksheet(0)  # Access the first worksheet

    data = sheet.get_all_records()

    print("\nYou can either run through all projects with status \"OK\" or only run through a specific project")
    begin = input("\n> Enter the ID of the project to run (if no ID is selected, all \"OK\" project will be run through) : ")
    if begin =="":
        print("All project will be formated as no ID were given")
    else :
        print(f"PROJECT-{begin}\" will be formated")

    for row in data: 
        if not row:
            continue  # Skip empty rows

        if begin !="" and int(row["ID"]) != int(begin):
            continue # Skip project untill selected ID
        elif begin =="" and row["State"]!="OK":
            continue #Skip not "OK" status

        if row["ID"]!="":
            ID = str(row["ID"])
        else :
            print("\n#############################################\n# ERROR please define an ID in the database #\n#############################################")
            print(f"\n/!\\ no ID for project \"{row["Name of the project in English"]}\" /!\\")
            break
        print(f"\n\"{row["Name of the project in English"]}\" is now defined as - PROJECT-" + ID + " -")

        filename = "PROJECT-" + ID  + ".md"  # Create filename from first cell
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as mdfile:
            
            ###########
            ## Title ##
            ###########

            mdfile.write(f"---\n\n")
            mdfile.write(f"<TODO run the command `/media & text` manually with the \"show media on the right option\">")
            mdfile.write(f"<TODO run the command `/title` in the left column and \"featured image\" in the right>")
            mdfile.write(f"\n# {row["Name of the project in English"]}") # Name of the project in English

            if row["Name of the project in it's original language"]!="":
                mdfile.write(f"\n## {row["Name of the project in it's original language"]}") # Name of the project in it's original language (optional)
            
            if row["Featured Image"]!="":
                mdfile.write(f"\n<TODO Featured image is > {row["Featured Image"]}")
                mdfile.write(f"\n<TODO ragged right > Credit : {row["Credit of the featured image"]}") # Credit for the image
            else : 
                print("/!\\ no registered Featured image /!\\")
            mdfile.write(f"\n\n---\n")

            ##############
            ## Abstract ##
            ##############

            mdfile.write(f"\n## Abstract\n{row["Abstract"]}") # Write the abstract
            if row["Presentation Documents"]!="":
                mdfile.write(f"\n\n- [{row["Name of the conference"]} ({row["Year of the conference"]})]({row["Presentation Documents"]})") # Write the url of the presentation slides as a hyperlink with [Conference (date)] as text
            mdfile.write(f"\n\n---\n")

            #############
            ## Contact ##
            #############

            mdfile.write(f"\n## Contact")
            mdfile.write(f"\n\n")

            mdfile.write(f"<b>Authors :</b>\n{row["Author names,affiliation"]}".replace(':',' : ').replace('\n','\n- ')) # Write Authors name and afficiations as a list
            mdfile.write(f"\n\n")

            # Supporting entities remove for now
            #mdfile.write(f"<b>Supported by :</b>\n{row[7]}".replace(':',' : ').replace('\n','\n- ')) # Write supporting entities as a list
            #mdfile.write(f"\n\n")

            if row["Related IPPOG member"] != "":
                mdfile.write(f"<b>Related IPPOG Collaboration member :</b>\n") # Write IPPOG members as hyperlink to the related ippog.org page
                contact = next(iter({row["Related IPPOG member"]})).split(', ')
                for i in range (len(contact)):
                    mdfile.write(f"- [{contact[i]}]({members_dico[contact[i]]})\n") # Call the URL from the dictionary

            mdfile.write(f"\n<b>Contact :</b>\n- {row["Public contact"]}".replace('@',' [at] ')) # Protect email by replacing @ with [at]

            mdfile.write(f"\n\n---\n")

            ############
            ## Status ##
            ############

            mdfile.write(f"\n## Project status\n{row["Project Status"]} (updated {datetime.today().strftime('%Y-%m-%d')})") # Write the project status at today's date

            mdfile.write(f"\n\n---\n")

            ################
            ## Ressoucres ##
            ################

            ressource = next(iter({row["Other resources"]})).split('\n') # Separate ressources and write them as a list of hyperlink
            if(ressource!=['']):
                mdfile.write(f"\n## Files & Resources")

                for j in range (len(ressource)):
                    if ressource[j]!="":
                        if len({ressource[j].replace(' :',':').replace(': ',':').split(':http')[0]}) == 2:
                            mdfile.write(f"\n- [{ressource[j].replace(' :',':').replace(': ',':').split(':http')[0]}](http{ressource[j].replace(' ','').split(':http')[1]})")
                        else:
                            print("/!\\ ERROR WHILE WRITING RESOURCES /!\\\n")
                mdfile.write(f"\n\n---\n")

            ######################
            ## Resources & Tags ##
            ######################

            mdfile.write(f"\n< TODO Run commande `/categories`> \n< TODO Run commande `/tags`>")

            ###########
            ## Bonus ##
            ###########

            ### Should not appear on the website, the PROJECT-ID should be used for the URL slug, Categories and Tags sould be added to the corresponding menu
            mdfile.write(f"\n\n<TODO Manually add the categories and tags then remove everything bellow>")
            mdfile.write(f"\nPROJECT-{ID}")
            mdfile.write(f"\nCategories : {row["Audiences"]} / {row["Langage"]} / {row["Topics"]} / {row["Type"]}")
            mdfile.write(f"\nTags : {row["Sub Types"]} / {row["Sub Topics"]}")

        print(f"Created: {filepath}")

    print(f'\nMarkdown files are avalable at : {pathlib.Path().resolve()}/output_markdown')

print("\n#################################")
print("# Welcome to the JSON to MD code #")
print("#################################\n")
print("This code enable the user to tranform online google-sheet file from https://docs.google.com/forms/d/e/1FAIpQLSckjdwv7daQZ8jv7D1wwx6mKeZo2Hp4hLGGmV8FT0VTthvOUg/viewform")
print("To a formated, almost ready to past on the https://ippog-resources-portal.web.cern.ch/ website, md file")
print("In case of problem, don't hesitate to contact hector.pillot [at] proton.me\n")

print("Do you want to use Online mode (through Google API) or local mode (through csv file)?")
flag = input("> Please input api or csv:\n")

json_to_md("output_markdown")