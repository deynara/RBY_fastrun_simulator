import os
import csv

class Pokemon():
    def __init__(self, species, level = 5, name=None, costum_moves = []):
        self.__bst = self.__get_stats(species)
        #print ("DEBUG", self.__bst)
        self.species = species.title()
        if name == None:
            self.name = species
        else:
            self.name = name
        
        self.exp = {}
        self.exp["level"] = level
        self.exp["total"] = 0
        self.exp["next"] = 0
        self.__init_exp(level)

        self.attacks = costum_moves
        self.__levelup_atks = {}
        self.__init_attacks(level)
        #self.attacks = costum_moves
        #if self.attacks != []: self.attacks = list(map(lambda x: x.title(), self.attacks))
        #self.__levelup_atks = self.__get_attacks()
        

        self.bst_debug = self.__bst
        self.lvl_atk_debug = self.__levelup_atks

    def __init_attacks(self, level):
        #Step 1 create dictionary levelup_attacks
        pkm = self.species.title()
        own_path =  os.path.dirname(os.path.realpath('__file__'))
        file_path = own_path[0:own_path.find("RBY_fastrun_simulator")] + "RBY_fastrun_simulator/raw_data/RB_attacks_level.csv"
        with open(file_path) as csv_file:
            reader = csv.reader(csv_file, delimiter=',') 
            entrys = [row for row in reader]
            header = entrys.pop(0)
        if pkm not in header:
            raise Exception(f"Error initializing move data, couldn't find |{pkm}|in 'RB_attacks_level.csv.")
        pos = header.index(pkm)
        for entry in entrys:
            new_key = int(entry[0])
            new_value = entry[pos]
            if new_value != "":
                if new_key not in self.__levelup_atks.keys():
                    self.__levelup_atks[new_key] = []
                self.__levelup_atks[new_key].append(new_value)
        #Step 2: get current moves
        if self.attacks != []:
            #print("DEBUG early return")
            return #has costum moveset ->early return
        if level < 1:
            raise Exception(f"Error initializing move data, level can't be lower than 1, gave |{level}|.")
        #print ("keys:", self.__levelup_atks.keys())
        for i in range(1, level+1):
            #print (i, i in self.__levelup_atks.keys())
            if i in self.__levelup_atks.keys():
                for attack in self.__levelup_atks[i]:
                    self.learn_attack(attack)
        

    def learn_attack(self, new_attack, forget=None):
        #print ("DEBUG new attack", new_attack)
        if new_attack in self.attacks: return
        if forget == None:
            if len(self.attacks) >= 4:
                self.attacks.pop(0)
            self.attacks.append(new_attack.title())
        else:
            forget = forget.title()
            if forget not in self.attacks:
                raise Exception (f"{self.name} can't forget a move (|{forget}|), it doesn't know.")
            else:
                self.attacks[self.attacks.index(forget)] = new_attack.title()
                

    def __get_attacks(self): #method replaced by __init_attacks
        pkm = self.species
        own_path =  os.path.dirname(os.path.realpath('__file__'))
        file_path = own_path[0:own_path.find("RBY_fastrun_simulator")] + "RBY_fastrun_simulator/raw_data/level_attacks.csv"
        with open(file_path) as csv_file:
            temp = csv_file.read() 
        spec_pos = temp.find(pkm.lower())
        Pkm_exists = spec_pos >= 0
        if not Pkm_exists:
            raise Exception (f"{pkm} was not found in level_attacks.csv")
        pass
        temp = temp[spec_pos:len(temp)]
        if temp.find("\n") >= 0:
            spec_line = temp[0:temp.find("\n")].split(", ")
        else:
            spec_line = temp.split(", ")

        lvl_attacks = {}
        for entry in spec_line:
            if entry.find(":") > 0:
                temp = list(map(lambda x: x.strip().title(), entry.split(":")))
                #print("temp: ", temp)
                lvl_attacks[int(temp.pop(0))] = temp

        if self.attacks == []: #learn levelupattacks if not costum moveset
            for i in range(self.exp["level"]+1):
                if i in lvl_attacks.keys():
                    for entry in lvl_attacks[i]:    
                        self.learn_attack(entry)         
        return lvl_attacks

    def __get_stats(self, pkm):
        own_path =  os.path.dirname(os.path.realpath('__file__'))
        file_path = own_path[0:own_path.find("RBY_fastrun_simulator")] + "RBY_fastrun_simulator/raw_data/pokemon.csv"
        with open(file_path) as csv_file:
            temp = csv_file.read() 
        spec_pos = temp.find(pkm.title())
        Pkm_exists = spec_pos >= 0
        if not Pkm_exists:
            raise Exception (f"|{pkm}| was not found in pokemon.csv")
        header = temp[0:temp.find("\n")].split(",")
        temp = temp[spec_pos:len(temp)]
        if temp.find("\n") >= 0:
            spec_line = temp[0:temp.find("\n")].split(",")
        else:
            spec_line = temp.split(",")
        bst = {}
        if len(header) != len(spec_line):
            raise IndexError(f"Bst_initialization: Unbalanced entry counts {len(header)}|{len(spec_line)} between header and species line {pkm}. Did you forget a comma?")
        for i in range(1, len(header)):
            bst[header[i]] = spec_line[i]
        return bst
    
    def __init_exp(self, level):
        if level < 1 or type(level) != int:
            raise Exception(f"Targetlevel ({level}) lower than 1 or not a whole number")
        n = self.exp["level"]      
        match (self.__bst["exp_group"]):
            case "fast":
                self.exp["total"] = int((4*n**3/5))
                if n < 100:
                    n += 1
                    self.exp["next"] = int((4*n**3/5)) - self.exp["total"]
            case "mid_fast":
                self.exp["total"] = n**3
                if n < 100:
                    n += 1
                    self.exp["next"] = n**3 - self.exp["total"]
            case "mid_slow":
                self.exp["total"] = int((6/5) * n**3 - 15 * n**2 + 100 * n - 140)
                if n < 100:
                    n += 1
                    self.exp["next"] = int((6/5) * n**3 - 15 * n**2 + 100 * n - 140) - self.exp["total"]
            case "slow":
                self.exp["total"] = int((5*n**3/4))
                if n < 100:
                    n += 1
                    self.exp["next"] = int((5*n**3/4)) - self.exp["total"]
            case _:
                raise Exception(f"Unknown Exp-group: {self.__bst['exp_group']}")
    
    def __repr__(self):
        vocals = "aeiou"
        proper_grammar = ""
        if self.species[0].lower() in vocals:
            proper_grammar = "n"
        return f"|{self.name}| is a{proper_grammar} {self.species} and knows these moves {self.attacks}\nExp:{self.exp}\nStats:{self.__bst}\nlevelup attacks:{self.__levelup_atks}\n"




def main():
    test = Pokemon("Bulbasaur", 5)
    print(f"{test.species} is at level {test.level}")
if __name__ == "__main__":
    main()