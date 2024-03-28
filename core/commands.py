import argparse

def create_parser():
    parser = argparse.ArgumentParser(prog="python main.py", 
                                     description="Does this site have mirror sites?")
    
    subparsers = parser.add_subparsers(dest="command", title="commands", help="Choose a command")

    parser_scrape_tags = subparsers.add_parser("scrape_tags", help="Search for mirror sites by comparing metadata.")
    parser_scrape_tags.add_argument("url", nargs="?", default="https://www.rt.com", help="Choose a source URL (https://www.example.com)")
    parser_scrape_tags.add_argument("user_agent", nargs="?", help="Provide your user-agent.")
    
    parser_compare_tags = subparsers.add_parser("compare_tags", help="Scrape the resulting sites from disinfo.id to check for mirrors to the source site.")
    parser_compare_tags.add_argument("--file", nargs="?", required=True, help="Provide a file containing the data (CSV or Excel)")
    parser_compare_tags.add_argument("--column", nargs="?", required=True, help="Specify the column name containing the URLs to the possible mirror sites")

    parser_scrape_css = subparsers.add_parser("scrape_css", help="Type the URL for the site you want to search for mirrors by comparing CSS classes.")
    parser_scrape_css.add_argument("--url", nargs="?", default="https://www.rt.com", help="Choose a source URL (https://www.example.com)")
    parser_scrape_css.add_argument("--user_agent", nargs="?", required=True, help="Provide your user-agent.")

    parser_compare_css = subparsers.add_parser("compare_css", help="Scrape the resulting sites from disinfo.id to check for mirrors to the source site.")
    parser_compare_css.add_argument("--file", nargs="?", required=True, help="Provide a file containing the data (CSV or Excel)")
    parser_compare_css.add_argument("--column", nargs="?", required=True, help="Specify the column name containing the URLs to the possible mirror sites")

    args = parser.parse_args()
    
    return args