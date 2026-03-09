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