# EPOCH 2 source — YOUR boilerplate notebook code + teach comments
# Cold (~50% narration): binary, insertion, partition/quick, merge, LL delete, hash, flask wiring, SQL params
# Warm (~25% narration): linear, bubble, node, BST, db open, OOP, fragments
# Converted paste file: monkeytype drills.txt  (literal \t \n)

# --- S&S.ipynb (warm) ---
def LinearSearch(Arr, FindValue):
    # probe each index left to right
    for i in range(len(Arr)):
        if Arr[i] == FindValue:
            return i  # return index of first match
    return -1  # not found

# --- S&S.ipynb binary (COLD ~50%) ---
# recursive binary search
def BinarySearch(Arr, FindValue, Low, High):
    # window is Arr[Low..High]; empty window => absent
    if Low > High:
        return -1
    # middle of current window only — never "if FindValue not in Arr"
    middle = (Low + High) // 2
    # exact hit
    if Arr[middle] == FindValue:
        return middle
    # target left of middle: discard middle and right half
    elif FindValue < Arr[middle]:
        # MUST return; High = middle-1 so bounds shrink
        return BinarySearch(Arr, FindValue, Low, middle - 1)
    # target right of middle: discard middle and left half
    else:
        # Low = middle+1; bare middle => infinite recursion
        return BinarySearch(Arr, FindValue, middle + 1, High)

# iterative binary search — same decisions, loop instead of call stack
def BinarySearchIterative(Arr, FindValue, Low, High):
    # keep looping while the window still has at least one index
    while Low <= High:
        middle = (Low + High) // 2
        if Arr[middle] == FindValue:
            return middle
        # shrink right edge
        elif FindValue < Arr[middle]:
            High = middle - 1
        # shrink left edge
        else:
            Low = middle + 1
    # markers crossed with no hit
    return -1

# --- S&S.ipynb insertion (COLD ~50%) ---
def InsertionSort(Arr):
    # Arr[0..i-1] already sorted; i is first unsorted index
    for i in range(1, len(Arr)):
        current = Arr[i]  # object taken from unsorted portion
        j = i - 1
        # shift larger sorted objects right until insertion spot found
        # do NOT pop() the last element into a fake "prefix"
        while j >= 0 and Arr[j] > current:
            Arr[j + 1] = Arr[j]
            j -= 1
        # hole at j+1 is where current belongs
        Arr[j + 1] = current  # insert into sorted portion
    return Arr

# --- S&S.ipynb bubble (warm ~25%) ---
def BubbleSort(Arr):
    n = len(Arr)
    swapped = True
    while swapped:
        swapped = False
        for i in range(n - 1):
            if Arr[i] > Arr[i + 1]:
                # swap to put current pair in correct order
                temp = Arr[i]
                Arr[i] = Arr[i + 1]
                Arr[i + 1] = temp
                swapped = True
        # after a no-swap pass, list is sorted
    return Arr

# --- S&S.ipynb partition+quick (COLD ~50%, your 2-space style) ---
def Partition(Arr, First, Last):
  # pivot is first element of this slice
  pivotValue = Arr[First]
  leftmark = First + 1 #index of second left object
  rightmark = Last #index of right-most object
  done = False

  while not done:
    # walk right while still <= pivot
    while leftmark <= rightmark and Arr[leftmark] <= pivotValue:
      #increment leftmark index until leftmark array value >= first term
      leftmark += 1
    # walk left while still >= pivot
    while Arr[rightmark] >= pivotValue and rightmark >= leftmark:
      #decrease rightmark index until rightmark array value <= first term
      rightmark -= 1
    #the loops above will stop if rightmark approaches leftmark

    if rightmark < leftmark:
      #end the loop when rightmark index < leftmark index
      done = True
    else:
      #swap leftmark and rightmark value in array
      temp = Arr[leftmark]
      Arr[leftmark] = Arr[rightmark]
      Arr[rightmark] = temp
  #swap first term and rightmark value — pivot's FINAL sorted index (do not stop at mid-swap)
  temp = Arr[First]
  Arr[First] = Arr[rightmark]
  Arr[rightmark] = temp
  return rightmark #output rightmark index

