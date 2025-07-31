from functions.write_file import write_file


def test():

    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")

    print("Result for 'pkg' directory:")
    print(result)

    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print("Result for '/bin' directory:")
    print(result)

    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print("Result for '../' directory:")
    print(result)


if __name__ == "__main__":
    test()
