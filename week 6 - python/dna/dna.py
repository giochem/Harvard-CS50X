import csv
import sys


def main():
    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # TODO: Read database file into a variable
    data = []
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for d in reader:
            data.append(d)

    # TODO: Read DNA sequence file into a variable
    sequences = ""
    with open(sys.argv[2]) as file:
        sequences = file.readline()

    # TODO: Find longest match of each STR in DNA sequence
    col = list(data[0].keys())
    longest_strs = []
    for i in range(1, len(col)):
        longest_str = longest_match(sequences, col[i])
        longest_strs.append(longest_str)

    # TODO: Check database for matching profiles
    res = "No match"
    for d in data:
        match = True
        for i in range(len(longest_strs)):
            if str(longest_strs[i]) != d[str(col[i + 1])]:
                match = False
                break
        if match == True:
            res = d["name"]
            break

    print(res)


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):
        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:
            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