def Quicksort(Array, First, Last):
  # one/zero length slice is already sorted
  if First < Last:
    SplitPoint = Partition(Array, First, Last)
    #recursively quicksort left half
    Quicksort(Array, First, SplitPoint - 1)
    #recursively quicksort right half
    Quicksort(Array, SplitPoint + 1, Last)
  return Array #return once fully sorted where index term >= last index

# --- S&S.ipynb merge (COLD ~50%, your 2-space style) ---
def merge(array, low, mid, high):
  # snapshot left Arr[low..mid] and right Arr[mid+1..high]
  left = array[low : mid + 1]
  right = array[mid + 1 : high + 1]
  i = 0
  j = 0
  # k writes back into original array starting at low
  k = low
  # take smaller head while both halves still have unread values
  while i < len(left) and j < len(right):
    if left[i] <= right[j]:
      array[k] = left[i]
      i += 1
    else:
      array[k] = right[j]
      j += 1
    k += 1
  # drain leftovers from left half
  while i < len(left):
    array[k] = left[i]
    i += 1
    k += 1
  # drain leftovers from right half
  while j < len(right):
    array[k] = right[j]
    j += 1
    k += 1
  return array

def mergeSort(array, low, high):
  # split until single-element runs, then merge on the way back up
  if low < high:
    mid = (low + high) // 2
    mergeSort(array, low, mid)
    mergeSort(array, mid + 1, high)
    merge(array, low, mid, high)
  return array

# --- ADT.ipynb Node (warm ~25%) ---
class Node:
    def __init__(self, data=None):
        self.__data = data
        self.__right = None  # next link; None = end

    def get_data(self):
        return self.__data

    def set_data(self, data):
        self.__data = data

    def get_right(self):
        return self.__right

    def set_right(self, right):
        self.__right = right

# --- ADT.ipynb LinkedList methods (insert warm; search/delete COLD) ---
def insert_end(self, data):
    new = Node()
    new.set_data(data)
    # empty => new head (is_empty / __start is None — no sentinel Node())
    if self.is_empty():
        self.__start = new
    else:
        current = self.__start
        while current.get_right() is not None:
            current = current.get_right()
        current.set_right(new)

def search(self, data):
    # linear search by traversing the chain
    current = self.__start
    # loop on current — testing get_right() skips the tail
    while current is not None and current.get_data() != data:
        current = current.get_right()
    return current  # Node if found, else None

def delete(self, data):
    if self.is_empty():
        return
    # HEAD case: no previous — move start forward (do not previous.set_right)
    if self.__start.get_data() == data:
        self.__start = self.__start.get_right()
        return

    previous = None
    current = self.__start
    while current is not None and current.get_data() != data:
        previous = current
        current = current.get_right()
    if current is None:
        return  # not found
    # bypass current
    previous.set_right(current.get_right())

# --- ADT.ipynb BST (warm-mid ~25%) ---
def insert(self, data):
    new = TreeNode(data)
    if self.__root is None:
        self.__root = new
        return

    current = self.__root
    while current:
        # insert rule: <= go left, > go right
        if data <= current.get_data():
            if current.get_left() is None:
                current.set_left(new)
                return
            current = current.get_left()
        else:
            if current.get_right() is None:
                current.set_right(new)
                return
            current = current.get_right()

def in_order(self, node):
    # takes a NODE so recursion can walk subtrees — left, visit, right
    if node is not None:
        self.in_order(node.get_left())
        print(node.get_data())
        self.in_order(node.get_right())

# --- ADT.ipynb HashTable (COLD ~50% on init) ---
class HashTable:
    def __init__(self, N):
        self.__n = N
        # N SEPARATE LinkedLists — NEVER [LinkedList()] * N (one shared object)
        self.__arr = [LinkedList() for _ in range(N)]

    def hash_function(self, key):
        return key % self.__n

    def insert(self, key):
        bucket = self.__arr[self.hash_function(key)]
        # skip duplicate keys already in this chain
        if bucket.search(key) is None:
            bucket.insert_front(key)

    def search(self, key):
        # self.__arr not bare arr; Node/None -> bool
        return self.__arr[self.hash_function(key)].search(key) is not None

