$(info 1 $(words foo bar baz)) # 3
$(info 2 $(words      foo       bar 				baz			)) # 3
$(info 3 $(words a b c d e f g h i j k l m n o p q r s t u v w x y z)) #26

foo=
$(info 4 $(words $(foo))) # 0

$(info 5 $(words )) # 0

# "Returns the number of words in text. Thus, the last word of text is:"
# -- gnu make manual
text := A B D E F G H I J K L M N O P Q R S T U V W X Y Z _ ! @ $$ % ^ & * ( ) iamlast
$(info 6 $(words $(text))) # 36
$(info 7 $(word $(words $(text)),$(text))) # iamlast



