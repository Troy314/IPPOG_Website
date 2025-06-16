import csv
import os
from datetime import datetime
import pathlib

## The members_dico Dictionnary link the IPPOG member to it's URL page on the website ippog.org
## /!\ It need to be updated for new members

members_dico =	{
"ALICE Collaboration": "https://ippog.org/members/alice-collaboration",
"ATLAS Collaboration": "https://ippog.org/members/atlas-collaboration",
"Australia": "https://ippog.org/members/australia-bondell",
"Austria": "https://ippog.org/members/austria",
"Belgium": "https://ippog.org/members/belgium-1",
"Belle II Collaboration": "https://ippog.org/members/belle-ii-collaboration-1",
"Brazil": "https://ippog.org/members/brazil",
"Bulgaria": "https://ippog.org/members/bulgaria",
"CERN": "https://ippog.org/members/cern-8",
"CMS Collaboration": "https://ippog.org/members/cms-collaboration",
"Cyprus": "https://ippog.org/members/cyprus",
"Czech Republic": "https://ippog.org/members/czech-republic",
"Denmark": "https://ippog.org/members/denmark",
"DESY": "https://ippog.org/members/desy-3",
"Finland": "https://ippog.org/members/finland",
"France": "https://ippog.org/members/france",
"Georgia": "https://ippog.org/members/georgia",
"Germany": "https://ippog.org/members/germany-0",
"Greece": "https://ippog.org/members/greece-1",
"GSI": "https://ippog.org/members/gsi",
"HAWC Collaboration": "https://ippog.org/members/hawc-collaboration",
"Hungary": "https://ippog.org/members/hungary-2",
"India": "https://ippog.org/members/india",
"Ireland": "https://ippog.org/members/ireland",
"Israel": "https://ippog.org/members/israel",
"Italy": "https://ippog.org/members/italy-1",
"Latvia": "https://ippog.org/members/latvia",
"LHCb Collaboration": "https://ippog.org/members/lhcb-collaboration",
"Mexico": "https://ippog.org/members/mexico",
"Montenegro": "https://ippog.org/members/montenegro-2",
"Netherlands": "https://ippog.org/members/netherlands-0",
"Norway": "https://ippog.org/members/norway",
"Pierre Auger Observatory": "https://ippog.org/members/pierre-auger-observatory",
"Poland": "https://ippog.org/members/poland",
"Portugal": "https://ippog.org/members/portugal",
"Romania": "https://ippog.org/members/romania",
"Slovakia": "https://ippog.org/members/slovakia",
"Slovenia": "https://ippog.org/members/slovenia-1",
"South Africa": "https://ippog.org/members/south-africa-1",
"Spain": "https://ippog.org/members/spain-1",
"Sweden": "https://ippog.org/members/sweden-2",
"Switzerland": "https://ippog.org/members/switzerland",
"United Kingdom": "https://ippog.org/members/united-kingdom-0",
"United States of America": "https://ippog.org/members/united-states-america"
}

