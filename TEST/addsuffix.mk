$(info 1 $(addsuffix .c,foo bar))
$(info 2 $(addsuffix .c, fo bo mo ,aa bb dd,xx)) # no info

ext=.c
$(info 3 $(addsuffix $(ext),foo bar))

dot=.
c=c
$(info 4 $(addsuffix $(dot)$(c),foo bar))

$(info 5 $(addsuffix c c,foo bar))


