import os
import sqlite3
from random import shuffle

class CAH():
    white = []
    black = []
    players = {}
    master = 0
    voted = {}
    votes = []
    czar = 0
    gamestate = 1
    mainserver = None
    def __init__(self):
        print(os.getcwd())
        conn = sqlite3.connect('db.db')
        db = conn.cursor()

        for line in db.execute('''SELECT * FROM white'''):
            self.white.append(str(line[0]))

        for line in db.execute('''SELECT * FROM black'''):
            self.black.append((str(line[0]), int(line[1])))

        shuffle(self.white)
        shuffle(self.black)

        conn.close()

    async def join(self, player):
        self.players[player] = [0, []]
        if len(self.players) == 1:
            self.master = player
        return 0

    async def list(self):
        return self.players

    async def start(self, player):
        if player != self.master:
            return -1 # insufficent permissions
        if len(self.players) < 3:
            return -2 # insufficent players
        if self.gamestate != 1:
            return -3
        self.gamestate = 2
        # give everyone 9 cards
        for i in self.players:
            while len(self.players[i][1]) < 9:
                self.players[i][1].append(self.white.pop())
        self.czar = self.master
        return 0

    async def initiateplayervote(self):

        self.voted.clear()
        self.votes.clear()

        for i in self.players:
            if i == self.czar:
                continue
            while len(self.players[i][1]) < 9 + self.black[0][1]:
                self.players[i][1].append(self.white.pop())

        return self.black[0] #returns tuple with black

    async def playervote(self, player, vote):
        if player == self.czar:
            return -5

        if len(self.players[player][1]) < max(vote) or min(vote) < 1:
            return -4 # out of bounds

        if len(vote) != self.black[0][1]:
            return -2


        self.voted[player] = [i-1 for i in vote]

        if len(self.voted) < len(self.players) - 1:
            return 1 # continue game
        if self.gamestate != 2:
            return -3
        self.gamestate = 3
        return 0 # proceed

    async def initiateczarvote(self):

        if self.gamestate != 3:
            return -3
        self.gamestate = 4

        self.votes = []
        for player in self.players:
            if self.czar == player:
                continue
            self.votes.append([player,])
            for card in self.voted[player]:
                self.votes[-1].append(self.players[player][1][card])
                self.white.append(self.players[player][1][card])
                self.players[player][1].pop(card)
        shuffle(self.votes)
        return self.votes

    async def czarvote(self, player, vote):


        if player != self.czar:
            return -6 # u aint czar

        if len(self.players) < vote or vote < 1:
            return -4 # czar dumb, out of bounds

        if self.gamestate != 4:
            return -3
        self.gamestate = 2

        winner = self.votes[vote-1][0]

        self.players[winner][0] += 1

        lastBlack = self.black.pop(0)

        self.black.append(lastBlack)
        self.czar = winner
        return (winner,lastBlack,self.votes[vote-1][1:])

    async def end(self, player):
        if player != self.master:
            return -1 # insufficent permissions
        self.gamestate = 1
        return 0
