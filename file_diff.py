"""
Project for Week 4 of "Python Data Representations".
Find differences in file contents.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

IDENTICAL = -1


def singleline_diff(line1, line2):
    if line1 == line2:
        return IDENTICAL
    shorter_line = min(len(line1), len(line2))

    for num in range(shorter_line):
        if line1[num] != line2[num]:
            return num
    return shorter_line


def singleline_diff_format(line1, line2, idx):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
      idx   - index at which to indicate difference
    Output:
      Returns a three line formatted string showing the location
      of the first difference between line1 and line2.

      If either input line contains a newline or carriage return,
      then returns an empty string.

      If idx is not a valid index, then returns an empty string.
    """

    if "\n" in line1 or "\r" in line1 or "\n" in line2 or "\r" in line2:
        return ""
    if idx < 0 or idx > min(len(line1), len(line2)):
        return ""
    return line1+"\n"+ "="*idx+"^"+"\n"+line2+"\n"



def multiline_diff(lines1, lines2):
    """
    Inputs:
      lines1 - list of single line strings
      lines2 - list of single line strings
    Output:
      Returns a tuple containing the line number (starting from 0) and
      the index in that line where the first difference between lines1
      and lines2 occurs.

      Returns (IDENTICAL, IDENTICAL) if the two lists are the same.
    """
    if lines1 == lines2 :
        return (IDENTICAL, IDENTICAL)
    shorterlist = lines1 if len(lines2) > len(lines1) else  lines2


    if len(lines1) == len(lines2):
        for line in range(len(lines1)):
            if singleline_diff(lines1[line], lines2[line]) != -1:
                return (line, singleline_diff(lines1[line], lines2[line]))
    elif len(lines1) == 0  or len(lines2) ==0 :
        return (0,0)
    else:
        for idx in range(len(shorterlist)):
            if lines1[idx] != lines2[idx]:
                return (idx, singleline_diff(lines1[idx],lines2[idx]))
            if(idx == len(shorterlist)-1):
                return (len(shorterlist),0)

def get_file_lines(filename):
    """
    Inputs:
      filename - name of file to read
    Output:
      Returns a list of lines from the file named filename.  Each
      line will be a single line string with no newline ('\n') or
      return ('\r') characters.

      If the file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    file = open(filename,"rt")
    list_line=[]
    for line in file :
        line=line.strip()
        if line != "\n" and line!=  "\r":
            list_line.append(line)
    file.close()
    return list_line


def file_diff_format(filename1, filename2):
    """
    Inputs:
      filename1 - name of first file
      filename2 - name of second file
    Output:
      Returns a four line string showing the location of the first
      difference between the two files named by the inputs.

      If the files are identical, the function instead returns the
      string "No differences\n".

      If either file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    lines1 = get_file_lines(filename1)


    lines2 = get_file_lines(filename2)

    multiplelinediff = multiline_diff(lines1,lines2)

    if multiplelinediff[0] == -1 :
        diffrenceval ="No differences\n"
    else :
        diffrenceval = "Line " + str(multiplelinediff[0]) + ":\n"
        singlelineformt = singleline_diff_format(lines1[multiplelinediff[0]], lines2[multiplelinediff[0]],multiplelinediff[1])
        diffrenceval += singlelineformt

    return diffrenceval


