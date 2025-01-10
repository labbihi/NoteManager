import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, simpledialog
from entities import *
import pandas as pd
from datetime import datetime


class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Étudiants et Notes")
        self.root.geometry("900x700")

        style = ttk.Style("cosmo")  # You can change the theme here

        self.create_header()
        self.create_main_content()
        self.create_footer()

        self.selected_class = None
        self.selected_evaluation = None

        self.classes = session.query(MClass).all()
        self.groups = session.query(Group).all()
        self.evaluations = session.query(Evalution).all()

    def create_header(self):
        header = ttk.Frame(self.root, bootstyle=DARK)
        header.pack(side=TOP, fill=X)
        ttk.Label(
            header, text="Gestion des Étudiants et Notes", font=("Helvetica", 18), bootstyle=(INVERSE)
        ).pack(pady=10)

    def create_main_content(self):
        self.main_content = ttk.Frame(self.root)
        self.main_content.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)

        # Sidebar
        self.sidebar = ttk.Frame(self.main_content, bootstyle=SECONDARY)
        self.sidebar.pack(side=LEFT, fill=Y)

        ttk.Button(self.sidebar, text="Classes", command=self.show_classes_and_students).pack(pady=5, padx=5)
        ttk.Button(self.sidebar, text="Groupes", command=self.show_groups).pack(pady=5, padx=5)
        ttk.Button(self.sidebar, text="Évaluations", command=self.show_evaluations).pack(pady=5, padx=5)
        ttk.Button(self.sidebar, text="Affectation", command=self.assign_group).pack(pady=5, padx=5)
        ttk.Button(self.sidebar, text="Notes", command=self.manage_notes).pack(pady=5, padx=5)

        self.content_frame = ttk.Frame(self.main_content)
        self.content_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

    def create_footer(self):
        footer = ttk.Frame(self.root, bootstyle=PRIMARY)
        footer.pack(side=BOTTOM, fill=X)
        self.lbl_status = ttk.Label(footer, text="Statut : Prêt", font=("Arial", 10), bootstyle=LIGHT)
        self.lbl_status.pack(pady=5)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_classes_and_students(self):
        self.clear_content_frame()
        ttk.Label(self.content_frame, text="Gestion des Classes et Étudiants", font=("Arial", 16)).pack(pady=10)

        frame_classes = ttk.Frame(self.content_frame, padding=10)
        frame_students = ttk.Frame(self.content_frame, padding=10)

        frame_classes.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        frame_students.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        ttk.Label(frame_classes, text="Gestion des Classes :", font=("Arial", 12)).grid(row=0, column=0, columnspan=3, pady=5)
        self.listbox_classes = ttk.Listbox(frame_classes, height=10, width=30)
        self.listbox_classes.grid(row=1, column=0, columnspan=3, pady=5)
        self.listbox_classes.bind("<<ListboxSelect>>", self.on_class_select)

        ttk.Button(frame_classes, text="Ajouter", command=self.add_class).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(frame_classes, text="Modifier", command=self.modify_class).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(frame_classes, text="Supprimer", command=self.delete_class).grid(row=2, column=2, padx=5, pady=5)

        self.treeview_students = ttk.Treeview(frame_students, columns=("Code", "Name", "Email"), show="headings")
        self.treeview_students.heading("Code", text="Code Massar")
        self.treeview_students.heading("Name", text="Nom")
        self.treeview_students.heading("Email", text="Email")
        self.treeview_students.pack(pady=5, padx=5)

    def on_class_select(self, event):
        selected_index = self.listbox_classes.curselection()
        if selected_index:
            selected_class_name = self.listbox_classes.get(selected_index[0])
            self.selected_class = next((cls for cls in self.classes if cls.name == selected_class_name), None)
            if self.selected_class:
                self.refresh_students()

    def refresh_students(self):
        for item in self.treeview_students.get_children():
            self.treeview_students.delete(item)
        if self.selected_class:
            for student in self.selected_class.students:
                self.treeview_students.insert("", "end", values=(student.code, student.name, student.email))

    def add_class(self):
        new_name = simpledialog.askstring("Nouvelle Classe", "Nom de la classe :")
        if new_name:
            new_class = MClass(name=new_name, year=2025)
            new_class.save()
            self.classes.append(new_class)
            self.refresh_classes()

    def modify_class(self):
        pass

    def delete_class(self):
        pass

    def show_groups(self):
        pass

    def show_evaluations(self):
        pass

    def assign_group(self):
        pass

    def manage_notes(self):
        pass


if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = StudentManagementApp(root)
    root.mainloop()
