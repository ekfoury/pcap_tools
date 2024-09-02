import csv
import sys

# Function to convert human-readable sizes to bytes
def size_to_bytes(size_str):
    if "kB" in size_str:
        return int(float(size_str.replace(" kB", "").replace(",", "")) * 1000)
    elif "MB" in size_str:
        return int(float(size_str.replace(" MB", "").replace(",", "")) * 1000000)
    elif "bytes" in size_str:
        return int(float(size_str.replace(" bytes", "").replace(",", "")))
    else:
        return int(size_str.replace(",", ""))

# Process the CSV file
def process_csv(input_file, output_file):
    with open(input_file, mode='r') as infile, open(output_file, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)

        # Write header
        writer.writerow(['src_ip', 'src_port', 'dst_ip', 'dst_port', 'num_frames', 'num_bytes', 'relative_start', 'duration'])

        for line in infile:
            # Split the line based on the fixed structure
            parts = line.split()

            
            # print(parts[0])
            # Extract the fields
            src_ip, src_port = parts[0].split(':')
            dst_ip, dst_port = parts[2].split(':')
            num_src_frames = parts[3]
            # print(num_src_frames)
            num_src_bytes = size_to_bytes(parts[4] + ' ' + parts[5])
            # print(num_src_bytes)
            num_dst_frames = parts[6]
            # print(num_dst_frames)
            num_dst_bytes = size_to_bytes(parts[7] + ' ' + parts[8])
            # print(num_dst_bytes)
            relative_start = parts[12]
            duration = parts[13]

            # Write the first direction
            if(int(num_src_frames) != 0):
                writer.writerow([dst_ip, dst_port, src_ip, src_port, num_src_frames, num_src_bytes, relative_start, duration])

            # Write the reverse direction
            if(int(num_dst_frames) != 0):
                writer.writerow([src_ip, src_port, dst_ip, dst_port, num_dst_frames, num_dst_bytes, relative_start, duration])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    process_csv(input_file, output_file)
