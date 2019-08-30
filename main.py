"""
Course-Project for Module Introduction to Programming in Python.

Solution to the n-body problem in 2D with vector (numpy) approach.
------------------------------------------------------------------------
Simuliert die Bewegung von n Objekten unter dem gegenseitigen Einfluss
ihrer Gravitation.
Kommandozeilenparameter sind die Gesamtzeit T,
über die die Simulation laufen soll und delta_t, die Zeiteinheiten.
Als input werden .txt Dateien aus dem Ordner "files"
(ursprünglich nbody.zip) verwendet.
Beispieleingaben:
python main.py < files/planets.txt 100000000 10000
python main.py < files/planetsparty.txt 100000000 1000
python main.py < files/dance10.txt 100000000000 10000
"""

import sys
import math
import stdio
import stddraw
import numpy as np
import picture as p

# newtons law of universal gravitation
# F = G*((m1*m2)/r**2))

# Kommandozeilenparameter
time = float(sys.argv[1])
delta_t = float(sys.argv[2])

g = 6.67e-11
bodies = []
current_time = 0

# Variablen vom Standardinput
num_bodies = stdio.readInt()
radius_univ = stdio.readFloat()

# Canvas vorbereiten
stddraw.setXscale(-radius_univ, radius_univ)
stddraw.setYscale(-radius_univ, radius_univ)
stddraw.setCanvasSize(1200, 1000)
stddraw.clear(stddraw.BLACK)


def force(mass_a, mass_b, position_a, position_b, g):
    delta = position_b - position_a
    # euklidische Distanz
    r = math.sqrt(delta[0]**2 + delta[1]**2)
    f = (g * mass_a * mass_b) / r**2
    force = f * (delta / r)
    return force


def acceleration(force, mass):
    acc = force / mass
    return acc

# Ausgehend von der Formel für Beschleunigung:
# a = delta_v / delta_t
# a = finale_geschwindigkeit - anfangs_geschwindigkeit / delta_t
# daraus abgeleitet:
# finale_geschwindigkeit = anfangsgeschwindigkeit + beschleunigung * delta_t


def new_speed(speed, delta_t, acc):
    velocity = speed + acc * delta_t
    return velocity


def new_position(position, delta_t, new_speed):
    new_pos = position + new_speed * delta_t
    return new_pos

####################################################################

while not stdio.isEmpty():
    body = stdio.readLine()
    body = body.split()
    # aufgrund von unterschiedlichen eingabedateien müssen ggf. fehler
    # umgangen werden
    try:
        # erstelle für jeden Körper ein eigenes Dictionary
        # und füge dies in die Liste der Körper (bodies) ein.
        body_dict = {
            # position und geschwindigkeit als vektoren
            "position": np.array([body[0], body[1]], dtype='f'),
            "speed": np.array([body[2], body[3]], dtype='f'),
            "mass": float(body[4]),
            "filename": body[5],
            "force": np.array([0, 0], dtype='f'),
            "acceleration": np.array([0, 0], dtype='f'),
        }
        bodies.append(body_dict)
    # wenn zwischendurch statt korrekter Eingabewerte Text erscheint:
    except ValueError:
        print("No useful input (Value Error)")
    # Falls nur einzelne "wörter" in der Eingabedatei stehen.
    # Dabei erscheint vor dem ValueError ein IndexError (bei body[1])
    except IndexError:
        print("IndexError", body)

####################################################################

while current_time <= time:
    current_time += delta_t
    # i ist jeweils ein Körper und j die anderen Körper, die auf i wirken
    for i in range(num_bodies):
        force_on_i = np.array([0, 0], dtype='f')  # vektor force x und y
        for j in range(num_bodies):
            if j != i:
                force_on_i += force(
                    bodies[i]["mass"], bodies[j]["mass"],
                    bodies[i]["position"], bodies[j]["position"], g
                )
        # Die entsprechenden Parameter im Dictionary eines Körpers
        # werden angepasst.
        bodies[i]["force"] = force_on_i

        bodies[i]["acceleration"] = acceleration(
            bodies[i]["force"], bodies[i]["mass"]
        )

        bodies[i]["speed"] = new_speed(
            bodies[i]["speed"], delta_t,
            bodies[i]["acceleration"]
        )

        bodies[i]["position"] = new_position(
            bodies[i]["position"], delta_t, bodies[i]["speed"]
        )

        stddraw.picture(
            p.Picture('files/'+bodies[i]["filename"]),
            bodies[i]["position"][0],
            bodies[i]["position"][1],
        )
    stddraw.show(1)
    stddraw.clear(stddraw.BLACK)
