$(info 0 $(word 0, foo bar baz, 0))  # *** first argument to 'word' function must be greater than 0.  Stop.
$(info 1 $(word 1, foo bar baz)|)
$(info 2 $(word 2, foo bar baz)|)
$(info 3 $(word 3, foo bar baz)|)
$(info e $(word 4, foo bar baz)|)

$(info 5 $(word       1, foo bar baz)|)
$(info 6 $(word				1, foo   bar   baz)|)