def csv_to_md(csv_filename, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    with open(csv_filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Read the first row as headers
        
        for row in reader:
            if not row:
                continue  # Skip empty rows

            ID = input("\n> Enter {'" + row[1] + "'} project ID : ") # Give an ID to the project if should be the same as the name of the webpage and the image
            print({row[1]}," is now defined as - PROJECT-" + ID + " -")

            filename = "PROJECT-" + ID  + ".md"  # Create filename from first cell
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, "w", encoding="utf-8") as mdfile:
                
                ###########
                ## Title ##
                ###########

                mdfile.write(f"---\n\n")
                mdfile.write(f"\media & text <run the command manually with the \"show media on the right option\">")
                mdfile.write(f"\n<Featured image> {row[3]}")
                mdfile.write(f"\n# {row[1]}") # Name of the project in English

                if row[2]!="":
                    mdfile.write(f"\n## {row[2]}") # Name of the project in it's original language (optional)
                mdfile.write(f"\n<ragged right>Credit : {row[4]}") # Credit for the image
                mdfile.write(f"\n\n---\n")

                ##############
                ## Abstract ##
                ##############

                mdfile.write(f"\n## Abstract\n{row[5]}") # Write the abstract
                if row[12]!="":
                    mdfile.write(f"\n\n[{row[12]} ({row[13]})]({row[14]})") # Write the url of the presentation slides as a hyperlink with [Conference (date)] as text
                mdfile.write(f"\n\n---\n")

                #############
                ## Contact ##
                #############

                mdfile.write(f"\n## Contact")
                mdfile.write(f"\n\n")

                mdfile.write(f"<b>Authors :</b>\n{row[6]}".replace(':',' : ').replace('\n','\n- ')) # Write Authors name and afficiations as a list
                mdfile.write(f"\n\n")

                mdfile.write(f"<b>Supported by :</b>\n{row[7]}".replace(':',' : ').replace('\n','\n- ')) # Write supporting entities as a list
                mdfile.write(f"\n\n")

                mdfile.write(f"<b>Related IPPOG Collaboration member :</b>\n") # Write IPPOG members as hyperlink to the related ippog.org page
                contact = next(iter({row[8]})).split(', ')
                print(row[8])
                for i in range (len(contact)):
                    mdfile.write(f"- [{contact[i]}]({members_dico[contact[i]]})\n") # Call the URL from the dictionary

                mdfile.write(f"\n<b>Contact :</b>\n- {row[9]}".replace('@',' [at] ')) # Protect email by replacing @ with [at]

                mdfile.write(f"\n\n---\n")

                ############
                ## Status ##
                ############

                mdfile.write(f"\n## Project status\n{row[11]} (updated {datetime.today().strftime('%Y-%m-%d')})") # Write the project status at today's date

                mdfile.write(f"\n\n---\n")

                ################
                ## Ressoucres ##
                ################

                ressource = next(iter({row[15]})).split('\n') # Separate ressources and write them as a list of hyperlink
                if(ressource!=['']):
                    print(ressource)
                    mdfile.write(f"\n## Files & Resources")

                    for j in range (len(ressource)):
                        mdfile.write(f"\n- [{ressource[j].split(':')[0]}]({ressource[j].split(':')[1]})")
                    mdfile.write(f"\n\n---\n")

                ######################
                ## Resources & Tags ##
                ######################

                mdfile.write(f"\n/categories <command need to be input manually>\n/tags <command need to be input manually>")

                ###########
                ## Bonus ##
                ###########

                ### Should not appear on the website, the PROJECT-ID should be used for the URL slug, Categories and Tags sould be added to the corresponding menu
                mdfile.write(f"\n\n<Manually add the categories and tags then remove everything bellow>")
                mdfile.write(f"\nPROJECT-{ID}")
                mdfile.write(f"\nCategories : {row[18]} / {row[19]} / {row[17]} / {row[16]}")
                mdfile.write(f"\nTags : {row[20]} / {row[21]} / {row[22]}")

            print(f"Created: {filepath}")

        print(f'\nMarkdown files are avalable at : {pathlib.Path().resolve()}/output_markdown')

print("\n#################################")
print("# Welcome to the CSV to MD code #")
print("#################################\n")
print("This code enable the user to tranform csv file from https://docs.google.com/forms/d/e/1FAIpQLSckjdwv7daQZ8jv7D1wwx6mKeZo2Hp4hLGGmV8FT0VTthvOUg/viewform")
print("To a formated, almost ready to past on the https://ippog-resources-portal.web.cern.ch/ website, md file")
print("In case of problem, don't hesitate to contact hector.pillot [at] proton.me\n")
#print("When downloading the csv file on https://framaforms.org/node/1181030/webform-results/download,")
#print("> In \"Sélectionner la liste des options\"")
#print("> Select \"Compact\"\n")
file = input("> Enter the csv file name without the extension .csv : ")
#file = "IPPOG success story submittion (réponses) - Réponses au formulaire 1"
print(f'The input file is : {pathlib.Path().resolve()}/{file}.csv')
csv_to_md(file+".csv", "output_markdown")