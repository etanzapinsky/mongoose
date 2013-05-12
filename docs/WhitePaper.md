Mongoose

An Agent-Based Modeling Simulation Language
===========================================

+ ------------------------------------- +

| |

| .--. |

| ( \_ \\ |

| / /: :\\ |

| ,=. \^ / . | |

| ---'.\_.--.\_ \\ : / |

| \\ '.\_\_=-. \\ .' ,-. |

| ( ' e\\ | : / \_ \\ |

| \\ , ' . .-'-\^ , | \\ / \\ \\ |

| |; \\!\_ \\|;. ;/.\_, \\ '--' ) |

| \^\^= \^= '.\_\_,''------' |

| |

+ ------------------------------------- +

Group 17

Mark Fischer (mlf2156) Language Guru

Chris Haueter (cmh2122) System Integrator

Michael Rubin (mnr2114) Project Manager

Bo Xu (bx2104) Tester

Etan Zapinsky (eez2107) System Architect

Introduction
------------

The modern commodity processor is a computational workhorse, capable of
doing 2.5 billion computations per second^[[1]](#ftnt1)^ and effectively
handling multi-threaded applications. Although these commonplace
computers are able to run complex simulations, there is still an
opportunity for a high-level language that abstracts away the
implementation details of configuring and running such simulations.
Mongoose is such a language, designed to easily facilitate creating
independent-agent, discrete-event simulations.

One use case for Mongoose is Schelling’s Segregation
Model^[[2]](#ftnt2)^. The premise of Schelling’s Segregation Model is
that there are different colors representing an individual’s tribe
affiliation, with individual agents of differing tribes dispersed across
a 2D Cartesian grid. For social scientists, this tribal affiliation is
used to represent any difference that they are interested in
researching, including gender, age, race and hobbies.

One formulation of this simulation relies on the rule that an individual
agent will move to a random free space on the board if e.g. more than
25% of its surrounding neighbors are of a different tribe. This can be
simulated using Mongoose’s independent-agent approach; in this case,
large numbers of agents interact with one another via their internal
preferences and their locations in the environment.

For example, Mongoose can be used by a researcher to investigate the
extent to which weak tribal preferences might lead to clustering of
distinct groups, or to determine whether the formation of tribal groups
will converge to a steady state, or the agents will be stuck in a
divergent pattern.

Furthermore, Mongoose provides syntax that allows for easy use of randomization, to enable the programmer to code simulations more efficiently.

Additional problems which Mongoose might be used to simulate are
Conway’s Game of Life^[[3]](#ftnt3)^ (discussed below), epidemiological
models, population growth, crowd simulation, traffic patterns, and
financial outcome prediction (e.g. retirement planning).

Language Properties
-------------------

### Simple and Object-Oriented

When creating a simulation, there are many common steps a programmer 
would have to take to get their program up and running. They have to 
specify environment invariants, environment agents, agents’ actions, 
and termination conditions. Our language should easily abstract writing 
these common lines of code the user would have to write for each simulation.

Mongoose is object-oriented to make interacting with an environment and 
agents, each with an internal state and actions, intuitive and manageable. 
Like Python, the language will provide first-order classes and objects. 
It will also provide invariants and terminating conditions. All of 
these objects would interact in specific ways so that the programmer 
will be able to create a mental model of the simulation
and truly understand how the different components relate to one another.

Environments and agents are fundamental classes of objects. Agents will
be situated in, and interact with their environments. This is an
important component of many agent-based models because any agent’s
future actions can depend on the local environment. This will help users
focus on the relevant abstractions for their model.

Our programming language uses Java-like syntax with some Python-esque 
elements and control logic as points of familiarity for users experienced 
with another high level programming language. In addition, the language 
provides domain-specific primitives for ease of use. These include 
keywords like environment, agent, pif and the built-in function print.

### Temporal

Mongoose cares about every time increment because in order to have a
discrete-event simulation, the language has to schedule events properly.
Each event occurs at a particular tick of the clock, which signifies a
change of state in the simulation. Between consecutive events, no change
in the system is assumed to occur, thus enabling the simulation to
directly jump from one event to the next. Each event is comprised of
behaviors acted out by various agents.

An advantage of this is that each tick of the clock provides a
convenient mechanism to allow the programmer to determine how much time
it takes to reach one environment state from another.

### Analysis

Performing the same actions thousands, if not millions of times is only
half of what makes a discrete-event simulation tool powerful. The other
important aspect is its ability to perform analysis on the simulation’s
results. How many organisms were spawned in Conway’s Game of Life? How
many died? What is an organism’s average life span? If our language
cannot answer these questions it is as if we have created a computer
that can run programs but has no way to print the results. Mongoose allows
the program to act differently based on how the simulation ended. 
Depending on which invariant was broken, a Mongoose program will execute
different code, before terminating.

Intended users
--------------

The intended users of the language are researchers and students who
desire to specify and run agent-based, discrete-event simulations with a
minimum of language boilerplate. They are assumed to be familiar with
basic concepts of simulation. They are also assumed to have some Python or
Java programming experience (at the very least, they should be aware of 
basic data structures and operators). Writing programs in Mongoose will be
comfortable for a programmer who has already used an ALGOL-family programming 
language such as C, Java or Python.

Existing Solutions
------------------

Mongoose focuses on discrete event simulations, i.e. the modeling of a
simulation as a discrete sequence of events in time. Specifically, our
language deals with Agent-Based Modelling (ABM), where the simulation
can be modeled as decentralized agents with behaviors in a common
environment. While there are many libraries and pieces of software built
for discrete event simulations, there are not a whole lot of languages.
Some of the languages that exist for solving these types of problems are
Simula and SIMSCRIPT. SIMSCRIPT, however, is written in a more
English-like syntax, which may be less familiar to programmers
experienced with C or Java, whom our language targets.

Additionally, Mongoose will be tailored towards agent-based modelling,
while Simula and SIMSCRIPT are not, and use a concurrent process
model.^[[4]](#ftnt4)^ While software like ExtendSim, Simio, AnyLogic, or
Flexsim allow for ABM, they are not full languages.

* * * * *

[[1]](#ftnt_ref1) When running an intel i7 with 2.5 GHz clock speed
(http://ark.intel.com/products/65525/Intel-Core-i7-3770T-Processor-8M-Cache-up-to-3\_70-GHz)

[[2]](#ftnt_ref2)
http://en.wikipedia.org/wiki/Thomas\_Schelling\#Models\_of\_segregation

[[3]](#ftnt_ref3)
http://en.wikipedia.org/wiki/Conway%27s\_Game\_of\_Life

[[4]](#ftnt_ref4)
http://cgibin.erols.com/ziring/cgi-bin/cep/cep.pl?\_key=Simscript
