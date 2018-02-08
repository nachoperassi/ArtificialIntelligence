import operator
from simpleai.search import (CspProblem, backtrack, min_conflicts, 
							LEAST_CONSTRAINING_VALUE, MOST_CONSTRAINED_VARIABLE, HIGHEST_DEGREE_VARIABLE)

variables = ['Armadura roja', 'Armadura blanca', 'Armadura amarilla','Armadura verde', 'Armadura azul',
			'Escudo trebol', 'Escudo cruz', 'Escudo pajaros', 'Escudo dragon', 'Escudo arbol',
			'Arma garrote', 'Arma hacha', 'Arma lanza', 'Arma espada', 'Arma martillo',
			'Amuleto pendiente', 'Amuleto anillo', 'Amuleto pulsera', 'Amuleto cinturon', 'Amuleto moneda',
			'Posicion 0', 'Posicion 1', 'Posicion 2', 'Posicion 3', 'Posicion 4']

values = []

# El color preferido de Bjarni es el rojo, por lo cual su armadura tiene que ser de ese color.
values.append(['Bjarni'])
for i in range(4):
	values.append(['Agnar', 'Cnut', 'Diarf', 'Egil'])

# Diarf esta seguro de que su escudo tenia un trebol dibujado.
values.append(['Diarf'])
for i in range(4):
	values.append(['Bjarni', 'Cnut', 'Agnar', 'Egil'])

# Cnut, conocido por no ser muy delicado, no tiene dudas de que el garrote era su arma predilecta.
values.append(['Cnut'])
for i in range(4):
	values.append(['Agnar', 'Bjarni', 'Diarf', 'Egil'])

# Egil recuerda que su amuleto era un pendiente con forma de triangulo.
values.append(['Egil'])
for i in range(4):
	values.append(['Agnar', 'Bjarni', 'Cnut', 'Diarf'])

# Agnar instintivamente se ubico en la primer posicion, por lo que seguramente es su posicion habitual.
values.append(['Agnar'])
for i in range(4):
	values.append(['Egil', 'Bjarni', 'Cnut', 'Diarf'])

dominios = { variables[i]:values[i] for i in range(25) }

restricciones = []

def at_left(vars, values):
	val1, val2 = values[0:2]
	posiciones = values[2:7]

	if val1 not in posiciones or val2 not in posiciones:
		return False
	else:
		return posiciones.index(val1) < posiciones.index(val2)

def besides(vars, values):
	val1, val2 = values[0:2]
	posiciones = values[2:7]

	if val1 not in posiciones or val2 not in posiciones:
		return False
	else:
		return abs(posiciones.index(val1) - posiciones.index(val2)) == 1

def besides_Agnar(vars, values):
	val = values[0]
	posiciones = values[1:6]

	if val not in posiciones or 'Agnar' not in posiciones:
		return False
	else:
		return abs(posiciones.index(val) - posiciones.index('Agnar')) == 1

def match_attr(vars, values):
	val1, val2 = values
	return val1 == val2

def allDiff(variables, values):
	return len(set(values)) == 5

for i in range(5):
	# Recorro la lista de variables, tomando los subgrupos correspondientes a cada objeto (Ej: variables[0:4], que
	# corresponde al subgrupo de las armaduras)
	desde = i + (i * 4)
	hasta = desde + 5
	restricciones.append((tuple(variables[desde:hasta]), allDiff))

#El jefe asegura que el guerrero que se vestia de verde, siempre se ubicaba a la izquierda del guerrero de blanco.
restricciones.append(((variables[3], variables[1], variables[20], variables[21],
					   variables[22], variables[23], variables[24]), at_left))

# Y tambien el guerrero de verde era famoso por su escudo con una cruz dibujada.
restricciones.append(((variables[3], variables[6]), match_attr))

# El guerrero que usaba un martillo de guerra, tenia un anillo con un dibujo de un herrero para la suerte, todos conocen la historia de como su padre le regalo ambas cosas.
restricciones.append(((variables[14], variables[16]), match_attr))

# El jefe recuerda que el guerrero de amarillo usaba un hacha danesa (un hacha de dos manos).
restricciones.append(((variables[2], variables[11]), match_attr))

# Y que el guerrero del centro (tercera posicion) tenia un bello escudo decorado con dibujos de mil pajaros diferentes.
restricciones.append(((variables[22], variables[7]), match_attr))

# Uno de los ninios de la aldea recuerda que el guerrero que usaba lanza, se ubicaba al lado del guerrero que usaba una brillante pulsera de oro para la suerte.
restricciones.append(((variables[12], variables[17], variables[20], variables[21],
					   variables[22], variables[23], variables[24]), besides))

# Y extraniamente, tambien recuerda que el guerrero que usaba un cinturon de cuero decorado como amuleto, se ubicaba al lado del guerrero del hacha danesa.
restricciones.append(((variables[18], variables[11], variables[20], variables[21],
					   variables[22], variables[23], variables[24]), besides))

# El jefe insiste que el guerrero que usaba espada, usaba un escudo decorado con un dibujo de un dragon.
restricciones.append(((variables[13], variables[8]), match_attr))


# Agnar dice que un guerrero que se ubicaba al lado suyo, usaba armadura azul.
restricciones.append(((variables[4], variables[20], variables[21],
					  variables[22], variables[23], variables[24]), besides_Agnar))

# Alguien mas sostiene que el guerrero de la lanza siempre estaba al lado del guerrero del escudo con dibujo de arbol.
restricciones.append(((variables[12],variables[9], variables[20], variables[21],
					   variables[22], variables[23], variables[24]), besides))


# ---------------------------------------------------------------------------
# CODIGO PARA GENERAR ENTREGA2.TXT CON LOS RESULTADOS DE LOS 2 METODOS DE CSP
# problem = CspProblem(variables, dominios, restricciones)

# result1 = backtrack(problem, variable_heuristic=MOST_CONSTRAINED_VARIABLE, 
# 					value_heuristic=LEAST_CONSTRAINING_VALUE)

# result2 = min_conflicts(problem, iterations_limit=50)

# repr_result1 = repr(result1)
# repr_result2 = repr(result2)

# file = open('entrega2.txt', 'w')

# file.write('1:' + repr_result1 + '\n')
# file.write('2:' + repr_result2)

# file.close()
#----------------------------------------------------------------------------

# CODIGO PARA UTILIZAR CON SCRIPT PROBAR_ENTREGA2

def resolver(metodo_busqueda, iteraciones):
	problem = CspProblem(variables, dominios, restricciones)

	if metodo_busqueda == 'backtrack':
		result = backtrack(problem, variable_heuristic=MOST_CONSTRAINED_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)
	else:
		result = min_conflicts(problem, iterations_limit=iteraciones)

	return result
