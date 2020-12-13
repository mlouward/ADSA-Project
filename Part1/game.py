import random as rd
import string
from player import Player
from tournament import Tournament, inorder, inorder_names

class Game():
    def __init__(self):
        names = get_player_names()
        # List of the players still in the game (not yet eliminated)
        self.players = [Player(i) for i in names]
        self.update_ranks()
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
        crewmates = players[2:]
        imp1.role = True
        imp2.role = True
        for player in crewmates:
            player.role = False
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

    def update_ranks(self):
        res = Tournament()
        for p in self.players:
            res.insert(p)
        self.ranking = res

    def delete_last_ten(self):

        for i in range(10):
            # Get min score in log(n)
            root = self.ranking.root
            while root.left:
                root = root.left
            self.ranking.delete(root.score)

    def play_rounds(self):
        ''' Used to simulate a round of the game, by taking 10 players
         per game and simulating scores for each game.
        '''
        players = inorder(self.ranking.root)
        # Play 3 random games, then update the ranking
        for i in range(3):
            print(f"Playing placement game {i+1}/3...")
            rd.shuffle(players)
            # List of all the random lobbies.
            lobbies = [players[i:i + 10] for i in range(1, 92, 10)]
            for lobby in lobbies:
                self.randomize_scores(lobby)
        self.players = inorder(self.ranking.root)
        self.update_ranks()
        print()

        # Now,play the 9 elimination rounds:
        for i in range(9):
            # Get players sorted by increasing score and create the lobbies
            # self.players = inorder(self.ranking.root)
            print(f"Playing ranked game {i+1}/9...")
            lobbies = [self.players[i:i + 10] for i in range(1,
                       len(self.players) + 1, 10)]
            for lobby in lobbies:
                self.randomize_scores(lobby)
            self.delete_last_ten()
        # Final ranking before 5 games reset
        self.players = inorder(self.ranking.root)
        print("\nFinal 10 players:")
        print(self.players)

        # Reset scores
        for player in self.players:
            player.score = 0

        finalists = self.players
        for i in range(5):
            print(f"Playing final game {i+1}/5...")
            rd.shuffle(finalists)
            self.randomize_scores(finalists)
        self.update_ranks()
        self.players = inorder(self.ranking.root)

        leaderboard = [f"TOP {i + 1}: {repr(p)}" for i, p in
        enumerate(self.players[::-1])]
        print("\n\nFinal Leaderboard:\n__________________________________\n-",
             '\n- '.join(leaderboard))

def get_player_names():
    with open("players_list.txt", "r") as f:
        res = f.readlines()
    return [i.strip() for i in res]

if __name__ == "__main__":
    game = Game()
    game.play_rounds()