import json
import requests
from Pokemon import Pokemon, Type, Tier, Category, Ability, Stats, Move
formats = ["AG", "Uber", "OU", "UUBL", "UU", "RUBL", "RU", "PUBL", "PU", "NUBL", "NU", "ZUBL", "ZU"]
types = ["Normal", "Fire", "Water", "Grass", "Electric", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic",
         "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"]
all_abilities = {}
all_moves = set()


def get_all_moves() -> {}:
    f = open("gen9ou-1825.json")
    all_gen_9_pokemon = json.load(f)
    # print(json.dumps(all_gen_9_pokemon["data"]["Iron Leaves"], indent=4))
    for k, v in all_gen_9_pokemon["data"].items():
        for m, val in v["Moves"].items():
            if m is not None and m != "":
                all_moves.add(m)

    with open("allmoves.json", "w") as f:
        json.dump(sorted(all_moves), f, indent=4)


def get_pokemon():
    with open("allmoves.json", "r") as f:
        global all_moves
        all_moves = json.load(f)

    with open("pokejson.json", "r") as f:
        all_data = json.load(f)
        all_pokemon = all_data["injectRpcs"][1][1]['pokemon']
        valid_pokemon = []

        for p in all_pokemon:
            in_tier = len(set(formats) & set(p["formats"]))
            if in_tier != 0 and p["oob"] is not None and len(p.get("alts", [])) == 0 and "SV" in p.get("oob").get("genfamily"):
                p.pop("height")
                p.pop("weight")
                p.pop("oob")
                get_pokeapi(p)
                valid_pokemon.append(p)
        json.dump(valid_pokemon, open("allpokemon.json", "w"), indent=4)
        print(json.dumps(valid_pokemon[0], indent=4))



def get_pokeapi(p):
    check_for_exception(p)
    pokemon_name = p.get("pokeapiname", p.get("name"))
    pokemon_name = pokemon_name.replace(" ", "-")
    pokemon_name = pokemon_name.lower()
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
    global all_moves
    if r.status_code == 200:
        poke_data = r.json()
        p_moves = []
        for m in poke_data.get("moves"):
            m_name = m["move"].get("name", "")
            m_name = m_name.replace("-", "")
            if m_name in all_moves:
                p_moves.append(m_name)
            p["moves"] = p_moves

    else:
        print(f"Unable to get PokeApi Data for {p['name']}.")
        print(f"Response Code: {r.status_code} {r.text}\n")

def check_for_exception(p):
    name = p["name"]
    if name in ("Tornadus", "Landorus", "Thundurus", "Enamorus"):
        p["pokeapiname"] = name + "-therian"
    elif "Tauros-Paldea" in name:
        p["pokeapiname"] = name + "-breed"
    elif name == "Toxtricity":
        p["pokeapiname"] = name + "-amped"
    elif name == "Indeedee":
        p["pokeapiname"] = name + "-male"
    elif name == "Indeedee-F":
        p["pokeapiname"] = "Indeedee-female"
    elif name == "Basculegion":
        p["pokeapiname"] = name + "-male"
    elif name == "Basculegion-F":
        p["pokeapiname"] = "Basculegion-female"
    elif name == "Mimikyu":
        p["pokeapiname"] = name + "-disguised"
    elif name == "Meloetta":
        p["pokeapiname"] = name + "-aria"

def Intersection(lst1, lst2):
    return set(lst1).intersection(lst2)

if __name__ == '__main__':
    get_pokemon()
