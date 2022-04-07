import enchant

d_us = enchant.Dict("en_US")
d_uk = enchant.Dict("en_UK")

def check_word(word):
    return True if d_us.check(word) or d_uk.check(word) else False

# print(d_uk.check("programme"))
# print(check_word("programme"))