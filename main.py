from hyperon import MeTTa
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
    transcript = metta.run() #TODO
    return transcript     #[[(, (transcribed_to (gene ENSG00000175793) (transcript ENST00000339276)))]]

#2 point
def get_protein(node):
    protein = metta.run() #TODO
    return protein

def metta_seralizer(metta_result):
    #TODO
    return result

result= (get_transcript(['gene ENSG00000175793'])) # change the gene id to "ENSG00000166913"
print(result) #[[(, (transcribed_to (gene ENSG00000175793) (transcript ENST00000339276)))]]

#6 point
parsed_result = metta_seralizer(result)
print(parsed_result) # [{'edge': 'transcribed_to', 'source': 'gene ENSG00000175793', 'target': 'transcript ENST00000339276'}]

