from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

curr_dir = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(curr_dir, "spectrum.db")


@app.route('/')
def index():
    return render_template('index.html')


def check_sn(serial_no):
    sn_digits = serial_no[4:13]
    # print(sn_digits)
    convert_table = {
        "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9,
        "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "O": 6, "P": 7, "Q": 8, "R": 9,
        "S": 2, "T": 3, "U": 4, "V": 5, "W": 6, "X": 7, "Y": 8, "Z": 9
    }
    weight = [8, 7, 6, 5, 4, 3, 2, 9, 4]
    total = 0

    for i in range(len(sn_digits)):
        if sn_digits[i].isdigit():
            # print(vin[i])
            total += int(sn_digits[i]) * weight[i]
        else:
            # print(vin[i], convert_table[vin[i]], weight[i])
            total += convert_table[sn_digits[i]] * weight[i]

    check_digit = total % 11
    # print(total, check_digit)

    check_table = {0: "S", 1: "P", 2: "E", 3: "C",
                   4: "T", 5: "R", 6: "U", 7: "M",
                   8: "X", 9: "Y", 10: "Z"}

    check_digit = check_table[check_digit]

    # print(check_digit, serial_no[-1], serial_no[-1] == check_digit)

    return check_digit == serial_no[-1]


def validation(serial_no):
    if serial_no == "":
        return "Presence check failed. Please enter the serial no. of the product."
    elif len(serial_no) != 14:
        return "Length check failed. Please make sure the serial no. has 14 characters."
    elif serial_no[:4] != "SPEC":
        return "Format check failed. Please make sure the serial no. starts with \"SPEC\"."
    else:
        for c in serial_no:
            if not (c.isalpha() or c.isdigit()):
                return "Format check failed. Please make sure the serial no. contains only alphanumeric values."
        if not check_sn(serial_no):
            return "Check digit failed. Please make sure the serial no. is valid."
        else:
            return "Pass"


@app.route("/warranty/", methods=["GET", "POST"])
def warranty():
    if request.method == "GET":
        return render_template('warranty.html')
    else:
        serial_no = request.form["serial_no"]
        validation_result = validation(serial_no)

        # if validation result is not "pass"
        # render warranty page for re-submition
        if validation_result != "Pass":
            return render_template(
                "warranty.html",
                error_msg=validation_result)

        # if "pass", query database to get sales record
        db = sqlite3.connect(db_file)
        query = """
SELECT ProductInfo.SerialNo, MonitorInfo.ModelNo, 
ScreenSize, Resolution, OrderDate, Email
FROM MonitorInfo, ProductInfo, SalesRecord
WHERE MonitorInfo.ModelNo = ProductInfo.ModelNo
AND ProductInfo.SerialNo = SalesRecord.SerialNo
AND ProductInfo.SerialNo = ?
        """
        cursor = db.execute(query, (serial_no,))
        record = cursor.fetchone()

        cursor.close()
        db.close()

        return render_template(
            "ack.html",
            record=record)


if __name__ == '__main__':
    app.run(debug=True)