# --- DB.ipynb open+seed (warm ~25%) ---
import sqlite3, csv

conn = sqlite3.connect("college.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

with open("STUDENT.csv") as file:
    reader = csv.reader(file)
    next(reader)  # skip header
    for row in reader:
        cur.execute("""
            INSERT OR IGNORE INTO Student(stu_id, name, civics_class, handphone)
            VALUES (?,?,?,?)
        """, (row[0], row[1], row[2], row[3]))
conn.commit()

# --- DB.ipynb CRUD params (COLD ~50%) ---
# CRUD pattern (parameterised — never splice user input into SQL)
# trailing comma makes a 1-tuple: (25999,) not (25999)
cur.execute("SELECT name, civics_class FROM Student WHERE stu_id = ?", (25999,))
for i in cur.fetchone():
    print(i)

cur.execute("UPDATE Student SET name = ? WHERE stu_id = ?", ("Renamed Student", 25999))
cur.execute("DELETE FROM Student WHERE stu_id = ?", (25999,))
conn.commit()

# --- DB.ipynb JOIN / HAVING (COLD-mid ~40%) ---
# INNER JOIN: only students who have at least one late record
cur.execute("""
SELECT Student.name, Late.date, Late.reason
FROM Student INNER JOIN Late ON Student.stu_id = Late.stu_id
WHERE Student.civics_class = ?
ORDER BY Late.date
""", ("25S02X",))
#fetch all records in dictionary form from selection filter
for row in cur.fetchall():
    print(row['name'], row['date'], row['reason'])

# WHERE filters rows; HAVING filters groups after COUNT
cur.execute("""
SELECT Student.civics_class, COUNT(*) AS total 
FROM Student INNER JOIN Late ON Student.stu_id = Late.stu_id
GROUP BY Student.civics_class 
HAVING COUNT(*) >= 3;
""")
for row in cur.fetchall():
    print(row['civics_class'], row['total'])

# % wildcards live in the Python tuple, not spliced into SQL
cur.execute("SELECT name FROM Student WHERE name LIKE ?", ("%Li%",))

# never-late: LEFT JOIN + right key IS NULL
cur.execute("""
SELECT Student.name
FROM Student LEFT OUTER JOIN Late ON Student.stu_id = Late.stu_id
WHERE Late.stu_id IS NULL AND Student.civics_class = ?
""", (c,))

# --- WEB DEV.ipynb flask (COLD ~50% on routes) ---
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
        # keys must match HTML name="category" / name="name" exactly
        category = request.form.get("category", "").strip()
        name = request.form.get("name", "").strip()
        if name and category:
            # MUST return redirect — constructing alone does nothing
            return redirect(url_for("results", category=category, name=name))
        error = "Please fill in all fields"
    return render_template("home.html", error=error)

@app.route("/results/<category>/<name>")
def results(category, name):
    # def name "results" must match url_for("results", ...)
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
    # template url_for('add_late') requires this exact function name
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

# exam habit: only start the server in the main program
if __name__ == "__main__":
    app.run(port=5000)

# --- POOP.ipynb (warm ~25%) ---
class Resource:
    def __init__(self, ID, title):
        self.__id = ID
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
        # parent first via super
        super().__init__(ID, title)
        self.__filesize = int(filesize)
        
    def describe(self):
        # getters for parent privates — do not touch parent __attrs
        return f"Digital Resource {self.get_id()}: {self.get_title()} ({self.__filesize} MB)"

# --- bare fragments (warm recognition; light notes) ---
(value,)
("%" + name + "%",)
conn.row_factory = sqlite3.Row
methods=["GET", "POST"]
return redirect(url_for("home"))
request.form.get("name", "").strip()
HAVING COUNT(*) >= 2
WHERE Late.stu_id IS NULL
return BinarySearch(Arr, FindValue, middle + 1, High)
while Low <= High:
    middle = (Low + High) // 2
[LinkedList() for _ in range(N)]
if Low > High:
    return -1
if self.__start.get_data() == data:
    self.__start = self.__start.get_right()
