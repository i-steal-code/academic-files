gate 0:
class diagram:
usually 3 classes, 1 parent 2 child
each class has constructor, setters and getters, and maybe sometimes a unique method
private methods (such as constructor init) are encapsulated and indicated by the - sign
child classes are linked with arrowed lines pointing from child to parent
question may ask to demonstrate polymorphism (method overriding) and inheritence (which is already demonstrated in the creation of child classes)
child classes use same init method as parent

encapsulation hides private methods and leave only some public methods available for use. This protects the class object.
inheritance is the use of a parent class to create a child class that inherits its methods and attributes
polymorphism is where the parent class's method is overridden by re-defining it in the child class to change its use in the child class while keeping the same method name. 

from a non-3NF table, PK is unique identifier for each record (can be composite to keep uniqueness), 1:M when one table has 1 field that links to many in another table (employee table with 1 unique employee ID for each record linked to order table with 1 employee ID being in multiple records for handling multiple orders). M:M when multiple records link to multiple other in both tables (join tables containing multiple IDs from other tables)

recursion is calling a function within a function to continuously stack function calls upon each other until the termination condition is reached and the call stack collapses to return something. after 2 calls, call stack holds a function returning a function returning what the function inside is running (nested stack)

client-server architecture for less local compute required to run applications, for server-side to handle back-end while client runs front-end. DNS to assign domain name to server so that clients accessing information on server can find the server through the web and retrieve information/communicate with server. packet switching to route packets to client through different routes to maintain fastest connection

JOIN in RDB merges 2 tables on that one unique identifier, but still has no transitive dependency as each field is still dependent on the 1 unique identifying PK

recursion needs a base case so that the call stack will reach a terminal and begin to return back, collapsing the call stack. without a base case, the call stack infinitely recurses and eats memory infinitely, resulting in a stack overflow.

polymorphism is not inheritance. both require a parent class to be used, but polymorphism is overriding the parent class's method to use the same method differently, while inheritance is using the parent class's method on the child class because it inherited it from the parent. 

gate 1:
ER diagram:
designing schema using real diagrams; rectangle with table name to indicate table, branched trident-like prong on a 'many' relationship and single line connection on a '1' relationship. join tables have many-many relationships and are almost like connecting nodes for other 1:M tables. 

pseudocode for sql; PK underlined to indicate PK (underline multiple for composite), FK named to reference other table

for 3NF, partial dependencies are dependencies where a non-key field is not fully dependent on the PK (its unique identifer is another non-key field ), and transitive dependencies are non-key fields that do not contribute anything meaningful to the unique identity of the PK (fields that do not actually tell you anything about the PK). partial dependencies move partially dependent fields out of places that they should not be (usually creating a new 1:M table in the process), while transitive dependencies remove redundant fields that do not bear meaningful information to the PK.

SELECT table.field FROM table INNER JOIN table2 ON table.id = table2.id WHERE (condition) 

UPDATE table
SET field = ...
WHERE (condition)

INSERT OR IGNORE INTO table
(field1, field2, field3)
VALUES 
(v1,v2,v3)

can use aggregate functions such as SUM, MIN, MAX, etc. after GROUP BY to obtain a filtered table with each record being a group of records based on the GROUP BY criterion, and then using HAVING to filter for desired data. WHERE != HAVING because HAVING can only be used on GROUP BY and WHERE cannot. 

Nosql beats sql for server horizontal scaling (more parallel servers), having a more flexible schema (sql schema is fixed by design and change in schema requires big database structural change) and nosql has embedded documents (record in a record) for relationships between tables 

only collect strictly necessary data (non-essential private data ommitted), limit access of data such that only authorised parties have access to data limited strictly to that which is necesssary for the task

company X needs a database (because doesnt want a website) and comes to us to get it done. we see what data they have, and design a database schema for that. then we create queries to find the specific data they need. they realise that they are more suited for a shorter, flexible Nosql database so we advise them whether it is good for them or not (it actually isnt, but they just saw a mongodb ad and thought it was cool). because they are noobs, we also advise them on data collection/distribution so they do not accidentally leak private information to data brokers and let every mega-corp access someone's credit card information and their birthday (which should not have even been collected). 

once you go past 3 nests of embedded documents, shit starts going wack in a Nosql database. queries break through multiple nests just to find 1 set of data, and when there are too many relationships between tables, embedded documents start to contain plenty of partial dependencies and things become a nightmare to structure. relational database wins when vertical scaling is required (more and more relationships between data, extremely M:M heavy in nature). 

