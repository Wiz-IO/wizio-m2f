$(info 1 $(addprefix src/,foo bar))

$(info 2 $(addprefix src/,foo,bar))

$(info 3 $(addsuffix .c,$(addprefix src/,foo bar)))

$(info 4 $(addprefix build/,$(addsuffix .c,$(addprefix src/,foo bar))))

$(info 5 $(addprefix c c,foo bar))


# MAKE
# src/foo src/bar
# src/foo,bar
# src/foo.c src/bar.c
# /c/Users/Georgi/build/src/foo.c /c/Users/Georgi/build/src/bar.c
# c cfoo c cbar
