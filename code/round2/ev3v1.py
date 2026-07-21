#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.parameters import Button
from pybricks.tools import wait

from pixycamev3.pixy2 import Pixy2


# ============================================================
# EV3
# ============================================================

EV3 = EV3Brick()


# ============================================================
# CONFIGURACIÓN PIXY
# ============================================================

# PixyCam conectada físicamente al puerto S1.
PIXY_PORT = 1

# Dirección configurada en PixyMon.
PIXY_I2C_ADDRESS = 0x54

# Colores enseñados en PixyMon:
# Signature 1 = rojo
# Signature 2 = verde

SIG_RED = 1
SIG_GREEN = 2


# ============================================================
# FUNCIÓN PARA DEJAR EL PROGRAMA EJECUTÁNDOSE
# ============================================================

def freeze():

    while True:
        wait(1000)


# ============================================================
# INICIAR
# ============================================================

EV3.screen.clear()
EV3.screen.print("PIXY TEST")
EV3.screen.print("IMPORT OK")

wait(700)


# ============================================================
# CREAR PIXY
# ============================================================

try:

    PIXY = Pixy2(
        port=PIXY_PORT,
        i2c_address=PIXY_I2C_ADDRESS
    )

    EV3.screen.clear()
    EV3.screen.print("PIXY CREATED")
    EV3.screen.print("PRESS RIGHT")

    EV3.speaker.beep(
        frequency=850,
        duration=200
    )

except Exception as error:

    EV3.screen.clear()
    EV3.screen.print("CREATE ERROR")
    EV3.screen.print(type(error).__name__)
    EV3.screen.print(str(error)[:20])

    print("==========================")
    print("CREATE ERROR")
    print("TYPE:", type(error))
    print("DETAIL:", repr(error))
    print("==========================")

    EV3.speaker.beep(
        frequency=250,
        duration=500
    )

    freeze()


# ============================================================
# ESPERAR BOTÓN DERECHO
# ============================================================

while Button.RIGHT not in EV3.buttons.pressed():
    wait(20)

while Button.RIGHT in EV3.buttons.pressed():
    wait(20)


EV3.screen.clear()
EV3.screen.print("READING PIXY")

wait(500)


# ============================================================
# BUCLE DE LECTURA
# ============================================================

while True:

    try:

        # 3 solicita:
        # bit 1 = Signature 1
        # bit 2 = Signature 2
        #
        # Por eso 3 busca rojo y verde.
        #
        # Máximo 5 bloques detectados.

        block_count, blocks = PIXY.get_blocks(
            3,
            5
        )

        EV3.screen.clear()
        EV3.screen.print("READ OK")
        EV3.screen.print("BLOCKS:", block_count)

        # ----------------------------------------------------
        # HAY ALGÚN OBSTÁCULO
        # ----------------------------------------------------

        if block_count > 0:

            # Elegir el bloque más grande.
            largest_block = blocks[0]
            largest_area = 0

            for block in blocks:

                area = (
                    block.width
                    * block.height
                )

                if area > largest_area:

                    largest_area = area
                    largest_block = block

            signature = largest_block.sig
            x = largest_block.x_center
            y = largest_block.y_center
            width = largest_block.width
            height = largest_block.height

            EV3.screen.print("SIG:", signature)
            EV3.screen.print("X:", x, "Y:", y)
            EV3.screen.print("W:", width, "H:", height)

            # ------------------------------------------------
            # ROJO
            # ------------------------------------------------

            if signature == SIG_RED:

                EV3.screen.print("RED")
                EV3.screen.print("PASS RIGHT")

                EV3.speaker.beep(
                    frequency=500,
                    duration=40
                )

            # ------------------------------------------------
            # VERDE
            # ------------------------------------------------

            elif signature == SIG_GREEN:

                EV3.screen.print("GREEN")
                EV3.screen.print("PASS LEFT")

                EV3.speaker.beep(
                    frequency=900,
                    duration=40
                )

            # ------------------------------------------------
            # OTRA FIRMA
            # ------------------------------------------------

            else:

                EV3.screen.print("OTHER COLOR")

            print(
                "SIG:", signature,
                "X:", x,
                "Y:", y,
                "WIDTH:", width,
                "HEIGHT:", height,
                "AREA:", largest_area
            )

        # ----------------------------------------------------
        # NO HAY OBJETO
        # ----------------------------------------------------

        else:

            EV3.screen.print("NO OBJECT")

            print("NO OBJECT")

    # ========================================================
    # ERROR DE LECTURA
    # ========================================================

    except Exception as error:

        error_type = type(error).__name__
        error_text = str(error)

        EV3.screen.clear()
        EV3.screen.print("BLOCK ERROR")
        EV3.screen.print(error_type)
        EV3.screen.print(error_text[:20])

        print("==========================")
        print("BLOCK ERROR")
        print("TYPE:", type(error))
        print("DETAIL:", repr(error))
        print("==========================")

        EV3.speaker.beep(
            frequency=250,
            duration=150
        )

        # Esperar antes de volver a intentar.
        wait(1000)

    wait(150)
