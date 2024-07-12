$(info Findstring Begin)

$(info 1 $(findstring a,a b c)|) 				# 1 a|
$(info 2 $(findstring a, b c)|)					# 2 |

s=foo bar baz
$(info 3 $(findstring foo, $s)|)				# 3 foo|
$(info 4 $(findstring foo, a b c $s d e f g)|)	# 4 foo|
$(info 5 $(findstring foo, foo bar baz)|)		# 5 foo|
$(info 6 $(findstring qux, foo bar baz)|)		# 6 |

s:=foo bar baz
$(info 7 $(findstring foo, $s)|)				# 7 foo|
$(info 8 $(findstring foo, a b c $s d e f g)|)	# 8 foo|

s=foo bar baz
$(info 9 $(findstring foo, $s)|)				# 9 foo|
$(info 0 $(findstring foo, a b c $s d e f g)|)	# 0 foo|
x=a b c d e f g
$(info 1 a=$(findstring a,$x)|)					# 1 a=a|
$(info 2 a=$(findstring a, $x )|)				# 2 a=a|
$(info 3 a=$(findstring a,$x $x $x)|)  			# 3 a=a|
$(info 4 a=$(findstring a,$x$x$x)|)    			# 4 a=a|

$(info 5 b=$(findstring a b,$x)|)    					# 5 b=a b| 		whitespace in "find" param is preserved as part of the string
$(info 6 b=$(findstring a  b,$x)|)  					# 6 b=| 		empty (whitespace mismatch)
$(info 7 b=$(findstring a  b, a  b  c  d  e  f  g )|)  	# 7 b=a  b|  	whitespace match

$(info 8 blank=>>$(findstring a b q,$x)<<)  				# 8 >><<
$(info 9 notblank=>>$(findstring a b q,$(subst c,q,$x))<<)  # 9 >>a b q<<

$(info 1 the=$(findstring the,hello there all you rabbits)|)  											# 1 the|
$(info 2 the=$(findstring the,now is the time for all good men to come to the aid of their country)|)  	# 2 the|

t=t
h=h
e=e
$(info 3 the=$(findstring $t$h$e,now is the time for all good men to come to the aid of their country)|)  # 3 the|
$(info 4 the=$(findstring $t$h$e,now is the time for all good men to come to the aid of their country)|)  # 4 the|
# case insensitve but will find 'the' in 'their'
$(info 5 the=$(findstring $t$h$e,now is THE time for all good men to come to THE aid of their country)|)  # 5 the|

$(info Findstring End)
@:;@:

