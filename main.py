from hyperon import *
import os
import glob
from hyperon import ExpressionAtom, SymbolAtom, GroundedAtom

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
    transcript = metta.run(f'''!(match &space
        (,  (transcribed_to ({node[0]}) $transcript)
            )
           (,(transcribed_to ({node[0]}) $transcript)))''')
    return transcript     #[[(, (transcribed_to (gene ENSG00000175793) (transcript ENST00000339276)))]]
   
#2 point
def get_protein(node):
    protein = metta.run(f'''!(match &space
        (,  (transcribed_to ({node[0]}) $transcript)
            (translates_to $transcript $protine)
            )
           (,(translates_to $transcript $protine)))''')
    return protein

def recurssive_seralize(children, result):
    for child in children:
        if isinstance(child, SymbolAtom):
            result.append(child)
        if isinstance(child, ExpressionAtom):
            recurssive_seralize(child.get_children(), result)
    return result

def metta_seralizer(metta_result):
    result = []
    parss =[]

    for node in metta_result[0]:
        node = node.get_children()
        for metta_symbol in node:
            if isinstance(metta_symbol, SymbolAtom) and  metta_symbol.get_name() == ",":
                continue
            if isinstance(metta_symbol, ExpressionAtom):
                res = recurssive_seralize(metta_symbol.get_children(), [])
                result.append(tuple(res))
    for r in result:
        predicate, src_type, src_id, tgt_type, tgt_id = r
        parss.append({
                "edge": predicate,
                "source": f"{src_type} {src_id}",
                "target": f"{tgt_type} {tgt_id}"
                    })
    return parss
    
result= (get_transcript(['gene ENSG00000166913'])) # change the gene id to "ENSG00000166913"
#print(result) #[[(, (transcribed_to (gene ENSG00000175793) (transcript ENST00000339276)))]]
# print(result[0][1]) 
get_protein(['gene ENSG00000166913'])
#6 point
parsed_result = metta_seralizer(result)
print(parsed_result) # [{'edge': 'transcribed_to', 'source': 'gene ENSG00000175793', 'target': 'transcript ENST00000339276'}]

