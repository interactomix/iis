# BIPS

Takes two or more sequences as input, produces a list of pairs of proteins
predicted to interact.

## Pre-Set

## Post-Set
Modlink



# iLoops

Takes a list of sequences and interactions.  For each protein pair it tests 
whether it is likely to be an interacting pair or not, based on the interactions
given.

## Pre-Set

## Post-Set
Modlink
iLoops



# Modlink+

Takes a list of sequences.  Predicts the structure of the sequences.

## Pre-Set
BIPS
iLoops

## Post-Set
M-VORFFIP
VDOCK



# M-VORFFIP

Takes a structure in PDB format.  Predicts functional sites on the structure.

## Pre-Set
Modlink

## Post-Set



# VDOCK

Takes two structures as input.  Predicts the interaction (most likely complex)
between the two molecules. Based on VORFFIP data.

## Pre-Set
Modlink

## Post-Set
PCRPI



# PCRPI

Takes structure of a protein protein complex.  Produces a list of residues that
have the largest contribution to the binding energy of the complex.

## Pre-Set
VDOCK
