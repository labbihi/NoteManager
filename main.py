from datetime import datetime
from tkinter import *
from tkinter import ttk
#import pandas as pd
from tkinter import simpledialog  # Import simpledialog


# Model Definitions
class Student:
    def __init__(self, id, name, email, group_name):
        self.id = id
        self.name = name
        self.birthdate = datetime
        self.email = email
        self.group_name = group_name

    def __repr__(self):
        return f"Student(ID: {self.id}, Name: {self.name}, Email: {self.email}, Group: {self.group_name})"


class Group:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Group(Name: {self.name}, Students: {len(self.students)}, Evaluation: {self.evaluation})"


class MClass:
    def __init__(self, name):
        self.name = name
        self.groups = {}
        self.students = []

    def add_group(self, group):
        if group.name not in self.groups:
            self.groups[group.name] = group

    def remove_group(self, group_name):
        if group_name in self.groups:
            del self.groups[group_name]

    def add_student(self, student):
        self.students.append(student)


    def __repr__(self):
        return f"MClass(Name: {self.name}, Groups: {len(self.groups)})"


class ClassGroup:
    def __init__(self, mclass, group, evaluation=None):
        self.mclass = mclass
        self.group = group
        self.evaluation = evaluation
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def set_evaluation(self, mark):
        self.evaluation = mark

    def __repr__(self):
        return f"ClassGroup(MClass: {self.mclass.name}, Group: {self.group.name}, Evaluation: {self.evaluation})"


# Function to Load Data and Create Objects
def load_data(file_path):
    # Load Excel data
    df = pd.read_excel(file_path, sheet_name="NotesCC")

    # Replace the column names below with the actual names from your Excel sheet
    column_mapping = {
        "MClasse": "MClass",
        "Groupe": "Group",
        "Nom": "Name",
        "Email": "Email",
        "Note": "Mark"
    }

    df.rename(columns=column_mapping, inplace=True)

    # Dictionaries to store classes and groups
    classes = {}

    for _, row in df.iterrows():
        class_name = row["MClass"]
        group_name = row["Group"]
        student_name = row["Name"]
        student_email = row["Email"]
        mark = row["Mark"]

        # Add class
        if class_name not in classes:
            classes[class_name] = MClass(class_name)

        # Add group to class
        class_obj = classes[class_name]
        if group_name not in class_obj.groups:
            group = Group(group_name)
            group.set_evaluation(mark)
            class_obj.add_group(group)
        else:
            group = class_obj.groups[group_name]

        # Add student to group
        student = Student(id=len(group.students) + 1, name=student_name, email=student_email, group_name=group_name)
        group.add_student(student)

    return classes


class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Project")
        self.root.geometry("800x700")
        self.root.config(bg="#f4e1e0")

        self.create_header()
        self.create_main_content()
        self.create_footer()

        self.classes = [MClass("Classe 1"), MClass("Classe 2"), MClass("Classe 3")]
        self.current_class = self.classes[0]  # Default class selection

        # Add some example groups to the classes
        group_a = Group("Groupe A")
        group_b = Group("Groupe B")
        self.current_class.add_group(group_a)
        self.current_class.add_group(group_b)

    def create_header(self):
        """Créer l'en-tête de l'application."""
        header = Frame(self.root, bg="#333", height=50)
        header.pack(side="top", fill="x")
        Label(header, text="Gestion des Étudiants", bg="#333", fg="white", font=("Arial", 16)).pack(pady=10)

    def create_main_content(self):
        """Créer la zone principale contenant la barre latérale et la zone de contenu."""
        self.main_content = Frame(self.root, bg="#f4e1e0")
        self.main_content.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Sidebar
        self.sidebar = Frame(self.main_content, bg="#555", width=200)
        self.sidebar.pack(side="left", fill="y")

        Button(self.sidebar, text="Classes", bg="#777", fg="white", command=self.show_classes_and_students,
               width=15).pack(pady=5, padx=5)
        Button(self.sidebar, text="Groupes", bg="#777", fg="white", command=self.show_groups, width=15).pack(pady=5,
                                                                                                             padx=5)
        Button(self.sidebar, text="Évaluation", bg="#777", fg="white", command=self.show_evaluation, width=15).pack(
            pady=5, padx=5)

        # Zone de contenu principale
        self.content_frame = Frame(self.main_content, bg="#f4e1e0")
        self.content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)





    def create_footer(self):
        """Créer le pied de page."""
        footer = Frame(self.root, bg="#333", height=30)
        footer.pack(side="bottom", fill="x")
        self.lbl_status = Label(footer, text="Statut : Prêt", bg="#333", fg="white", font=("Arial", 10))
        self.lbl_status.pack(pady=5)

    def clear_content_frame(self):
        """Supprimer tous les widgets du content_frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_classes_and_students(self):
        """Afficher les classes et les étudiants dans le même cadre."""
        self.clear_content_frame()

        # Title
        Label(self.content_frame, text="Gestion des Classes et Etudiants", bg="#f4e1e0", font=("Arial", 16)).grid(
            row=0, column=0, columnspan=3, pady=10)

        # Frame for class management buttons
        Label(self.content_frame, text="Gestion des Classes :", bg="#f4e1e0", font=("Arial", 12)).grid(
            row=1, column=0, pady=5)

        Button(self.content_frame, text="Ajouter Classe", command=self.add_class).grid(row=2, column=0, padx=5, pady=5)
        Button(self.content_frame, text="Modifier Classe", command=self.modify_class).grid(row=2, column=1, padx=5,
                                                                                           pady=5)
        Button(self.content_frame, text="Supprimer Classe", command=self.delete_class).grid(row=2, column=2, padx=5,
                                                                                            pady=5)

        # Listbox for displaying classes
        Label(self.content_frame, text="Liste des classes :", bg="#f4e1e0", font=("Arial", 12)).grid(
            row=3, column=0, pady=5)

        self.listbox_classes = Listbox(self.content_frame, height=10, width=30)
        self.listbox_classes.grid(row=4, column=0, padx=10, pady=5)

        # Fill listbox with classes
        for mclass in self.classes:
            self.listbox_classes.insert(END, mclass.name)

        # Bind action to class selection
        self.listbox_classes.bind("<<ListboxSelect>>", self.on_class_select)

        # Frame for student management buttons
        Label(self.content_frame, text="Gestion des Etudiants :", bg="#f4e1e0", font=("Arial", 12)).grid(
            row=1, column=1, padx=10, pady=5)

        Button(self.content_frame, text="Ajouter Etudiant", command=self.add_student).grid(row=2, column=3, padx=5,
                                                                                           pady=5)
        Button(self.content_frame, text="Modifier Etudiant", command=self.modify_student).grid(row=2, column=4, padx=5,
                                                                                               pady=5)
        Button(self.content_frame, text="Supprimer Etudiant", command=self.delete_student).grid(row=2, column=5, padx=5,
                                                                                                pady=5)

        # Treeview for displaying students
        Label(self.content_frame, text="Liste des étudiants :", bg="#f4e1e0", font=("Arial", 12)).grid(
            row=3, column=1, pady=5)

        self.treeview_students = ttk.Treeview(self.content_frame, columns=("ID", "Name", "Email", "Group"),
                                              show="headings")
        self.treeview_students.heading("ID", text="ID")
        self.treeview_students.heading("Name", text="Nom")
        self.treeview_students.heading("Email", text="Email")
        self.treeview_students.heading("Group", text="Groupe")

        self.treeview_students.column("ID", width=100)
        self.treeview_students.column("Name", width=150)
        self.treeview_students.column("Email", width=200)
        self.treeview_students.column("Group", width=100)

        self.treeview_students.grid(row=4, column=1, padx=10, pady=5, columnspan=6)

    def on_class_select(self, event):
        """Afficher la liste des étudiants pour la classe sélectionnée."""
        selected_index = self.listbox_classes.curselection()
        if selected_index:
            selected_class_name = self.listbox_classes.get(selected_index[0])
            self.selected_class = next((cls for cls in self.classes if cls.name == selected_class_name), None)
            if self.selected_class:
                self.show_students()

    def show_students(self):
        """Mettre à jour la liste des étudiants dans le Treeview."""
        if self.selected_class:
            # Vider le Treeview avant de le remplir
            for item in self.treeview_students.get_children():
                self.treeview_students.delete(item)

            for student in self.selected_class.students:
                self.treeview_students.insert("", "end",
                                              values=(student.id, student.name, student.email, student.group_name))

    def add_class(self):
        """Ajouter une nouvelle classe."""
        new_name = simpledialog.askstring("Nouvelle Classe", "Nom de la classe :")
        if new_name:
            new_class = MClass(new_name)
            self.classes.append(new_class)
            self.refresh_classes()

    def modify_class(self):
        """Modifier le nom d'une classe."""
        selected_class = self.listbox_classes.curselection()
        if selected_class:
            selected_class = selected_class[0]
            old_name = self.classes[selected_class].name
            new_name = simpledialog.askstring("Modifier Classe", f"Modifier le nom de la classe '{old_name}' :")
            if new_name:
                self.classes[selected_class].name = new_name
                self.refresh_classes()

    def delete_class(self):
        """Supprimer une classe."""
        selected_class = self.listbox_classes.curselection()
        if selected_class:
            selected_class = selected_class[0]
            del self.classes[selected_class]
            self.refresh_classes()

    def refresh_classes(self):
        """Recharger la liste des classes."""
        self.listbox_classes.delete(0, END)
        for mclass in self.classes:
            self.listbox_classes.insert(END, mclass.name)

    def add_student(self):
        """Ajouter un étudiant à la classe sélectionnée."""
        if not self.selected_class:
            return
        id = simpledialog.askstring("ID Etudiant", "ID de l'étudiant :")
        name = simpledialog.askstring("Nom Etudiant", "Nom de l'étudiant :")
        email = simpledialog.askstring("Email Etudiant", "Email de l'étudiant :")
        group_name = simpledialog.askstring("Groupe Etudiant", "Nom du groupe :")
        if id and name and email and group_name:
            student = Student(id, name, email, group_name)
            self.selected_class.students.append(student)
            self.show_students()

    def modify_student(self):
        """Modifier les informations d'un étudiant."""
        selected_student_index = self.treeview_students.selection()
        if selected_student_index:
            selected_student = self.selected_class.students[int(selected_student_index[0]) - 1]
            new_name = simpledialog.askstring("Modifier Etudiant",
                                              f"Modifier le nom de l'étudiant '{selected_student.name}' :")
            if new_name:
                selected_student.name = new_name
                self.show_students()

    def delete_student(self):
        """Supprimer un étudiant."""
        selected_student_index = self.treeview_students.selection()
        if selected_student_index:
            del self.selected_class.students[int(selected_student_index[0]) - 1]
            self.show_students()

    def clear_content_frame(self):
        """Vider le cadre de contenu."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()


    def show_groups(self):
        """Afficher le contenu pour 'Groupes'."""
        self.clear_content_frame()
        Label(self.content_frame, text="Gestion des Groupes", bg="#f4e1e0", font=("Arial", 16)).pack(pady=10)

        # Example of buttons for adding, modifying, and deleting groups
        button_frame = Frame(self.content_frame)
        button_frame.pack(pady=10)

        # Buttons
        Button(button_frame, text="Ajouter", command=self.add_group).grid(row=0, column=0, padx=5)
        Button(button_frame, text="Modifier", command=self.modify_group).grid(row=0, column=1, padx=5)
        Button(button_frame, text="Supprimer", command=self.delete_group).grid(row=0, column=2, padx=5)

        # Group listbox
        Label(self.content_frame, text="Liste des groupes :", bg="#f4e1e0", font=("Arial", 12)).pack(pady=5)

        self.group_listbox = Listbox(self.content_frame)
        self.group_listbox.pack(pady=5, padx=10)

        # Populate the listbox with group names of the current class
        for group in self.current_class.groups.values():
            self.group_listbox.insert(END, group.name)

    def add_group(self):
        """Ajouter un groupe à la classe actuelle."""
        new_name = simpledialog.askstring("Nouveau Groupe", "Nom du groupe :")
        if new_name:
            new_group = Group(new_name)
            self.current_class.add_group(new_group)
            self.refresh_groups()

    def modify_group(self):
        """Modifier un groupe dans la classe actuelle."""
        selected_group = self.group_listbox.curselection()
        if selected_group:
            selected_group = selected_group[0]
            old_name = list(self.current_class.groups.keys())[selected_group]
            new_name = simpledialog.askstring("Modifier Groupe", f"Modifier le nom du groupe '{old_name}' :")
            if new_name:
                group = self.current_class.groups.pop(old_name)
                group.name = new_name
                self.current_class.add_group(group)
                self.refresh_groups()

    def delete_group(self):
        """Supprimer un groupe de la classe actuelle."""
        selected_group = self.group_listbox.curselection()
        if selected_group:
            selected_group = selected_group[0]
            group_name = list(self.current_class.groups.keys())[selected_group]
            self.current_class.remove_group(group_name)
            self.refresh_groups()

    def refresh_groups(self):
        """Recharger la liste des groupes de la classe actuelle."""
        self.group_listbox.delete(0, END)
        for group in self.current_class.groups.values():
            self.group_listbox.insert(END, group.name)

    def show_evaluation(self):
        """Afficher le contenu pour 'Évaluation'."""
        self.clear_content_frame()
        Label(self.content_frame, text="Gestion des Évaluations", bg="#f4e1e0", font=("Arial", 16)).pack(pady=10)
        # Exemple de widgets pour les Évaluations
        Label(self.content_frame, text="Entrez une note :", bg="#f4e1e0", font=("Arial", 12)).pack(pady=5)
        Entry(self.content_frame).pack(pady=5, padx=10)


if __name__ == "__main__":
    root = Tk()
    app = StudentManagementApp(root)
    root.mainloop()
