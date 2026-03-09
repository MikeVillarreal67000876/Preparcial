from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List
import csv
import random

app = FastAPI(title="Pokemon API - Pre Parcial")


class Pokemon(BaseModel):
    id: int
    name: str
    attack: int
    live: int
    type: str

    def attack_action(self):
        return f"{self.name} attacks with power {self.attack}"

    def leave_pokeball(self):
        return f"{self.name} leaves the Pokeball!"


def load_pokemons_from_csv(filename: str) -> List[Pokemon]:
    pokemons = []
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            pokemons.append(
                Pokemon(
                    id=int(row["id"]),
                    name=row["name"],
                    attack=int(row["attack"]),
                    live=int(row["live"]),
                    type=row["type"]
                )
            )
    return pokemons


pokemons = load_pokemons_from_csv("pokemon.csv")


@app.get("/")
def home():
    return {"message": "Welcome trainer to the Pokemon API"}


@app.get("/showallpokemons/", response_model=List[Pokemon])
def show_all_pokemons():
    return pokemons


@app.get("/showonepokemon/", response_model=Pokemon)
def show_one_pokemon(name: str = Query(...)):
    for pokemon in pokemons:
        if pokemon.name.lower() == name.lower():
            return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")


@app.get("/showonepokemonbyid/", response_model=Pokemon)
def show_one_pokemon_by_id(id: int = Query(...)):
    for pokemon in pokemons:
        if pokemon.id == id:
            return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")


@app.get("/pokemonbattle/")
def pokemon_battle(
    pokemon1: str = Query(...),
    pokemon2: str = Query(...)
):
    p1 = None
    p2 = None

    for pokemon in pokemons:
        if pokemon.name.lower() == pokemon1.lower():
            p1 = pokemon
        if pokemon.name.lower() == pokemon2.lower():
            p2 = pokemon

    if not p1 or not p2:
        raise HTTPException(status_code=404, detail="One or both pokemons not found")

    score1 = p1.attack + p1.live + random.randint(1, 20)
    score2 = p2.attack + p2.live + random.randint(1, 20)

    if score1 > score2:
        winner = p1.name
    elif score2 > score1:
        winner = p2.name
    else:
        winner = "Draw"

    return {
        "message": "What an exciting battle!",
        "pokemon_1": p1,
        "pokemon_2": p2,
        "pokemon_1_action": p1.attack_action(),
        "pokemon_2_action": p2.attack_action(),
        "winner": winner
    }


@app.get("/pokemonorderedby/", response_model=List[Pokemon])
def pokemon_ordered_by(
    field: str = Query(...),
    desc: bool = Query(False)
):
    valid_fields = ["id", "name", "attack", "live", "type"]

    if field not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field. Use one of: {valid_fields}"
        )

    ordered_list = sorted(
        pokemons,
        key=lambda pokemon: getattr(pokemon, field),
        reverse=desc
    )

    return ordered_list