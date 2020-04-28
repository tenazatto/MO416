import argparse
import os

from pacmanProblem import PacmanProblem
from report import report
from search import astar_search, hill_climbing, greedy_best_first_search, breadth_first_graph_search, \
    depth_first_graph_search


def default(str):
    return str + ' [Default: %default]'

usageStr = """
USAGE:      python pacman.py <options>
EXAMPLES:   (1) python pacman.py
                - starts an interactive game
            (2) python pacman.py --layout smallClassic --zoom 2
            OR  python pacman.py -l smallClassic -z 2
                - starts an interactive game on a smaller board, zoomed in
"""

parser = argparse.ArgumentParser(description=usageStr)
parser.add_argument('-l', '--layout', dest='layout',
                    help=default('the LAYOUT_FILE from which to load the map layout'),
                    metavar='LAYOUT_FILE', default='mediumClassic')


def main():
    args = parser.parse_args()

    bounds, ghosts, pacman, goal = mapPositions(args.layout)

    print('Barreiras:', bounds)
    print('Fantasmas:', ghosts)
    print('Pacman:', pacman)
    print('Gol:', goal)
    print()

    #Problema e algoritmos
    problem = PacmanProblem(obstacles=bounds | ghosts, initial=pacman, goal=goal)
    gfsProblem = greedy_best_first_search(problem)
    astarProblem = astar_search(problem)
    bfsProblem = breadth_first_graph_search(problem)
    dfsProblem = depth_first_graph_search(problem)
    hcProblem = hill_climbing(problem)
    print('Greedy Best First Search:')
    print('Caminho:', gfsProblem.path())
    print('Gol:', gfsProblem)
    print('A* Search:')
    print('Caminho:', astarProblem.path())
    print('Solução:', astarProblem.solution())
    print('Estados:', path_states(astarProblem))
    print('Gol:', astarProblem)
    print('Breadth-First Search:')
    print('Caminho:', bfsProblem.path())
    print('Solução:', bfsProblem.solution())
    print('Estados:', path_states(bfsProblem))
    print('Gol:', dfsProblem)
    print('Depth-First Search:')
    print('Caminho:', dfsProblem.path())
    print('Solução:', dfsProblem.solution())
    print('Estados:', path_states(dfsProblem))
    print('Gol:', dfsProblem)
    print('Hill Climbing:')
    print('Caminho:', hcProblem.path())
    print('Solução:', hcProblem.solution())
    print('Estados:', path_states(hcProblem))
    print('Gol:', dfsProblem)
    print()
    print('Gerando saídas...')
    generateOutput(set(gfsProblem.solution()) - {pacman, goal}, gfsProblem.explored - {pacman, goal}, args.layout, 'gfs')
    generateOutput(set(astarProblem.solution()) - {pacman, goal}, astarProblem.explored - {pacman, goal}, args.layout, 'astar')
    generateOutput(set(bfsProblem.solution()) - {pacman, goal}, bfsProblem.explored - {pacman, goal}, args.layout, 'bfs')
    generateOutput(set(dfsProblem.solution()) - {pacman, goal}, dfsProblem.explored - {pacman, goal}, args.layout, 'dfs')
    generateOutput(set(hcProblem.solution()) - {pacman, goal}, hcProblem.explored - {pacman, goal}, args.layout, 'hc')

    print()
    print('Desempenho:')
    report([greedy_best_first_search, astar_search, breadth_first_graph_search, depth_first_graph_search, hill_climbing], [problem])

def path_actions(node):
    "The sequence of actions to get to this node."
    if node.parent is None:
        return []
    return path_actions(node.parent) + [node.action]

def path_states(node):
    "The sequence of states to get to this node."
    if node is None:
        return []
    return path_states(node.parent) + [node.state]

def mapPositions(layoutFile):
    with open('layouts/'+ layoutFile +'.lay', 'r') as layout:
        x = 1
        bounds = set()
        ghosts = set()
        pacman = (1,1)
        goal = (2,2)
        for line in layout.readlines():
            y = 1
            for ch in line:
                if (ch == '%'):
                    bounds |= {(x, y)}
                elif (ch == 'G'):
                    ghosts |= {(x, y)}
                elif (ch == 'P'):
                    pacman = (x, y)
                elif (ch == 'o'):
                    goal = (x, y)

                y += 1

            x += 1
        return bounds, ghosts, pacman, goal

def generateOutput(nodes, explored, layoutFile, searchFile):
    if not os.path.exists('solutions'):
        os.makedirs('solutions')

    with open('layouts/'+ layoutFile +'.lay', 'r') as layout:
        lines = layout.readlines()
        lines = drawNodeOutput(lines, explored, '+')
        lines = drawNodeOutput(lines, nodes, '*')

        with open('solutions/' + layoutFile + '_' + searchFile + '.lay', 'w') as solution:
            solution.write("".join(lines))

def drawNodeOutput(lines, nodes, char):
    numnodes = 1
    for node in nodes:
        x = 1
        for line in lines:
            if (x == node[0]):
                aux = list(line)
                aux[node[1] - 1] = char
                lines[node[0] - 1] = "".join(aux)
            x += 1
        numnodes += 1

    return lines

if __name__ == '__main__':
    main()