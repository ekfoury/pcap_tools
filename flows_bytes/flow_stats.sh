#!/bin/bash

# Validate input arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <pcap_file> <report_file>"
    exit 1
fi

input_file="$1"
output_file=out
final_output_file="$2"

# Validate if input_file exists
if [ ! -f "$input_file" ]; then
    echo "Error: Input file '$input_file' does not exist."
    exit 1
fi

# Run tshark to analyze the input file, filter for IP and TCP traffic,
# and write TCP conversation statistics to output_file
tshark -r "$input_file" -Y "ip and tcp" -z conv,tcp -q > "$output_file"

# Remove lines containing IPv6 addresses from output_file
grep -v -E "([a-fA-F0-9]{1,4}:){2,7}[a-fA-F0-9]{1,4}(:[0-9]+)?" "$output_file" > temp_file && mv temp_file "$output_file"

# Remove the first 5 lines from output_file
tail -n +6 "$output_file" > temp_file && mv temp_file "$output_file"

# Remove the last line from output_file
head -n -1 "$output_file" > temp_file && mv temp_file "$output_file"

# Process the cleaned output_file using the Python script
python3 processor.py "$output_file" "$final_output_file"
rm $output_file
