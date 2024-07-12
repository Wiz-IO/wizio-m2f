
$(info 1 $(wordlist 2, 3, foo bar baz))
$(info 2 $(wordlist 1, 3, foo bar baz))

# *** invalid first argument to 'wordlist' function: '0'.  Stop.
#$(info 1 $(wordlist 0, 3, foo bar baz))

# start > end
$(info 3 $(wordlist 3, 2, foo bar baz)) # empty


x:=aa bb cc dd ee ff gg hh ii jj kk ll mm nn oo pp qq rr ss tt uu vv ww xx yy zz
$(info 3 $(wordlist 1, 2, $(x)))
$(info 4 $(wordlist 20, 30, $(x)))
$(info 5 $(wordlist 99, 9999, $(x)))

x:=   aa    bb    cc    dd    ee    ff    gg    hh    ii    jj    kk    ll    mm    nn    oo    pp    qq    rr    ss    tt    uu    vv    ww    xx    yy    zz   # trailing spaces
$(info 6 >>$(wordlist 1, 2, $(x))<<)
$(info 7 >>$(wordlist 20, 30, $(x))<<)
$(info 8 $(wordlist 99, 9999, $(x)))

$(info empty=$(wordlist 1,10,$(empty)))

x:=		aa	bb	cc	dd	ee	ff	gg	hh	ii	jj	kk	ll	mm	nn	oo	pp	qq	rr	ss	tt	uu	vv	ww	xx	yy	zz		# trailing spaces
$(info tab1 >>$(wordlist 1, 2, $(x))<<)
$(info tab2 >>$(wordlist 20, 30, $(x))<<)
$(info tab3 $(wordlist 99, 9999, $(x)))

# string too short for any match
$(info exceed=$(wordlist 8,10,aa bb cc))

$(info one=$(wordlist 1,10,aaaaaaaaaaaa))
$(info one=$(wordlist 2,10,aaaaaaaaaaaa))

$(info one=$(wordlist 1,0,aa aa aa aaa))

$(info files=$(wordlist 1,3,$(sort $(wildcard *.py))))



