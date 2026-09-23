# EPOCH 3 — monkeytype source (readable master)
# Goal: deep/broad understanding. Comments are the lesson — do not strip for speed runs yet.
# Paste file: monkeytype drills.txt  (literal \t / \n)
#
# DROPPED as repetitive / derivative of another chunk:
#   LinearSearch          → trivial scan; same idea as LL search walk
#   BubbleSort            → adjacent-swap cousin of insertion; low P2 EV
#   BinarySearchIterative → same decisions as recursive (shown as notes beside recursive)
#   S&S Hash(object)      → use ADT HashTable only
#   insert_front alone    → appears inside HashTable.insert
#   bare (value,) crumbs  → covered inside SQL/Flask blocks
#   Flask+mongo           → optional hedge; practise from WEB DEV misc when needed, not here
#
# SESSION: one block per paste. Prefer cold S&S/ADT before DB/Flask.

# ========== R1 recursion patterns (S&S misc) ==========
def Fact(n):
    # factorial: n! = n * (n-1) * ... * 1
    # base case stops the stack — without it, Fact keeps calling forever (overflow)
    if n <= 1:
        return 1
    # recursive case: one multiply + a smaller Fact; stack unwinds after base returns
    return n * Fact(n - 1)

def Sum1toN(n):
    # same shape as Fact: combine current n with answer for n-1
    # base: nothing left to add
    if n <= 0:
        return 0
    return n + Sum1toN(n - 1)

def ReverseString(s):
    # build reversed string from the outside in
    # base: empty or one character is already reversed
    if len(s) <= 1:
        return s
    # last char sits at the front; recurse on the prefix s[:-1]
    return s[-1] + ReverseString(s[:-1])

# ========== S1 binary search (recursive is the form to type; iterative = same logic) ==========
# recursive binary search — sorted Arr only
def BinarySearch(Arr, FindValue, Low, High):
    # invariant: if FindValue exists, it lies in Arr[Low..High] inclusive
    # empty window (bounds crossed) => absent — check this BEFORE using middle
    if Low > High:
        return -1
    # mid index of the current window (integer divide)
    middle = (Low + High) // 2
    if Arr[middle] == FindValue:
        return middle  # hit
    elif FindValue < Arr[middle]:
        # target is left of middle — discard middle and everything to its right
        # MUST return the recursive call; High = middle-1 so the window shrinks
        return BinarySearch(Arr, FindValue, Low, middle - 1)
    else:
        # target is right of middle — discard middle and everything to its left
        # Low = middle+1; using bare middle would infinite-loop on the same window
        return BinarySearch(Arr, FindValue, middle + 1, High)
# ±1 drops middle because it was already tested and is not in the remaining region
#
# iterative twin (do not paste separately): replace recursion with
#   while Low <= High:  ... High = middle-1 or Low = middle+1 ...
# same comparisons; no call stack; return -1 when the while ends

# ========== S2 insertion sort ==========
def InsertionSort(Arr):
    # Arr[0..i-1] is already sorted; i walks through the unsorted tail
    for i in range(1, len(Arr)):
        current = Arr[i]  # card pulled from the unsorted portion
        j = i - 1
        # walk left through the sorted prefix; shift anything bigger than current right
        # (do NOT pop() the last element into a fake prefix — that breaks the sort)
        while j >= 0 and Arr[j] > current:
            Arr[j + 1] = Arr[j]  # shift right; leaves a hole behind
            j -= 1  # step left
        # loop ends one index PAST the insertion spot, so the hole is at j+1
        Arr[j + 1] = current  # drop current into the sorted portion
    return Arr

# ========== S3 partition + quicksort ==========
def partition(arr, first, last):
    # Hoare-style school partition: first element is the pivot
    pivotvalue = arr[first]
    leftmark = first + 1  # starts just after pivot
    rightmark = last  # starts at the right end of this slice
    done = False
    while not done:  # keep going until the marks cross
        # IMPORTANT: test bounds BEFORE arr[leftmark] or you get IndexError
        while leftmark <= rightmark and arr[leftmark] <= pivotvalue:
            # still <= pivot — keep moving right
            leftmark += 1
        while rightmark >= leftmark and arr[rightmark] >= pivotvalue:
            # still >= pivot — keep moving left
            rightmark -= 1
        if rightmark < leftmark:
            # marks crossed — no more pair swaps
            done = True
        else:
            # both marks found something on the wrong side — swap them
            temp = arr[leftmark]
            arr[leftmark] = arr[rightmark]
            arr[rightmark] = temp
    # final step: park pivot at rightmark — THIS is its final sorted index
    # (stopping after the mid-swaps without this step leaves the pivot wrong)
    arr[first] = arr[rightmark]
    arr[rightmark] = pivotvalue
    return rightmark  # split point for the two recursive halves

