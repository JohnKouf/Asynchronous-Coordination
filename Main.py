import random

import plotly
import datetime


class OscillatorSimulation(object):
    def __init__(self):
        self.cur_state = 'inactive'
        self.nextstate = 'inactive'
        self.simultime = datetime.datetime.now()


cols = 4
rows = 250
simularray = [[OscillatorSimulation() for j in range(cols)] for i in range(rows)]


# p = 0.2

xs = [-1, 0, 1, 1, -1, -1, 0, 1, 0]
ys = [-1, -1, -1, 0, 0, 1, 1, 1, 0]
s_range = [2, 4]
p_range = [0.1, 0.4]
delta_range = [2, 4]
osci = None

arounds = 0


def FindPosibillity(pp):
    posibilities = [-1 for i in range(10)]
    ones = int(pp * 10)
    zeros = int(10 - ones)

    for n in range(0, ones):
        flag = True
        while flag:
            ran = random.randint(0, 9)
            if posibilities[ran] == -1:
                posibilities[ran] = 1
                flag = False
    for n in range(0, zeros):
        flag = True
        while flag:
            ran = random.randint(0, 9)
            if posibilities[ran] == -1:
                posibilities[ran] = 0
                flag = False
    posib = random.randint(0, 9)
    if posibilities[posib] == 0:
        return False
    else:
        return True


def simulationpart(i, col, row, around, osci, p, delta, S):
    print("S = "+str(S))
    print("p = "+str(p))
    x = col + xs[i]
    y = row + ys[i]
    if -1 < x < cols and -1 < y < rows:
        if simularray[y][x].cur_state == 'active':
            around = around + 1
    if around < S and FindPosibillity(p):
        osci.nextstate = 'active'
        osci.simultime = delta


def makeinactive():
    for row in range(rows):
        for col in range(cols):
            osci = simularray[row][col]
            osci.cur_state = 'inactive'
            osci.nextstate = 'inactive'
            osci.simultime = 0


def basicprogress():
    for row in range(rows):
        for col in range(cols):
            osci = simularray[row][col]
            if osci.cur_state != osci.nextstate:
                osci.cur_state = osci.nextstate


def simulation():
    global osci, arounds
    for delta in delta_range:
        for p in p_range:
            for S in s_range:
                active_oscillators = []
                simul_times = []
                for time in range(100):
                    on = 0
                    for row in range(rows):
                        for col in range(cols):
                            osci = simularray[row][col]
                            if osci.cur_state == 'inactive':
                                arounds = 0
                                for i in range(len(xs)):
                                    simulationpart(i, col, row, arounds, osci, p, delta, S)
                            else:
                                osci.simultime = osci.simultime - 1
                                on = on + 1
                                if osci.simultime == 0:
                                    osci.nextstate = 'inactive'

                    basicprogress()

                    simul_times.append(datetime.datetime.now())
                    active_oscillators.append(on)

                makeinactive()

                makeGraph(simul_times, active_oscillators, 'Experiment' + ' Δ=%d, p=%0.1f, S=%d' % (delta, p, S),
                          'Active Swings',
                          'Time (t)')


def makeGraph(xx, yy, diag_title, yaxis_title, xaxis_title):
    from plotly.graph_objs import Scatter, Layout

    plotly.offline.plot({
        "data": [
            Scatter(x=xx, y=yy)
        ],
        "layout": Layout(
            title=diag_title,
            xaxis=dict(
                title=xaxis_title
            ),
            yaxis=dict(
                title=yaxis_title
            )

        )
    })


if __name__ == "__main__":
    print('Simulation is running...\nYou will see the results in your default browser!')
    simulation()
