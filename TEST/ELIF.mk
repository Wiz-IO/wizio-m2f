$(info Test Begin)
X = 4
ifndef X
	$(info TRUE)
else
	$(info FALSE)
endif

$(info TEST FOR ${X})
ifeq (${X},1)
	$(info 1 = ${X})
else ifeq (${X},2)
	$(info 2 = ${X})
else ifeq (${X},3)
	$(info 3 = ${X})
else ifeq (${X},4)
	$(info 4 = ${X})
else
	$(info IS ${X})
	ifeq (${X},42)
		$(info Hack The Planet) # comment
	endif
endif
undefine X
$(info Test End)
include test.mk
