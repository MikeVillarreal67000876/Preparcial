from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()


class Pokemon(BaseModel):
    id: int
    name: str
    attack: int
    live: int
    type: str


pokemons = [
    Pokemon(id=1, name="Bulbasaur", attack=49, live=45, type="Grass"),
    Pokemon(id=4, name="Charmander", attack=52, live=39, type="Fire"),
    Pokemon(id=7, name="Squirtle", attack=48, live=44, type="Water"),
]


@app.get("/")
def home():
    return {"message": "Welcome trainer!"}


@app.get("/showallpokemons/", response_model=List[Pokemon])
def show_all_pokemons():
    return pokemons


@app.get("/showonepokemon/", response_model=Pokemon)
def show_one_pokemon(name: str):
    for pokemon in pokemons:
        if pokemon.name.lower() == name.lower():
            return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")


@app.get("/showonepokemonbyid/", response_model=Pokemon)
def show_one_pokemon_by_id(id: int):
    for pokemon in pokemons:
        if pokemon.id == id:
            return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")


@app.get("/pokemonbattle/")
def pokemon_battle(pokemon1: str, pokemon2: str):
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
        "winner": winner
    }


@app.get("/pokemonorderedby/", response_model=List[Pokemon])
def pokemon_ordered_by(field: str, desc: bool = False):
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