"""
Web3.LOC Mobile App Example
Using Kivy for cross-platform mobile development
Same functionality as the web version
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import asyncio
import threading
from github_storage_python import GitHubStorage


class ContractCard(BoxLayout):
    """Widget for displaying contract information"""
    
    def __init__(self, contract_data, storage, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = '150dp'
        self.spacing = '5dp'
        
        self.contract = contract_data
        self.storage = storage
        
        # Contract info
        name = contract_data.get('name', 'Unknown')
        address = contract_data.get('address', '')[:20] + '...'
        chain = contract_data.get('chain', '').title()
        
        self.add_widget(Label(
            text=f"[b]{name}[/b]", 
            markup=True,
            size_hint_y=None,
            height='30dp'
        ))
        
        self.add_widget(Label(
            text=f"Address: {address}",
            size_hint_y=None,
            height='25dp'
        ))
        
        self.add_widget(Label(
            text=f"Chain: {chain}",
            size_hint_y=None,
            height='25dp'
        ))
        
        # Export buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')
        
        sol_btn = Button(text='Download .sol', size_hint_x=0.33)
        sol_btn.bind(on_press=self.download_sol)
        button_layout.add_widget(sol_btn)
        
        readme_btn = Button(text='Download README', size_hint_x=0.33)
        readme_btn.bind(on_press=self.download_readme)
        button_layout.add_widget(readme_btn)
        
        info_btn = Button(text='View Info', size_hint_x=0.33)
        info_btn.bind(on_press=self.show_info)
        button_layout.add_widget(info_btn)
        
        self.add_widget(button_layout)
    
    def download_sol(self, instance):
        """Download contract as .sol file"""
        def run_download():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                contract_id = self.contract['address']
                chain = self.contract['chain']
                
                sol_content = loop.run_until_complete(
                    self.storage.export_contract_sol(contract_id, chain)
                )
                
                filename = f"{self.contract.get('name', 'contract')}_{contract_id[:8]}.sol"
                self.storage.save_file(sol_content, filename, './downloads/')
                
                Clock.schedule_once(lambda dt: self.show_popup(f"Downloaded: {filename}"), 0)
                
            except Exception as e:
                Clock.schedule_once(lambda dt: self.show_popup(f"Error: {str(e)}"), 0)
        
        threading.Thread(target=run_download).start()
    
    def download_readme(self, instance):
        """Download contract as README file"""
        def run_download():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                contract_id = self.contract['address']
                chain = self.contract['chain']
                
                readme_content = loop.run_until_complete(
                    self.storage.export_contract_readme(contract_id, chain)
                )
                
                filename = f"{self.contract.get('name', 'contract')}_{contract_id[:8]}_README.md"
                self.storage.save_file(readme_content, filename, './downloads/')
                
                Clock.schedule_once(lambda dt: self.show_popup(f"Downloaded: {filename}"), 0)
                
            except Exception as e:
                Clock.schedule_once(lambda dt: self.show_popup(f"Error: {str(e)}"), 0)
        
        threading.Thread(target=run_download).start()
    
    def show_info(self, instance):
        """Show contract information popup"""
        info_text = f"""
