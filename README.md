# Makefile Interpreter ( Python )

Rather, a build variables Collector, does not perform Rules<br>
I want to use it as PlatformIO ( NuttX and others who use Maке ) plugin<br>
( with CMAKE I still fail due to lack of (inside) information )<br>
I also want to note that I am not a Python Pro, so don't shoot the pianist...<br>
( There are probably bugs or a wrong strategy )<br>
To note the fact that in [48 years of Make](https://en.wikipedia.org/wiki/Make_(software)) there is no such interpreter (or I did not find one)

The idea started years ago with the Raspberry Pi Pico SDK ( **wizio-pico** ).<br>

I must note that it is incompetently constructed SDK, CMAKE-based ... for a handful of ARM code<br>
( this is not negativity towards Raspberry, it is simply the way things are ).<br>

**What happens**:<br>
Initially, it was a **Linux**-dependent SDK.<br>
( I don't know how it is now, but it probably works with difficulty on Windows )<br>
So, CMAKE collects Build Variables depending on the settings of your project.<br>
By Build Variables, understand: **KEY = VALUE** ... CFLAGS = -DSOME -IPATH etc.<br>
With these variables, MAKE files are eventually built, which compile "everything"<br> 
(Pico SDK: a simple blink takes a minute and much more)

The problem was that CMAKE/MAKE is difficult to interpret for embedding in an IDE  ( let's say VSCode )<br>
and if they "**lazily**" use specific PC OS Shell commands:<br>
The platforms do not reach users with other OS like Windows ( or a list of Install: this, that ).<br>

And considering that the SDK is constantly being updated, integration becomes almost impossible.<br>
The SDK architects justify themselves: The SDK works! That's how it should be!<br>
Yes, fine, but we are in the 21st century, there are perfect scripting languages like Python & JS,<br>
and you are using dependent Build Systems from the last century...<br>

Anyway! Many years ago, I came across **NuttX** ( POSIX OS ... something like a mini Linux )<br>
and tried to integrate it into Microchip MPLAB IDE<br>
( blah ... somewhere down in my git under the name: TizenRT-PIC32 ).<br>
Currently, NuttX has 1265 makefiles ... UNIX OS Dependent ( because of a few lazy Shell commands )<br>
and it is constantly being updated...<br>
Basically, it compiles code into static libraries ( depending on the project settings )<br>
and finally combines everything into an ELF - your project.<br>

Deviation: The renowned **Zephyr Project** uses:<br>
CMAKE + Shell + Python to generate Makefiles<br>
Then: MAKE + Shell + Python to invoke GCC with flags and files !?!?!<br>
( extremely clever, isn't it ... for a multi-million USD Project )<br>

VSCode / **PlatformIO** uses SCONS, which is a cross-platform and powerful **Python Build System**<br>
I don't know a developer who doesn't have Python installed on their computer.<br>
Surely, you realize that Python is used to train AI, so running GCC should be a breeze.<br>
( I intentionally translated it (README.md) with ChatGPT )

After several months of experiments and analysis, it turns out that <br>
NuttX makefiles -> KEYS = VALUES -> GCC<br>
and the only thing (this project) needed is to take these KEYS = VALUES somehow and integrate them into PlatformIO.<br>
And the main idea is:<br>

* CLICK - Install ( regardless of OS )
* CLICK - New Project
* CLICK - Configure
* CLICK - Compile / Upload ... POSIX OS for a vast number of boards and microcontrollers.

CLICK, CLICK (almost like Arduino, but much more advanced) can be done by all little and grown-up kids...<br>
and explain to your CEO: how many customers you will have and what kind of ecosystem you will have.<br>
[Something like that happens](https://www.youtube.com/watch?v=esO7zpXCDjs&ab_channel=GeorgiAngelov)

TODO: blah ... many tests !!!
