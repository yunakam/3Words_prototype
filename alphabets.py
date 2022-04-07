import pygame
import random

icon_a = pygame.image.load(r'icons\a.png') 
icon_b = pygame.image.load(r'icons\b.png') 
icon_c = pygame.image.load(r'icons\c.png') 
icon_d = pygame.image.load(r'icons\d.png') 
icon_e = pygame.image.load(r'icons\e.png') 
icon_f = pygame.image.load(r'icons\f.png') 
icon_g = pygame.image.load(r'icons\g.png') 
icon_h = pygame.image.load(r'icons\h.png') 
icon_i = pygame.image.load(r'icons\i.png') 
icon_j = pygame.image.load(r'icons\j.png') 
icon_k = pygame.image.load(r'icons\k.png') 
icon_l = pygame.image.load(r'icons\l.png') 
icon_m = pygame.image.load(r'icons\m.png') 
icon_n = pygame.image.load(r'icons\n.png') 
icon_o = pygame.image.load(r'icons\o.png') 
icon_p = pygame.image.load(r'icons\p.png') 
icon_q = pygame.image.load(r'icons\q.png') 
icon_r = pygame.image.load(r'icons\r.png') 
icon_s = pygame.image.load(r'icons\s.png') 
icon_t = pygame.image.load(r'icons\t.png') 
icon_u = pygame.image.load(r'icons\u.png') 
icon_v = pygame.image.load(r'icons\v.png') 
icon_w = pygame.image.load(r'icons\w.png') 
icon_x = pygame.image.load(r'icons\x.png') 
icon_y = pygame.image.load(r'icons\y.png') 
icon_z = pygame.image.load(r'icons\z.png') 

all_alphabets = {
    'a': icon_a,
    'b': icon_b,
    'c': icon_c,
    'd': icon_d,
    'e': icon_e,
    'f': icon_f,
    'g': icon_g,
    'h': icon_h,
    'i': icon_i,
    'j': icon_j,
    'k': icon_k,
    'l': icon_l,
    'm': icon_m,
    'n': icon_n,
    'o': icon_o,
    'p': icon_p,
    'q': icon_q,
    'r': icon_r,
    's': icon_s,
    't': icon_t,
    'u': icon_u,
    'v': icon_v,
    'w': icon_w,
    'x': icon_x,
    'y': icon_y,
    'z': icon_z
}

vowels_n = {
    'a': icon_a,
    'e': icon_e,
    'i': icon_i,
    'n': icon_n,
    'o': icon_o,
    'u': icon_u,
}


# randomly get 16 samples from all alphabets list
random_alphabets = random.choices(list(all_alphabets.keys()), k=16)

# randomly get 8 samples from vowels&n list
random_vowels = random.choices(list(vowels_n.keys()), k=8)

# Create a list of alphabets to go to the center pane
alph_cards = random_alphabets + random_vowels

random.shuffle(alph_cards)
alph_cards = [(key, all_alphabets[key]) for key in alph_cards]

print(alph_cards)


################################
#
# all_alphabets = [
#     icon_a,
#     icon_b,
#     icon_c,
#     icon_d,
#     icon_e,
#     icon_f,
#     icon_g,
#     icon_h,
#     icon_i,
#     icon_j,
#     icon_k,
#     icon_l,
#     icon_m,
#     icon_n,
#     icon_o,
#     icon_p,
#     icon_q,
#     icon_r,
#     icon_s,
#     icon_t,
#     icon_u,
#     icon_v,
#     icon_w,
#     icon_x,
#     icon_y,
#     icon_z
# ]

# vowels_n = [icon_a, icon_e, icon_i, icon_n, icon_o, icon_u]
# random_alphabets = random.sample(all_alphabets.items(), 15)
# random_vowels = random.sample(vowels_n.items(), 9)
# alph_cards = dict(random_alphabets, **random_vowels)
