# ruscat_os.py
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import subprocess
import sys
import os
import random
import time
import json
from datetime import datetime
import hashlib
import threading

class NetworkManager:
    def __init__(self):
        self.available_networks = []
        self.connected_network = None
        self.network_status = "Disconnected"
        self.can_devices = []
        
    def scan_wifi_networks(self):
        """Scan for available WiFi networks (simulated)"""
        simulated_networks = [
            {"ssid": "HomeWiFi", "signal": 90, "security": "WPA2", "connected": False},
            {"ssid": "Office_Network", "signal": 75, "security": "WPA2", "connected": False},
            {"ssid": "Free_Public_WiFi", "signal": 60, "security": "Open", "connected": False},
            {"ssid": "RusCat_Hotspot", "signal": 85, "security": "WPA2", "connected": False},
        ]
        
        if not self.connected_network:
            simulated_networks[0]["connected"] = True
            self.connected_network = simulated_networks[0]
            self.network_status = "Connected"
        
        self.available_networks = simulated_networks
        return self.available_networks
    
    def connect_to_wifi(self, ssid, password=None):
        """Connect to a WiFi network (simulated)"""
        for network in self.available_networks:
            if network["ssid"] == ssid:
                if network["security"] != "Open" and not password:
                    return False, "Password required"
                
                self.network_status = "Connecting..."
                time.sleep(1)
                
                self.connected_network = network
                network["connected"] = True
                self.network_status = "Connected"
                return True, f"Connected to {ssid}"
        
        return False, "Network not found"
    
    def disconnect_wifi(self):
        """Disconnect from current WiFi network"""
        if self.connected_network:
            ssid = self.connected_network["ssid"]
            self.connected_network = None
            self.network_status = "Disconnected"
            return True, f"Disconnected from {ssid}"
        return False, "Not connected"
    
    def get_network_status(self):
        """Get current network status"""
        if self.connected_network:
            return {
                "status": "Connected",
                "ssid": self.connected_network["ssid"],
                "signal": self.connected_network["signal"],
                "security": self.connected_network["security"]
            }
        else:
            return {"status": "Disconnected", "ssid": None}
    
    def scan_can_devices(self):
        """Scan for CAN bus devices (simulated)"""
        simulated_devices = [
            {"id": "CAN_001", "type": "Engine Control", "status": "Online", "data_rate": "500 kbps"},
            {"id": "CAN_002", "type": "Transmission", "status": "Online", "data_rate": "250 kbps"},
            {"id": "CAN_003", "type": "Brake System", "status": "Offline", "data_rate": "125 kbps"},
        ]
        self.can_devices = simulated_devices
        return self.can_devices
    
    def send_can_message(self, device_id, message):
        """Send CAN bus message (simulated)"""
        device = None
        for dev in self.can_devices:
            if dev["id"] == device_id:
                device = dev
                break
        
        if not device:
            return False, "Device not found"
        
        if device["status"] != "Online":
            return False, "Device offline"
        
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[CAN] {timestamp} -> {device_id}: {message}")
        return True, f"Message sent to {device_id}"
    
    def receive_can_messages(self):
        """Receive CAN bus messages (simulated)"""
        messages = [
            {"timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3], "device": "CAN_001", "message": "RPM: 2500"},
            {"timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3], "device": "CAN_002", "message": "Gear: 3"},
        ]
        return messages

class AccountManager:
    def __init__(self):
        self.accounts_file = "ruscat_accounts.json"
        self.current_user = None
        self.accounts = self.load_accounts()
        self.create_default_dev_account()
    
    def create_default_dev_account(self):
        """Create default developer account"""
        if "RusCatDev" not in self.accounts:
            self.accounts["RusCatDev"] = {
                'password': self.hash_password("che6072che6072hacker"),
                'profile_type': "Developer",
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'last_login': None,
                'permissions': {
                    'system_tools': True,
                    'user_management': True,
                    'debug_mode': True,
                    'file_system': True,
                    'process_management': True,
                    'network_access': True,
                    'can_bus_access': True
                },
                'settings': {
                    'theme': 'dark',
                    'auto_login': False,
                    'dev_mode': True
                },
                'game_stats': {
                    'number_guessing': {'plays': 0, 'best_score': 0},
                    'reaction_test': {'plays': 0, 'best_time': 999},
                    'memory_game': {'plays': 0, 'best_level': 0}
                }
            }
            self.save_accounts()
            print("🔧 Default developer account 'RusCatDev' created!")
    
    def load_accounts(self):
        """Load accounts from JSON file"""
        try:
            if os.path.exists(self.accounts_file):
                with open(self.accounts_file, 'r') as f:
                    return json.load(f)
            return {}
        except:
            return {}
    
    def save_accounts(self):
        """Save accounts to JSON file"""
        try:
            with open(self.accounts_file, 'w') as f:
                json.dump(self.accounts, f, indent=2)
            return True
        except:
            return False
    
    def hash_password(self, password):
        """Simple password hashing"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_account(self, username, password, profile_type="User"):
        """Create a new account"""
        if username in self.accounts:
            return False, "Username already exists!"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters!"
        
        if len(password) < 4:
            return False, "Password must be at least 4 characters!"
        
        permissions = {
            'system_tools': profile_type == "Developer",
            'user_management': profile_type == "Developer", 
            'debug_mode': profile_type == "Developer",
            'file_system': profile_type == "Developer",
            'process_management': profile_type == "Developer",
            'network_access': profile_type == "Developer",
            'can_bus_access': profile_type == "Developer"
        }
        
        self.accounts[username] = {
            'password': self.hash_password(password),
            'profile_type': profile_type,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'last_login': None,
            'permissions': permissions,
            'settings': {
                'theme': 'dark',
                'auto_login': False,
                'dev_mode': profile_type == "Developer"
            },
            'game_stats': {
                'number_guessing': {'plays': 0, 'best_score': 0},
                'reaction_test': {'plays': 0, 'best_time': 999},
                'memory_game': {'plays': 0, 'best_level': 0}
            }
        }
        
        if self.save_accounts():
            return True, f"Account '{username}' created successfully!"
        else:
            return False, "Failed to save account!"
    
    def login(self, username, password):
        """Login to an account"""
        if username not in self.accounts:
            return False, "Account not found!"
        
        account = self.accounts[username]
        if account['password'] == self.hash_password(password):
            account['last_login'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.current_user = username
            self.save_accounts()
            return True, f"Welcome back, {username}!"
        else:
            return False, "Invalid password!"
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
        return True
    
    def get_current_user_info(self):
        """Get current user information"""
        if self.current_user and self.current_user in self.accounts:
            return self.accounts[self.current_user]
        return None
    
    def is_developer(self):
        """Check if current user is a developer"""
        user_info = self.get_current_user_info()
        return user_info and user_info['profile_type'] == "Developer"
    
    def has_permission(self, permission):
        """Check if current user has specific permission"""
        user_info = self.get_current_user_info()
        return user_info and user_info['permissions'].get(permission, False)

class PowerManager:
    @staticmethod
    def shutdown():
        """Shutdown the computer"""
        try:
            if messagebox.askyesno("Shutdown", "Are you sure you want to shutdown?"):
                print("🔄 Shutting down system...")
                if os.name == 'nt':
                    os.system("shutdown /s /t 0")
                elif sys.platform.startswith('linux'):
                    os.system("shutdown -h now")
                elif sys.platform == "darwin":
                    os.system("shutdown -h now")
                else:
                    messagebox.showwarning("Not Supported", "Shutdown not supported")
        except Exception as e:
            messagebox.showerror("Error", f"Shutdown failed: {e}")

    @staticmethod
    def restart():
        """Restart the computer"""
        try:
            if messagebox.askyesno("Restart", "Are you sure you want to restart?"):
                print("🔄 Restarting system...")
                if os.name == 'nt':
                    os.system("shutdown /r /t 0")
                elif sys.platform.startswith('linux'):
                    os.system("reboot")
                elif sys.platform == "darwin":
                    os.system("shutdown -r now")
                else:
                    messagebox.showwarning("Not Supported", "Restart not supported")
        except Exception as e:
            messagebox.showerror("Error", f"Restart failed: {e}")

class TournamentManager:
    def __init__(self, account_manager):
        self.account_manager = account_manager
        self.players = []
        self.scores = {}
        self.tournament_active = False
        
    def add_player(self, player_name):
        if player_name not in self.players:
            self.players.append(player_name)
            self.scores[player_name] = 0
            return True
        return False
    
    def start_tournament(self):
        if len(self.players) >= 2:
            self.tournament_active = True
            return True
        return False
    
    def get_leaderboard(self):
        return sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
    
    def reset_tournament(self):
        self.players = []
        self.scores = {}
        self.tournament_active = False

class MiniGame:
    def __init__(self, account_manager):
        self.account_manager = account_manager
    
    def number_guessing_game(self):
        """Simple number guessing game"""
        window = tk.Toplevel()
        window.title("Number Guessing Game")
        window.geometry("300x200")
        window.configure(bg='#2D2D2D')
        
        number = random.randint(1, 100)
        attempts = 0
        
        def check_guess():
            nonlocal attempts
            try:
                guess = int(entry.get())
                attempts += 1
                
                if guess < number:
                    result_label.config(text="Too low! Try higher.", fg='#FFAA00')
                elif guess > number:
                    result_label.config(text="Too high! Try lower.", fg='#FFAA00')
                else:
                    result_label.config(text=f"Correct! {attempts} attempts!", fg='#00FF00')
            except ValueError:
                result_label.config(text="Enter a valid number!", fg='#FF5555')
        
        tk.Label(window, text="Guess number (1-100)", fg='white', bg='#2D2D2D').pack(pady=10)
        entry = tk.Entry(window, font=('Arial', 12))
        entry.pack(pady=5)
        tk.Button(window, text="Submit", command=check_guess, bg='#007ACC', fg='white').pack(pady=5)
        result_label = tk.Label(window, text="", fg='white', bg='#2D2D2D')
        result_label.pack(pady=5)

class DeveloperTools:
    def __init__(self, account_manager, root):
        self.account_manager = account_manager
        self.root = root
        self.network_manager = NetworkManager()
    
    def show_network_manager(self):
        """Show network management interface"""
        window = tk.Toplevel(self.root)
        window.title("🌐 Network Manager")
        window.geometry("600x500")
        window.configure(bg='#1E1E1E')
        
        notebook = ttk.Notebook(window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # WiFi Tab
        wifi_frame = tk.Frame(notebook, bg='#1E1E1E')
        notebook.add(wifi_frame, text="📶 WiFi")
        
        # Status
        status_frame = tk.Frame(wifi_frame, bg='#2D2D2D')
        status_frame.pack(fill='x', padx=10, pady=10)
        tk.Label(status_frame, text="Network Status", font=('Arial', 12, 'bold'), fg='white', bg='#2D2D2D').pack()
        self.status_label = tk.Label(status_frame, text="Disconnected", font=('Arial', 11), fg='#FF5555', bg='#2D2D2D')
        self.status_label.pack()
        
        # Networks list
        list_frame = tk.Frame(wifi_frame, bg='#1E1E1E')
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.network_list = tk.Listbox(list_frame, bg='#2D2D2D', fg='white', font=('Arial', 10))
        self.network_list.pack(fill='both', expand=True)
        
        # Buttons
        btn_frame = tk.Frame(wifi_frame, bg='#1E1E1E')
        btn_frame.pack(fill='x', padx=10, pady=10)
        tk.Button(btn_frame, text="Scan Networks", command=self.scan_networks, bg='#007ACC', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Connect", command=self.connect_to_network, bg='#00AA00', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Disconnect", command=self.disconnect_network, bg='#FF5555', fg='white').pack(side='left', padx=5)
        
        # CAN Bus Tab
        can_frame = tk.Frame(notebook, bg='#1E1E1E')
        notebook.add(can_frame, text="🔌 CAN Bus")
        
        # CAN devices
        devices_frame = tk.Frame(can_frame, bg='#2D2D2D')
        devices_frame.pack(fill='x', padx=10, pady=10)
        tk.Label(devices_frame, text="CAN Devices", font=('Arial', 12, 'bold'), fg='white', bg='#2D2D2D').pack()
        
        self.devices_tree = ttk.Treeview(devices_frame, columns=('ID', 'Type', 'Status'), show='headings', height=4)
        self.devices_tree.heading('ID', text='Device ID')
        self.devices_tree.heading('Type', text='Type')
        self.devices_tree.heading('Status', text='Status')
        self.devices_tree.pack(fill='x', padx=10, pady=5)
        
        # CAN messages
        msg_frame = tk.Frame(can_frame, bg='#1E1E1E')
        msg_frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.can_console = tk.Text(msg_frame, bg='#000000', fg='#00FF00', font=('Consolas', 9), height=8)
        self.can_console.pack(fill='both', expand=True)
        
        control_frame = tk.Frame(can_frame, bg='#1E1E1E')
        control_frame.pack(fill='x', padx=10, pady=5)
        self.message_entry = tk.Entry(control_frame, width=30)
        self.message_entry.pack(side='left', padx=5)
        tk.Button(control_frame, text="Send", command=self.send_can_message, bg='#007ACC', fg='white').pack(side='left', padx=5)
        tk.Button(control_frame, text="Scan Devices", command=self.scan_can_devices, bg='#00AA00', fg='white').pack(side='left', padx=5)
        
        self.scan_networks()
        self.scan_can_devices()
    
    def scan_networks(self):
        """Scan for WiFi networks"""
        networks = self.network_manager.scan_wifi_networks()
        self.network_list.delete(0, tk.END)
        
        for network in networks:
            status = " ✅" if network.get('connected', False) else ""
            text = f"{network['ssid']} ({network['signal']}%){status}"
            self.network_list.insert(tk.END, text)
        
        self.update_network_status()
    
    def update_network_status(self):
        """Update network status display"""
        status = self.network_manager.get_network_status()
        if status['status'] == 'Connected':
            self.status_label.config(text=f"Connected: {status['ssid']}", fg='#00FF00')
        else:
            self.status_label.config(text="Disconnected", fg='#FF5555')
    
    def connect_to_network(self):
        """Connect to selected network"""
        selection = self.network_list.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a network first!")
            return
        
        network_text = self.network_list.get(selection[0])
        ssid = network_text.split(' ')[0]
        
        password = None
        if "WPA" in network_text:
            password = simpledialog.askstring("Password", f"Password for {ssid}:", show='*')
        
        success, message = self.network_manager.connect_to_wifi(ssid, password)
        if success:
            messagebox.showinfo("Success", message)
            self.scan_networks()
        else:
            messagebox.showerror("Error", message)
    
    def disconnect_network(self):
        """Disconnect from current network"""
        success, message = self.network_manager.disconnect_wifi()
        if success:
            messagebox.showinfo("Success", message)
            self.scan_networks()
        else:
            messagebox.showerror("Error", message)
    
    def scan_can_devices(self):
        """Scan for CAN bus devices"""
        devices = self.network_manager.scan_can_devices()
        
        for item in self.devices_tree.get_children():
            self.devices_tree.delete(item)
        
        for device in devices:
            self.devices_tree.insert('', 'end', values=(
                device['id'], device['type'], device['status']
            ))
    
    def send_can_message(self):
        """Send CAN bus message"""
        selection = self.devices_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select a CAN device first!")
            return
        
        device_id = self.devices_tree.item(selection[0])['values'][0]
        message = self.message_entry.get().strip()
        
        if not message:
            messagebox.showwarning("Warning", "Enter a message!")
            return
        
        success, result = self.network_manager.send_can_message(device_id, message)
        if success:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.can_console.insert(tk.END, f"[{timestamp}] SENT -> {device_id}: {message}\n")
            self.message_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", result)
        
        self.can_console.see(tk.END)
    
    def show_system_info(self):
        """Show system information"""
        window = tk.Toplevel(self.root)
        window.title("System Information")
        window.geometry("500x400")
        window.configure(bg='#2D2D2D')
        
        info_text = tk.Text(window, bg='#1A1A1A', fg='#00FF00', font=('Consolas', 10))
        info_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        info = f"""System Information:
Python: {sys.version}
Platform: {sys.platform}
Current User: {self.account_manager.current_user}
Screen: {self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}
"""
        info_text.insert(tk.END, info)
        info_text.config(state='disabled')
    
    def show_user_manager(self):
        """User management tool"""
        window = tk.Toplevel(self.root)
        window.title("User Manager")
        window.geometry("400x300")
        window.configure(bg='#2D2D2D')
        
        tk.Label(window, text="User Manager", font=('Arial', 14, 'bold'), fg='white', bg='#2D2D2D').pack(pady=10)
        
        user_list = tk.Listbox(window, bg='#2D2D2D', fg='white', font=('Arial', 11))
        user_list.pack(fill='both', expand=True, padx=10, pady=5)
        
        for username in self.account_manager.accounts.keys():
            user_list.insert(tk.END, username)
        
        btn_frame = tk.Frame(window, bg='#2D2D2D')
        btn_frame.pack(fill='x', padx=10, pady=10)
        tk.Button(btn_frame, text="View Details", bg='#007ACC', fg='white').pack(side='left', padx=5)
        tk.Button(btn_frame, text="Refresh", bg='#00AA00', fg='white').pack(side='left', padx=5)
    
    def show_process_manager(self):
        """Simple process manager"""
        window = tk.Toplevel(self.root)
        window.title("Process Manager")
        window.geometry("500x300")
        window.configure(bg='#2D2D2D')
        
        tk.Label(window, text="Process Manager", font=('Arial', 14, 'bold'), fg='white', bg='#2D2D2D').pack(pady=10)
        
        process_text = tk.Text(window, bg='#1A1A1A', fg='#00FF00', font=('Consolas', 9))
        process_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        process_text.insert(tk.END, "Process monitoring would be here...\n")
        process_text.insert(tk.END, "In real implementation, use psutil library\n")
        process_text.config(state='disabled')

class RusCatOS:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("RusCat OS")
        self.root.configure(bg='#2D2D2D')
        
        # Initialize account manager first
        self.account_manager = AccountManager()
        
        # Show login screen
        if not self.show_login_screen():
            sys.exit()
        
        # Continue with OS setup after successful login
        self.setup_os()
    
    def show_login_screen(self):
        """Show login/registration screen"""
        login_window = tk.Toplevel(self.root)
        login_window.title("RusCat OS - Login")
        login_window.geometry("400x400")
        login_window.configure(bg='#2D2D2D')
        login_window.transient(self.root)
        login_window.grab_set()
        
        # Center the window
        login_window.update_idletasks()
        x = (login_window.winfo_screenwidth() // 2) - (200)
        y = (login_window.winfo_screenheight() // 2) - (200)
        login_window.geometry(f"400x400+{x}+{y}")
        
        # Title
        title_label = tk.Label(
            login_window,
            text="🐱 RusCat OS\nAccount Login",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#2D2D2D',
            justify='center'
        )
        title_label.pack(pady=30)
        
        # Login Frame
        login_frame = tk.Frame(login_window, bg='#2D2D2D')
        login_frame.pack(pady=20, padx=40, fill='x')
        
        tk.Label(login_frame, text="Username:", fg='white', bg='#2D2D2D').pack(anchor='w')
        username_entry = tk.Entry(login_frame, font=('Arial', 12))
        username_entry.pack(fill='x', pady=5)
        
        tk.Label(login_frame, text="Password:", fg='white', bg='#2D2D2D').pack(anchor='w', pady=(10,0))
        password_entry = tk.Entry(login_frame, font=('Arial', 12), show='*')
        password_entry.pack(fill='x', pady=5)
        
        result_label = tk.Label(login_window, text="", fg='yellow', bg='#2D2D2D')
        result_label.pack(pady=10)
        
        def attempt_login():
            username = username_entry.get().strip()
            password = password_entry.get()
            
            if not username or not password:
                result_label.config(text="Please enter username and password!", fg='red')
                return
            
            success, message = self.account_manager.login(username, password)
            result_label.config(text=message, fg='green' if success else 'red')
            
            if success:
                login_window.destroy()
        
        def show_register():
            register_window = tk.Toplevel(login_window)
            register_window.title("Create Account")
            register_window.geometry("350x300")
            register_window.configure(bg='#2D2D2D')
            
            tk.Label(register_window, text="Create Account", font=('Arial', 14, 'bold'), fg='white', bg='#2D2D2D').pack(pady=20)
            
            tk.Label(register_window, text="Username:", fg='white', bg='#2D2D2D').pack()
            new_user = tk.Entry(register_window, font=('Arial', 12))
            new_user.pack(pady=5)
            
            tk.Label(register_window, text="Password:", fg='white', bg='#2D2D2D').pack()
            new_pass = tk.Entry(register_window, font=('Arial', 12), show='*')
            new_pass.pack(pady=5)
            
            def register():
                username = new_user.get().strip()
                password = new_pass.get()
                
                if not username or not password:
                    return
                
                success, message = self.account_manager.create_account(username, password)
                if success:
                    register_window.destroy()
                else:
                    print(message)
            
            tk.Button(register_window, text="Create", command=register, bg='#00AA00', fg='white').pack(pady=20)
        
        # Buttons
        button_frame = tk.Frame(login_window, bg='#2D2D2D')
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Login", command=attempt_login,
                 bg='#007ACC', fg='white', font=('Arial', 12), width=15).pack(pady=5)
        
        tk.Button(button_frame, text="Create Account", command=show_register,
                 bg='#00AA00', fg='white', font=('Arial', 12), width=15).pack(pady=5)
        
        # Auto-fill developer account
        def fill_dev_account():
            username_entry.delete(0, tk.END)
            username_entry.insert(0, "RusCatDev")
            password_entry.focus()
        
        if "RusCatDev" in self.account_manager.accounts:
            tk.Button(button_frame, text="Use Dev Account", command=fill_dev_account,
                     bg='#FFD700', fg='black', font=('Arial', 10)).pack(pady=5)
        
        # Enter key to login
        password_entry.bind('<Return>', lambda e: attempt_login())
        
        # Wait for login
        login_window.wait_window()
        return self.account_manager.current_user is not None
    
    def setup_os(self):
        """Setup OS after successful login"""
        # Start in fullscreen
        self.fullscreen = True
        self.root.attributes('-fullscreen', True)
        
        # Get screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.taskbar_height = 40
        
        # Initialize managers
        self.power_manager = PowerManager()
        self.tournament_manager = TournamentManager(self.account_manager)
        self.mini_game = MiniGame(self.account_manager)
        self.dev_tools = DeveloperTools(self.account_manager, self.root)
        
        # Bind keys
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.exit_fullscreen)
        
        self.setup_desktop()
        self.setup_taskbar()
        self.create_sample_apps()
        
        self.start_menu = None
        self.open_windows = []
        
        print(f"👤 Logged in as: {self.account_manager.current_user}")
        print("🚀 RusCat OS Started Successfully!")
    
    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes('-fullscreen', self.fullscreen)
        
        if not self.fullscreen:
            self.root.geometry("800x600")
        
        print(f"🔲 Fullscreen: {self.fullscreen}")
        
    def exit_fullscreen(self, event=None):
        if self.fullscreen:
            self.toggle_fullscreen()
    
    def setup_desktop(self):
        self.desktop = tk.Frame(self.root, bg='#2D2D2D')
        self.desktop.pack(fill='both', expand=True)
        
        user_info = self.account_manager.get_current_user_info()
        welcome_text = f"RusCat OS\nWelcome, {self.account_manager.current_user}!\nPress F11 to toggle fullscreen"
        
        title_label = tk.Label(
            self.desktop, 
            text=welcome_text,
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#2D2D2D',
            justify='center'
        )
        title_label.place(relx=0.5, rely=0.1, anchor='center')
        
    def setup_taskbar(self):
        self.taskbar = tk.Frame(self.root, bg='#3C3C3C', height=self.taskbar_height)
        self.taskbar.pack(fill='x', side='bottom')
        self.taskbar.pack_propagate(False)
        
        # User info
        user_label = tk.Label(
            self.taskbar,
            text=f"👤 {self.account_manager.current_user}",
            fg='white',
            bg='#3C3C3C',
            font=('Arial', 9)
        )
        user_label.pack(side='left', padx=5, pady=5)
        
        start_btn = tk.Button(
            self.taskbar,
            text="🐱 Start",
            bg='#007ACC',
            fg='white',
            border=0,
            font=('Arial', 10, 'bold'),
            command=self.toggle_start_menu
        )
        start_btn.pack(side='left', padx=5, pady=5)
        
        # Developer tools button
        if self.account_manager.is_developer():
            dev_btn = tk.Button(
                self.taskbar,
                text="🔧 Dev",
                bg='#FFD700',
                fg='black',
                border=0,
                font=('Arial', 10),
                command=self.show_dev_tools_menu
            )
            dev_btn.pack(side='left', padx=2, pady=5)
        
        power_btn = tk.Button(
            self.taskbar,
            text="⭕",
            bg='#FF5555',
            fg='white',
            border=0,
            font=('Arial', 12),
            command=self.show_power_menu
        )
        power_btn.pack(side='right', padx=5, pady=5)
        
        self.clock_label = tk.Label(
            self.taskbar,
            text=datetime.now().strftime("%H:%M"),
            fg='white',
            bg='#3C3C3C',
            font=('Arial', 10)
        )
        self.clock_label.pack(side='right', padx=10)
        
        self.update_clock()
    
    def show_dev_tools_menu(self):
        """Show developer tools menu"""
        dev_menu = tk.Menu(self.root, tearoff=0, bg='#4A4A4A', fg='white')
        dev_menu.add_command(label="System Information", command=self.dev_tools.show_system_info)
        dev_menu.add_command(label="User Manager", command=self.dev_tools.show_user_manager)
        dev_menu.add_command(label="Process Manager", command=self.dev_tools.show_process_manager)
        dev_menu.add_command(label="Network Manager", command=self.dev_tools.show_network_manager)
        dev_menu.add_separator()
        dev_menu.add_command(label="Admin Panel", command=self.open_admin_panel)
        
        try:
            dev_menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally:
            dev_menu.grab_release()
    
    def open_admin_panel(self):
        """Open the RusCat Admin Panel"""
        try:
            if os.path.exists("ruscattool.py"):
                subprocess.Popen([sys.executable, "ruscattool.py"])
            else:
                messagebox.showinfo("Info", "Admin panel file not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def show_power_menu(self):
        power_menu = tk.Menu(self.root, tearoff=0, bg='#4A4A4A', fg='white')
        power_menu.add_command(label="Restart Computer", command=self.power_manager.restart)
        power_menu.add_command(label="Shutdown Computer", command=self.power_manager.shutdown)
        power_menu.add_separator()
        power_menu.add_command(label="Log Out", command=self.logout)
        
        try:
            power_menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally:
            power_menu.grab_release()
    
    def logout(self):
        if messagebox.askyesno("Log Out", "Are you sure you want to log out?"):
            self.root.destroy()
    
    def toggle_start_menu(self):
        if self.start_menu and self.start_menu.winfo_exists():
            self.start_menu.destroy()
            self.start_menu = None
        else:
            self.show_start_menu()

    def show_start_menu(self):
        self.start_menu = tk.Toplevel(self.root)
        self.start_menu.title("Start Menu")
        self.start_menu.configure(bg='#4A4A4A')
        self.start_menu.overrideredirect(True)
        
        menu_width = 300
        menu_height = 400
        x_pos = 5
        y_pos = self.screen_height - self.taskbar_height - menu_height - 5
        
        self.start_menu.geometry(f"{menu_width}x{menu_height}+{x_pos}+{y_pos}")
        
        menu_frame = tk.Frame(self.start_menu, bg='#4A4A4A')
        menu_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # User header
        user_header = tk.Label(
            menu_frame,
            text=f"👤 {self.account_manager.current_user}",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#007ACC',
            width=30
        )
        user_header.pack(pady=10)
        
        # Apps section
        apps = [
            ("📝 Text Editor", self.open_text_editor),
            ("🌐 Browser", self.open_browser),
            ("🎮 Games", self.mini_game.number_guessing_game),
            ("📊 Profile", self.show_user_profile),
        ]
        
        if self.account_manager.is_developer():
            apps.extend([
                ("🔧 Dev Tools", self.show_dev_tools_menu),
                ("🌐 Network", self.dev_tools.show_network_manager),
                ("👑 Admin Panel", self.open_admin_panel)
            ])
        
        for app_text, app_command in apps:
            btn = tk.Button(
                menu_frame,
                text=app_text,
                font=('Arial', 11),
                bg='#5A5A5A',
                fg='white',
                border=0,
                anchor='w',
                command=app_command
            )
            btn.pack(fill='x', pady=2)
        
        # Power section
        power_frame = tk.Frame(menu_frame, bg='#4A4A4A')
        power_frame.pack(fill='x', pady=(20, 0))
        
        power_buttons = [
            ("🚪 Log Out", self.logout),
            ("🔁 Restart", self.power_manager.restart),
            ("⭕ Shutdown", self.power_manager.shutdown)
        ]
        
        for btn_text, btn_command in power_buttons:
            btn = tk.Button(
                power_frame,
                text=btn_text,
                font=('Arial', 11),
                bg='#555555',
                fg='white',
                border=0,
                anchor='w',
                command=btn_command
            )
            btn.pack(fill='x', pady=1)
        
        self.start_menu.bind("<FocusOut>", lambda e: self.close_start_menu())

    def show_user_profile(self):
        """Show user profile"""
        window = tk.Toplevel(self.root)
        window.title("User Profile")
        window.geometry("400x300")
        window.configure(bg='#4A4A4A')
        
        user_info = self.account_manager.get_current_user_info()
        
        header = tk.Label(
            window,
            text=f"👤 {self.account_manager.current_user}'s Profile",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#4A4A4A'
        )
        header.pack(pady=10)
        
        info_text = f"Profile Type: {user_info['profile_type']}\n"
        info_text += f"Account Created: {user_info['created_at']}\n"
        info_text += f"Last Login: {user_info['last_login'] or 'Never'}\n"
        
        tk.Label(window, text=info_text, fg='white', bg='#4A4A4A', font=('Arial', 11)).pack(pady=20)

    def create_sample_apps(self):
        apps = [
            {"name": "Text Editor", "x": 100, "y": 200},
            {"name": "Browser", "x": 100, "y": 300},
            {"name": "Games", "x": 200, "y": 200},
            {"name": "Profile", "x": 200, "y": 300},
        ]
        
        if self.account_manager.is_developer():
            apps.extend([
                {"name": "Dev Tools", "x": 300, "y": 200},
                {"name": "Network", "x": 300, "y": 300}
            ])
        
        for app in apps:
            self.create_app_icon(app["name"], app["x"], app["y"])

    def create_app_icon(self, name, x, y):
        icon_frame = tk.Frame(
            self.desktop,
            bg='#4A4A4A',
            width=80,
            height=80,
            relief='raised',
            borderwidth=1
        )
        icon_frame.place(x=x, y=y)
        
        icon_label = tk.Label(
            icon_frame,
            text="📱",
            font=('Arial', 20),
            bg='#4A4A4A',
            fg='white'
        )
        icon_label.pack(pady=5)
        
        name_label = tk.Label(
            icon_frame,
            text=name,
            font=('Arial', 10),
            bg='#4A4A4A',
            fg='white'
        )
        name_label.pack()
        
        icon_frame.bind("<Double-Button-1>", lambda e: self.open_app(name))

    def open_app(self, app_name):
        app_functions = {
            "Text Editor": self.open_text_editor,
            "Browser": self.open_browser,
            "Games": self.mini_game.number_guessing_game,
            "Profile": self.show_user_profile,
            "Dev Tools": self.show_dev_tools_menu,
            "Network": self.dev_tools.show_network_manager
        }
        
        if app_name in app_functions:
            app_functions[app_name]()

    def open_text_editor(self):
        window = tk.Toplevel(self.root)
        window.title("Text Editor")
        window.geometry("400x300")
        window.configure(bg='#4A4A4A')
        
        text_widget = tk.Text(window, bg='#2D2D2D', fg='white', font=('Arial', 11))
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)

    def open_browser(self):
        window = tk.Toplevel(self.root)
        window.title("Browser")
        window.geometry("500x400")
        window.configure(bg='#4A4A4A')
        
        tk.Label(window, text="RusCat Browser", font=('Arial', 14, 'bold'), fg='white', bg='#4A4A4A').pack(pady=20)
        tk.Label(window, text="Browser functionality would be here", fg='white', bg='#4A4A4A').pack()

    def close_start_menu(self):
        if self.start_menu:
            self.start_menu.destroy()
            self.start_menu = None

    def update_clock(self):
        self.clock_label.config(text=datetime.now().strftime("%H:%M"))
        self.root.after(1000, self.update_clock)

    def run(self):
        print("🚀 RusCat OS Started!")
        print(f"👤 User: {self.account_manager.current_user}")
        print("🎯 Features: Accounts, Games, Network, CAN Bus, Admin Tools")
        self.root.mainloop()

if __name__ == "__main__":
    os_system = RusCatOS()
    os_system.run()
