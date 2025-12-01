import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import itertools
import string
import time
from datetime import datetime
import hashlib

class BruteForceTool:
    def __init__(self, root):
        self.root = root
        self.root.title("BruteForce Toolkit - Educational Tool")
        self.root.geometry("900x700")
        
        # Variables
        self.running = False
        self.attempts = 0
        self.start_time = None
        self.thread = None
        
        # Setup styles
        self.setup_styles()
        
        # Create UI
        self.create_widgets()
        
    def setup_styles(self):
        """Setup ttk styles"""
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Red.TButton', background='#ff4444')
        style.configure('Green.TButton', background='#44ff44')
        
    def create_widgets(self):
        """Create all UI widgets"""
        # Title
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E))
        ttk.Label(title_frame, text="BruteForce Toolkit - Educational Purpose Only", 
                 style='Title.TLabel').pack()
        ttk.Label(title_frame, text="This tool is for learning about cybersecurity concepts only",
                 foreground='red').pack()
        
        # Notebook for different tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Dictionary Attack Tab
        self.create_dictionary_tab()
        
        # Brute Force Tab
        self.create_bruteforce_tab()
        
        # Hash Cracker Tab
        self.create_hash_tab()
        
        # Status/Log Tab
        self.create_log_tab()
        
        # Control buttons
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        self.start_btn = ttk.Button(control_frame, text="Start Attack", 
                                   command=self.start_attack, style='Green.TButton')
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(control_frame, text="Stop", 
                                  command=self.stop_attack, style='Red.TButton', state='disabled')
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(control_frame, text="Clear Logs", 
                                   command=self.clear_logs)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        
    def create_dictionary_tab(self):
        """Create dictionary attack tab"""
        dict_frame = ttk.Frame(self.notebook)
        self.notebook.add(dict_frame, text="Dictionary Attack")
        
        # Target section
        ttk.Label(dict_frame, text="Target String/Password:", style='Subtitle.TLabel').grid(
            row=0, column=0, sticky=tk.W, padx=10, pady=(10, 5))
        
        self.target_var = tk.StringVar()
        ttk.Entry(dict_frame, textvariable=self.target_var, width=50, show="*").grid(
            row=1, column=0, padx=10, pady=(0, 10))
        
        ttk.Button(dict_frame, text="Show/Hide", 
                  command=self.toggle_password).grid(row=1, column=1, padx=5)
        
        # Dictionary file section
        ttk.Label(dict_frame, text="Dictionary File:", style='Subtitle.TLabel').grid(
            row=2, column=0, sticky=tk.W, padx=10, pady=(10, 5))
        
        dict_control_frame = ttk.Frame(dict_frame)
        dict_control_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 10), sticky=(tk.W, tk.E))
        
        self.dict_path_var = tk.StringVar(value="Enter path or use sample dictionary")
        ttk.Entry(dict_control_frame, textvariable=self.dict_path_var, width=40).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(dict_control_frame, text="Browse", command=self.browse_dict).pack(side=tk.LEFT)
        ttk.Button(dict_control_frame, text="Use Sample", command=self.load_sample_dict).pack(side=tk.LEFT, padx=10)
        
        # Options
        options_frame = ttk.LabelFrame(dict_frame, text="Options", padding="10")
        options_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        self.use_variations = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Try common variations (1337 speak, etc.)", 
                       variable=self.use_variations).grid(row=0, column=0, sticky=tk.W)
        
        self.case_sensitive = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Case sensitive", 
                       variable=self.case_sensitive).grid(row=1, column=0, sticky=tk.W)
        
    def create_bruteforce_tab(self):
        """Create brute force attack tab"""
        bf_frame = ttk.Frame(self.notebook)
        self.notebook.add(bf_frame, text="Brute Force")
        
        # Target section (reused)
        ttk.Label(bf_frame, text="Target String/Password:", style='Subtitle.TLabel').grid(
            row=0, column=0, sticky=tk.W, padx=10, pady=(10, 5))
        
        self.bf_target_var = tk.StringVar()
        ttk.Entry(bf_frame, textvariable=self.bf_target_var, width=50, show="*").grid(
            row=1, column=0, padx=10, pady=(0, 10))
        
        # Character set selection
        charset_frame = ttk.LabelFrame(bf_frame, text="Character Set", padding="10")
        charset_frame.grid(row=2, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        self.use_lowercase = tk.BooleanVar(value=True)
        ttk.Checkbutton(charset_frame, text="Lowercase (a-z)", 
                       variable=self.use_lowercase).grid(row=0, column=0, sticky=tk.W)
        
        self.use_uppercase = tk.BooleanVar(value=True)
        ttk.Checkbutton(charset_frame, text="Uppercase (A-Z)", 
                       variable=self.use_uppercase).grid(row=1, column=0, sticky=tk.W)
        
        self.use_digits = tk.BooleanVar(value=True)
        ttk.Checkbutton(charset_frame, text="Digits (0-9)", 
                       variable=self.use_digits).grid(row=2, column=0, sticky=tk.W)
        
        self.use_special = tk.BooleanVar(value=False)
        ttk.Checkbutton(charset_frame, text="Special Characters (!@#$%)", 
                       variable=self.use_special).grid(row=3, column=0, sticky=tk.W)
        
        # Custom charset
        ttk.Label(charset_frame, text="Custom Characters:").grid(row=4, column=0, sticky=tk.W, pady=(10, 0))
        self.custom_charset_var = tk.StringVar()
        ttk.Entry(charset_frame, textvariable=self.custom_charset_var, width=40).grid(
            row=5, column=0, sticky=(tk.W, tk.E))
        
        # Length settings
        length_frame = ttk.LabelFrame(bf_frame, text="Password Length", padding="10")
        length_frame.grid(row=3, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        ttk.Label(length_frame, text="Min:").grid(row=0, column=0, padx=5)
        self.min_length_var = tk.StringVar(value="1")
        ttk.Spinbox(length_frame, from_=1, to=10, textvariable=self.min_length_var, width=5).grid(
            row=0, column=1, padx=5)
        
        ttk.Label(length_frame, text="Max:").grid(row=0, column=2, padx=5)
        self.max_length_var = tk.StringVar(value="4")
        ttk.Spinbox(length_frame, from_=1, to=10, textvariable=self.max_length_var, width=5).grid(
            row=0, column=3, padx=5)
        
        # Speed control
        speed_frame = ttk.LabelFrame(bf_frame, text="Speed Control", padding="10")
        speed_frame.grid(row=4, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        ttk.Label(speed_frame, text="Delay between attempts (seconds):").grid(row=0, column=0, sticky=tk.W)
        self.delay_var = tk.StringVar(value="0.01")
        ttk.Scale(speed_frame, from_=0, to=1, variable=self.delay_var, 
                 orient=tk.HORIZONTAL, length=200).grid(row=0, column=1, padx=10)
        
    def create_hash_tab(self):
        """Create hash cracking tab"""
        hash_frame = ttk.Frame(self.notebook)
        self.notebook.add(hash_frame, text="Hash Cracker")
        
        # Hash input
        ttk.Label(hash_frame, text="Target Hash:", style='Subtitle.TLabel').grid(
            row=0, column=0, sticky=tk.W, padx=10, pady=(10, 5))
        
        self.hash_target_var = tk.StringVar()
        ttk.Entry(hash_frame, textvariable=self.hash_target_var, width=60).grid(
            row=1, column=0, padx=10, pady=(0, 10))
        
        # Hash type selection
        ttk.Label(hash_frame, text="Hash Algorithm:", style='Subtitle.TLabel').grid(
            row=2, column=0, sticky=tk.W, padx=10, pady=(10, 5))
        
        self.hash_type_var = tk.StringVar(value="md5")
        hash_types = ["md5", "sha1", "sha256", "sha512"]
        
        for i, hash_type in enumerate(hash_types):
            ttk.Radiobutton(hash_frame, text=hash_type.upper(), 
                          variable=self.hash_type_var, value=hash_type).grid(
                row=3, column=i, padx=10, pady=5, sticky=tk.W)
        
        # Wordlist for hash cracking
        ttk.Label(hash_frame, text="Wordlist:", style='Subtitle.TLabel').grid(
            row=4, column=0, sticky=tk.W, padx=10, pady=(10, 5))
        
        self.hash_wordlist_var = tk.StringVar(value="Use built-in common passwords")
        ttk.Entry(hash_frame, textvariable=self.hash_wordlist_var, width=50).grid(
            row=5, column=0, padx=10, pady=(0, 10))
        
        ttk.Button(hash_frame, text="Browse Wordlist", 
                  command=self.browse_hash_wordlist).grid(row=5, column=1, padx=5)
        
    def create_log_tab(self):
        """Create logging/status tab"""
        log_frame = ttk.Frame(self.notebook)
        self.notebook.add(log_frame, text="Attack Log")
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(log_frame, text="Statistics", padding="10")
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Stats labels
        self.attempts_var = tk.StringVar(value="Attempts: 0")
        self.time_var = tk.StringVar(value="Time elapsed: 00:00:00")
        self.speed_var = tk.StringVar(value="Speed: 0 attempts/sec")
        
        ttk.Label(stats_frame, textvariable=self.attempts_var).grid(row=0, column=0, sticky=tk.W, padx=5)
        ttk.Label(stats_frame, textvariable=self.time_var).grid(row=0, column=1, sticky=tk.W, padx=20)
        ttk.Label(stats_frame, textvariable=self.speed_var).grid(row=0, column=2, sticky=tk.W, padx=20)
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20, width=80)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def toggle_password(self):
        """Toggle password visibility"""
        current_tab = self.notebook.index(self.notebook.select())
        
        if current_tab == 0:  # Dictionary tab
            entry = self.root.children['!frame'].children['!frame2'].children['!entry']
        else:  # Brute force tab
            entry = self.root.children['!frame'].children['!frame3'].children['!entry']
        
        if entry.cget('show') == '*':
            entry.config(show='')
        else:
            entry.config(show='*')
    
    def browse_dict(self):
        """Browse for dictionary file"""
        # Simplified for example - you'd use filedialog in real implementation
        self.dict_path_var.set("dictionary.txt")
        
    def load_sample_dict(self):
        """Load sample dictionary"""
        sample_words = ["password", "123456", "admin", "letmein", "welcome", "qwerty",
                       "password123", "123456789", "football", "monkey", "abc123"]
        with open("sample_dict.txt", "w") as f:
            f.write("\n".join(sample_words))
        self.dict_path_var.set("sample_dict.txt")
        self.log("Loaded sample dictionary with common passwords")
        
    def browse_hash_wordlist(self):
        """Browse for hash cracking wordlist"""
        self.hash_wordlist_var.set("wordlist.txt")
        
    def start_attack(self):
        """Start the selected attack"""
        if self.running:
            return
            
        current_tab = self.notebook.index(self.notebook.select())
        
        # Validate inputs based on current tab
        if current_tab == 0:  # Dictionary
            target = self.target_var.get()
            if not target:
                messagebox.showwarning("Warning", "Please enter a target string")
                return
            if not self.dict_path_var.get() or "Enter path" in self.dict_path_var.get():
                messagebox.showwarning("Warning", "Please select or create a dictionary")
                return
                
        elif current_tab == 1:  # Brute force
            target = self.bf_target_var.get()
            if not target:
                messagebox.showwarning("Warning", "Please enter a target string")
                return
                
        elif current_tab == 2:  # Hash cracker
            target = self.hash_target_var.get()
            if not target:
                messagebox.showwarning("Warning", "Please enter a hash")
                return
                
        # Start attack in separate thread
        self.running = True
        self.attempts = 0
        self.start_time = time.time()
        
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        
        # Start attack thread
        self.thread = threading.Thread(target=self.run_attack, args=(current_tab,), daemon=True)
        self.thread.start()
        
        # Start timer
        self.update_timer()
        
    def run_attack(self, attack_type):
        """Run the selected attack in a thread"""
        try:
            if attack_type == 0:  # Dictionary
                self.dictionary_attack()
            elif attack_type == 1:  # Brute force
                self.bruteforce_attack()
            elif attack_type == 2:  # Hash cracker
                self.hash_attack()
        except Exception as e:
            self.log(f"Error: {str(e)}")
            self.running = False
            
    def dictionary_attack(self):
        """Perform dictionary attack"""
        target = self.target_var.get()
        dict_path = self.dict_path_var.get()
        
        self.log(f"Starting dictionary attack on target: {target[:10]}...")
        self.log(f"Using dictionary: {dict_path}")
        
        try:
            with open(dict_path, 'r') as f:
                words = [line.strip() for line in f if line.strip()]
                
            # Try variations if enabled
            if self.use_variations.get():
                variations = self.generate_variations(words)
                words.extend(variations)
                
            for word in words:
                if not self.running:
                    break
                    
                # Check if case insensitive
                test_word = word if self.case_sensitive.get() else word.lower()
                test_target = target if self.case_sensitive.get() else target.lower()
                
                self.attempts += 1
                
                if test_word == test_target:
                    self.log(f"[SUCCESS] Found password: {word}")
                    self.log(f"Attempts: {self.attempts}")
                    self.running = False
                    return
                    
                if self.attempts % 100 == 0:
                    self.log(f"Tried {self.attempts} passwords...")
                    
                time.sleep(float(self.delay_var.get()))
                
        except FileNotFoundError:
            self.log(f"Dictionary file not found: {dict_path}")
            
        self.log("Dictionary attack completed - password not found")
        self.running = False
        
    def bruteforce_attack(self):
        """Perform brute force attack"""
        target = self.bf_target_var.get()
        
        # Build character set
        charset = ""
        if self.use_lowercase.get():
            charset += string.ascii_lowercase
        if self.use_uppercase.get():
            charset += string.ascii_uppercase
        if self.use_digits.get():
            charset += string.digits
        if self.use_special.get():
            charset += "!@#$%^&*()"
        if self.custom_charset_var.get():
            charset += self.custom_charset_var.get()
            
        if not charset:
            self.log("Error: No character set selected")
            self.running = False
            return
            
        min_len = int(self.min_length_var.get())
        max_len = int(self.max_length_var.get())
        
        self.log(f"Starting brute force attack on target: {target[:10]}...")
        self.log(f"Character set size: {len(charset)}")
        self.log(f"Trying lengths {min_len} to {max_len}")
        
        # Try all combinations
        for length in range(min_len, max_len + 1):
            if not self.running:
                break
                
            self.log(f"Trying length {length}...")
            
            for combination in itertools.product(charset, repeat=length):
                if not self.running:
                    break
                    
                attempt = ''.join(combination)
                self.attempts += 1
                
                if attempt == target:
                    self.log(f"[SUCCESS] Found password: {attempt}")
                    self.log(f"Attempts: {self.attempts}")
                    self.running = False
                    return
                    
                if self.attempts % 1000 == 0:
                    self.log(f"Tried {self.attempts} combinations...")
                    
                time.sleep(float(self.delay_var.get()))
                
        self.log("Brute force attack completed - password not found")
        self.running = False
        
    def hash_attack(self):
        """Perform hash cracking attack"""
        target_hash = self.hash_target_var.get().strip()
        hash_type = self.hash_type_var.get()
        
        self.log(f"Starting hash crack for {hash_type.upper()}: {target_hash[:20]}...")
        
        # Get wordlist
        if "built-in" in self.hash_wordlist_var.get():
            words = ["password", "123456", "admin", "letmein", "welcome", 
                    "qwerty", "password123", "123456789", "football", "monkey"]
        else:
            try:
                with open(self.hash_wordlist_var.get(), 'r') as f:
                    words = [line.strip() for line in f if line.strip()]
            except:
                self.log("Error loading wordlist")
                self.running = False
                return
                
        for word in words:
            if not self.running:
                break
                
            # Calculate hash
            if hash_type == "md5":
                test_hash = hashlib.md5(word.encode()).hexdigest()
            elif hash_type == "sha1":
                test_hash = hashlib.sha1(word.encode()).hexdigest()
            elif hash_type == "sha256":
                test_hash = hashlib.sha256(word.encode()).hexdigest()
            elif hash_type == "sha512":
                test_hash = hashlib.sha512(word.encode()).hexdigest()
                
            self.attempts += 1
            
            if test_hash == target_hash:
                self.log(f"[SUCCESS] Found match: {word}")
                self.log(f"Hash: {test_hash}")
                self.running = False
                return
                
            if self.attempts % 100 == 0:
                self.log(f"Tried {self.attempts} words...")
                
            time.sleep(float(self.delay_var.get()))
            
        self.log("Hash attack completed - no match found")
        self.running = False
        
    def generate_variations(self, words):
        """Generate common password variations"""
        variations = []
        leet_dict = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'}
        
        for word in words[:50]:  # Limit to first 50 for performance
            # 1337 speak variations
            leet_word = word
            for char, replacement in leet_dict.items():
                leet_word = leet_word.replace(char, replacement)
            variations.append(leet_word)
            
            # Add numbers
            for i in range(10):
                variations.append(f"{word}{i}")
                variations.append(f"{i}{word}")
                
            # Capitalization variations
            variations.append(word.capitalize())
            variations.append(word.upper())
            
        return variations
        
    def update_timer(self):
        """Update timer and statistics"""
        if self.running:
            elapsed = time.time() - self.start_time
            hours, remainder = divmod(elapsed, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            self.time_var.set(f"Time elapsed: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
            
            if elapsed > 0:
                speed = self.attempts / elapsed
                self.speed_var.set(f"Speed: {speed:.1f} attempts/sec")
                
            self.attempts_var.set(f"Attempts: {self.attempts}")
            
            # Schedule next update
            self.root.after(1000, self.update_timer)
        else:
            self.stop_attack()
            
    def stop_attack(self):
        """Stop the current attack"""
        self.running = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.status_var.set("Attack stopped")
        
    def log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        # Thread-safe logging
        self.root.after(0, lambda: self._add_to_log(log_message))
        
    def _add_to_log(self, message):
        """Add message to log text widget"""
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        
    def clear_logs(self):
        """Clear the log text"""
        self.log_text.delete(1.0, tk.END)
        self.attempts_var.set("Attempts: 0")
        self.time_var.set("Time elapsed: 00:00:00")
        self.speed_var.set("Speed: 0 attempts/sec")

def main():
    root = tk.Tk()
    app = BruteForceTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()
