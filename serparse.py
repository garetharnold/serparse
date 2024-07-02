import json
import pandas as pd
import argparse
import re
import os
from datetime import datetime
from urllib.parse import urlparse

ASCII_ART = """
  __|  __|  _ \  _ \    \    _ \   __|  __| 
\__ \  _|     /  __/   _ \     / \__ \  _|  
____/ ___| _|_\ _|   _/  _\ _|_\ ____/ ___| 
                                            
"""

def print_help():
    print(ASCII_ART)
    print("Usage: serparse.py -i <inputfile1> <inputfile2> ... [-o <outputformat>]")
    print()
    print("Options:")
    print("  -i, --input       Input JSON file(s)")
    print("  -o, --output      Output file format: csv, urls, or json (default: json)")
    print()
    print("Please ensure the tlds.json and blacklist.json files are available in the same directory.")
    print("Examples of these files can be found in the README.")
    print()

    

def load_and_process_files(input_files, tld_block_list, domain_block_list):
    combined_data = []
    seen_domains = set()
    log_entries = []

    for file_path in input_files:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if isinstance(data, list):
                data = data[0]
            if isinstance(data, dict) and 'organic' in data:
                entries = data['organic']
            else:
                log_entries.append(f"Unexpected JSON structure in {file_path}")
                continue

            for entry in entries:
                title = entry.get('title', '')
                link = entry.get('link', '')
                snippet = entry.get('snippet', '')
                domain = urlparse(link).netloc

                if (not tld_block_list or not any(domain.endswith(tld) for tld in tld_block_list)) and \
                   (not domain_block_list or not any(blocked in link for blocked in domain_block_list)):
                    if domain not in seen_domains:
                        combined_data.append({
                            'title': title,
                            'link': link,
                            'snippet': snippet,
                            'domain': domain
                        })
                        seen_domains.add(domain)
                    else:
                        log_entries.append(f"Duplicate domain removed: {domain}")
                else:
                    log_entries.append(f"Blocked domain or TLD removed: {link}")

    return combined_data, log_entries

def save_to_csv(processed_data, output_file):
    df = pd.DataFrame(processed_data)
    df.to_csv(output_file, index=False)

def save_to_urls_csv(processed_data, output_file):
    urls = [entry['domain'] for entry in processed_data]
    df = pd.DataFrame(urls, columns=['urls'])
    df.to_csv(output_file, index=False)

def save_log(log_entries, log_file):
    with open(log_file, 'w') as file:
        file.write("\n".join(log_entries))

def main():
    parser = argparse.ArgumentParser(description='Process JSON files and output to CSV')
    parser.add_argument('-i', '--input', nargs='+', help='Input JSON file(s)')
    parser.add_argument('-o', '--output', help='Output file format: csv, urls, or json (default: json)')
    args = parser.parse_args()

    if not args.input:
        print_help()
        return

    tld_block_list = []
    domain_block_list = []

    tld_block_list_file = 'tlds.json'
    domain_block_list_file = 'blacklist.json'

    if os.path.isfile(tld_block_list_file):
        with open(tld_block_list_file, 'r') as file:
            tlds_data = json.load(file)
        tld_block_list = [entry['tld'] for entry in tlds_data['blocked_tlds']]

    if os.path.isfile(domain_block_list_file):
        with open(domain_block_list_file, 'r') as file:
            domains_data = json.load(file)
        domain_block_list = domains_data['blocked_domains']

    processed_data, log_entries = load_and_process_files(args.input, tld_block_list, domain_block_list)
    
    current_time = datetime.now().strftime("%H-%M-%d-%m-%Y")
    output_file_base = f"serparse-{current_time}"
    log_file = f"{output_file_base}.log"
    
    if args.output == 'csv':
        output_file = f"{output_file_base}.csv"
        save_to_csv(processed_data, output_file)
    elif args.output == 'urls':
        output_file = f"{output_file_base}-urls.csv"
        save_to_urls_csv(processed_data, output_file)
    else:
        output_file = f"{output_file_base}.json"
        with open(output_file, 'w') as file:
            json.dump(processed_data, file, indent=4)

    save_log(log_entries, log_file)
    print(f'Data successfully saved to {output_file}')
    print(f'Log saved to {log_file}')

if __name__ == "__main__":
    main()