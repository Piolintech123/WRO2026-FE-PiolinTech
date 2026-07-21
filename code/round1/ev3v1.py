#!/usr/bin/env python3
from ev3dev2.sensor import INPUT_2, INPUT_4, INPUT_3
from ev3dev2.sensor.lego import UltrasonicSensor, ColorSensor
from ev3dev2.motor import MediumMotor, OUTPUT_B, OUTPUT_D
from time import sleep
import math
from ev3dev2.button import Button
from ev3dev2.led import Leds

# --- CONFIGURACIÓN DE HARDWARE (SOLO 2 MOTORES) ---
rast = UltrasonicSensor(INPUT_2)        # Pared Derecha
chap = UltrasonicSensor(INPUT_3)        # Pared Izquierda
color_sensor = ColorSensor(INPUT_4)    # Suelo / Líneas

motor_a = MediumMotor(OUTPUT_B)         # Motor de Dirección
motor_b = MediumMotor(OUTPUT_D)         # Motor Único de Tracción

motor_a.reset()

btn = Button()
leds = Leds()
leds.set_color('LEFT', 'ORANGE')
leds.set_color('RIGHT', 'ORANGE')

# Esperar presionar el botón central para iniciar
btn.wait_for_bump('enter')
leds.set_color('LEFT', 'GREEN')
leds.set_color('RIGHT', 'GREEN')

def clamp(value, minimum, maximum):
    if value > maximum: value = maximum
    if value < minimum: value = minimum
    return value

def amotor(degrese, cl=50):
    diff = degrese - motor_a.position
    diff = clamp(diff, -cl, cl)
    motor_a.on(diff)

a = 0

def lineChek():
    global a
    cr1 = color_sensor.color
    if (motor_b.position > 1000 and (cr1 in [1, 2, 5, 7])) or (a == 0 and (cr1 in [1, 2, 5, 7])):
        a += 1
        motor_b.reset()

abi = [1, 2]       # Colores sentido Azul
narengi = [5, 7]  # Colores sentido Naranja
cr1 = color_sensor.color
speed = 40

# --- TRAMO INICIAL DE CENTRADO (120 CICLOS) ---
g = 0
while g != 120:
    cr1 = color_sensor.color
    if cr1 != 6:
        speed = 100

    motor_b.on(speed)

    r = rast.distance_centimeters
    c = chap.distance_centimeters
    fr = (-2 * (math.sqrt(11 * r))) + 100
    fc = (-2 * (math.sqrt(11 * c))) + 100
    target = (fc * 1.3) - (fr * 1.3)
    amotor(clamp(target, -28, 28))
    g += 1

# --- BUCLE PRINCIPAL (SEGUIMIENTO DE PARED) ---
while True:
    cr1 = color_sensor.color

    # Caso 1: Pista en sentido Azul -> Seguir pared IZQUIERDA
    if cr1 in abi:
        while True:
            lineChek()
            motor_b.on(100)
            
            distance = chap.distance_centimeters
            diff = (distance - 28) * -2
            diff = diff - motor_a.position
            amotor(clamp(diff, -35, 35))
            
            lineChek()
            
            # Fin de carrera
            if a == 11:
                for _ in range(60):
                    motor_b.on(100)
                    distance = chap.distance_centimeters
                    diff = (distance - 28) * -2 - motor_a.position
                    amotor(clamp(diff, -35, 35))
                break
        break

    # Caso 2: Pista en sentido Naranja -> Seguir pared DERECHA
    elif cr1 in narengi:
        while True:
            lineChek()
            motor_b.on(100)
            
            distance = rast.distance_centimeters
            diff = (distance - 28) * 2
            diff = diff - motor_a.position
            amotor(clamp(diff, -35, 35))
            
            lineChek()
            
            # Fin de carrera
            if a == 11:
                for _ in range(60):
                    motor_b.on(100)
                    distance = rast.distance_centimeters
                    diff = (distance - 28) * 2 - motor_a.position
                    amotor(clamp(diff, -35, 35))
                break
        break

# Detener motores al finalizar
motor_b.off()
motor_a.off()

