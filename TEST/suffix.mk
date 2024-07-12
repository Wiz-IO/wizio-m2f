$(info 1 c=$(suffix src/foo.c src-1.0/bar.c hacks .c))

$(info 2 dot=$(suffix .ssh))
$(info 3 dot=$(suffix ......foo.....c))
$(info 4 dot=$(suffix ......foo.....c...c.c))
$(info 5 dot=$(suffix ..))

$(info 6 long=$(suffix .thisisalongnamethatviolatescommonsense))

$(info 7 weird=$(suffix foo.c/bar))

$(info 8 path=$(suffix /this/is/a/test/foo.c))

$(info 9 mydir=$(suffix $(sort $(wildcard *.py *.mk))))

$(info 0 empty=>>$(suffix foo bar baz qux)<<)


# c=.c .c .c
# dot=.ssh
# dot=.c
# dot=.c
# dot=.
# long=.thisisalongnamethatviolatescommonsense
# weird=
# path=.c
# mydir=.py .py .py .py
# empty=>><<
