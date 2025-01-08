from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from entities import *
from tkinter import messagebox


class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Étudiants et Notes")
        self.root.geometry("800x700")
        self.root.config(bg="#f4e1e0")

        self.create_header()
        self.create_main_content()
        self.create_footer()

        self.classes = session.query(MClass).all()


    def create_header(self):
        header = Frame(self.root, bg="#333", height=50)
        header.pack(side="top", fill="x")
        Label(header, text="Gestion des Étudiants et Notes", bg="#333", fg="white", font=("Arial", 16)).pack(pady=10)

    def create_main_content(self):
        self.main_content = Frame(self.root, bg="#f4e1e0")
        self.main_content.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Sidebar
        self.sidebar = Frame(self.main_content, bg="#555", width=200)
        self.sidebar.pack(side="left", fill="y")

        Button(self.sidebar, text="Classes", bg="#777", fg="white", command=self.show_classes_and_students, width=15).pack(pady=5, padx=5)
        Button(self.sidebar, text="Groupes", bg="#777", fg="white", command=self.show_groups, width=15).pack(pady=5, padx=5)
        Button(self.sidebar, text="Notes", bg="#777", fg="white", command=self.manage_notes, width=15).pack(pady=5, padx=5)

        # Main content frame
        self.content_frame = Frame(self.main_content, bg="#f4e1e0")
        self.content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    def create_footer(self):
        footer = Frame(self.root, bg="#333", height=30)
        footer.pack(side="bottom", fill="x")
        self.lbl_status = Label(footer, text="Statut : Prêt", bg="#333", fg="white", font=("Arial", 10))
        self.lbl_status.pack(pady=5)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    #
    # def show_classes_and_students(self):
    #     self.clear_content_frame()
    #
    #     Label(self.content_frame, text="Gestion des Classes et Étudiants", bg="#f4e1e0", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=10)
    #
    #     # Class management
    #     Label(self.content_frame, text="Gestion des Classes :", bg="#f4e1e0", font=("Arial", 12)).grid(row=1, column=0, pady=5)
    #
    #
    #     # Class list
    #     self.listbox_classes = Listbox(self.content_frame, height=10, width=30)
    #     self.listbox_classes.grid(row=3, column=0, padx=10, pady=5,  columnspan=4)
    #     self.listbox_classes.bind("<<ListboxSelect>>", self.on_class_select)
    #
    #     # Buttons
    #     Button(self.content_frame, text="Ajouter", command=self.add_class).grid(row=4, column=0, padx=5, pady=5)
    #     Button(self.content_frame, text="Modifier", command=self.modify_class).grid(row=4, column=1, padx=5)
    #     Button(self.content_frame, text="Supprimer", command=self.delete_class).grid(row=4, column=2, padx=5)
    #
    #     self.refresh_classes()
    #
    #     # Frame for student management buttons
    #     Label(self.content_frame, text="Gestion des Etudiants :", bg="#f4e1e0", font=("Arial", 12)).grid(
    #         row=1, column=3, padx=10, pady=5)
    #
    #     # Student Treeview
    #     self.treeview_students = ttk.Treeview(self.content_frame, columns=("ID", "Name", "Email", "Group"), show="headings")
    #     self.treeview_students.heading("ID", text="ID")
    #     self.treeview_students.heading("Name", text="Nom")
    #     self.treeview_students.heading("Email", text="Email")
    #     self.treeview_students.heading("Group", text="Groupe")
    #
    #     self.treeview_students.column("ID", width=100)
    #     self.treeview_students.column("Name", width=150)
    #     self.treeview_students.column("Email", width=200)
    #     self.treeview_students.column("Group", width=100)
    #
    #     self.treeview_students.grid(row=3, column=5, padx=10, pady=5, columnspan=4)
    #
    #     Button(self.content_frame, text="Ajouter", command=self.add_student).grid(row=4, column=5, padx=5,pady=5)
    #     Button(self.content_frame, text="Modifier", command=self.modify_student).grid(row=4, column=6, padx=5,pady=5)
    #     Button(self.content_frame, text="Supprimer", command=self.delete_student).grid(row=4, column=7, padx=5,pady=5)
    #     Button(self.content_frame, text="Importer", command=self.delete_student).grid(row=4, column=8, padx=5,pady=5)

    def show_classes_and_students(self):
        self.clear_content_frame()

        Label(self.content_frame, text="Gestion des Classes et Étudiants", bg="#f4e1e0", font=("Arial", 16)).pack(
            pady=10)

        # Create frames for classes and students
        frame_classes = Frame(self.content_frame, bg="#f4e1e0", bd=2, relief="groove", padx=10, pady=10)
        frame_students = Frame(self.content_frame, bg="#f4e1e0", bd=2, relief="groove", padx=10, pady=10)

        frame_classes.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        frame_students.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        # Class management frame
        Label(frame_classes, text="Gestion des Classes :", bg="#f4e1e0", font=("Arial", 12)).grid(row=0, column=0,
                                                                                                  columnspan=3, pady=5)

        # Class list
        self.listbox_classes = Listbox(frame_classes, height=10, width=30)
        self.listbox_classes.grid(row=1, column=0, columnspan=3, pady=5)
        self.listbox_classes.bind("<<ListboxSelect>>", self.on_class_select)

        # Class buttons
        Button(frame_classes, text="Ajouter", command=self.add_class).grid(row=2, column=0, padx=5, pady=5)
        Button(frame_classes, text="Modifier", command=self.modify_class).grid(row=2, column=1, padx=5, pady=5)
        Button(frame_classes, text="Supprimer", command=self.delete_class).grid(row=2, column=2, padx=5, pady=5)

        self.refresh_classes()

        # Student management frame
        Label(frame_students, text="Gestion des Étudiants :", bg="#f4e1e0", font=("Arial", 12)).grid(row=0, column=0,
                                                                                                     columnspan=4,
                                                                                                     pady=5)

        # Student Treeview
        self.treeview_students = ttk.Treeview(frame_students, columns=("ID", "Name", "Email", "Group"), show="headings")
        self.treeview_students.heading("ID", text="ID")
        self.treeview_students.heading("Name", text="Nom")
        self.treeview_students.heading("Email", text="Email")
        self.treeview_students.heading("Group", text="Groupe")

        self.treeview_students.column("ID", width=100)
        self.treeview_students.column("Name", width=150)
        self.treeview_students.column("Email", width=200)
        self.treeview_students.column("Group", width=100)

        self.treeview_students.grid(row=1, column=0, columnspan=4, pady=5, padx=5)

        # Student buttons
        Button(frame_students, text="Ajouter", command=self.add_student).grid(row=2, column=0, padx=5, pady=5)
        Button(frame_students, text="Modifier", command=self.modify_student).grid(row=2, column=1, padx=5, pady=5)
        Button(frame_students, text="Supprimer", command=self.delete_student).grid(row=2, column=2, padx=5, pady=5)
        Button(frame_students, text="Importer", command=self.import_students).grid(row=2, column=3, padx=5, pady=5)

    def on_class_select(self, event):
        selected_index = self.listbox_classes.curselection()
        if selected_index:
            selected_class_name = self.listbox_classes.get(selected_index[0])
            self.selected_class = next((cls for cls in self.classes if cls.name == selected_class_name), None)
            if self.selected_class:
                self.refresh_students()

    def refresh_classes(self):
        self.listbox_classes.delete(0, END)
        for mclass in self.classes:
            self.listbox_classes.insert(END, mclass.name)

    def refresh_students(self):
        for item in self.treeview_students.get_children():
            self.treeview_students.delete(item)
        if self.selected_class:
            for student in self.selected_class.students:
                self.treeview_students.insert("", "end", values=(student.id, student.name, student.email))

    def add_class(self):
        new_name = simpledialog.askstring("Nouvelle Classe", "Nom de la classe :")
        if new_name:
            new_class = MClass(name=new_name, year=2025)
            session.add(new_class)  # Add to the database session
            session.commit()  # Commit the transaction
            self.classes.append(new_class)  # Update local list
            self.refresh_classes()

    from entities import MClass  # Import de MClass depuis entities.py

    def modify_class(self):
        """Modifier le nom d'une classe existante."""
        selected_class = self.listbox_classes.curselection()

        if selected_class:
            selected_class = selected_class[0]
            old_class = self.classes[selected_class]
            old_name = old_class.name

            # Demander le nouveau nom à l'utilisateur
            new_name = simpledialog.askstring("Modifier Classe", f"Modifier le nom de la classe '{old_name}' :")

            if new_name:
                try:
                    # Mettre à jour le nom de la classe
                    old_class.name = new_name

                    # Sauvegarder la modification dans la base de données
                    old_class.save()

                    # Rafraîchir la liste locale et l'interface graphique
                    self.classes[selected_class] = old_class
                    self.refresh_classes()

                    # Afficher une confirmation dans la console
                    print(f"Classe modifiée : {old_name} -> {new_name}")
                except Exception as e:
                    print(f"Erreur lors de la modification de la classe : {e}")

    def delete_class(self):
        """Supprimer une classe sélectionnée."""
        selected_class = self.listbox_classes.curselection()

        if selected_class:
            # Récupérer la classe sélectionnée dans la liste
            selected_class = selected_class[0]
            class_to_delete = self.classes[selected_class]

            # Demander une confirmation à l'utilisateur
            confirm = messagebox.askyesno(
                "Supprimer Classe",
                f"Êtes-vous sûr de vouloir supprimer la classe '{class_to_delete.name}' ?"
            )

            if confirm:
                try:
                    # Supprimer la classe de la base de données
                    class_to_delete.delete()

                    # Supprimer la classe de la liste locale
                    del self.classes[selected_class]

                    # Rafraîchir l'affichage
                    self.refresh_classes()

                    # Message de confirmation dans la console
                    print(f"Classe supprimée : {class_to_delete.name}")
                except Exception as e:
                    # Afficher une erreur si la suppression échoue
                    print(f"Erreur lors de la suppression de la classe : {e}")
                    messagebox.showerror("Erreur", f"Impossible de supprimer la classe : {e}")
        else:
            # Aucun élément sélectionné
            messagebox.showwarning("Aucune Sélection", "Veuillez sélectionner une classe à supprimer.")



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

    def add_student(self):
        """Ouvrir une fenêtre pour ajouter un étudiant à la classe sélectionnée."""
        if not self.selected_class:
            messagebox.showwarning("Aucune Classe", "Veuillez sélectionner une classe pour ajouter un étudiant.")
            return

        # Fenêtre Toplevel pour ajouter un étudiant
        add_window = Toplevel(self.content_frame)
        add_window.title("Ajouter un Étudiant")
        add_window.geometry("400x300")
        add_window.grab_set()  # Bloquer les interactions avec la fenêtre principale

        # Widgets pour saisir les informations de l'étudiant
        Label(add_window, text="Nom :", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky=W)
        entry_name = Entry(add_window, width=30)
        entry_name.grid(row=0, column=1, padx=10, pady=10)

        Label(add_window, text="Email :", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky=W)
        entry_email = Entry(add_window, width=30)
        entry_email.grid(row=1, column=1, padx=10, pady=10)

        Label(add_window, text="Téléphone :", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky=W)
        entry_phone = Entry(add_window, width=30)
        entry_phone.grid(row=2, column=1, padx=10, pady=10)

        Label(add_window, text="Date de Naissance (AAAA-MM-JJ) :", font=("Arial", 12)).grid(row=3, column=0, padx=10,
                                                                                            pady=10, sticky=W)
        entry_birthdate = Entry(add_window, width=30)
        entry_birthdate.grid(row=3, column=1, padx=10, pady=10)

        def save_student():
            name = entry_name.get()
            email = entry_email.get()
            phone = entry_phone.get()
            birthdate = entry_birthdate.get()

            if name and email:
                try:
                    new_student = Student(
                        name=name,
                        email=email,
                        phone=phone,
                        birthdate=date.fromisoformat(birthdate) if birthdate else None,
                        mclass_id=self.selected_class.id
                    )
                    new_student.save()

                    self.selected_class.students.append(new_student)
                    self.show_students()

                    messagebox.showinfo("Succès", "Étudiant ajouté avec succès.")
                    add_window.destroy()  # Fermer la fenêtre
                except Exception as e:
                    messagebox.showerror("Erreur", f"Impossible d'ajouter l'étudiant : {e}")
            else:
                messagebox.showwarning("Données Incomplètes", "Veuillez remplir au moins le nom et l'email.")

        # Bouton pour sauvegarder l'étudiant
        Button(add_window, text="Ajouter", command=save_student).grid(row=4, column=0, columnspan=2, pady=20)

    def modify_student(self):
        """Ouvrir une fenêtre pour modifier les informations d'un étudiant."""
        selected_item = self.treeview_students.selection()

        if not selected_item:
            messagebox.showwarning("Aucun Étudiant", "Veuillez sélectionner un étudiant à modifier.")
            return

        selected_student_index = int(selected_item[0]) - 1
        selected_student = self.selected_class.students[selected_student_index]

        # Fenêtre Toplevel pour modifier un étudiant
        modify_window = Toplevel(self.content_frame)
        modify_window.title("Modifier un Étudiant")
        modify_window.geometry("400x250")
        modify_window.grab_set()  # Bloquer les interactions avec la fenêtre principale

        # Widgets pour modifier les informations de l'étudiant
        Label(modify_window, text="Nom :", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky=W)
        entry_name = Entry(modify_window, width=30)
        entry_name.insert(0, selected_student.name)
        entry_name.grid(row=0, column=1, padx=10, pady=10)

        Label(modify_window, text="Email :", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky=W)
        entry_email = Entry(modify_window, width=30)
        entry_email.insert(0, selected_student.email)
        entry_email.grid(row=1, column=1, padx=10, pady=10)

        def save_changes():
            new_name = entry_name.get()
            new_email = entry_email.get()

            if new_name and new_email:
                try:
                    selected_student.name = new_name
                    selected_student.email = new_email
                    selected_student.save()

                    self.show_students()
                    messagebox.showinfo("Succès", "Étudiant modifié avec succès.")
                    modify_window.destroy()  # Fermer la fenêtre
                except Exception as e:
                    messagebox.showerror("Erreur", f"Impossible de modifier l'étudiant : {e}")
            else:
                messagebox.showwarning("Données Incomplètes", "Veuillez remplir le nom et l'email.")

        # Bouton pour sauvegarder les modifications
        Button(modify_window, text="Modifier", command=save_changes).grid(row=2, column=0, columnspan=2, pady=20)

    def delete_student(self):
        """Supprimer un étudiant après confirmation."""
        selected_student_id = self.treeview_students.selection()  # Get the selected item IDs
        print(selected_student_id)  # Debugging: to check what's selected

        if not selected_student_id:
            messagebox.showwarning("Aucun Étudiant", "Veuillez sélectionner un étudiant à supprimer.")
            return

        # Récupérer l'ID de l'étudiant sélectionné (l'ID dans la première colonne)
        student_id = self.treeview_students.item(selected_student_id[0], "values")[
            0]  # ID is in the first column
        print(f"Selected Student ID: {student_id}")  # Debugging: Check the ID retrieved

        # Vérifier si l'étudiant existe dans la liste des étudiants
        selected_student = next(
            (student for student in self.selected_class.students if student.id == student_id), None)

        print(selected_student)

        if not selected_student:
            messagebox.showerror("Erreur", "L'étudiant sélectionné n'existe pas.")
            return

        # Demander confirmation à l'utilisateur
        confirm = messagebox.askyesno(
            "Confirmation de Suppression",
            f"Êtes-vous sûr de vouloir supprimer l'étudiant '{selected_student.name}' ?"
        )

        if confirm:
            try:
                # Supprimer l'étudiant de la base de données
                selected_student.delete()  # Suppression dans la base de données

                # Mettre à jour la liste locale
                self.selected_class.students = [
                    student for student in self.selected_class.students if student.id != selected_student.id
                ]
                self.show_students()  # Rafraîchir l'affichage des étudiants

                messagebox.showinfo("Succès", "L'étudiant a été supprimé avec succès.")
            except Exception as e:
                print(f"Erreur lors de la suppression de l'étudiant : {e}")
                messagebox.showerror("Erreur", f"Impossible de supprimer l'étudiant : {e}")

    def show_students(self):
        """Mettre à jour la liste des étudiants dans le Treeview."""
        if self.selected_class:
            # Vider le Treeview avant de le remplir
            for item in self.treeview_students.get_children():
                self.treeview_students.delete(item)

            for student in self.selected_class.students:
                self.treeview_students.insert("", "end",
                                              values=(student.id, student.name, student.email, student.group_name))


    def import_students(self):
        print(" importaions...........")

    def manage_notes(self):
        self.clear_content_frame()
        Label(self.content_frame, text="Gestion des Notes", bg="#f4e1e0", font=("Arial", 16)).pack(pady=10)

        # Example: Add functionality to update student notes
        # Logic here depends on your requirements

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


# Main application
if __name__ == "__main__":
    root = Tk()
    app = StudentManagementApp(root)
    root.mainloop()
