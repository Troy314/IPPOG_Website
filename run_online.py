import csv
import os
from datetime import datetime
import pathlib

from dictionaries.member_dictionary import members_dico

import gspread
from google.oauth2.service_account import Credentials

def json_to_md(output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load Google Sheets API credentials
    #SERVICE_ACCOUNT_FILE = "YOURJSONFILE"  # Update with your JSON file
    SERVICE_ACCOUNT_FILE = "ippog-466111-e8e5130144ad.json"
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    # Authenticate and create the client
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)

    # Open the Google Sheet by ID
    SHEET_ID = "1x_SdxdlHwG8chH77WqrTAAgijY2XBY3nPIi2p3TKqzs"  # Sheet ID
    sheet = client.open_by_key(SHEET_ID).get_worksheet(0)  # Access the first worksheet

    data = sheet.get_all_records()

    print("\nYou can either run through all projects with status \"OK\" or only run through a specific project")
    begin = input("\n> Enter the ID of the project to run (if no ID is selected, all \"OK\" project will be run through) : ")
    if begin =="":
        print("All project will be formated as no ID were given")
    else :
        print(f"PROJECT-{begin}\" will be formated")

    for row in data: 
        row = list(row.values())

        if not row:
            continue  # Skip empty rows

        if begin !="" and int(row[0]) != int(begin):
            continue # Skip project untill selected ID
        elif begin =="" and row[23]!="OK":
            continue #Skip not "OK" status

        if row[0]!="":
            ID = str(row[0])
        else :
            print("\n#############################################\n# ERROR please define an ID in the database #\n#############################################")
            print(f"\n/!\\ no ID for project \"{row[1]}\" /!\\")
            break
        print(f"\n\"{row[1]}\" is now defined as - PROJECT-" + ID + " -")

        filename = "PROJECT-" + ID  + ".md"  # Create filename from first cell
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as mdfile:
            
            ###########
            ## Title ##
            ###########

            mdfile.write(f"---\n\n")
            mdfile.write(f"[draft] title: {row[1]}")
            mdfile.write(f"\n[draft] ID: {ID}")
            mdfile.write(f"\n[draft] run `/media & text` with the \"show media on the right\"")
            mdfile.write(f"\n[draft] run `/title` in left column")
            mdfile.write(f"\n[draft] choose \"featured image\" in right column")

            if row[2]!="":
                mdfile.write(f"\n[draft] subtitle: {row[2]}") # Name of the project in it's original language (optional)
            
            if row[3]!="":
                mdfile.write(f"\n[draft] link to image: {row[3]}")
                mdfile.write(f"\n[draft] Align the credits to the righ, bellow the image")
                mdfile.write(f"\n\nCredit: {row[4]}") # Credit for the image
            else : 
                print("/!\\ no registered Featured image /!\\")
            mdfile.write(f"\n\n---\n")

            ##############
            ## Abstract ##
            ##############

            mdfile.write(f"\n## Abstract\n{row[5]}") # Write the abstract
            if row[13]!="":
                mdfile.write(f"\n\n- [{row[11]} ({row[12]})]({row[13]})") # Write the url of the presentation slides as a hyperlink with [Conference (date)] as text
            mdfile.write(f"\n\n---\n")

            #############
            ## Contact ##
            #############

            mdfile.write(f"\n## Contact")
            mdfile.write(f"\n\n")

            mdfile.write(f"<b>Authors:</b>\n{row[6]}".replace('\n','\n- ')) # Write Authors name and afficiations as a list
            mdfile.write(f"\n\n")

            # Supporting entities remove for now
            #mdfile.write(f"<b>Supported by :</b>\n{row[7]}".replace('\n','\n- ')) # Write supporting entities as a list
            #mdfile.write(f"\n\n")

            if row[19] != "":
                mdfile.write(f"<b>Related IPPOG Collaboration members:</b>\n") # Write IPPOG members as hyperlink to the related ippog.org page
                contact = next(iter({row[19]})).split(', ')
                for i in range (len(contact)):
                    mdfile.write(f"- [{contact[i]}]({members_dico[contact[i]]})\n") # Call the URL from the dictionary

            mdfile.write(f"\n<b>Contact:</b>\n- {row[8]}".replace('@',' [at] ')) # Protect email by replacing @ with [at]

            mdfile.write(f"\n\n---\n")

            ############
            ## Status ##
            ############

            mdfile.write(f"\n## Project status\n{row[10]} (updated {datetime.today().strftime('%Y-%m-%d')})") # Write the project status at today's date

            mdfile.write(f"\n\n---\n")

            ################
            ## Ressoucres ##
            ################

            ressource = next(iter({row[14]})).split('\n') # Separate ressources and write them as a list of hyperlink
            if(ressource!=['']):
                mdfile.write(f"\n## Files & Resources")

                for j in range (len(ressource)):
                    if ressource[j]!="":
                        if len(ressource[j].replace(' :',':').replace(': ',':').split(':http')) == 2:
                            mdfile.write(f"\n- [{ressource[j].replace(' :',':').replace(': ',':').split(':http')[0]}](http{ressource[j].replace(' ','').split(':http')[1]})")
                        else:
                            print("/!\\ ERROR WHILE WRITING RESOURCES /!\\")
                            print("ERROR may come from missing \"https\" or blank")
                            print("problem happened at Resource column, line: ",ressource[j].replace(' :',':').replace(': ',':').split(':http'),"\n")
                mdfile.write(f"\n\n---\n")

            ######################
            ## Resources & Tags ##
            ######################

            mdfile.write(f"\n[draft] run `/categories` \n[draft] run `/tags`")

            ###########
            ## Bonus ##
            ###########

            ### Should not appear on the website, the PROJECT-ID should be used for the URL slug, Categories and Tags sould be added to the corresponding menu
            mdfile.write(f"\n\n[draft] Add the categories and tags bellow")
            mdfile.write(f"\n[draft] Categories: {row[17]} / {row[18]} / {row[16]} / {row[15]}")
            mdfile.write(f"\n[draft] Tags: {row[20]} / {row[21]}")

        print(f"Created: {filepath}")

    print(f'\nMarkdown files are avalable at: {pathlib.Path().resolve()}/output_markdown')

print("\n#################################")
print("# Welcome to the JSON to MD code #")
print("#################################\n")
print("This code enable the user to tranform online google-sheet file from https://docs.google.com/forms/d/e/1FAIpQLSckjdwv7daQZ8jv7D1wwx6mKeZo2Hp4hLGGmV8FT0VTthvOUg/viewform")
print("To a formated, almost ready to past on the https://ippog-resources-portal.web.cern.ch/ website, md file")
print("In case of problem, don't hesitate to contact hector.pillot [at] proton.me\n")

json_to_md("output_markdown")