import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import json
import os


# ========================================================================== #
# ================================ INFO ==================================== #
# ========================================================================== #
# Adds and Searches for contacts stored in a json file. 
# ========================================================================== #
# ================================ TODO ==================================== #
# ========================================================================== #
# TODO: 
# ========================================================================== #


CONTACTS_DATA = "./contacts.json"


def add_contact():
    """
    Add a new contact to the contact book.

    This function retrieves the company name, client name, phone number, 
    and email address from the respective Tkinter entry widgets. It then 
    creates a new contact dictionary with these details and appends it to 
    the contacts list stored in a JSON file. If the JSON file does not 
    exist, it creates a new one. After successfully adding the contact, 
    it clears the entry fields and shows a success message. If the client 
    name or phone number is missing, it shows a warning message.

    Parameters:
    None

    Returns:
    None
    """
    company = entry_company.get()
    client = entry_client.get()
    phone = entry_phone.get()
    email = entry_email.get()

    if client and phone:
        new_contact = {
            "company": company if company else "N/A", 
            "client": client, 
            "phone": phone,
            "email": email if email else "N/A",
        }

        if os.path.exists(CONTACTS_DATA):
            with open(CONTACTS_DATA, 'r') as file:
                contacts = json.load(file)
        else:
            contacts = []

        contacts.append(new_contact)

        with open(CONTACTS_DATA, 'w') as file:
            json.dump(contacts, file, indent=4)

        messagebox.showinfo("Success", "Contact added successfully!")
        entry_company.delete(0, tk.END)
        entry_client.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        entry_email.delete(0, tk.END)
    
    else:
        messagebox.showwarning("Input Error", 
                               "Client name and phone number are required!")


def show_results(results):
    """
    Display the search results in a new Tkinter window.

    This function creates a new top-level window to display the search 
    results. It uses a ScrolledText widget to show the details of each 
    contact found in the search. Each contact's company name, client name, 
    phone number, and email address are displayed in the ScrolledText 
    widget.

    Parameters:
    results (list): A list of dictionaries, where each dictionary contains 
                    the details of a contact (company, client, phone, email).

    Returns:
    None
    """

    def save_changes():
        """
        Save the updated contact information from the ScrolledText widget.

        This function retrieves the updated contact information from the 
        ScrolledText widget, parses it, and updates the contacts list stored 
        in the JSON file. It then saves the updated contacts list back to the 
        JSON file and displays a success message. The function also closes the 
        search results window after saving the changes.

        Parameters:
        None

        Returns:
        None
        """
        updated_text = result_text.get("1.0", tk.END).strip()
        updated_contacts = []
        for contact_text in updated_text.split("\n\n"):
            lines = contact_text.split("\n")
            if len(lines) == 4:
                company = lines[0].split(": ")[1]
                client = lines[1].split(": ")[1]
                phone = lines[2].split(": ")[1]
                email = lines[3].split(": ")[1]
                updated_contacts.append({
                    "company": company,
                    "client": client,
                    "phone": phone,
                    "email": email
                })
        
        with open(CONTACTS_DATA, 'w') as file:
            json.dump(updated_contacts, file, indent=4)
        
        messagebox.showinfo("Success", "Changes saved successfully!")
        result_window.destroy()

    result_window = tk.Toplevel(root)
    result_window.title("Search Results")
    result_window.geometry("400x500")

    result_text = ScrolledText(result_window, wrap=tk.WORD, font=("Helvetica", 12))
    result_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    for contact in results:
        result_text.insert(tk.END, f"Company: {contact['company']}\n")
        result_text.insert(tk.END, f"Client: {contact['client']}\n")
        result_text.insert(tk.END, f"Phone: {contact['phone']}\n")
        result_text.insert(tk.END, f"Email: {contact['email']}\n")
        result_text.insert(tk.END, "\n")

    result_text.config(state=tk.NORMAL)

    save_button = tk.Button(result_window, text="Save Changes", 
                            command=save_changes)
    save_button.pack(side=tk.RIGHT, padx=10, pady=10)


def search_contact():
    """
    Search for contacts in the contact book based on the search term.

    This function retrieves the search term from the Tkinter entry widget 
    and searches for contacts in the JSON file that match the search term 
    in either the company name or client name. If matching contacts are 
    found, it displays the results in a new Tkinter window. If no matches 
    are found, it shows an information message. If the search term is 
    empty, it shows a warning message.

    Parameters:
    None

    Returns:
    None
    """
    search_term = entry_search.get()

    if not search_term:
        messagebox.showwarning("Input Error", "Search field is required!")
        return

    if os.path.exists(CONTACTS_DATA):
        with open(CONTACTS_DATA, 'r') as file:
            contacts = json.load(file)

        results = [
                    contact for contact in contacts 
                   if (search_term.lower() in contact['company'].lower() or 
                       search_term.lower() in contact['client'].lower())
                    ]

        if results:
            show_results(results)
        else:
            messagebox.showinfo("No Results", "No contacts found.")
    else:
        messagebox.showinfo("No Contacts", "No contacts available to search.")

    entry_search.delete(0, tk.END)

# ========================================================================== #
# ================================ GUI ===================================== #
# ========================================================================== #
root = tk.Tk()
root.title("Contact Book")
root.config(padx=25, pady=25)

# Labels and entry fields for contact information
tk.Label(root, text="Company Name:").grid(row=0, column=0, padx=10, pady=5)
entry_company = tk.Entry(root, width=30)
entry_company.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="*Client Name:").grid(row=1, column=0, padx=10, pady=5)
entry_client = tk.Entry(root, width=30)
entry_client.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="*Phone Number:").grid(row=2, column=0, padx=10, pady=5)
entry_phone = tk.Entry(root, width=30)
entry_phone.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Email:").grid(row=3, column=0, padx=10, pady=5)
entry_email = tk.Entry(root, width=30)
entry_email.grid(row=3, column=1, padx=10, pady=5)

# Buttons to add and search  contacts
tk.Button(root, text="Add Contact", command=add_contact).grid(row=4, 
                                    column=1, columnspan=2, pady=10)
tk.Label(root, text="Search:").grid(row=5, column=0, padx=10, pady=5)
entry_search = tk.Entry(root, width=30)
entry_search.grid(row=5, column=1, padx=10, pady=5)
tk.Button(root, text="Search Contacts", command=search_contact).grid(row=6, 
                                        column=1, columnspan=2, pady=10)


root.mainloop()
