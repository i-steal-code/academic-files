import sqlite3, csv

conn = sqlite3.connect("database.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("""
DROP TABLE IF EXISTS student
""")
cur.execute("""
DROP TABLE IF EXISTS late
""")

with open('STUDENT.csv') as file:
    reader = csv.reader(file)
    #easy access of fields
    f = next(reader)
    cur.execute(f"""
CREATE TABLE IF NOT EXISTS student (
{f[0]} INTEGER PRIMARY KEY,
{f[1]} TEXT,
{f[2]} TEXT,
{f[3]} INTEGER
)
""")
    for row in reader:
        cur.execute(f"""
INSERT OR IGNORE INTO student
({f[0]},{f[1]},{f[2]},{f[3]})
VALUES
(?,?,?,?)
""",
(row[0], row[1], row[2], row[3]))

with open('LATE.csv') as file:
    reader = csv.reader(file)
    h = next(reader)
    cur.execute(f"""
CREATE TABLE IF NOT EXISTS late(
{h[0]} TEXT,
{h[1]} INTEGER PRIMARY KEY,
{h[2]} TEXT
)
""")
    for row in reader:
        cur.execute(f"""
INSERT OR IGNORE INTO late
({h[0]},{h[1]},{h[2]})
values
(?,?,?)
""",
(row[0],row[1],row[2]))

conn.commit()
print("successfully created table and seeded data\ncommencing data retrieval")
search_query = input("enter a class to search for students who were late from that class: \n")
cur.execute(f"""
SELECT student.{f[1]}, student.{f[2]}, late.{h[0]}, late.{h[2]}
FROM student INNER JOIN late ON student.{f[0]} = late.{h[1]}
WHERE student.{f[2]} = ?
""",
(search_query, ))
result = cur.fetchall()
print(f"here is a list of students from {search_query}")
for row in result:
    print(row[f[1]])
conn.close()
