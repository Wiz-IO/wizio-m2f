$(info 1 $(sort z y x b c a))
$(info 2  $(sort  z  y  x  b  c  a))
$(info 3		$(sort		z		y		x		b		c		a))

x=x
y=y
z=z
$(info 4 $(sort a $x b $y c $z))

$(info 5 $(sort a $x $x b $y $y c $z $z))
$(info 6 $(sort a $x$x b $y$y c $z$z))

$(info 7 $(sort $(wildcard *.py)))

$(info 8 $(sort $(sort a $x $x b $y $y c $z $z)))



