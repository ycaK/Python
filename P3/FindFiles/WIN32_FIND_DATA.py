"""
Simple class for processing a tuple representing a WIN32_FIND_DATA structure
Author: Kacy538 (ycaK)
"""


class Resolve(object):
    def __init__(self, WIN32_FIND_DATA):
        self.WIN32_FIND_DATA = WIN32_FIND_DATA
        if not WIN32_FIND_DATA:
            print("File not found!")
        else:
            try:
                self.create_time = WIN32_FIND_DATA[0][1]
                self.access_time = WIN32_FIND_DATA[0][2]
                self.write_time = WIN32_FIND_DATA[0][3]
                self.n_file_size_high = WIN32_FIND_DATA[0][4]
                self.n_file_size_low = WIN32_FIND_DATA[0][5]
                self.reserved_zero = WIN32_FIND_DATA[0][6]
                self.reserved_one = WIN32_FIND_DATA[0][7]
                self.file_name = WIN32_FIND_DATA[0][8]
                self.alternate_file_name = WIN32_FIND_DATA[0][9]
                if not self.alternate_file_name:
                    self.alternate_file_name = "None"
            except:
                print("Error while processing data!")

    def display_all(self):
        if not self.WIN32_FIND_DATA:
            print("Data not found!")
        else:
            try:
                print("----------------------------------")
                print("File creation time:", self.create_time)
                print("File access time:", self.access_time)
                print("Time of last file write:", self.write_time)
                print("High order DWORD of file size:", self.n_file_size_high)
                print("Low order DWORD of file size:", self.n_file_size_low)
                print("Contains reparse tag if path is a reparse point:", self.reserved_zero)
                print("Reserved:", self.reserved_one)
                print("The name of the file:", self.file_name)
                print("Alternative name of the file, expressed in 8.3 format:", self.alternate_file_name)
                print("----------------------------------")
            except:
                print("Error while displaying processed data!")

    def ret_create_time(self):
        try:
            return self.create_time
        except:
            return None

    def ret_access_time(self):
        try:
            return self.access_time
        except:
            return None

    def ret_write_time(self):
        try:
            return self.write_time
        except:
            return None

    def ret_n_file_size_high(self):
        try:
            return self.n_file_size_high
        except:
            return None

    def ret_n_file_size_low(self):
        try:
            return self.n_file_size_low
        except:
            return None

    def ret_reserved_zero(self):
        try:
            return self.reserved_zero
        except:
            return None

    def ret_reserved_one(self):
        try:
            return self.reserved_one
        except:
            return None

    def ret_file_name(self):
        try:
            return self.file_name
        except:
            return None

    def ret_alternate_file_name(self):
        try:
            return self.alternate_file_name
        except:
            return None
