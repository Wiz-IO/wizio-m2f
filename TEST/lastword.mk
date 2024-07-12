$(info 0 out=$(lastword foo bar baz)|) # 0 out=baz|

# commas mean nothing
a=a,b,c,d,e,f,g,h,i,j
$(info 1 out=$(lastword $(a))|) # 1 out=a,b,c,d,e,f,g,h,i,j|

a=a b c d e f g h i j
$(info 2 out=$(lastword $(a))|) # 2 out=j|

a=1
b=3
c=8
x=$(lastword $a,$b,$c)
$(info 3 out=$(x)|) # 3 out=1,3,8|
