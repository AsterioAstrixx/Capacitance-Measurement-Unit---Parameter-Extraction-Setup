import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import webbrowser  # Import for opening URLs


class CVAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DEPLETION WIDTH CALCULATION SETUP OF HETEROJUNCTION DIODE")
        self.root.geometry("900x750")

        # Constants
        self.q = 1.6e-19  # elementary charge (C)
        self.eps_0 = 8.85e-12  # vacuum permittivity (F/m)
        self.eps_r = 11.7  # relative permittivity for Silicon
        self.eps_s = self.eps_r * self.eps_0  # semiconductor permittivity
        self.A = 1e-6  # junction area in m²

        # Variables to store analysis results
        self.df = None
        self.V_bi = None
        self.V_bi_mod = None
        self.N_A = None
        self.W = None
        self.slope = None
        self.intercept = None
        self.r_value = None

        # Default voltage range for linear regression
        self.min_v = -5.0
        self.max_v = -1.0

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Create heading frame to hold logo and title
        heading_frame = ttk.Frame(self.root)
        heading_frame.pack(fill=tk.X, pady=5)

        # Load and display logo image
        try:
            logo_img = Image.open(r"C:\Users\ankur\Downloads\DATA - Python project Heterojunction\jiitlogo.png")
            logo_img = logo_img.resize((150, 150))  # Adjust size as needed
            self.logo_photo = ImageTk.PhotoImage(logo_img)

            logo_label = ttk.Label(heading_frame, image=self.logo_photo)
            logo_label.pack(side=tk.LEFT, padx=10)
        except Exception as e:
            print(f"Error loading logo: {e}")

        # Application heading (moved to heading_frame)
        heading_label = ttk.Label(
            heading_frame,
            text="DEPLETION WIDTH CALCULATION SETUP OF HETEROJUNCTION DIODE",
            font=("Arial", 14, "bold")
        )
        heading_label.pack(side=tk.LEFT, padx=10)

        # Frame for controls
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)

        # Load data button
        self.load_button = ttk.Button(control_frame, text="Load CSV Data", command=self.load_data)
        self.load_button.pack(side=tk.LEFT, padx=5)

        # Show calculation results button
        self.show_results_button = ttk.Button(control_frame, text="Show Calculation Results",
                                              command=self.show_calculation_results)
        self.show_results_button.pack(side=tk.LEFT, padx=5)
        self.show_results_button["state"] = "disabled"

        # Show calculation steps button
        self.show_steps_button = ttk.Button(control_frame, text="Show Calculation Steps",
                                            command=self.show_calculation_steps)
        self.show_steps_button.pack(side=tk.LEFT, padx=5)
        self.show_steps_button["state"] = "disabled"

        # Show device properties button
        self.show_properties_button = ttk.Button(control_frame, text="Show Device Properties",
                                                 command=self.show_device_properties)
        self.show_properties_button.pack(side=tk.LEFT, padx=5)
        self.show_properties_button["state"] = "disabled"

        # Add button to open URL - project principles
        self.principle_button = tk.Button(
            control_frame,
            text="Principle Working of the Project",
            command=self.open_principle_url,
            bg="pink",  # Pink background
            fg="black",  # Black text
            font=("Arial", 10, "bold")
        )
        self.principle_button.pack(side=tk.LEFT, padx=10)

        # Add LinkedIn connection button
        self.linkedin_button = tk.Button(
            control_frame,
            text="Connect on LinkedIn",
            command=self.open_linkedin_url,
            bg="blue",  # Blue background
            fg="white",  # White text
            font=("Arial", 10, "bold")
        )
        self.linkedin_button.pack(side=tk.LEFT, padx=10)

        # Add junction diagram after the control buttons
        try:
            junction_img = Image.open(r"C:\Users\ankur\Downloads\DATA - Python project Heterojunction\junction.png")
            junction_img = junction_img.resize((350, 250), Image.LANCZOS)  # High-quality resize
            self.junction_photo = ImageTk.PhotoImage(junction_img)

            # Use tk.Label instead of ttk.Label
            junction_label = tk.Label(self.root, image=self.junction_photo)
            junction_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading junction diagram: {e}")

        # Results frame (initially hidden)
        self.results_frame = ttk.LabelFrame(self.root, text="Calculation Results", padding="10")

        # Results labels
        self.v_bi_label = ttk.Label(self.results_frame, text="Built-in Potential (V_bi): ")
        self.v_bi_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)

        self.v_bi_mod_label = ttk.Label(self.results_frame, text="|V_bi|: ")
        self.v_bi_mod_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)

        self.n_a_label = ttk.Label(self.results_frame, text="Carrier Concentration (N_A): ")
        self.n_a_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)

        self.w_label = ttk.Label(self.results_frame, text="Depletion Width (W): ")
        self.w_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)

        self.r_squared_label = ttk.Label(self.results_frame, text="R² Value: ")
        self.r_squared_label.grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)

        # Steps frame (initially hidden)
        self.steps_frame = ttk.LabelFrame(self.root, text="Calculation Steps", padding="10")

        # Steps text
        self.steps_text = tk.Text(self.steps_frame, wrap=tk.WORD, height=8, width=70)
        self.steps_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.steps_text.config(state=tk.DISABLED)

        # Device properties frame (initially hidden)
        self.properties_frame = ttk.LabelFrame(self.root, text="Device Properties", padding="10")

        # Device properties table
        self.properties_tree = ttk.Treeview(self.properties_frame, columns=("Property", "Value"), show="headings",
                                            height=6)
        self.properties_tree.heading("Property", text="Property")
        self.properties_tree.heading("Value", text="Value")
        self.properties_tree.column("Property", width=150)
        self.properties_tree.column("Value", width=350)
        self.properties_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Graph selection buttons frame
        graph_buttons_frame = ttk.LabelFrame(self.root, text="Select Graph to Display", padding="10")
        graph_buttons_frame.pack(fill=tk.X, padx=10, pady=5)

        # Buttons for each graph
        self.inv_c2_button = ttk.Button(graph_buttons_frame, text="1/C² vs. V",
                                        command=lambda: self.show_graph("inv_c2"))
        self.inv_c2_button.grid(row=0, column=0, padx=5, pady=5)

        self.c_button = ttk.Button(graph_buttons_frame, text="C vs. V", command=lambda: self.show_graph("c"))
        self.c_button.grid(row=0, column=1, padx=5, pady=5)

        self.g_button = ttk.Button(graph_buttons_frame, text="G vs. V", command=lambda: self.show_graph("g"))
        self.g_button.grid(row=0, column=2, padx=5, pady=5)

        self.all_button = ttk.Button(graph_buttons_frame, text="All Graphs", command=lambda: self.show_graph("all"))
        self.all_button.grid(row=0, column=3, padx=5, pady=5)

        # Frame for the graph
        self.graph_frame = ttk.Frame(self.root, padding="10")
        self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready. Load a CSV file to begin.")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Disable buttons initially
        self.toggle_buttons(False)

    # Function to open the LinkedIn URL
    def open_linkedin_url(self):
        """Open the LinkedIn profile URL in the default web browser"""
        url = "https://www.linkedin.com/in/ankur-majumdar-487824278/"
        webbrowser.open(url)
        self.status_var.set("Opening LinkedIn profile in web browser...")

    # Function to open the project principles URL
    def open_principle_url(self):
        """Open the project principles URL in the default web browser"""
        url = "https://miro.com/app/board/uXjVI96mjk4=/?share_link_id=678813090497"
        webbrowser.open(url)
        self.status_var.set("Opening project principles in web browser...")

    def toggle_buttons(self, state):
        """Enable or disable all interactive buttons"""
        for button in [self.inv_c2_button, self.c_button, self.g_button, self.all_button,
                       self.show_results_button, self.show_steps_button, self.show_properties_button]:
            if state:
                button["state"] = "normal"
            else:
                button["state"] = "disabled"

    def load_data(self):
        """Load CSV data"""
        file_path = filedialog.askopenfilename(
            title="Select CV Data File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not file_path:
            return

        try:
            self.df = pd.read_csv(file_path)
            self.status_var.set(f"Loaded {file_path}")

            # Clean column names
            self.df.columns = self.df.columns.str.strip()

            # Verify required columns
            required_cols = ["VBias", "C", "G"]
            missing_cols = [col for col in required_cols if col not in self.df.columns]

            if missing_cols:
                messagebox.showerror("Missing Columns",
                                     f"The following required columns are missing: {', '.join(missing_cols)}")
                self.df = None
                return

            # Calculate 1/C²
            self.df['1/C^2'] = 1 / (self.df['C'] ** 2)

            # Extract device properties
            self.extract_device_properties()

            messagebox.showinfo("Data Loaded", f"Successfully loaded {len(self.df)} data points.")
            self.analyze_data()  # Run analysis automatically

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            self.df = None

    def extract_device_properties(self):
        """Extract device properties from loaded CSV"""
        self.device_properties = {}

        # Properties to extract
        property_columns = ["Record Time", "Monitor Unit", "Frequency", "Batch ID", "Record Date"]

        # Check for each property column
        for prop in property_columns:
            try:
                if prop in self.df.columns:
                    # Get first non-null value for the property
                    values = self.df[prop].dropna()
                    if len(values) > 0:
                        self.device_properties[prop] = values.iloc[0]
                    else:
                        self.device_properties[prop] = "N/A"
                else:
                    self.device_properties[prop] = "N/A"
            except:
                self.device_properties[prop] = "N/A"

        # Add additional calculated properties
        self.device_properties["Number of Data Points"] = len(self.df)
        self.device_properties["Voltage Range"] = f"{self.df['VBias'].min():.2f} V to {self.df['VBias'].max():.2f} V"

    def analyze_data(self):
        """Perform CV analysis on the loaded data"""
        if self.df is None:
            messagebox.showwarning("No Data", "Please load a CSV file first.")
            return

        try:
            # Select linear region for regression
            steep_region = self.df[(self.df['VBias'] >= self.min_v) & (self.df['VBias'] <= self.max_v)]

            if len(steep_region) < 2:
                messagebox.showerror("Error", "Not enough data points in the selected voltage range.")
                return

            V_steep = steep_region['VBias']
            invC2_steep = steep_region['1/C^2']

            # Linear regression
            self.slope, self.intercept, self.r_value, p_value, std_err = linregress(V_steep, invC2_steep)

            # Extract parameters
            self.V_bi = -self.intercept / self.slope
            self.V_bi_mod = abs(self.V_bi)
            self.N_A = 2 / (self.q * self.eps_s * self.A ** 2 * self.slope)
            self.W = np.sqrt(2 * self.eps_s * self.V_bi_mod / (self.q * self.N_A)) * 1e9  # nm

            # Update results display
            self.v_bi_label.config(text=f"Built-in Potential (V_bi): {self.V_bi:.4f} V")
            self.v_bi_mod_label.config(text=f"|V_bi|: {self.V_bi_mod:.4f} V")
            self.n_a_label.config(text=f"Carrier Concentration (N_A): {self.N_A:.4e} m⁻³ = {self.N_A / 1e6:.4e} cm⁻³")
            self.w_label.config(text=f"Depletion Width (W): {self.W:.4f} nm")
            self.r_squared_label.config(text=f"R² Value: {self.r_value ** 2:.4f}")

            # Prepare calculation steps text
            self.prepare_calculation_steps()

            # Enable buttons
            self.toggle_buttons(True)

            # Show all graphs by default
            self.show_graph("all")

            self.status_var.set(
                f"Analysis completed successfully. {len(steep_region)} points used for linear regression.")

        except Exception as e:
            messagebox.showerror("Analysis Error", f"Error during analysis: {str(e)}")

    def prepare_calculation_steps(self):
        """Prepare the calculation steps text"""
        steps = f"""
1. Plotting C-V Characteristics:
   - Generated 1/C² vs. V plot
   - Selected voltage range: {self.min_v} V to {self.max_v} V
   - Linear regression performed on selected range
   - Found linear relationship: 1/C² = {self.slope:.4e} × V + {self.intercept:.4e}
   - R² value: {self.r_value ** 2:.4f}

2. Extracting Key Parameters:
   - Built-in Potential (V_bi): -intercept/slope = -({self.intercept:.4e})/({self.slope:.4e}) = {self.V_bi:.4f} V
   - Carrier Concentration (N_A): 2/(q × εs × A² × slope)
     = 2/({self.q} × {self.eps_s} × {self.A ** 2} × {self.slope})
     = {self.N_A:.4e} m⁻³

3. Calculating Depletion Width:
   - Using formula: W = √(2εs|V_bi|/(q × N_A))
   - W = √(2 × {self.eps_s} × {self.V_bi_mod})/({self.q} × {self.N_A})
   - W = {self.W:.4f} nm (with V_ext = 0)
"""
        self.calculation_steps = steps

    def show_calculation_results(self):
        """Show the calculation results frame"""
        # Hide other frames if visible
        self.hide_info_frames()

        # Show results frame
        if not self.results_frame.winfo_ismapped():
            self.results_frame.pack(fill=tk.X, padx=10, pady=5, before=self.graph_frame)
        else:
            self.results_frame.pack_forget()

    def show_calculation_steps(self):
        """Show the calculation steps frame"""
        # Hide other frames if visible
        self.hide_info_frames()

        # Show steps frame
        if not self.steps_frame.winfo_ismapped():
            self.steps_frame.pack(fill=tk.X, padx=10, pady=5, before=self.graph_frame)
            self.steps_text.config(state=tk.NORMAL)
            self.steps_text.delete(1.0, tk.END)
            self.steps_text.insert(tk.END, self.calculation_steps)
            self.steps_text.config(state=tk.DISABLED)
        else:
            self.steps_frame.pack_forget()

    def show_device_properties(self):
        """Show the device properties frame"""
        # Hide other frames if visible
        self.hide_info_frames()

        # Show properties frame
        if not self.properties_frame.winfo_ismapped():
            self.properties_frame.pack(fill=tk.X, padx=10, pady=5, before=self.graph_frame)

            # Clear existing items
            for item in self.properties_tree.get_children():
                self.properties_tree.delete(item)

            # Add device properties to treeview
            for prop, value in self.device_properties.items():
                self.properties_tree.insert("", "end", values=(prop, value))

        else:
            self.properties_frame.pack_forget()

    def hide_info_frames(self):
        """Hide all information frames"""
        if self.results_frame.winfo_ismapped():
            self.results_frame.pack_forget()
        if self.steps_frame.winfo_ismapped():
            self.steps_frame.pack_forget()
        if self.properties_frame.winfo_ismapped():
            self.properties_frame.pack_forget()

    def clear_graph_frame(self):
        """Clear the current graph"""
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

    def show_graph(self, graph_type):
        """Display the selected graph"""
        if self.df is None:
            return

        self.clear_graph_frame()

        if graph_type == "all":
            fig = Figure(figsize=(7, 8), dpi=100)

            # 1/C² vs V plot
            ax1 = fig.add_subplot(311)
            self.plot_inv_c2(ax1)

            # C vs V plot
            ax2 = fig.add_subplot(312)
            self.plot_c(ax2)

            # G vs V plot
            ax3 = fig.add_subplot(313)
            self.plot_g(ax3)

            fig.tight_layout()

        else:
            fig = Figure(figsize=(7, 5), dpi=100)
            ax = fig.add_subplot(111)

            if graph_type == "inv_c2":
                self.plot_inv_c2(ax)
            elif graph_type == "c":
                self.plot_c(ax)
            elif graph_type == "g":
                self.plot_g(ax)

        # Add figure to tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_inv_c2(self, ax):
        """Plot 1/C² vs V graph"""
        V = self.df['VBias']
        invC2 = self.df['1/C^2']

        # Select linear region
        steep_region = self.df[(self.df['VBias'] >= self.min_v) & (self.df['VBias'] <= self.max_v)]
        V_steep = steep_region['VBias']
        invC2_steep = steep_region['1/C^2']

        # Plot data points
        ax.scatter(V, invC2 * 1e-24, color='blue', alpha=0.6, label='All data')
        ax.scatter(V_steep, invC2_steep * 1e-24, color='red', label='Selected region')

        # Plot regression line
        x_fit = np.linspace(min(V), max(V), 100)
        y_fit = (self.slope * x_fit + self.intercept) * 1e-24
        ax.plot(x_fit, y_fit, 'r--', label=f'Fit (R² = {self.r_value ** 2:.4f})')

        # Plot V_bi if within reasonable range
        if -2 * max(abs(V)) < self.V_bi < 2 * max(abs(V)):
            ax.axvline(self.V_bi, color='green', linestyle='--', label=f'V_bi = {self.V_bi:.2f} V')

        ax.set_xlabel('Voltage (V)')
        ax.set_ylabel('1/C² (F⁻² × 10²⁴)')
        ax.set_title('1/C² vs. V')
        ax.grid(True, alpha=0.3)
        ax.legend()

    def plot_c(self, ax):
        """Plot C vs V graph"""
        V = self.df['VBias']
        C = self.df['C']

        ax.scatter(V, C * 1e12, color='purple')
        ax.set_xlabel('Voltage (V)')
        ax.set_ylabel('Capacitance (pF)')
        ax.set_title('C vs. V')
        ax.grid(True, alpha=0.3)

    def plot_g(self, ax):
        """Plot G vs V graph"""
        V = self.df['VBias']
        G = self.df['G']

        ax.plot(V, G * 1e6, color='orange')
        ax.set_xlabel('Voltage (V)')
        ax.set_ylabel('Conductance (µS)')
        ax.set_title('G vs. V')
        ax.grid(True, alpha=0.3)


if __name__ == "__main__":
    root = tk.Tk()
    app = CVAnalysisApp(root)
    root.mainloop()