def quickSort(array, first, last):
    # one or zero elements: already sorted — stop
    if first < last:
        split = partition(array, first, last)  # one pivot fixed forever at split
        quickSort(array, first, split - 1)  # sort left of pivot
        quickSort(array, split + 1, last)  # sort right of pivot
    return array

# ========== S4 merge + mergesort ==========
def merge(array, low, mid, high):
    # copy the two halves out — array[low..mid] and array[mid+1..high]
    left = array[low : mid + 1]
    right = array[mid + 1 : high + 1]
    # after divide-and-conquer, left and right are already sorted runs
    # using copies means this merge is NOT an in-place algorithm
    l = 0  # read head of left
    r = 0  # read head of right
    a = low  # write position back into the original array
    # repeatedly take the smaller head until one run is empty
    while l < len(left) and r < len(right):
        if left[l] <= right[r]:
            array[a] = left[l]
            l += 1
        else:
            array[a] = right[r]
            r += 1
        a += 1
    # drain whichever run still has leftovers (only one of these loops runs)
    while l < len(left):
        array[a] = left[l]
        l += 1
        a += 1
    while r < len(right):
        array[a] = right[r]
        r += 1
        a += 1
    return array  # range [low..high] is now one sorted run

def mergeSort(array, low, high):
    # single element is trivially sorted
    if low < high:
        # divide — same mid idea as binary search
        mid = (low + high) // 2
        mergeSort(array, low, mid)  # sort left half (keeps splitting)
        mergeSort(array, mid + 1, high)  # sort right half
        # conquer — as the call stack unwinds, merge sorted halves back together
        merge(array, low, mid, high)
    return array  # same list object throughout; sorted in-range

# ========== A1 node ==========
class Node:
    def __init__(self, data=None):
        # double-underscore = name-mangled "private"; outside code uses getters/setters
        self.__data = data  # payload stored in this node
        self.__right = None  # link to next node; None means end of chain

    def get_data(self):
        # read access without touching __data from outside the class
        return self.__data

    def set_data(self, data):
        # write access — keeps encapsulation even for a simple field
        self.__data = data

    def get_right(self):
        # follow the chain one step; None ⇒ you are on the tail
        return self.__right

    def set_right(self, right):
        # rewire the link (insert / delete both end here)
        self.__right = right

# ========== A2 linked list core (ADT.ipynb) ==========
# LinkedList shell assumed: __start = None, is_empty() → __start is None
# (typing the shell alone is low EV once you know the pattern)
def insert_end(self, data):
    new = Node()
    new.set_data(data)
    # empty list: new node becomes the head
    # no sentinel node; never use a mutable default like Node() in a signature
    if self.is_empty():
        self.__start = new
    else:
        # walk to the last node (its right link is None)
        current = self.__start
        while current.get_right() is not None:
            current = current.get_right()
        current.set_right(new)  # hook new onto the tail

def search(self, data):
    # linear scan along the chain — same idea as LinearSearch, but on links not indexes
    current = self.__start
    # loop on the NODE itself — testing get_right() in the while would skip the tail
    while current is not None and current.get_data() != data:
        current = current.get_right()
    return current  # Node if found, else None

def delete(self, data):
    if self.is_empty():
        return
    # HEAD case: there is no previous node — just move start forward
    # (calling previous.set_right here would crash; bare except would hide the bug)
    if self.__start.get_data() == data:
        self.__start = self.__start.get_right()
        return
    previous = None
    current = self.__start
    while current is not None and current.get_data() != data:
        previous = current
        current = current.get_right()
    if current is None:
        return  # not found — leave list unchanged
    # bypass current: previous now points at current's successor
    previous.set_right(current.get_right())

