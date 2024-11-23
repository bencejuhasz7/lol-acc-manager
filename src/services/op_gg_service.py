import requests
from bs4 import BeautifulSoup
from lxml import html

class OpGGService:
    """Service for handling op.gg related operations."""
    
    BASE_URL = "https://www.op.gg/summoners/{server}/{name}"
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def _format_account_name(self, name):
        """Format account name for URL (replace # with -)."""
        return name.replace("#", "-")
    
    def _format_server_name(self, server):
        """Format server name for URL (lowercase)."""
        return server.lower()
    
    def get_all_account_urls(self):
        """Get all account URLs that will be requested."""
        urls = []
        
        for server in self.data_manager.accounts_data:
            if server != "servers":
                formatted_server = self._format_server_name(server)
                
                for account in self.data_manager.accounts_data[server]:
                    formatted_name = self._format_account_name(account["name"])
                    url = self.BASE_URL.format(
                        server=formatted_server,
                        name=formatted_name
                    )
                    urls.append({
                        "account_name": account["name"],
                        "server": server,
                        "url": url
                    })
        
        return urls
    
    def get_rank_info(self, url, account_data):
        """Get rank information from op.gg URL and update account data."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Initialize ranks with "Unranked"
            account_data["ranks"] = {
                "solo": {"rank": "Unranked", "lp": ""},
                "flex": {"rank": "Unranked", "lp": ""}
            }
            self.data_manager.save_accounts()  # Save initial Unranked state
            
            # Find Solo/Duo ranked section
            solo_section = soup.find("div", {"class": "css-1wk31w7 egd6cgn0"})
            if solo_section:
                content_div = solo_section.find("div", {"class": "content"})
                if content_div:
                    info_div = content_div.find("div", {"class": "info"})
                    if info_div:
                        tier_div = info_div.find("div", {"class": "tier"})
                        lp_div = info_div.find("div", {"class": "lp"})
                        
                        if tier_div and lp_div:
                            account_data["ranks"]["solo"]["rank"] = tier_div.text.strip()
                            account_data["ranks"]["solo"]["lp"] = lp_div.text.strip()
                            self.data_manager.save_accounts()
            
            # Find Flex ranked section
            flex_section = soup.find("div", {"class": "css-1muxmfk egd6cgn0"})
            if flex_section:
                content_div = flex_section.find("div", {"class": "content"})
                if content_div:
                    info_div = content_div.find("div", {"class": "info"})
                    if info_div:
                        tier_div = info_div.find("div", {"class": "tier"})
                        lp_div = info_div.find("div", {"class": "lp"})
                        
                        if tier_div and lp_div:
                            account_data["ranks"]["flex"]["rank"] = tier_div.text.strip()
                            account_data["ranks"]["flex"]["lp"] = lp_div.text.strip()
                            self.data_manager.save_accounts()
            
            return True
            
        except Exception as e:
            print(f"Error fetching rank info: {str(e)}")
            # Initialize with "Unranked" on error
            account_data["ranks"] = {
                "solo": {"rank": "Unranked", "lp": ""},
                "flex": {"rank": "Unranked", "lp": ""}
            }
            self.data_manager.save_accounts()
            return False
    
    def update_all_ranks(self, loading_dialog=None):
        """Update ranks for all accounts."""
        urls = self.get_all_account_urls()
        
        for item in urls:
            # Find the account in the data structure
            account_data = next(
                acc for acc in self.data_manager.accounts_data[item["server"]]
                if acc["name"] == item["account_name"]
            )
            
            # Initialize ranks if not present with "No data"
            if "ranks" not in account_data:
                account_data["ranks"] = {
                    "solo": {"rank": "No data", "lp": ""},
                    "flex": {"rank": "No data", "lp": ""}
                }
                # Save the initialization
                self.data_manager.save_accounts()
            
            # Update ranks
            self.get_rank_info(item["url"], account_data)
            
            # Update loading dialog if provided
            if loading_dialog:
                loading_dialog.update_progress(item["account_name"])
    
    def print_urls(self):
        """Print all URLs that will be requested."""
        urls = self.get_all_account_urls()
        print("\nFetching ranks for all accounts:")
        print("-" * 50)
        for item in urls:
            print(f"Account: {item['account_name']}")
            print(f"Server: {item['server']}")
            print(f"URL: {item['url']}")
            
            # Find the account data
            account_data = next(
                acc for acc in self.data_manager.accounts_data[item["server"]]
                if acc["name"] == item["account_name"]
            )
            
            # Get and print rank info
            success = self.get_rank_info(item['url'], account_data)
            if success:
                print("\nRank Information:")
                print(f"Solo/Duo: {account_data['ranks']['solo']['rank']} {account_data['ranks']['solo']['lp']}")
                print(f"Flex: {account_data['ranks']['flex']['rank']} {account_data['ranks']['flex']['lp']}")
            print("-" * 50) 