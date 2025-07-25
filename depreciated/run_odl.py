import csv
import os
from datetime import datetime
import pathlib

from member_dictionary import members_dico

def csv_to_md(csv_filename, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    with open(csv_filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Read the first row as headers
        
        begin = input("\n> Enter the ID of the first project to run (if no ID is selected, all project will be run through) : ")
        if begin =="":
            print("All project will be formated as no ID were given")
        else :
            print(f"Projects starting from ID \"PROJECT-{begin}\" will be formated")

        for row in reader:
            if not row:
                continue  # Skip empty rows

            if begin !="" and int(row[0]) < int(begin):
                continue # Skip stating project

            if row[23]!="OK":
                continue #Skip not "OK" status

            if row[0]!="":
                ID = row[0]
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
                mdfile.write(f"<TODO run the command `/media & text` manually with the \"show media on the right option\">")
                mdfile.write(f"<TODO run the command `/title` in the left column and \"featured image\" in the right>")
                mdfile.write(f"\n# {row[1]}") # Name of the project in English

                if row[2]!="":
                    mdfile.write(f"\n## {row[2]}") # Name of the project in it's original language (optional)
                
                if row[3]!="":
                    mdfile.write(f"\n<TODO Featured image is > {row[3]}")
                    mdfile.write(f"\n<TODO ragged right > Credit : {row[4]}") # Credit for the image
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

                mdfile.write(f"<b>Authors :</b>\n{row[6]}".replace(':',' : ').replace('\n','\n- ')) # Write Authors name and afficiations as a list
                mdfile.write(f"\n\n")

                # Supporting entities remove for now
                #mdfile.write(f"<b>Supported by :</b>\n{row[7]}".replace(':',' : ').replace('\n','\n- ')) # Write supporting entities as a list
                #mdfile.write(f"\n\n")

                if row[19] != "":
                    mdfile.write(f"<b>Related IPPOG Collaboration member :</b>\n") # Write IPPOG members as hyperlink to the related ippog.org page
                    contact = next(iter({row[19]})).split(', ')
                    for i in range (len(contact)):
                        mdfile.write(f"- [{contact[i]}]({members_dico[contact[i]]})\n") # Call the URL from the dictionary

                mdfile.write(f"\n<b>Contact :</b>\n- {row[8]}".replace('@',' [at] ')) # Protect email by replacing @ with [at]

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
                            mdfile.write(f"\n- [{ressource[j].replace(' :',':').replace(': ',':').split(':http')[0]}](http{ressource[j].replace(' ','').split(':http')[1]})")
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
                mdfile.write(f"\nCategories : {row[17]} / {row[18]} / {row[16]} / {row[15]}")
                mdfile.write(f"\nTags : {row[20]} / {row[21]}")

            print(f"Created: {filepath}")

        print(f'\nMarkdown files are avalable at : {pathlib.Path().resolve()}/output_markdown')

print("\n#################################")
print("# Welcome to the CSV to MD code #")
print("#################################\n")
print("This code enable the user to tranform csv file from https://docs.google.com/forms/d/e/1FAIpQLSckjdwv7daQZ8jv7D1wwx6mKeZo2Hp4hLGGmV8FT0VTthvOUg/viewform")
print("To a formated, almost ready to past on the https://ippog-resources-portal.web.cern.ch/ website, md file")
print("In case of problem, don't hesitate to contact hector.pillot [at] proton.me\n")

file = input("> Enter the csv file name without the extension .csv : ")
#file = "exemple_file"

print(f'The input file is : {pathlib.Path().resolve()}/{file}.csv')
csv_to_md(file+".csv", "output_markdown")