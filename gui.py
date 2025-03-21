import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import os
import requests

# Hugging Face API settings
API_URL = "https://api-inference.huggingface.co/models/villefrancisco/finetuned_modelLegal"
API_TOKEN = "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"  # Replace with your token

# Function to summarize text using Hugging Face Inference API
def summarize_text(text):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": 2900,  # Adjust as needed
            "min_length": 50,
            "do_sample": False,
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            summary = result[0].get("generated_text", "Summary not found.")
        else:
            summary = "Summary not found."
        return summary
    except Exception as e:
        return f"Error generating summary: {str(e)}"

# Function to handle file upload
def upload_files():
    file_paths = filedialog.askopenfilenames(
        title="Select Files",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    
    if file_paths:
        for file_path in file_paths:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    text = file.read()
                
                # Generate summary using the Hugging Face API
                summary = summarize_text(text)
                
                # Save the summary to a file
                summary_name = summary.split("\n")[0].strip()
                summary_name = "".join(c for c in summary_name if c.isalnum() or c in (" ", "_"))
                summary_file = os.path.join("summaries", f"{summary_name}.txt")
                
                # Ensure the file name is unique
                counter = 1
                while os.path.exists(summary_file):
                    summary_file = os.path.join("summaries", f"{summary_name}_{counter}.txt")
                    counter += 1
                
                with open(summary_file, "w", encoding="utf-8") as f:
                    f.write(summary)
                
                # Update the sidebar with the new summary
                update_sidebar()
                
                # Display the file name and summary in the text area
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"File: {file_path}\n")
                result_text.insert(tk.END, f"Summary:\n{summary}\n\n")
            except Exception as e:
                messagebox.showerror("Error", f"Error processing {file_path}: {str(e)}")

# Function to update the sidebar with saved summaries
def update_sidebar():
    # Clear the sidebar
    for widget in sidebar_frame.winfo_children():
        widget.destroy()
    
    # Load saved summaries
    for file_name in os.listdir("summaries"):
        if file_name.endswith(".txt"):
            # Create a button for each summary
            summary_button = tk.Button(
                sidebar_frame,
                text=file_name[:-4],  # Remove .txt extension
                width=20,
                command=lambda f=file_name: load_summary(f)
            )
            summary_button.pack(pady=5)

# Function to load a summary into the text area
def load_summary(file_name):
    summary_file = os.path.join("summaries", file_name)
    with open(summary_file, "r", encoding="utf-8") as f:
        summary = f.read()
    result_text.delete(1.0, tk.END)  # Clear the text area
    result_text.insert(tk.END, summary)

# Function to copy the current summary to the clipboard
def copy_summary():
    # Get the text from the text area
    summary = result_text.get(1.0, tk.END)
    if summary.strip():
        # Copy the text to the clipboard
        root.clipboard_clear()
        root.clipboard_append(summary)
        root.update()  # Required to finalize the clipboard update
        status_label.config(text="Summary copied to clipboard!")
    else:
        status_label.config(text="No summary to copy!")

# Function to delete the currently displayed summary
def delete_summary():
    # Get the currently displayed summary
    summary = result_text.get(1.0, tk.END).strip()
    if not summary:
        messagebox.showwarning("No Summary", "No summary is currently displayed.")
        return
    
    # Find the corresponding file in the summaries directory
    for file_name in os.listdir("summaries"):
        summary_file = os.path.join("summaries", file_name)
        try:
            with open(summary_file, "r", encoding="utf-8") as f:
                file_content = f.read().strip()
            if file_content == summary:
                # Close the file explicitly
                f.close()
                # Delete the file
                os.remove(summary_file)
                # Update the sidebar
                update_sidebar()
                # Clear the text area
                result_text.delete(1.0, tk.END)
                status_label.config(text="Summary deleted successfully!")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting {file_name}: {str(e)}")
            return
    
    # If no matching file was found
    messagebox.showwarning("File Not Found", "The corresponding summary file could not be found.")

# Create the main window
root = tk.Tk()
root.title("Legal Document Summarizer")
root.geometry("800x500")  # Set window size

# Create a sidebar frame with a scrollbar
sidebar_frame = tk.Frame(root, width=200, bg="lightgray")
sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

# Add a canvas and scrollbar to the sidebar
canvas = tk.Canvas(sidebar_frame, bg="lightgray")
scrollbar = ttk.Scrollbar(sidebar_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="lightgray")

# Configure the canvas
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Pack the canvas and scrollbar
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Create a main content frame
content_frame = tk.Frame(root)
content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Create a button to upload files
upload_button = tk.Button(content_frame, text="Upload Files", command=upload_files)
upload_button.pack(pady=10)

# Create a scrollable text area to display results
result_text = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD, width=70, height=20)
result_text.pack(padx=10, pady=10)

# Create a button to copy the current summary
copy_button = tk.Button(content_frame, text="Copy Summary", command=copy_summary)
copy_button.pack(pady=5)

# Create a button to delete the current summary
delete_button = tk.Button(content_frame, text="Delete Summary", command=delete_summary)
delete_button.pack(pady=5)

# Create a status label to show messages
status_label = tk.Label(content_frame, text="", fg="green")
status_label.pack(pady=5)

# Update the sidebar with saved summaries when the program starts
update_sidebar()

# Run the GUI
root.mainloop()