import sys

def calculate_marks(mark1, mark2, mark3):
    total = mark1 + mark2 + mark3
    average = total / 3
    return total, average


if __name__ == "__main__":

    mark1 = int(sys.argv[1])
    mark2 = int(sys.argv[2])
    mark3 = int(sys.argv[3])

    total, average = calculate_marks(mark1, mark2, mark3)

    print("=============================")
    print("STUDENT MARKS REPORT")
    print("=============================")
    print(f"Subject 1 : {mark1}")
    print(f"Subject 2 : {mark2}")
    print(f"Subject 3 : {mark3}")
    print(f"Total     : {total}")
    print(f"Average   : {average:.2f}")
    print("=============================")
