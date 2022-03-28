from __future__ import annotations
import copy
import csv
from dataclasses import dataclass
from typing import Optional
import ipytest
ipytest.autoconfig()


CTIFile: dict

# Interp. A data type to represent the data in an spColumn .cti file
# Keys are strings representing the headings within the file
# Values is a list of lists of data representing the data that comes under that heading.
#    Values consisting of a blank line (empty data in the file format) are represented by an empty list of list
#    Headings in the file that do not have data below them (e.g. the first line of the file) have values of None
#    to represent that there is no line of data after the heading.

# Examples
CTI_00 = {} # An empty file
CTI_01 = {
    "#spColumn Text Input (CTI) File": None, # This is the first line in the file
    "[spColumn Version]": [[7.0]],
    "[Project]": [["RJC Design Table"]],
    "[Column ID]": [["300x900A"]],
    ...: ... # There are many lines of data in the CTI file format
}


def read_cti_file(filename: str) -> list[list]:
    """
    Reads the data in 'filename', an spColumn .cti file.
    """
    acc = []
    with open(filename, 'r') as file:
        reader = csv.reader(file, )
        for line in reader:
            acc.append(line)
    return acc


def convert_strings_to_numbers(file_data: list) -> list:
    """
    Returns the data in 'file_data' but with the any numerical strings converted into strings.
    """
    acc = []
    for item in file_data:
        if isinstance(item, list):
            acc.append(convert_strings_to_numbers(item))
        elif "." not in item and item.replace("-","").isnumeric():
            acc.append(int(item))
        elif "." in item and item.replace("-","").replace(".","").isnumeric():
            acc.append(float(item))
        else:
            acc.append(item)
    return acc


def file_data_to_ctifile(file_data: list) -> CTIFile:
    """
    Returns a CTIFile dictionary from the data in 'file_data'
    """
    cti_file = {}
    current_section = ""
    for line in file_data:
        first_item = line[0]
        if isinstance(first_item, str) and "#" in first_item:
            cti_file.update({first_item: None})
        elif isinstance(first_item, str) and "[" in first_item:
            current_section = first_item
            cti_file.update({current_section: []})
        else:
            cti_file[current_section].append(line)
    return cti_file


def update_factored_loads(factored_loads: list[list[float]], cti_file: CTIFile) -> CTIFile:
    """
    Returns 'cti_file' with its factored loads data replaced with the information in 'factored_loads'.
    """
    new_cti_file = copy.deepcopy(cti_file)
    new_factored_loads = copy.deepcopy(factored_loads)
    num_loads = len(factored_loads)
    new_cti_file['[Factored Loads]'] = new_factored_loads
    new_cti_file['[Factored Loads]'].insert(0, [num_loads])
    new_cti_file['[User Options]'][0][17] = num_loads
    return new_cti_file


def save_cti_file(new_filename: str, cti_file: CTIFile) -> None:
    """
    Returns None. Writes the data in 'cti_file' to a new file with 'new_filename'.
    """
    with open(new_filename, 'w', newline='') as new_file:
        cti_writer = csv.writer(new_file)
        for section_heading, section_data in cti_file.items():
            cti_writer.writerow([section_heading])
            if section_data is not None:
                for line in section_data:
                    cti_writer.writerow(line)