import gym
from gym import spaces
import random


def cmp(a, b):
    return float(a > b) - float(a < b)


class deck():
    def __init__(self, decks=1):
        self.cards = []
        for i in range(decks):
            self.cards.append(
                v for v in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] for s in range(4))

        self.cards = [item for sublist in self.cards for item in sublist]

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop(0)

    def deal_hand(self):
        hand = []
        for i in range(2):
            hand.append(self.deal())

        return hand


def usable_ace(hand):  # Does this hand have a usable ace?
    return int(1 in hand and sum(hand) + 10 <= 21)


def can_double(hand):
    return int(len(hand) == 2)


def sum_hand(hand):  # Return current hand total
    if usable_ace(hand):
        return sum(hand) + 10
    return sum(hand)


def is_bust(hand):  # Is this hand a bust?
    return sum_hand(hand) > 21


def is_natural(hand):  # Is this hand a natural blackjack?
    return sorted(hand) == [1, 10]


def score(hand):  # What is the score of this hand (0 if bust)
    return 0 if is_bust(hand) else sum_hand(hand)


class BlackJackEnv(gym.Env):

    def __init__(self, natural=True):
        """
        Actions:
        0 - Stay
        1 - Hit
        2 - Double Down
        3 - Surrender
        # Furture Implementation
        4 - Insurance
        5 - Split
        """
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Tuple((
            # User hand sum
            spaces.Discrete(32),
            # Dealer card showing
            spaces.Discrete(11),
            # Player has useable ace
            spaces.Discrete(2),
            # Player can double
            spaces.Discrete(2),
        ))
        self.natural = natural

    def step(self, action):
        assert self.action_space.contains(action)
        if action == 1:  # player hit, add card
            self.player.append(self.Deck.deal())
            if is_bust(self.player):
                done = True
                reward = -1.
            else:
                done = False
                reward = 0.
        elif action == 2:  # player doubled down
            done = True
            self.player.append(self.Deck.deal())
            if is_bust(self.player):
                reward = -2.
            else:
                while sum_hand(self.dealer) < 17:
                    self.dealer.append(self.Deck.deal())
                reward = cmp(score(self.player), score(self.dealer)) * 2
        elif action == 3:
            done = True
            reward = -0.5
        else:
            done = True
            while sum_hand(self.dealer) < 17:
                self.dealer.append(self.Deck.deal())
            reward = cmp(score(self.player), score(self.dealer))
            if self.natural and is_natural(self.player) and reward == 1.:
                reward = 1.5
        return self._get_obs(), reward, done, {}

    def _get_obs(self):
        return sum_hand(self.player), self.dealer[0], usable_ace(self.player), can_double(self.player)

    def reset(self):
        self.Deck = deck(decks=6)
        self.Deck.shuffle()
        self.dealer = self.Deck.deal_hand()
        self.player = self.Deck.deal_hand()
        return self._get_obs()

    def render(self, mode='human', close=False):
        # TODO
        return


if __name__ == '__main__':
    bjGame = BlackJackEnv()
    player, dealer, ace, double = bjGame.reset()
    done = False

    while done == False:
        print([player, dealer, ace])
        action = input("Stay or Hit:")
        state, reward, done, keys = bjGame.step(int(action))
        player = state[0]
        dealer = state[1]
        ace = state[2]

    print([player, dealer, ace, reward])
