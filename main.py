from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

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