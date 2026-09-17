patches for blurt 1 issues:

partial dependency is where a non-key field is not directly correlated to the whole PK (related to half of composite key, but not the other). e.g. would be production date related to batchID and factoryID but not productID on a join table with productID, factoryID and batchID. since production date is not actually related to productID, it should not be from this table and should be moved off to the batches table instead (with batchID PK)

transitive dependency is where a non-key field is linked to the PK via a middleman, (A -> B -> C) and is not directly related to the PK. so, in this case A should be moved out to another table that references B as PK for that new table. on larger scale, 3NF truly makes the relational database relational, solidifying the schema to do everything that RDB is good at. 

extreme are edge cases, abnormal are outright invalid cases (shouldnt be happening but we need safeguards for that)

check digits catch transcription error, verifying that the entire front chunk is complete and matches the end check digit

do i really need to re-justify this? bsts just dont store most recent nor oldest identity

every recursion runs a new function that returns to the current function's return address. in the example of factorial recursion, first call with input n will check for base case (n=1). if not, it will return n * factorial(n-1) which calls the function on top of the current stack. once this cycle reaches the base case, the function collapses the stack by unpacking everything and returning everything to their respective return addresses and you get n * (n-1) * (n-2) * ... 

