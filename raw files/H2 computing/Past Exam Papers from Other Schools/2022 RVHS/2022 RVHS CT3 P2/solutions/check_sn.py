import random


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


# print(check_sn("SPEC123456789S"))


def gen_sn():
    for i in range(100):
        sn_digits = "SPEC"
        for i in range(9):
            rvalue = random.randint(0, 35)
            if rvalue < 10:
                sn_digits += str(rvalue)
            else:
                sn_digits += chr(rvalue-10+65)

        # print(sn_digits)
        print(sn_digits + check_sn(sn_digits))