# ========== A3 BST insert + traversals ==========
# TreeNode = Node with get_left/set_left + get_right/set_right (same encapsulation idea)
def insert(self, data):
    new = TreeNode(data)
    # empty tree: first insert becomes the root
    if self.__root is None:
        self.__root = new
        return
    current = self.__root
    while current:
        # BST rule: <= goes left, > goes right (duplicates allowed on left here)
        if data <= current.get_data():
            if current.get_left() is None:
                current.set_left(new)  # found the empty child slot
                return
            current = current.get_left()  # keep walking left
        else:
            if current.get_right() is None:
                current.set_right(new)
                return
            current = current.get_right()

def in_order(self, node):
    # MUST take a node so recursion can walk subtrees (do not hardcode self.__root only)
    # left → visit → right  ⇒  keys come out in ascending order
    if node is not None:
        self.in_order(node.get_left())
        print(node.get_data())
        self.in_order(node.get_right())

def pre_order(self, node):
    # same recursion skeleton; visit moved to the FRONT
    # visit → left → right  ⇒  root first (useful for copying / prefix forms)
    if node is not None:
        print(node.get_data())
        self.pre_order(node.get_left())
        self.pre_order(node.get_right())

def post_order(self, node):
    # visit moved to the END
    # left → right → visit  ⇒  children before parent (useful for deleting / postfix)
    if node is not None:
        self.post_order(node.get_left())
        self.post_order(node.get_right())
        print(node.get_data())

# ========== A4 hash table (separate chaining) ==========
class HashTable:
    def __init__(self, N):
        self.__n = N  # table size = number of buckets
        # N SEPARATE LinkedLists — NEVER [LinkedList()] * N (that shares ONE list object)
        # list comprehension builds N independent chains for collisions
        self.__arr = [LinkedList() for _ in range(N)]

    def hash_function(self, key):
        # map key → bucket index in 0 .. N-1
        return key % self.__n

    def insert(self, key):
        # land in one bucket, then treat that bucket as a normal linked list
        bucket = self.__arr[self.hash_function(key)]
        # skip if already in this chain (search returns Node or None)
        if bucket.search(key) is None:
            bucket.insert_front(key)  # insert_front lives on LinkedList — not typed alone

    def search(self, key):
        # use self.__arr (not bare arr); convert Node/None into a bool for the caller
        return self.__arr[self.hash_function(key)].search(key) is not None

# ========== P1 JSON files (POOP misc) ==========
import json

def load_json(filename):
    # open text file → json.load → Python list or dict (depends on the file's top-level shape)
    # encoding matters on Windows; always pass utf-8 for exam-style data files
    with open(filename, encoding="utf-8") as f:
        return json.load(f)

def save_json(filename, data):
    # reverse path: Python object → JSON text on disk
    # "w" truncates/creates; indent=2 is for humans (optional in exams)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ========== D1 db open + csv seed (DB.ipynb spine) ==========
import sqlite3, csv

conn = sqlite3.connect("college.db")
# Row lets you use row["name"] instead of tuple indexes
conn.row_factory = sqlite3.Row
cur = conn.cursor()

with open("STUDENT.csv") as file:
    reader = csv.reader(file)
    next(reader)  # skip header row
    for row in reader:
        # ? placeholders — never splice user input into the SQL string
        cur.execute("""
            INSERT OR IGNORE INTO Student(stu_id, name, civics_class, handphone)
            VALUES (?,?,?,?)
        """, (row[0], row[1], row[2], row[3]))
conn.commit()

# ========== D2 parameterised CRUD (trailing comma matters) ==========
# (25999,) is a one-tuple — the comma is required or Python passes a bare int
# ? placeholders bind values safely; never f-string user input into the SQL text
cur.execute("SELECT name, civics_class FROM Student WHERE stu_id = ?", (25999,))
row = cur.fetchone()  # Row or None if no match — check before unpacking in real code
for i in row:
    print(i)

# UPDATE/DELETE also take a tuple of params; commit or the change never hits disk
cur.execute("UPDATE Student SET name = ? WHERE stu_id = ?", ("Renamed Student", 25999))
cur.execute("DELETE FROM Student WHERE stu_id = ?", (25999,))
conn.commit()

# ========== D3 JOIN / HAVING / LIKE / never-late ==========
# INNER JOIN: only students who have at least one matching Late row
cur.execute("""
SELECT Student.name, Late.date, Late.reason
FROM Student INNER JOIN Late ON Student.stu_id = Late.stu_id
WHERE Student.civics_class = ?
ORDER BY Late.date
""", ("25S02X",))
for row in cur.fetchall():
    print(row['name'], row['date'], row['reason'])