Name: {self.contract.get('name', 'Unknown')}
Address: {self.contract.get('address', 'Unknown')}
Chain: {self.contract.get('chain', 'Unknown').title()}
Type: {self.contract.get('type', 'Unknown')}
Verified: {'Yes' if self.contract.get('verified') else 'No'}
Compiler: {self.contract.get('compiler_version', 'Unknown')}
        """
        
        self.show_popup(info_text, title="Contract Information")
    
    def show_popup(self, message, title="Info"):
        """Show popup message"""
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.6)
        )
        popup.open()


class Web3LOCMobileApp(BoxLayout):
    """Main mobile app interface"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = '10dp'
        self.padding = '10dp'
        
        self.storage = GitHubStorage()
        self.contracts = []
        
        self.build_interface()
    
    def build_interface(self):
        """Build the mobile interface"""
        
        # Title
        title = Label(
            text='[size=24][b]Web3.LOC Mobile[/b][/size]',
            markup=True,
            size_hint_y=None,
            height='50dp'
        )
        self.add_widget(title)
        
        # Search section
        search_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        
        self.search_input = TextInput(
            hint_text='Search contracts...',
            multiline=False,
            size_hint_x=0.6
        )
        search_layout.add_widget(self.search_input)
        
        self.chain_spinner = Spinner(
            text='All Chains',
            values=['All Chains', 'Ethereum', 'Base'],
            size_hint_x=0.2
        )
        search_layout.add_widget(self.chain_spinner)
        
        search_btn = Button(text='Search', size_hint_x=0.2)
        search_btn.bind(on_press=self.search_contracts)
        search_layout.add_widget(search_btn)
        
        self.add_widget(search_layout)
        
        # Export section
        export_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')
        
        csv_btn = Button(text='Export CSV')
        csv_btn.bind(on_press=self.export_csv)
        export_layout.add_widget(csv_btn)
        
        stats_btn = Button(text='View Stats')
        stats_btn.bind(on_press=self.show_stats)
        export_layout.add_widget(stats_btn)
        
        refresh_btn = Button(text='Refresh')
        refresh_btn.bind(on_press=self.refresh_data)
        export_layout.add_widget(refresh_btn)
        
        self.add_widget(export_layout)
        
        # Status label
        self.status_label = Label(
            text='Ready to search contracts',
            size_hint_y=None,
            height='30dp'
        )
        self.add_widget(self.status_label)
        
        # Contracts list
        self.scroll = ScrollView()
        self.contracts_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.contracts_layout.bind(minimum_height=self.contracts_layout.setter('height'))
        
        self.scroll.add_widget(self.contracts_layout)
        self.add_widget(self.scroll)
        
        # Load initial data
        Clock.schedule_once(lambda dt: self.refresh_data(None), 1)
    
    def search_contracts(self, instance):
        """Search for contracts"""
        def run_search():
            try:
                self.update_status("Searching...")
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # Build search filters
                filters = {'limit': 20}
                
                search_term = self.search_input.text.strip()
                if search_term:
                    filters['name_filter'] = search_term
                
                chain = self.chain_spinner.text.lower()
                if chain != 'all chains':
                    filters['chain'] = chain
                
                # Search contracts
                contracts = loop.run_until_complete(
                    self.storage.search_contracts(filters)
                )
                
                self.contracts = contracts
                Clock.schedule_once(lambda dt: self.update_contracts_display(), 0)
                Clock.schedule_once(lambda dt: self.update_status(f"Found {len(contracts)} contracts"), 0)
                
            except Exception as e:
                Clock.schedule_once(lambda dt: self.update_status(f"Search error: {str(e)}"), 0)
        
        threading.Thread(target=run_search).start()
    
    def refresh_data(self, instance):
        """Refresh contract data"""
        def run_refresh():
            try:
                self.update_status("Loading recent contracts...")
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # Get recent contracts
                contracts = loop.run_until_complete(
                    self.storage.get_recent_contracts(15)
                )
                
                self.contracts = contracts
                Clock.schedule_once(lambda dt: self.update_contracts_display(), 0)
                Clock.schedule_once(lambda dt: self.update_status(f"Loaded {len(contracts)} recent contracts"), 0)
                
            except Exception as e:
                Clock.schedule_once(lambda dt: self.update_status(f"Load error: {str(e)}"), 0)
        
        threading.Thread(target=run_refresh).start()
    
    def export_csv(self, instance):
        """Export contracts as CSV"""
        def run_export():
            try:
                self.update_status("Exporting CSV...")
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # Export current contracts as CSV
                filters = {'limit': len(self.contracts)} if self.contracts else {'limit': 50}
                csv_content = loop.run_until_complete(
                    self.storage.export_contracts_csv(filters)
                )
                
                filename = f"web3loc_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                self.storage.save_file(csv_content, filename, './downloads/')
                
                Clock.schedule_once(lambda dt: self.update_status(f"Exported: {filename}"), 0)
                Clock.schedule_once(lambda dt: self.show_popup(f"CSV exported successfully!\nFile: {filename}"), 0)
                
            except Exception as e:
                Clock.schedule_once(lambda dt: self.update_status(f"Export error: {str(e)}"), 0)
        
        threading.Thread(target=run_export).start()
    
    def show_stats(self, instance):
        """Show contract statistics"""
        def run_stats():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                stats = loop.run_until_complete(
                    self.storage.get_contract_statistics()
                )
                
                stats_text = f"""
Total Contracts: {stats.get('total_contracts', 0)}
Ethereum: {stats.get('chains', {}).get('ethereum', 0)}
Base: {stats.get('chains', {}).get('base', 0)}
Last Updated: {stats.get('last_updated', 'Unknown')[:19] if stats.get('last_updated') else 'Unknown'}
                """
                
                Clock.schedule_once(lambda dt: self.show_popup(stats_text, "Repository Statistics"), 0)
                
            except Exception as e:
                Clock.schedule_once(lambda dt: self.show_popup(f"Error loading stats: {str(e)}"), 0)
        
        threading.Thread(target=run_stats).start()
    
    def update_contracts_display(self):
        """Update the contracts display"""
        self.contracts_layout.clear_widgets()
        
        for contract in self.contracts:
            card = ContractCard(contract, self.storage)
            self.contracts_layout.add_widget(card)
        
        if not self.contracts:
            no_contracts = Label(text='No contracts found')
            self.contracts_layout.add_widget(no_contracts)
    
    def update_status(self, message):
        """Update status message"""
        Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', message), 0)
    
    def show_popup(self, message, title="Info"):
        """Show popup message"""
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.6)
        )
        popup.open()


class Web3LOCApp(App):
    """Main Kivy App"""
    
    def build(self):
        return Web3LOCMobileApp()


if __name__ == '__main__':
    # Create downloads directory
    import os
    os.makedirs('./downloads', exist_ok=True)
    
    # Run the mobile app
    Web3LOCApp().run()
