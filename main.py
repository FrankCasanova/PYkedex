import flet as ft
import asyncio
import aiohttp
from typing import List, Any, Dict
import asyncio
from typing import Awaitable

pokemon_actual = 0

async def move_pokemon_image(image):
    while True:
        # Mueve la imagen hacia abajo (incrementa la posición Y)
        image.top += 6
        await asyncio.sleep(0.1)  # Espera antes de actualizar
        # Mueve la imagen hacia arriba (decrementa la posición Y)
        image.top -= 6
        await asyncio.sleep(0.1)  # Espera antes de actualizar
        
async def main(page: ft.Page):
    ## Inicializamos la ventana
    page.window_width = 720
    page.window_height = 1280
    page.window_resizable = True
    page.padding = 0
    page.margin = 0
    page.fonts = {
        "zpix": "https://github.com/SolidZORO/zpix-pixel-font/releases/download/v3.1.8/zpix.ttf"
    }
    page.title = "Pykedex"
    page.scroll = ft.ScrollMode.ALWAYS
    page.theme_mode = ft.ThemeMode.LIGHT
    await page.update_async()

    ## Funciones del programa:
    async def peticion(url: str) -> Dict[str, Any]:
        """
        Sends an asynchronous GET request to the specified URL using aiohttp.ClientSession.
        Args:
            url (str): The URL to send the GET request to.
        Returns:
            dict: The JSON response from the GET request.
        """
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            return await response.json()
    

    async def evento_get_pokemon(e: ft.ContainerTapEvent) -> None:
        """
        Fetches Pokemon data based on the given event.
        Args:
            e (ft.ContainerTapEvent): The event containing the control information.
        Returns:
            None
        """
        global pokemon_actual
        pokemon_actual += 1 if e.control == flecha_superior else -1
        numero = (pokemon_actual % 1008) + 1
        resultado1, resultado2 = await asyncio.gather(
            peticion(f"https://pokeapi.co/api/v2/pokemon/{numero}"),
            peticion(f"https://pokeapi.co/api/v2/pokemon-species/{numero}")
        )
        types: List[str] = [t['type']['name'] for t in resultado1['types']]
        types_string: str = ' / '.join(types)
        datos: str = f"Number:{numero}\nName: {resultado1['name']}\nType: {types_string}\n"
        datos += f"Description: {resultado2['flavor_text_entries'][0]['flavor_text']}".replace("\n", " ")
        texto.value = datos
        sprite_url: str = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{numero}.png"
        imagen.src = sprite_url
        await page.update_async()

    async def blink() -> Awaitable[None]:
        """
        Asynchronously blinks the blue light.
        Returns:
            Awaitable[None]: A future representing the completion of the blink operation.
        """
        while True:
            await asyncio.sleep(1)
            luz_azul.bgcolor = ft.colors.BLUE_100
            await page.update_async()
            await asyncio.sleep(0.1)
            luz_azul.bgcolor = ft.colors.BLUE
            await page.update_async()


            
    ## Interfaz del programa
    luz_azul = ft.Container(width=70, height=70, left=5, top=5, bgcolor=ft.colors.BLUE, border_radius=50)
    boton_azul = ft.Stack([
        ft.Container(width=80, height=80, bgcolor=ft.colors.WHITE, border_radius=50),
        luz_azul,
        ]
    )

    items_superior = [
        ft.Container(boton_azul, width=80, height=80),
        ft.Container(width=40, height=40, bgcolor=ft.colors.RED_200, border_radius=50),
        ft.Container(width=40, height=40, bgcolor=ft.colors.YELLOW, border_radius=50),
        ft.Container(width=40, height=40, bgcolor=ft.colors.GREEN, border_radius=50),
    ]

    imagen = ft.Image(
                src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/132.png",
                scale=10, # Redimensionamos a tamano muy grande
                width=30, #Con esto se reescalara a un tamano inferior automaticamente
                height=30,
                top=350/2,
                right=550/2,
    )
    
     
    stack_central = ft.Stack(
        [
            ft.Container(width=600, height=400, bgcolor=ft.colors.WHITE, border_radius=20),
            ft.Container(width=550, height=350, bgcolor=ft.colors.BLACK, top=25, left=25),
            imagen,
        ]
    )

    triangulo = ft.canvas.Canvas([
        ft.canvas.Path(
                [
                    ft.canvas.Path.MoveTo(40, 0),
                    ft.canvas.Path.LineTo(0,50),
                    ft.canvas.Path.LineTo(80,50),
                ],
                paint=ft.Paint(
                    style=ft.PaintingStyle.FILL,
                ),
            ),
        ],
        width=80,
        height=50,
    )

    
    flecha_superior = ft.Container(triangulo, width=80, height=50, on_click=evento_get_pokemon)

    flechas = ft.Column(
        [
            flecha_superior,
             #radianes 180 grados = 3.14159
            ft.Container(triangulo, width=80, height=50, rotate=ft.Rotate(angle=3.14159), on_click=evento_get_pokemon),
        ]
    )

    texto = ft.Text(
        value="...",
        color=ft.colors.BLACK,
        size=19,
        font_family="zpix",
        width=400,
        height=300,
        
        
        
    )

    items_inferior = [
        ft.Container(width=50), #Margen izquierdos
        ft.Container(texto, padding=10, width=400, height=300, bgcolor=ft.colors.GREEN, border_radius=20),
        ft.Container(width=30), #Margen derecho
        ft.Container(flechas, width=80, height=120),
        
    ]

    superior = ft.Container(content=ft.Row(items_superior),width=600,height=80, margin = ft.margin.only(top=40))
    centro = ft.Container(stack_central, width=600,height=400, margin = ft.margin.only(top=40), alignment=ft.alignment.center)
    inferior = ft.Container(content=ft.Row(items_inferior), width=600,height=400, margin = ft.margin.only(top=80))

    col = ft.Column(spacing=0, controls=[
        superior,
        centro,
        inferior,
    ])

    contenedor = ft.Container(col, width=720, height=1280, bgcolor=ft.colors.RED, alignment=ft.alignment.top_center)
    
    await page.add_async(contenedor)
    asyncio.create_task(move_pokemon_image(imagen))
    await blink()
    
    
    
    

import flet_fastapi
# ft.app(target=main, host="127.0.0.1", port=8000)
app = flet_fastapi.app(main)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app',reload=True)