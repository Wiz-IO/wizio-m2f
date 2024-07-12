x=a b c d e f g
$(info 1 $(strip $x))

x=a  b  c  d  e  f  g
$(info 2 $(strip $x))

x=  a  b  c  d  e  f  g    # spaces at end
$(info 3 $(strip $x))
$(info 4 $(strip $x $x $x))
$(info 5 $(sort $(strip $x $x $x)))
$(info 6 $(filter a e,$(sort $(strip $x $x $x))))

x=  aa  bb  cc  dd  ee  ff  gg    # spaces at end
$(info 7 $(strip $x))
$(info 8 $(strip $x $x $x))
$(info 9 $(sort $(strip $x $x $x)))
$(info 0 $(filter aa ee,$(sort $(strip $x $x $x))))

x=		a		b		c		d		e		f		g
$(info 1 $(strip $x))

# missing args
x:=
$(info 2 empty>>$(strip )<<)
$(info 3 empty>>$(strip 				)<<)



