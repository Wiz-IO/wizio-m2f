$(info 1 Result is: empty: $(or,,boo)) # bad argument
$(info 2 Result is: $(or , ,boo))
$(info 3 Result is: $(or ,         ,boo))

VAR1 :=
VAR2 := Value of VAR2
RESULT := $(or $(VAR1), $(VAR2))
$(info 4 Result is: $(RESULT))

$(info 5 Result is: empty: $(and,,boo)) # bad argument

VAR1 := Value of VAR1
VAR2 := Value of VAR2
RESULT := $(and $(VAR1), $(VAR2))
$(info 6 Result is: $(RESULT))