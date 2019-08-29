:- [$context].

:- dynamic $preds.

$query

:- forall(query(Q), (Q -> writeln(yes:Q) ; writeln(no:Q))).
:- halt.
   
