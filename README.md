# Exploring Russian State Media Content Laundering

Recent research (Koronska et al., 2024) shows that networks of websites, which serve as pathways for Russian state and pro-Kremlin media, are able to operate in EU member countries despite clear restrictions in place.

This is mostly achieved through networks of mirror websites that by posing as ‘independent’ and / or ‘alternative’ news outlets are able to distribute by stealth Russian state media content. They operate either under new domain names or domain names that are related to the banned outlets. One such example is sputnikglobe.com - a mirror site of Sputnik News that is up and running in countries like the UK and the Netherlands.

### Disinfo.id software
Using a newly developed software, which has been developed to study contenet laudering, it's possible to collect content copies and networks of mirror websites automatically. This program is used best alongside this software to sift out specifically mirror websites from the dataset resulting from running a URL through disinfo.id.

## Manual
Run a URL through disinfo.id and save the resulting data containing the matching websites as either a CSV or Excel file. Be sure to save the file in this folder. You will then be able to use this data to compare metadata or CSS classes with the source website. 

When analyzing metadata, the program will scrape the Verification IDs from the source website and compare them with URLs within the provided dataset. The Verification ID is a unique identifier used for verifying ownership of authenticity of a website or online account. They can establish the legitimacy of a site or account, potentially linking it to a specific owner or organization.

Not all websites contain Verification IDs. If this is the case, another option is to look for similarities in CSS classes within the code used to design the websites. If 90% of the CSS classes are shared between websites, it's a match.

### Commands
1. **Scrape metadata from the source website** $ python main.py scrape_tags
> _Program will ask for a source url and User-Agent as input. Returns the Verification IDs from the source website if available._

2. **Compare metadata from the source to other sites**: $ python main.py compare_tags
> _Program will ask for a dataset and column containing URLs as input. Returns a list of mirror websites, if Verification IDs from the source are available._

3. **Scrape CSS classes from the source website**: $ python main.py scrape_css
> _Program will ask for a source url and User-Agent as input. Returns the unique CSS classes from the source website._

4. **Compare CSS classes from the source to other sites:** $ python main.py compare_css
> _Program will ask for a dataset and column containing URLs as input. Returns a list of mirror websites based on similar CSS classes._