import random as rd
import string
from player import Player
from tournament import Tournament, inorder, inorder_names

class Game():
    def __init__(self):
        names = get_player_names()
        players = [Player(i) for i in names]
        self.ranking = Tournament()
        for player in players:
            self.ranking.insert(player)
        #print(inorder_names(self.ranking.root))

    def __repr__(self):
        res = ""
        for player in inorder(self.ranking.root):
            res += f"{repr(player)}\n"
        return res

    def randomize_scores(self, players:list):
        '''
        Method to assign coherent scores to the 10 players given the set of
        rules of Among Us.
        args:
            players: list of 10 players in the game.
        '''
        rd.shuffle(players)
        (imp1, imp2) = players[:2]
        imp1.role = True
        imp2.role = True
        crewmates = players[2:]
        tmp = rd.randint(1, 100)

        if tmp > 30:
            # Crewmates win
            # Impostors points
            tmp = rd.randint(0, 6)
            tmp2 = rd.randint(tmp, 6)
            imp1.score += tmp
            imp2.score += tmp2 - tmp
            # Max 2 undiscovered bodies
            tmp = rd.randint(0, min(2, tmp2))
            sneaky_killers = rd.choices([imp1, imp2], k=tmp)
            for k in sneaky_killers:
                #print("sneaky:", k.name)
                k.score += 3
            # Crew points
            tmp = rd.randint(1, 100)
            if tmp > 80:
                # 20% chance of task win, they all get 6 points
                #print("task win")
                for m in crewmates:
                    m.score += 6
                tmp = rd.randint(1, 100)
                if tmp > 30:
                    # One of the impostors is dead (unmasked by p)
                    # 70% chance of one impostor dying while task win.
                    p = rd.choice(crewmates)
                    p.score += 3
                    #print("unmasked by:", p.name)
            else:
                #print("real win")
                # Real win (80% chance)
                # 2 random crewmates chosen who unmasked an impostor.
                # Can be the same.
                # Win points
                for m in crewmates:
                    m.score += 5
                # Unmask points
                (p1, p2) = rd.choices(crewmates, k=2)
                p1.score += 3
                p2.score += 3
                # Task points
                task_pts = rd.randint(0, 7)
                task_finishers = rd.sample(crewmates, k=task_pts)
                for crewmate in task_finishers:
                    #print("finished tasks:", crewmate.name)
                    crewmate.score += 1
        else:
            #print("Imp wins")
            # Impostors win
            # Crew points
            task_pts = rd.randint(0, 7)
            task_finishers = rd.sample(crewmates, k=task_pts)
            for crewmate in task_finishers:
                #print("finished tasks:", crewmate.name)
                crewmate.score += 1
            # Impostor points
            # Win points
            imp1.score += 10
            imp2.score += 10
            tmp = rd.randint(1, 100)
            if tmp > 50:
                # Solo win: 8 kills in total
                tmp = rd.randint(0, 8)
                imp1.score += tmp
                imp2.score += 8 - tmp
                # Unmask points
                p = rd.choice(crewmates)
                p.score += 3
                #print("unmasked by:", p.name)
                # Probability of undiscovered bodies
                tmp = rd.randint(1, 100)
                if tmp <= 20:
                    # 2 undiscovered bodies
                    sneaky_killers = rd.choices([imp1, imp2], k=2)
                    for k in sneaky_killers:
                        #print("sneaky:", k.name)
                        k.score += 3
                elif tmp <= 80:
                    # 1 undiscovered body
                    sneaky_killer = rd.choice([imp1, imp2])
                    sneaky_killer.score += 3
            else:
                # Duo win: 6 kills in total
                tmp = rd.randint(0, 6)
                imp1.score += tmp
                imp2.score += 6 - tmp
                # Probability of undiscovered bodies
                tmp = rd.randint(1, 100)
                if tmp <= 20:
                    # 2 undiscovered bodies
                    sneaky_killers = rd.choices([imp1, imp2], k=2)
                    for k in sneaky_killers:
                        #print("sneaky:", k.name)
                        k.score += 3
                elif tmp <= 80:
                    # 1 undiscovered body
                    sneaky_killer = rd.choice([imp1, imp2])
                    #print("sneaky:", sneaky_killer.name)
                    sneaky_killer.score += 3

    def update_ranks(self, players):
        res = Tournament()
        for p in players:
            res.insert(p)
        self.ranking = res

    def delete_last_ten(self):
        pass

    def play_rounds(self):
        ''' Used to simulate a round of the game, by taking 10 players
         per game and simulating scores for each game.
        '''
        players = inorder(self.ranking.root)
        # Play 3 random games, then update the ranking
        for _ in range(3):
            rd.shuffle(players)
            # List of all the random lobbies.
            lobbies = [players[i:i + 10] for i in range(1, 92, 10)]
            for lobby in lobbies:
                self.randomize_scores(lobby)
        self.update_ranks(players)
        print(self)

        # Now,play the 9 elimination rounds:
        for _ in range(9):
            # Get players sorted by increasing score and create the lobbies
            players = inorder(self.ranking.root)
            lobbies = [players[i:i + 10] for i in range(1, 92, 10)]
            for lobby in lobbies:
                self.randomize_scores(lobby)
            self.update_ranks(players)
            self.delete_last_ten()

def get_player_names():
    with open("players_list.txt", "r") as f:
        res = f.readlines()
    return [i.strip() for i in res]

if __name__ == "__main__":
    game = Game()
    game.play_rounds()