from simpleai.search.viewers import BaseViewer, WebViewer
from simpleai.search import SearchProblem, astar, depth_first, breadth_first, uniform_cost, greedy

def tuple2list(t):
	return [list(row) for row in t]

def list2tuple(l):
	return tuple(tuple(row) for row in l)

def manhattan(state, index_aparato, field_to):
    distance = abs(state[index_aparato][0] - field_to[0]) + abs(state[index_aparato][1] - field_to[1])
    return distance

class Bomberobot(SearchProblem):
	
	def cost(self, state1, action, state2):
		return 1
	
	def actions(self, state):
		state = tuple2list(state)

		rob_row = state[0][0]
		rob_col = state[0][1]

		actions = []
		# aparato_to_move = None
		aparatos = []

		'''Antes de detectar las acciones disponibles, verifico que no haya aparatos quemados.
		La presencia de aparatos quemados invalida el path elegido, y como consecuencia se debe
		devolver una lista de acciones vacia para generar el callejon sin salida'''

		aparatos_quemados = False
		for aparato in state:
			if aparato[2] > 500:
				aparatos_quemados = True

		'''Si no hay aparatos quemados, detecto las acciones posibles. Sino, la lista de acciones queda vacia'''
		if aparatos_quemados == False:
			'''Busco los aparatos en la posicion del robot'''
			for index, aparato in enumerate(state):
				if index != 0:
					if aparato[0] == rob_row and aparato[1] == rob_col:
						aparato.insert(0, index)
						aparatos.append(aparato)

			'''Mover el robot + empujar aparatos'''
			if rob_row > 0:
				actions.append([0, rob_row - 1, rob_col])

				for aparato in aparatos:
					actions.append([aparato[0], rob_row - 1, rob_col])

			if rob_row < 3:
				actions.append([0, rob_row + 1, rob_col])

				for aparato in aparatos:
					actions.append([aparato[0], rob_row + 1, rob_col])

			if rob_col > 0:
				actions.append([0, rob_row, rob_col - 1])

				for aparato in aparatos:
					actions.append([aparato[0], rob_row, rob_col - 1])

			if rob_col < 3:
				actions.append([0, rob_row, rob_col + 1])

				for aparato in aparatos:
					actions.append([aparato[0], rob_row, rob_col + 1])

			''' Enfriar'''
			actions.append([-1, rob_row, rob_col])

			state = list2tuple(state)

		return actions


	def result(self, state, action):
		state = tuple2list(state)

		
		if action[0] == -1:
			'''Accion enfriar'''
			for index, aparato  in enumerate(state):
				if index != 0 and aparato[0] == action[1] and aparato[1] == action[2]:
					aparato[2] -= 150
		elif action[0] == 0:
			'''Accion mover'''
			state[0][0] = action[1]
			state[0][1] = action[2]

		elif action[0] > 0:
			'''Accion empujar'''
			n = action[0]

			state[n][0] = action[1]
			state[n][1] = action[2]

			state[0][0] = action[1]
			state[0][1] = action[2]

		'''Aumentar temperatura por turno'''
		for index, aparato in enumerate(state):
			if index != 0 and (aparato[0] != 3 or aparato[1] != 3):
				state[index][2] += 25

		state = list2tuple(state)

		return state

	def is_goal(self, state):
		not_goal = False
		for index,a in enumerate(state):
			if index != 0:
				if a[0] != 3 or a[1] != 3 or a[2] > 500:
					not_goal = True
		if not_goal == True:
			return False
		else: 
			return True

	def heuristic(self, state):
		possible_path_costs = []
		rob_row = state[0][0]
		rob_col = state[0][1]

		for index, aparato in enumerate(state):
		    '''Calcular todos los posibles costos de caminos, segun el aparato que se elija salvar primero'''
		    if index != 0:
		        path_cost = 0
		        '''Aparato que se recoje primero, es decir, desde la posicion actual del robot'''
		        path_cost = manhattan(state, index, [rob_row, rob_col]) + manhattan(state, index, [3, 3])
		        '''Los demas aparatos que se recojen desde la salida'''
		        for index2, aparato2 in enumerate(state):
		            if index2 != 0 and index2 != index:
		                path_cost = path_cost + manhattan(state, index2, [3, 3]) * 2

		        possible_path_costs.append(path_cost)

		'''Elegir el minimo costo'''
		return min(path_cost for path_cost in possible_path_costs)
	
def resolver(metodo_busqueda, posiciones_aparatos):
	viewer = BaseViewer()

	initial = []

	robot = [3,3,1]

	namespace = __import__(__name__)

	initial.append(robot)

	for a in posiciones_aparatos:
		aparato = [a[0], a[1], 300]
		initial.append(aparato)

	initial = list2tuple(initial)

	result = getattr(namespace, metodo_busqueda)(Bomberobot(initial), viewer = viewer, graph_search = True)

	print('Result state: ')
	print(result.state)
	print('Result path: ')
	for action, state in result.path():
		print('Action: ', action)
		print('State: ', state)
		print('')

	print(viewer.stats)

	return result


# if __name__ == '__main__':
# resolver('greedy', ((1,2),(2,0),(3,0)))
