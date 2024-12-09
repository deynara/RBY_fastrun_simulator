import os, sys
#including relative paths for import of modules in there
own_path =  os.path.dirname(__file__)
#print(own_path, "\n")
sys.path.append(f"{own_path}/pythoncode/classes")

from class_pokemon import *
def testing(test):
    print ("\n----------new test starting-------")
    quote = '"'
    #print(test.species[0].lower())
    if test.species[0].lower() in "aeiou": 
        proper_grammar = "n"
    else: proper_grammar = ""

    print(f"{quote}{test.name}{quote} is a{proper_grammar} {test.species}. \n")
    print(f"After collecting {test.exp['total']} exp it reached level {test.exp['level']} and needs {test.exp['next']} exp more for the next level.")
    print(f"{test.name} knows these attacks: {test.attacks}")
    print(f"\n{test.species}'s can learn these moves by levelup:\n{test.lvl_atk_debug}\n")

def main():

    print("-----Starting Main----")
    
    #testing(Pokemon("bulbasaur"))
    #testing(Pokemon("ivysaur",17, costum_moves = []))
    #testing(Pokemon("Starmie",21, name= "Misty's Starmie", costum_moves = ["Tackle", "water gun", "bubble beam"]))
    #print(Pokemon("Bulbasaur"))
    #print(Pokemon("Eevee", 15, "Veevee"))
    print(Pokemon("ivysaur", 22, "the Evolved"))
    #print(test.bst_debug)


    #stats = get_stats (test)
    #print (stats)


            

        
        

if __name__ == "__main__":
    main()