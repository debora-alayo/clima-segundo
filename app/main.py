from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from .events import Emit
import os
import requests
import pika
import logging
from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from .models import Base, ClimaCiudad



emit_events = Emit()

url = "https://weatherapi-com.p.rapidapi.com/current.json"
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')


load_dotenv()

headers = {
	"X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

app = FastAPI(debug=True)


database_url = "postgresql://postgres:example@postgres-service:5432/example_db"

engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

#funcion para obtener el clima
def get_weather(ciudad):

    querystring = {"q":ciudad}
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:       
        data = response.json()       
        filtered_data = {
            "temp_c": data["current"]["temp_c"],
            "precip_mm": data["current"]["precip_mm"],           
        } 
        print(response.status_code)    
        return filtered_data   
    else:
        print(response.text)        
        return "Error"

def anadir_ciudad(ciudad,fecha_a):
    clima_c = get_weather(ciudad)

    if clima_c == "Error":
        logging.error(f"Error al buscar/agregar información de clima para {ciudad}")
        raise HTTPException(status_code=404, detail="No se ha podido encontrar el clima de la ciudad")
        return "Error"
    
    temp = clima_c["temp_c"]
    precip = clima_c["precip_mm"]
    db = SessionLocal()
    db_ciudad = ClimaCiudad(nombre=ciudad, temperatura=temp, precipitacion=precip, fecha=fecha_a)

    db.add(db_ciudad)
    db.commit()
    db.refresh(db_ciudad)
    db.close()

    return db_ciudad


@app.get("/") 
async def root():
    return {"message": "Microservicio Clima :D"}


class ClimaCiudads(BaseModel):
    temperatura: str
    precipitacion: str

    

@app.get(
        "/weather/{ciudad}",
        response_model=ClimaCiudads,
        summary="Obtener clima",
        description="Obtener la temperatura y la precipitacion del día en una ciudad",
    )
     #solicitan clima
async def weather(ciudad: str):

    fecha_actual = datetime.now().date()

    db = SessionLocal()
    ciudad_db = db.query(ClimaCiudad).filter(ClimaCiudad.nombre == ciudad, ClimaCiudad.fecha == fecha_actual).first()
    db.close()

    if ciudad_db is None:
        logging.info(f"El clima para {ciudad} de hoy no esta en la base de datos")
        ciudad_cr = anadir_ciudad(ciudad,fecha_actual) #ciudad creada
        if ciudad_cr == "Error":
            raise HTTPException(status_code=404, detail="No se ha podido encontrar el clima de la ciudad")
        
        
        logging.info(f"El clima para {ciudad} se ha agregado a la base de datos")
        temperatura = ciudad_cr.temperatura
        precipitacion = ciudad_cr.precipitacion
        
    else:
        temperatura = ciudad_db.temperatura
        precipitacion = ciudad_db.precipitacion

    
    filtered_data = {
        "temperatura": temperatura,
        "precipitacion": precipitacion,           
       }
    logging.info(f"El clima en {ciudad} es de {temperatura}°C")
    emit_events.send(1, "check", filtered_data)       
    return filtered_data
    
