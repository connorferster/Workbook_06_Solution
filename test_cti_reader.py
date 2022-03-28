from cti_reader import *

def test_read_cti_file():
    test_data = read_cti_file('300x900c55.cti')
    assert test_data[0] == ['#spColumn Text Input (CTI) File']
    assert test_data[17] == ['[Irregular Options]']
    

def test_convert_strings_to_numbers():
    converted_file_data = convert_strings_to_numbers(read_cti_file("300x900c55.cti"))
    assert converted_file_data[18][0] == -2 # Test negative integers got converted
    assert converted_file_data[18][7] == -1270.0 # Test negative floats got converted
    assert converted_file_data[11][0] == '[Design Run Flag]' # Test strings stayed the same
    
    
def test_file_data_to_ctifile():
    converted_file_data = convert_strings_to_numbers(read_cti_file("300x900c55.cti"))
    cti_data = file_data_to_ctifile(converted_file_data)
    test_data = [
        ["#Heading with no data"],
        ["[Section Heading]"],
        ["Data under section heading 1", 2, 3],
        ["Data under section heading 2", 3, 4],
        ["[New Section Heading]"],
        ["Single piece of data under new section heading"],
    ]
    test_cti = file_data_to_ctifile(test_data)
    assert test_cti["#Heading with no data"] is None
    assert test_cti["[Section Heading]"] == [["Data under section heading 1", 2, 3], ["Data under section heading 2", 3, 4]]
    assert test_cti["[New Section Heading]"] == [["Single piece of data under new section heading"]]
    assert cti_data["[Factored Loads]"] == [
        [6],
        [5600.0, 0.0, 0.0],
        [5600.0, 0.0, -0.0],
        [5000.0, 0.0, 0.0],
        [5000.0, 0.0, -0.0],
        [5000.0, 0.0, 0.0],
        [5000.0, 0.0, -0.0],
    ]
    

def test_update_factored_loads():
    new_loads = [[1000, 200, 300], [2000, 400, 600]]
    test_data = {
        "# First line": None,
        "[User Options]": [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]],
        "[Factored Loads]": [[1], [0, 1, 2]]
    }
    updated_test_data = update_factored_loads(new_loads, test_data)
    assert updated_test_data["[Factored Loads]"] == [[2], new_loads[0], new_loads[1]]
    assert updated_test_data["[User Options]"] == [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 2, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]]
    

def test_save_cti_file():
    test_cti = {
        "#First Row": None,
        "[Second Section]": [["Some data"]],
        "[Third Section]": [[1, 2, 3], [4, 5, 6]],
        "[Fourth Section]": [["Some more data"], ["With another line"]],
    }
    save_cti_file("new_test_file.cti", test_cti)
    acc = []
    with open("new_test_file.cti", 'r') as file:
        for line in file.readlines():
            acc.append(line)
    assert acc[0] == "#First Row\n"
    assert acc[1] == "[Second Section]\n"
    assert acc[2] == "Some data\n"
    assert acc[3] == "[Third Section]\n"
    assert acc[4] == "1,2,3\n"
    assert acc[5] == "4,5,6\n"
    assert acc[6] == "[Fourth Section]\n"
    assert acc[7] == "Some more data\n"
    assert acc[8] == "With another line\n"