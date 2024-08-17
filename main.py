from hyperon import *
import os
import glob

metta = MeTTa()
metta.run(f"!(bind! &space (new-space))")

def load_dataset(path: str) -> None:
    if not os.path.exists(path):
        raise ValueError(f"Dataset path '{path}' does not exist.")
    paths = glob.glob(os.path.join(path, "**/*.metta"), recursive=True)
    if not paths:
        raise ValueError(f"No .metta files found in dataset path '{path}'.")
    for path in paths:
        print(f"Start loading dataset from '{path}'...")
        try:
            metta.run(f'''
                !(load-ascii &space {path})
                ''')
        except Exception as e:
            print(f"Error loading dataset from '{path}': {e}")
    print(f"Finished loading {len(paths)} datasets.")

# Example usage:
try:
    dataset = load_dataset("./Data")
   
except Exception as e:
    print(f"An error occurred: {e}")

# 2 point
def get_transcript(node):

    gene = node[0]
    query = f"!(match &space (transcribed_to ({gene}) $result) (transcribed_to ({gene}) $result))"
    transcript = metta.run(query)
    return transcript   #[[(, (transcribed_to (gene ENSG00000175793) (transcript ENST00000339276)))]]

#2 point
def get_protein(node):
    gene = node[0]
    query = f"!(match &space (transcribed_to ({gene}) $result) $result)"
    transcript = metta.run(query)
    protine = []
    for i in transcript[0]:
        query = f"!(match &space (translates_to {i} $result) (translates_to {i} $result))"
        protine.append(metta.run(query))

    return protine 

def metta_seralizer(metta_result):
    result = []
    for i in metta_result[0]:
        expr1 = metta.parse_single(f"{i}")
        
        edge = ""
        source = ""
        target = ""
        
        for index, atom in enumerate(expr1.get_children()):
            atom_str = str(atom).strip('()')
            
            if index == 0:
                edge = atom_str
            elif index == 1:
                source = atom_str
            elif index == 2: 
                target = atom_str

        result.append({
            'edge': edge,
            'source': source,
            'target': target
        })

    return result


result= (get_transcript(['gene ENSG00000166913'])) # change the gene id to "ENSG00000166913"
# print(result) #[[(transcribed_to (gene ENSG00000166913) (transcript ENST00000353703)), (transcribed_to (gene ENSG00000166913) (transcript ENST00000372839))]]


# #6 point
parsed_result = metta_seralizer(result)
print(parsed_result) # [{'edge': 'transcribed_to', 'source': 'gene ENSG00000175793', 'target': 'transcript ENST00000339276'}]
