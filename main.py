from core.commands import create_parser
from utils.file import read_file, convert_file
from scraping.metadata_analysis import scrape_tags, compare_tags
from scraping.css_analysis import scrape_css, compare_css

from urllib.parse import urlparse


def main():
    args = create_parser()

    source_url = input("Type the URL for the site you want to search for mirrors by comparing metadata: ")
    user_agent = input("Provide your User-Agent: ")

    if args.command == "scrape_tags":
        source_tags = scrape_tags(source_url, user_agent)
        if source_tags:
            print(source_tags)
        else:
            print(f"No Verification ID tags found for {args.url}. Re-check if it's a valid URL or try CSS analysis instead.")
    
    if args.command == "compare_tags":
        file_name = input("Provide a file containing the data (CSV or Excel): ")
        df = read_file(file_name)
        
        column_name = input("Specify the column name containing the URLs to the possible mirror sites: ")
        target_urls = convert_file(df, column_name)
        
        mirrors = compare_tags(source_url, target_urls, user_agent)
        print(mirrors)
    
    if args.command == "scrape_css":
        source_css = scrape_css(source_url, user_agent)
        print(source_css)
    
    if args.command == "compare_css":
        file_name = input("Provide a file containing the data (CSV or Excel): ")
        df = read_file(file_name)
        
        column_name = input("Specify the column name containing the URLs to the possible mirror sites: ")
        target_urls = convert_file(df, column_name)

        mirrors = compare_css(source_url, target_urls, user_agent)
        print(mirrors)


if __name__ == "__main__":
    main()