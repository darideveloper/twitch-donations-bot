from time import sleep

import PyChromeDevTools

class ChromDevWrapper ():
    
    def __init__ (self, port:int):    
        """ Conhect to chrome using PyChromeDevTools

        Args:
            port (int): port or chrome running in debug mode
        """
        
        self.base_wait_time = 2
        
        try:
            self.chrome = PyChromeDevTools.ChromeInterface(port=port)
        except:
            print ("Chome is not open. Please open chrome with the custom shorcut and try again.")
            quit ()
        self.chrome.Network.enable()
        self.chrome.Page.enable()
        
        
    def count_elems (self, selector:str):
        """ Count elemencts who match with specific css selector

        Args:
            selector (str): css selector
        """
        
        response = self.chrome.Runtime.evaluate (expression=f"document.querySelectorAll('{selector}').length")
        try:
            return response[0]['result']["result"]["value"]
        except:
            return 0
    
    def set_page (self, page:str):
        """ Navigate to specific page

        Args:
            page (str): url to navigate
        """
        
        self.chrome.Page.navigate(url=page)
        self.chrome.wait_event("Page.frameStoppedLoading", timeout=60)
        sleep (self.base_wait_time)
        
    def delete_cookies (self):
        """ Delete all cookies in chrome
        """
        
        self.chrome.Network.clearBrowserCookies()
        sleep (self.base_wait_time)  
    
    def set_cookies (self, cookies:list):
        """ Set cookies in chrome

        Args:
            cookies (list): cookies to set with name, value, domain, path, 
                secure, httpOnly and sameSite
        """
        
        for cookie in cookies:
            self.chrome.Network.setCookie(
                name=cookie["name"], 
                value=cookie["value"], 
                domain=cookie["domain"], 
                path=cookie["path"], 
                secure=cookie["secure"], 
                httpOnly=cookie["httpOnly"], 
                sameSite=cookie["sameSite"]
            )
                
        sleep (self.base_wait_time)
            
    def send_data_js (self, selector:str, data:str):
        """ Send data to specific input, with js

        Args:
            selector (str): css selector
            data (str): data to send
        """
                        
        self.chrome.Runtime.evaluate (expression=f"document.querySelector('{selector}').value = '{data}'")
        sleep (self.base_wait_time)
        
    def send_data (self, selector:str, data:str):
        """ Send data to specific input using chrome api

        Args:
            selector (str): css selector
            data (str): data to send
        """
        
        # Get input
        dom = self.chrome.DOM.getDocument()
        element = self.chrome.DOM.getDocument()[0]["result"]["root"]["nodeId"]
        result = self.chrome.DOM.querySelector(nodeId=element, selector=selector)
        node_id = result[0]["result"]["nodeId"]
        
        # Focus on the input text box
        self.chrome.DOM.focus(nodeId=node_id)
        
        # Type text
        for char in data:
            self.chrome.Input.dispatchKeyEvent (type="char", text=char, unmodifiedText=char)
        sleep (self.base_wait_time)
                
    def click (self, selector:str):
        """ Click on specific element

        Args:
            selector (str): css selector
        """
        
        self.chrome.Runtime.evaluate (expression=f"document.querySelector('{selector}').click()")
        sleep (self.base_wait_time)
        
    def get_text (self, selector:str):
        """ Get text of visible element

        Args:
            selector (str): css selector
        """
        
        response = self.chrome.Runtime.evaluate (expression=f"document.querySelector ('{selector}').textContent")
        try: 
            return response[0]['result']["result"]["value"].strip()
        except:
            return ""