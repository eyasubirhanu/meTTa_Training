from hyperon import MeTTa
from hyperon.atoms import ExpressionAtom, SymbolAtom
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
    
    transcript = metta.run(f'''
            !(match &space (transcribed_to ({node[0]}) $B) (transcribed_to ({node[0]}) $B))
        ''') #TODO
    return transcript     #[[(, (transcribed_to (gene ENSG00000175793) (transcript ENST00000339276)))]]

#2 point
def get_protein(node):
    protein = metta.run(f'''
        ! (match &space (, (transcribed_to ({node[0]}) $B) (translates_to $B $C) )  (translates_to $B $C))
    ''') #TODO
    return protein

def reduce_expression(atoms):
    result = []
    for atom in atoms.get_children():
        if isinstance(atom, SymbolAtom):
            result.append(atom.get_name())
    return " ".join(result)

def metta_seralizer(metta_result):
    # result = [{'edge':metta_result[0][0].get_children()[0],
    #            'source':str(metta_result[0][0].get_children()[1])[1:-1],
    #            'target':str(metta_result[0][0].get_children()[2])[1:-1]}]
    
    result = []
    legend = {1: "source", 2:"target"}
    for meta in metta_result[0]:
        values = {}
        for atom in meta.get_children():
            if isinstance(atom, ExpressionAtom):
                values[legend[meta.get_children().index(atom)]] = reduce_expression(atom)
            elif isinstance(atom, SymbolAtom):
               values['edge'] = atom
            
        result.append(values)

    
    return result

result= (get_transcript(['gene ENSG00000166913'])) # change the gene id to "ENSG00000166913"
print(result) #[[(, (transcribed_to (gene ENSG00000175793) (transcript ENST00000339276)))]]

#6 point
parsed_result = metta_seralizer(result)
print(parsed_result) # [{'edge': 'transcribed_to', 'source': 'gene ENSG00000175793', 'target': 'transcript ENST00000339276'}]