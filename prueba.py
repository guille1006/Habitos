import asyncio


async def funcion_1(estado, estado_cambiado):
    await asyncio.sleep(3)

    if estado_cambiado.is_set():
        return

    estado["boton"] = True
    estado_cambiado.set()


async def funcion_2(estado, estado_cambiado):
    await asyncio.sleep(5)

    if estado_cambiado.is_set():
        return

    estado["boton"] = False
    estado_cambiado.set()


async def controlar_boton(valor_inicial):
    estado = {"boton": valor_inicial}
    estado_cambiado = asyncio.Event()

    t1 = asyncio.create_task(funcion_1(estado, estado_cambiado))
    t2 = asyncio.create_task(funcion_2(estado, estado_cambiado))

    await estado_cambiado.wait()

    t1.cancel()
    t2.cancel()

    return estado["boton"]


async def main():
    for _ in range(10):
        boton = input("Escribe algo: ")
        resultado = await controlar_boton(boton)
        print("Estado final:", resultado)


asyncio.run(main())