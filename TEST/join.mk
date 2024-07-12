$(info 1 $(join a b,.c .o))

$(info 2 $(join a b c d e f g ,.c .o))

$(info 3 $(join a b ,.c .o .f .pas .cc .rs .ada))
$(info 4 $(join	a	b	,.c	.o	.f	.pas	.cc	.rs	.ada))
$(info 5    $(join     a     b     ,.c     .o     .f     .pas     .cc     .rs     .ada    ))

a=a
b=b
c=c
$(info 6 $(join $a $b $c,$a $b $c))
a=aa aa
b=bb bb
c=cc cc
$(info 7 $(join $a $b $c,$a $b $c))

# "This function can merge the results of the dir and notdir functions, to produce
# the original list of files which was given to those two functions."
# -- GNU Make manual 4.3 Jan 2020

#filenames=/etc/passwd /etc/shadow /etc/group
#$(info 8 $(join $(dir $(filenames)), $(notdir $(filenames))))



