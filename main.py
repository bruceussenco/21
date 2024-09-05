import random
import pygame

screen_width  = 640
screen_height = 360
screen_margin = 16
card_width  = 40
card_height = 64
cards_pile_pos = ((screen_width  - card_width)/2,
                  (screen_height - card_height)/2)

suits = ("♢ ", "♤ ", "♡ ", "♧ ")
suits_names = ("diamonds", "spades", "hearts", "clubs")
suits_textures = []
player_decks = ([], [], [], [])
players_deck_pos = (
    (cards_pile_pos[0], screen_height - card_height - screen_margin),
    (screen_width - card_width - screen_margin, cards_pile_pos[1]),
    (cards_pile_pos[0], screen_margin),
    (screen_margin, cards_pile_pos[1])
)


class Card:
    def __init__(self, suit, num):
        self.suit = suit
        self.num  = num

    def __str__(self):
        return suits[self.suit] + self.num

    def render(self, pos):
        screen.blit(card_texture, pos)
        screen.blit(suits_textures[self.suit], pos)


def reset():
    global cards
    cards = []
    for suit in range(4):
        cards.append(Card(suit, "A"))
        for i in range(2, 10): cards.append(Card(suit, str(i)))
        cards.append(Card(suit, "J"))
        cards.append(Card(suit, "Q"))
        cards.append(Card(suit, "K"))
    random.shuffle(cards)

    for i in range(4):
        for j in range(2):
            player_decks[i].append(cards.pop())


def update():
    pass

def render():
    screen.fill((200, 20, 30))
    screen.blit(card_back_texture, cards_pile_pos)
    render_cards()

def render_cards():
    # player1 cards
    card_margin = -20
    card_count = len(player_decks[0])
    first_card_x = players_deck_pos[0][0] - \
                   (card_count-1)/2 * (card_width + card_margin)
    for i in range(card_count):
        pos = (
            first_card_x + i * (card_width + card_margin),
            players_deck_pos[0][1]
        )
        player_decks[0][i].render(pos)

    # player2 cards
    card_count = len(player_decks[1])
    first_card_x = screen_width - card_count*card_width \
                 - (card_count-1)*card_margin - screen_margin
    for i in range(card_count):
        pos = (
            first_card_x + i * (card_width + card_margin),
            players_deck_pos[1][1]
        )
        screen.blit(card_back_texture, pos)

    # player3 cards
    card_count = len(player_decks[2])
    first_card_x = players_deck_pos[2][0] - \
                   (card_count-1)/2 * (card_width + card_margin)
    for i in range(card_count):
        pos = (
            first_card_x + i * (card_width + card_margin),
            players_deck_pos[2][1]
        )
        screen.blit(card_back_texture, pos)

    # player4 cards
    card_count = len(player_decks[3])
    first_card_x = screen_margin
    for i in range(card_count):
        pos = (
            first_card_x + i * (card_width + card_margin),
            players_deck_pos[3][1]
        )
        screen.blit(card_back_texture, pos)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# setup
cards = []
card_texture = pygame.image.load("card.png").convert_alpha()
card_back_texture = pygame.image.load("card_back.png").convert_alpha()
for suit_name in suits_names:
    suits_textures.append(pygame.image.load(suit_name + ".png").convert_alpha())

reset()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update()
    render()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