PDPA means to store strictly necessary personal data and use it responsibily by not letting it fall into the wrong hands (bad actors that do not have the client's best interests in mind e.g. data brokers), and also protecting the client's personal data that bad actors are trying to obtain using cybersec methods (data protection, etc.) 

gate 2:

write outcomes (YN combinations) in 1st quadrant, outcome ticks in second quadrant, actions in 3rd quadrant and conditions in 4th quadrant. to remove redundancies, remove outcomes where result is limited by 1 condition and other factors are irrelevant for that condition. 

validation ensures that data exists in the correct type and format. verification ensures that the data is correct. validation can be existence validation (input throwing "invalid entry" error when a null object is submitted), while verification can be double entry to ensure data entered is not just valid, but accurate

normal test data is data that happens in the average case, which is data that the algorithm was mainly designed to handle. (truly random array for a sorting algorithm)
abnormal test data is data that are rare occurences that may require more robust algorithm logic to handle. (partial chunk is sorted in an array)
extreme test data are edge cases that require special logic within an algorithm to handle them and fully cover all possible test cases. (fully sorted array, fully equal array, null array, etc.)

check digit's purpose is to ensure that data transfer is not lossy. it contains verification information used to check against the rest of the packet to ensure that the rest of the packet exists and corresponds to the check digit. mod-11 uses the last digit as the check digit, which is obtained by using a weighed sum of the payload (multipliction weights depends on length of payload, usually in descending order and ends on 2 for last payload digit) and modulus division on the weighted sum by 11 to obtain remainder of 0-10. remainder is subtracted from 11 to obtain final check digit, ranging from 0-10 (10 will be converted to 'X') and slapped onto the back of a payload.

backup creates a copy of the current state for restoration purposes when the main fails (corruption, destruction). without a backup, in the event of a failure on main, there is a high chance of work being lost and that is very bad. archive functions as records of past versions and is a form of storage for the past. unlike a backup, it cannot restore lost work as it is merely a past version, and restoring from an archive will not recover work that was lost from main. 

ASCII is the old system of characters operating on 7 bits of data for each character (and hence 2^7 unique characters), while Unicode uses 4 bytes (2^32 unique characters), containing significantly more characters than ASCII and allowing for characters of different languages and special symbols to be transmitted. 

bin to hex is done by grouping each bin number into 4s and then converting that into hex. mentally, its more like converting it to denary first using the (binary digit * 2^n) + ... sum, then turning it to hex (because denary to single digit hex requires 0 mental compute). works in reverse; each hex digit is converted to 4 digit binary chunks.

there are certain conditions for each scenario. need to record down each possible combination of conditions that can happen ad then what results it can possibly lead to, corresponding to the conditions laid out.

check digit is not the same as data integrity because data integrity encompasses more than just check digit; it includes methods that do not just verify data, but features to keep data protected, features to ensure sensitive data do not need to take on the risk of exposure 

keeping backups off-site ensures that main site failure/attacks do not destroy the backup so that backups can still run.

gate 3:

superclass is a parent class that child (or subclasses) inherit or polymorph from. attributes are the variables that you initialise a class with during class object definition. methods are the functions that you can execute on a class object, and are exclusive to that class object (but can be inherited or polymorphed by children)

an object is a object that takes on the defined properties of objects in a certain class, while the class is the definition of that particular group of object's various characteristics. for e.g. string is a class for a bunch of string objects that we shall call "nick gurr" and "knee guard". both are classified under the string class, which has methods such as upper(). so you can run the method on these objects because they are under the string class. however, calling it upon string as an object does nothing because string is the class, not an operable object with methods to execute. however, you can stick string into help() to understand how objects with this class work. 

private data needs to be hidden because... some inner workings of a class should not be revealed to the public and bad actors may exploit this sensitive information (using an unencapsulated init to break the program, finding out secret variables within a class and using it to reverse engineer the program, etc.). To safely let the public interface with the class, getter and setters that limit control over the object are available. internal secret variables that are encapsulated will conveniently not have getters or setters, and variables with getters and setters can only be accessed through these legal means

inheritance is... quite literally inheritance. child inherits the same properties as the parent, like the init and other methods. child can reuse almost everything that belongs to parent but can add more methods to extend its functionality and specialise in whatever it needs to do. 

polymorphism allows the child to morph the originally inherited method into a different one. this can change the method to function differently, suiting the child's needs more specifically. for example, if we have a parent class of 'array' and children of 'list' and 'tuple', and parent has a .sort() method. due to the difference in the nature of both children, we will have to modify how the sort logic works, even though it actually does the same thing. this allows use to immute the object to a different type (we change an array class object to become a list class object), while using the same method name on it. This allows us to input the object of any of the 3 classes and still be able to run the 'same' method, which is really cool.

im not sure if composition is in the syllabus but composition is more useful when the core functionality of a child class is not so similar to its parent, and that parent class changes may break a child that closely inherits the parent class. composition used when a class needs to reference a small set of methods from a parent but does not want to have too many dependencies. composition is more modular in that sense

children cannot access parent private attributes and methods because they are encapsulated. if the children could do that, it breaks the whole point of encapsulation where data is contained and protected within each class (bad actors can set up a child and start calling private data from parent, bypassing security). you will have to use the public methods of the parent class within the child in order to access private attributes.

gate 4:

adding data finds a space in memory to insert the new data and also a way to reference the new data from the data struct object. to check existence, will need to search for the data and pinpoint its existence in memory. what on earth is recent. sorted does linear sweep to ensure each object is sorted by the criterion correctly (compare current and next) to return a boolean for sorted state. first in first out is the concept behind queue where a queue buffers processes/data in a cache, returning the front of the queue (first in is the first out) and inserting new stuff at the end of the queue so everything gets their turn in the line. 

arrays are simple for storing data in a static memory allocation, has low overhead and is simple for programmers to code when list size is fixed. this is because you are literally referencing a chunk of memory and just reading off that portion. it becomes slow when dynamic application is required (constant popping and insertion of middle nodes), needing a memory re-allocation to use the same data struct. 

last in first out stacks are generally good for recursive call stacking (the newest thing MUST be finished first) and also allows for faster access and control over the new, urgent thing (rapidly undoing current action).

queues in linear serve as good, fixed buffers, but sometimes you do not have so much memory to play with or the implementation requires something more dynamic. circular queues have shifting head and tails for the queue, allowing for the queue to work with dynamic allocation of the front of the queue and does not have to shift the entire queue in memory to move the whole line (linear either leaves head empty or has to move entire queue forward, making mem allocation a bit of a nightmare when queues are larger and requires more flexibility). due to the less movement and also more dynamic mem allocation of circular queues, it takes up less mem space and compute to use a queue. the only downside is that you need to allocate a fixed amount of space to circular queues and changing its size requires more resources than linear queues. linear wins where queue size rapidly changes.

hash tables are like magic; instantaneous indexing and extremely organised data organisation with a pretty decent memory allocation. hash functions look at the data being inserted and hash a unique index for that object. hash functions are consistently fast and doing this, so search is average O(1). of course, its hard to get a hash function to hash an unique index for everything (and if it could, we would have the hash table scattered so far and wide across memory shit would go nuts), so when 2 data objects get hashed to the same index, they collide and you have to figure out how to handle them; give them the adjacent index, or shelve them under the same index as a linked list? The only problem about hash tables are that it is a non-graph data structure, so there are no defined relationships and no ordered traversal. if you want to find the history of insertion or directly get a sorted list of all hash table objects, you cant or will need a fair bit of compute, because hash table is merely a library for data, not a tree that tells you how data is related to each other. 

binary search trees essentialy is the opposite of hash table in the sense that it prioritises data relationships (everything is inserted in the structure of a binary search) for extremely fast traversal and search times in a completely different way from hash tables. because bst is already in the shape of a binary search, search times sweep through the tree in the same logic and time complexity as a binary search. this also means that you can devise algorithms to easily sort the entire tree (which is a big plus). the only problem comes when the edge case insertion happens; first data is small, and every subsequent data inserted is larger and larger which ends up with everything being shoved to the left and ultimately becoming simply a sorted linked list (which actually isnt too bad) that has a traversal time of... you guessed it: O(n), same as a linked list. The cool thing is that its just sorted because of the bst insertion logic, but every new insertion follows sorted linked list insertion that makes you traverse the entire list to insert at the end, giving you a insertion complexity of O(n) as well (which destroys the whole point of the bst)

array is a literal chunk of memory allocated to store stuff. static, fast, and rigid in structure. breaks the moment you need rapidly changing/dynamically moving data. linked list is all over the place; nodes can be anywhere in memory, and connect to each other by referencing each other's memory locations. this allows fast modification of the middle, by reforming node connections to include a new one in the network or delete one. This technically takes up more memory because you need to store the pointers and then the data itself, and also costs more compute since running around so much is not free, but its more dynamic and allows one to rapidly modify data. in a static array, you know that chunk of memory is that array, so blind lookups are allowed and direct (you want index 2? check the 3rd slot of this chunk in the memory. boom. instant data) 

recursion base case acts as terminal to collase call stack and end when desired condition is hit. until then, recursive function repeatedly calls itself within itself with the new input and works toward base case. 

call stack pushes new function with new input to compute, and pops it once it finishes computing and subsequently collapses the call stack. In the event that the termination event is not hit during the recursion, you run the risk of infinitely calling onto the stack and eventually causing the stack to overflow (run out of memory).

iterative loops the same code until a certain loop condition is hit, which calls a stack of code and collapses it on the go (queue-like). in recursion, the function runs with the input, and when base case is not triggered, repeatedly passes it into itself again with the modified input. once the input reaches the base case, the function starts returning the output and it repeatedly collapses the stack by returning it to the previous function that was recursed. 

in bst insertion, use binary search's compare current to decide go left or right until you end up at a non-parent node and you can insert. in-order traversal puts a dot at the bottom-side of a bst (visual graph) and traces it from one end to the other to link everything together in an ascending order. pre and post put the dot on the left and right side of each node respectively. i dont remember what pre and post give but i do know that you jsut have to trace the dots without intersecting with the graph. 

array bst is stupid. bst but instead of dynamic mem allocation with nodes and pointers floating in mem. it uses a static array that tells you which is the left and right node of each index using 2 other lists. this allows you to reference the next item in array bst and figure out which index to reference for the left and right. free space list in dynamic data structures are used to store a linked list of empty nodes so thay they do not simply waste memory (for systems without garbage collection) and you can recycle them for future use. important to know for low-level programming, because memory and compute allocation is critical. of course, in modern day, we mostly use high-level python because its a waste of human time to do all this especially when AI can transcribe high-level python into low-level C or even assembly with all the mem and time complexity issues taken into account. 

merge sort divides the array and conquers them bit by bit. it is very consistent and always uses the same time complexity of O(n log n), but memory complexity grows with array size. merge sort is stable because objects of the same comparative value remain in the same order as in the original array.

quicksort average case O(n log n) because its also kind of like a divide and conquer, but in a more dynamic in-place way compared to mergesort. however, it is unstable because of how dynamic it is; same comparative value data may swap places in quicksort from original array because of pivoting. quicksort worse case scenario is O(n^2) when a pivot gives a lopsided split (every pivot detected is on the extreme left side), which turns quicksort into a complicated bubble sort. 

insertion sort is good when it is nearly sorted because only the erratical data is being re-inserted, and reduces time complexity to a small O(n) because the sort is mostly just linear sweeps to catch minor errors while verifying sorted sequences

binary search needs sorted input because the logic that it operates on assumes that the list is sorted in a certain order so that it can skim past the irrelavant data and shrink the search zone. hash tables are not binary search because instead of shrinking the search zone, it simply computes the index that the data belongs at immediately. why search for something, when you already figured out where it is?

oldest in bst is easy to find because it is root node. however, most recent is impossible to find because any one of the non-parent nodes could have been the recent one, so it is uncertain as to which is the most recently inserted. a queue would be the best (especially circular) for this application, as the head and tail is clearly indicated at every point of looking at the data structure. a stack would work, but has significant compute overhead as you have to collapse the stack to reach the bottom and obtain oldest, which is a O(n) operation. 

merge beats quick when probability of quick edge cases is high, or fidelity is required (quick is unstable). 

unbalanced bst comes from base data insertion order (large chunks of sorted data) and the cost is the complexity of a bst implementation with the functionality of a linear linked list (doing allat just for O(n) time complexity)

gate 5:

url has protocol (http or https), DNS, (www.ihateniggers.com) and path (/homepage), with query (?=ijiji) and fragment (#yeah)

DNS scours through a route of domain servers (look for top level domain, then scope down to regional, national, etc.) to find the ip address of that domain you are referring to. then, you know where to look at to find server stuff

http transfers method (post or get) with the path (file location for resource) and has a header that tells you what the request is about, followed by a payload that carries all the relevant data for the backend to process. the back end server sends a response in the same protocol, putting that payload in your computer and loading up a website (or redirecting you). 

client-server allows one to offload the backend stuff onto a server and allow the weak, cheap cheap client-side device to boot up a web-based application faster than if everything was loaded locally. this centralises the back end, connecting clients seamlessly but also placing a larger strain on the server (server overloading). 

native app good when you have bad wifi. hard to play web games underground. web app good when app needs to centralise data to prevent client modification (exploiters taking advantage of local architecture to hack game clients) 

yeah actually i dont know much about the rest of networks im gonna learn that soon (in time for exam)

gate 6:

i ran out of mental compute here 


