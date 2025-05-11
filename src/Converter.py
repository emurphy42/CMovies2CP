import json5, shutil, os, json

from .Logger import logger

class Converter:
    manifest: dict = {}
    inputContent: dict = {}
    outputContent: dict = {
        "Format": "2.0",
        "Changes": []
    }
    
    def __init__(self):
        self.manifest = json5.load(open('input/manifest.json', encoding='utf8'))
        self.inputContent = json5.load(open('input/content.json', encoding='utf8'))

        if os.path.exists('output'):
            shutil.rmtree('output')
        shutil.copytree('input', 'output')

    def convert(self):
        # add images
        images = []
        for movie in self.inputContent['Movies']:
            if movie['Sheet'] != None and movie['Sheet'] != '' and not (movie['Sheet'] in images):
                images.append(movie['Sheet'])
        for image in images:
            change = {
                "Action": "Load",
                "Target": "Mods/{{ModId}}/" + image,
                "FromFile": image
            }
            self.outputContent['Changes'].append(change)

        # add movies
        for movie in self.inputContent['Movies']:
            # { additional keys not yet converted: "Scale" "Frames" "Looped" "AnimationSpeed!" "CranePrizeType" "CranePrizeName" }
            entry = {
                movie['Id']: {
                    'ID': movie['Id'],
                    'Seasons': [movie['Season']],
                    # manually adding e.g. 'YearModulus': 3, 'YearRemainder': 1 will limit it to years 2, 5, 8, etc.
                    'Texture': 'Mods/{{ModId}}/' + movie['Sheet'],
                    'SheetIndex': movie['SheetIndex'],
                    'Title': movie['Title'],
                    'Description': movie['Description'],
                    'Tags': movie['Tags'],
                    'Scenes': movie['Scenes']
                }
            }
            change = {
                "Action": "EditData",
                "Target": "Data/Movies",
                "Entries": entry
            }
            self.outputContent['Changes'].append(change)

        # add movie reactions, if any
        if 'Reactions' in self.inputContent:
            for reaction_set in self.inputContent['Reactions']:
                for reaction in reaction_set['Reactions']:
                    entry = {
                        'Reaction': reaction
                    }
                    change = {
                        "Action": "EditData",
                        "Target": "Data/MoviesReactions",
                        "TargetField": [reaction_set['NPCName'], 'Reactions'],
                        "Entries": entry
                    }
                    self.outputContent['Changes'].append(change)

        # finish up
        self.translateManifest()
        self.save()

    def translateManifest(self):
        self.manifest['UniqueID'] += '.CP'
        self.manifest['Author'] += ' ~ CMovies2CP'

        self.manifest['ContentPackFor']['UniqueID'] = 'Pathoschild.ContentPatcher'
        
        if 'Dependencies' in self.manifest:
            self.manifest['Dependencies'] = \
                [mod for mod in self.manifest['Dependencies'] if mod['UniqueID'] not in ['OldMod.Framework']]
        
    def save(self):
        
        with open('output/manifest.json', 'w') as f:
            json.dump(self.manifest, f, indent=4)
        
        with open('output/content.json', 'w') as f:
            json.dump(self.outputContent, f, indent=4)