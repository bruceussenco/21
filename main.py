import random
import pygame

class Card:
    def __init__(self, suit, num):
        self.suit = suit
        self.num  = num

    def __str__(self):
        return suits[self.suit] + numbers[self.num]

    def render(self, pos):
        screen.blit(card_texture, pos)
        screen.blit(suits_textures[self.suit], pos)
        screen.blit(numbers_texts[self.num], (pos[0]+card_width/8, pos[1]+card_height/8))

class Player:
    def __init__(self):
        self.cards = []

    def add_card(self):
        self.cards.append(cards.pop())

    def get_cards_sum(self):
        sum = 0
        for card in self.cards:
            if card.num > 9: sum += 10
            else:            sum += card.num+1
        return sum

screen_width  = 640
screen_height = 360
screen_margin = 16
card_width  = 40
card_height = 64
cards_pile_pos = ((screen_width  - card_width)/2,
                  (screen_height - card_height)/2)

numbers = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "J", "Q", "K")
suits = ("♢ ", "♤ ", "♡ ", "♧ ")
suits_names = ("diamonds", "spades", "hearts", "clubs")
suits_textures = []
players = (Player(), Player(), Player(), Player())
players_deck_pos = (
    (cards_pile_pos[0], screen_height - card_height - screen_margin),
    (screen_width - card_width - screen_margin, cards_pile_pos[1]),
    (cards_pile_pos[0], screen_margin),
    (screen_margin, cards_pile_pos[1])
)


def reset():
    global cards
    global round
    global players
    round = 0
    cards = []
    players = (Player(), Player(), Player(), Player())
    for suit in range(4):
        for number in range(12):
            cards.append(Card(suit, number))
    random.shuffle(cards)

    for i in range(4):
        for j in range(2):
            players[i].cards.append(cards.pop())

def update(events, keys):
    global running
    global round

    z_down = False
    x_down = False

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z: z_down = True
            if event.key == pygame.K_x: x_down = True

    if round == 4:
        pass
    elif round == 0:
        if z_down:
            players[round].add_card()
        if x_down or len(players[round].cards) >= 7:
            round += 1
    else:
        sum = players[round].get_cards_sum()
        if sum <= 16 and len(players[round].cards) < 7:
            players[round].add_card()
        else:
            round += 1

def render():
    screen.fill((200, 20, 30))
    if len(cards) > 0:
        screen.blit(card_back_texture, cards_pile_pos)

    render_cards(round == 4)

def render_cards(show):
    # player1 cards
    card_margin = -20
    card_count = len(players[0].cards)
    first_card_x = players_deck_pos[0][0] - \
                   (card_count-1)/2 * (card_width + card_margin)
    for i in range(card_count):
        pos = (first_card_x + i * (card_width + card_margin),
               players_deck_pos[0][1])
        players[0].cards[i].render(pos)

    # player2 cards
    card_count = len(players[1].cards)
    first_card_x = screen_width - card_count*card_width \
                 - (card_count-1)*card_margin - screen_margin
    for i in range(card_count):
        pos = (first_card_x + i * (card_width + card_margin),
               players_deck_pos[1][1])
        if show: players[1].cards[i].render(pos)
        else:    screen.blit(card_back_texture, pos)

    # player3 cards
    card_count = len(players[2].cards)
    first_card_x = players_deck_pos[2][0] - \
                   (card_count-1)/2 * (card_width + card_margin)
    for i in range(card_count):
        pos = (first_card_x + i * (card_width + card_margin),
               players_deck_pos[2][1])
        if show: players[2].cards[i].render(pos)
        else:    screen.blit(card_back_texture, pos)

    # player4 cards
    card_count = len(players[3].cards)
    first_card_x = screen_margin
    for i in range(card_count):
        pos = (first_card_x + i * (card_width + card_margin),
               players_deck_pos[3][1])
        if show: players[3].cards[i].render(pos)
        else:    screen.blit(card_back_texture, pos)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# setup
round = 0
cards = []
card_texture = pygame.image.load("card.png").convert_alpha()
card_back_texture = pygame.image.load("card_back.png").convert_alpha()
for suit_name in suits_names:
    suits_textures.append(pygame.image.load(suit_name + ".png").convert_alpha())

# setup text
pygame.font.init()
numbers_font = pygame.font.SysFont('Comic Sans MS', 15)
numbers_texts = []
for i in range(12):
    numbers_texts.append(numbers_font.render(numbers[i], False, (0, 0, 0)))

reset()

while running:
    update(pygame.event.get(), pygame.key.get_pressed())
    render()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