# WHERE filters rows BEFORE grouping; HAVING filters groups AFTER COUNT
# aggregates like COUNT(*) must not go in WHERE
cur.execute("""
SELECT Student.civics_class, COUNT(*) AS total
FROM Student INNER JOIN Late ON Student.stu_id = Late.stu_id
GROUP BY Student.civics_class
HAVING COUNT(*) >= 3;
""")
for row in cur.fetchall():
    print(row['civics_class'], row['total'])

# LIKE wildcards live in the Python tuple, not glued into the SQL text
cur.execute("SELECT name FROM Student WHERE name LIKE ?", ("%Li%",))

# never-late: keep all students (LEFT JOIN); no Late row ⇒ Late.stu_id IS NULL
cur.execute("""
SELECT Student.name
FROM Student LEFT OUTER JOIN Late ON Student.stu_id = Late.stu_id
WHERE Late.stu_id IS NULL AND Student.civics_class = ?
""", (c,))

# ========== F1 flask wiring (WEB DEV.ipynb) ==========
from flask import Flask, render_template, request, redirect, url_for
import sqlite3, csv

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def home():
    error = None
    if request.method == "POST":
        # keys must match HTML name="category" / name="name" exactly (typos fail silently)
        category = request.form.get("category", "").strip()
        name = request.form.get("name", "").strip()
        if name and category:
            # MUST return redirect — constructing the object alone does nothing
            return redirect(url_for("results", category=category, name=name))
        error = "Please fill in all fields"
    return render_template("home.html", error=error)

@app.route("/results/<category>/<name>")
def results(category, name):
    # function name "results" must match url_for("results", ...)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT student.Student_Name, student.Class_Group, late.Date, late.Reason
        FROM student INNER JOIN late ON student.Student_ID = late.Student_ID
        WHERE student.Student_Name LIKE ? AND late.Reason = ?
    """, (f"%{name}%", category))
    data = cur.fetchall()
    conn.close()
    return render_template("results.html", results=data, category=category, name=name)

@app.route("/add", methods=["GET", "POST"])
def add_late():
    # template uses url_for('add_late') — this def name is not optional
    error = None
    if request.method == "POST":
        stu_id = request.form.get("stu_id", "").strip()
        date = request.form.get("date", "").strip()
        reason = request.form.get("reason", "").strip()
        if not (stu_id and date and reason):
            error = "Please fill in all fields"
        else:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO late VALUES (?,?,?)", (date, stu_id, reason))
            conn.commit()
            conn.close()
            return redirect(url_for("home"))
    return render_template("add.html", error=error)

if __name__ == "__main__":
    app.run(port=5000)

# ========== O1 OOP (POOP.ipynb) ==========
class Resource:
    def __init__(self, ID, title):
        self.__id = ID  # private — outside code uses getters
        self.__title = title

    def get_id(self):
        return self.__id

    def get_title(self):
        return self.__title

    def set_title(self, title):
        self.__title = title

    def describe(self):
        return f"Resource {self.__id}: {self.__title}"

class DigitalResource(Resource):
    def __init__(self, ID, title, filesize):
        # chain parent constructor first (inheritance setup)
        super().__init__(ID, title)
        self.__filesize = int(filesize)

    def describe(self):
        # override — polymorphism: same method name, child behaviour
        # use getters for parent privates; do not touch parent __attrs directly
        return f"Digital Resource {self.get_id()}: {self.get_title()} ({self.__filesize} MB)"

# ========== K1 sockets brush-up (SOCKETS.ipynb) ==========
def recv_line(sock):
    # TCP gives a byte stream, not messages — recv(1024) may be partial or combined
    # keep reading until a newline delimiter arrives (or the peer closes)
    data = b""
    while b"\n" not in data:
        chunk = sock.recv(1024)
        if not chunk:
            break  # peer closed; return whatever we have so far
        data += chunk
    return data.decode("utf-8").strip()

# server spine: socket() → bind → listen → accept → loop recv_line / sendall → close
# client spine: socket() → connect → sendall((line+"\n").encode()) → recv → close
# always encode before send / decode after recv (utf-8); P2 usually needs one client at a time
# sendall, not send — send may write only part of the buffer
