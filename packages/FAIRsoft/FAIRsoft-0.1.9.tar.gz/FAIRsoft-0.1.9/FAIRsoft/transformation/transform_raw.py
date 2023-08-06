import os
import importlib

import FAIRsoft
import FAIRsoft.utils
from FAIRsoft.transformation.meta_transformers import tool_generators 

def get_raw_data_db(source, alambique):
    c = alambique.count({"@data_source":source})
    p = f"{c} entries from {source}"
    print(p)
    raw = alambique.find({"@data_source":source})
    return raw

   
def output_bioconda_dict(generator, source):
    if source == 'bioconda_recipes':
        generator.type_dictionary('bioconda_types.json')

def open_raw_files(source):
    import json
    files_sources = {
        'BIOCONDUCTOR':'OUTPUT_BIOCONDUCTOR',
        'BIOCONDA':'OUTPUT_OPEB_TOOLS',
        'BIOTOOLS':'OUTPUT_OPEB_TOOLS',
        'TOOLSHED':'OUTPUT_TOOLSHED',
        'GALAXY_METADATA':'OUTPUT_TOOLSHED',
        'SOURCEFORGE':'OUTPUT_SOURCEFORGE',
        'GALAXY_EU': 'OUTPUT_OPEB_TOOLS',
        'OPEB_METRICS': 'OUTPUT_OPEB_METRICS',
        'BIOCONDA_RECIPES':'OUTPUT_BIOCONDA_RECIPES',
        'BIOCONDA_CONDA':'OUTPUT_BIOCONDA_CONDA',
        'REPOSITORIES': 'OUTPUT_REPOS',
    }
    try:
        OUTPUT_PATH = os.getenv('OUTPUT_PATH', './data')
        data_file = OUTPUT_PATH    + '/' + os.getenv(files_sources[source])
    except KeyError:
        print("No file for {}".format(source))
        raise
    except TypeError:
        print("No file for {}".format(files_sources[source]))
        raise
    else:
        with open(data_file, 'r') as infile:
            raw = json.load(infile)
        p = f"{len(raw)} entries from {FAIRsoft.utils.sources_labels[source]}"
        print(p)
        return raw

def add_to_pretools_file(insts, output_file):
    import json
    if not os.path.isfile(output_file):
            with open(output_file, 'w') as outfile:
                json.dump(insts, outfile)
    else:   
        with open(output_file) as json_data_file:
            pretools = json.load(json_data_file)
        pretools.append(insts)


def transform_this_source(raw, this_source_label):
    # Instantiate toolGenerator specific to this source
    generator_module = importlib.import_module(f".meta_transformers", 'FAIRsoft.transformation')
    generator = generator_module.tool_generators[this_source_label](raw)
    
    # Export types dictionary in case of bioconda raw data 
    output_bioconda_dict(generator, this_source_label)
    
    # From instance objects to dictionaries
    insts = [i.__dict__ for i in generator.instSet.instances ]
    return(insts)



if __name__ == '__main__':
    # Run whole transformation pipeline
    ALAMBIQUE = os.getenv('ALAMBIQUE', 'alambique')
    PRETOOLS = os.getenv('PRETOOLS', 'pretools') 

    STORAGE_MODE = os.getenv('STORAGE_MODE', 'db')
    if STORAGE_MODE =='db':
        # raw data (input) collection
        alambique = FAIRsoft.utils.connect_collection(ALAMBIQUE)
        # transformed data collection
        pretools = FAIRsoft.utils.connect_collection(PRETOOLS)

    else:
        # Path of output file where the transformed data will be stored
        output_file = os.getenv('OUTPUT_PATH', './') + '/' + PRETOOLS + '.json'

    
    for source in FAIRsoft.utils.sources_to_transform:
        # Check if source has to be transformed
        if os.getenv(source) == 'True':
            # label to match "source" field in the raw data and appropriate transformer
            this_source_label = FAIRsoft.utils.sources_labels[source]
                        
            # 1. getting raw data
            print(f"Starting transformation of raw tools metadata from {this_source_label}")
            if STORAGE_MODE =='db':
                raw_data = get_raw_data_db(source, alambique)
            else:
                raw_data = open_raw_files(source)
            
            if not raw_data:
                print(f"No data for {this_source_label}")
            else:
                # 2. transformation
                print(f"Transforming raw tools metadata from {this_source_label}")
                insts = transform_this_source(raw_data, this_source_label)
                
                # 3. output transformed data
                if STORAGE_MODE =='db':
                    log = {'errors':[], 'n_ok':0, 'n_err':0, 'n_total':len(insts)}
                    for inst in insts:
                        log = FAIRsoft.utils.push_entry(inst, pretools)
                        
                    print(f"Pushed to database")
           
                else:
                    add_to_pretools_file(insts, output_file)    
                    print(f"Saved to file")
