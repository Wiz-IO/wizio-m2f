$(info 0 $(firstword foo bar baz)|) # 0 foo|
$(info 0 $(firstword   foo   bar   baz)|) # 0 foo|

# from the GNU make manual
comma:= ,
empty:=
space:= $(empty) $(empty)

# commas mean nothing
a=a,b,c,d,e,f,g,h,i,j
$(info 1 out=$(firstword $(a))|) # 1 out=a,b,c,d,e,f,g,h,i,j|

a=a b c d e f g h i j
$(info 2 out=$(firstword $(a))|) # 2 out=a|

a=a    b    c    d    e    f    g    h    i    j
$(info 3 out=$(firstword $(a))|) # 3 out=a|

a=       a    b    c    d    e    f    g    h    i    j
$(info 4 out=$(firstword $(a))|) # 4 out=a|

b=e d c b a
c=8 7 6 5 3 0 9
x=$(firstword $a,$b,$c)
$(info 5 first=$(x)|) # 5 first=a|

a=1
b=3
c=8
x=$(firstword $a,$b,$c)
$(info 6 first=$(x)|) # 6 first=1,3,8|

a=2 1
$(info 7 first=$(x)|) # 7 first=2|

x = $(firstword $a${space}$b${space}$c${space})
$(info 8 spaces abc first=>>$(x)<<) # 8 spaces abc first=>>2<<

x=$(firstword)
$(info 9 empty first=>>$(x)<<) # 9 empty first=>><<

x=$(firstword ${space} ${space} ${space})
$(info 0 empty first=>>$(x)<<) # 0 empty first=>><<


