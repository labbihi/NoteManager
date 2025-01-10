from tkinter import *
from tkinter import ttk
from tkinter import simpledialog

from select import select

from entities import *
from tkinter import filedialog, messagebox
import pandas as pd
from datetime import datetime




class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Étudiants et Notes")
        self.root.geometry("800x700")
        self.root.config(bg="#f4e1e0")

        self.create_header()
        self.create_main_content()
        self.create_footer()
        self.selected_class = None



        self.selected_evaluation = None

        # Charger les données depuis la base
        self.classes = session.query(MClass).all()
        self.groups = session.query(Group).all()
        self.evaluations = session.query(Evalution).all()


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
        Button(self.sidebar, text="Evaluations", bg="#777", fg="white", command=self.show_evalutions, width=15).pack(pady=5, padx=5)
        Button(self.sidebar, text="Affectation", bg="#777", fg="white", command=self.create_widgets, width=15).pack(pady=5, padx=5)
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
        Button(frame_classes, text="Importé", command=self.create_class_from_excel).grid(row=2, column=3, padx=5, pady=5)

        self.refresh_classes()

        # Student management frame
        Label(frame_students, text="Gestion des Étudiants :", bg="#f4e1e0", font=("Arial", 12)).grid(row=0, column=0,
                                                                                                     columnspan=4,
                                                                                                     pady=5)

        # Student Treeview
        self.treeview_students = ttk.Treeview(frame_students, columns=("Code", "Name", "Email"), show="headings")
        self.treeview_students.heading("Code", text="Code Massar")
        self.treeview_students.heading("Name", text="Nom")
        self.treeview_students.heading("Email", text="Email")


        self.treeview_students.column("Code", width=100)
        self.treeview_students.column("Name", width=150)
        self.treeview_students.column("Email", width=200)

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
                self.treeview_students.insert("", "end", values=(student.code , student.name, student.email))

    def add_class(self):
        new_name = simpledialog.askstring("Nouvelle Classe", "Nom de la classe :")
        if new_name:
            new_class = MClass(name=new_name, year=2025)
            session.add(new_class)  # Add to the database session
            session.commit()  # Commit the transaction
            self.classes.append(new_class)  # Update local list
            self.refresh_classes()

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
        """Supprimer une classe sélectionnée et ses étudiants associés."""
        selected_class = self.listbox_classes.curselection()

        if selected_class:
            # Récupérer la classe sélectionnée dans la liste
            selected_class = selected_class[0]
            class_to_delete = self.classes[selected_class]

            # Demander une confirmation à l'utilisateur
            confirm = messagebox.askyesno(
                "Supprimer Classe",
                f"Êtes-vous sûr de vouloir supprimer la classe '{class_to_delete.name}' et tous les étudiants associés ?"
            )

            if confirm:
                try:
                    # Supprimer les étudiants associés à la classe
                    for student in class_to_delete.students:
                        student.delete()  # Supposer que `delete` est une méthode de suppression pour les étudiants

                    # Supprimer la classe de la base de données
                    class_to_delete.delete()

                    # Supprimer la classe de la liste locale
                    del self.classes[selected_class]

                    # Rafraîchir l'affichage
                    self.refresh_classes()

                    # Message de confirmation dans la console
                    print(f"Classe et étudiants supprimés : {class_to_delete.name}")
                except Exception as e:
                    # Afficher une erreur si la suppression échoue
                    print(f"Erreur lors de la suppression de la classe et des étudiants : {e}")
                    messagebox.showerror("Erreur", f"Impossible de supprimer la classe et les étudiants : {e}")
            else:
                print("Suppression annulée.")
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
        """Ouvrir une fenêtre pour ajouter un étudiant à la classe sélectionnée avec un code saisi."""
        if not self.selected_class:
            messagebox.showwarning("Aucune Classe", "Veuillez sélectionner une classe pour ajouter un étudiant.")
            return

        # Fenêtre Toplevel pour ajouter un étudiant
        add_window = Toplevel(self.content_frame)
        add_window.title("Ajouter un Étudiant")
        add_window.geometry("400x350")
        add_window.grab_set()  # Bloquer les interactions avec la fenêtre principale

        # Widgets pour saisir les informations de l'étudiant
        Label(add_window, text="Code Massar :", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky=W)
        entry_code = Entry(add_window, width=30)
        entry_code.grid(row=0, column=1, padx=10, pady=10)

        Label(add_window, text="Nom :", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky=W)
        entry_name = Entry(add_window, width=30)
        entry_name.grid(row=1, column=1, padx=10, pady=10)

        Label(add_window, text="Email :", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky=W)
        entry_email = Entry(add_window, width=30)
        entry_email.grid(row=2, column=1, padx=10, pady=10)

        Label(add_window, text="Téléphone :", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10, sticky=W)
        entry_phone = Entry(add_window, width=30)
        entry_phone.grid(row=3, column=1, padx=10, pady=10)

        Label(add_window, text="Date de Naissance (AAAA-MM-JJ) :", font=("Arial", 12)).grid(row=4, column=0, padx=10,
                                                                                            pady=10, sticky=W)
        entry_birthdate = Entry(add_window, width=30)
        entry_birthdate.grid(row=4, column=1, padx=10, pady=10)

        def save_student():
            student_code = entry_code.get().strip()
            name = entry_name.get().strip()
            email = entry_email.get().strip()
            phone = entry_phone.get().strip()
            birthdate = entry_birthdate.get().strip()

            if not student_code or not name or not email:
                messagebox.showwarning("Données Incomplètes", "Veuillez remplir le code, le nom et l'email.")
                return

            try:
                # Vérifier si le code est unique
                existing_student = session.query(Student).filter_by(code=student_code).first()
                if existing_student:
                    messagebox.showerror("Erreur", f"Le code étudiant '{student_code}' existe déjà.")
                    return

                # Créer et sauvegarder le nouvel étudiant
                new_student = Student(
                    code=student_code,
                    name=name,
                    email=email,
                    phone=phone,
                    birthdate=date.fromisoformat(birthdate) if birthdate else None,
                    mclass_id=self.selected_class.id
                )
                new_student.save()

                # Ajouter à la liste d'étudiants de la classe sélectionnée et rafraîchir l'interface
                self.selected_class.students.append(new_student)
                self.show_students()

                messagebox.showinfo("Succès", "Étudiant ajouté avec succès.")
                add_window.destroy()  # Fermer la fenêtre
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ajouter l'étudiant : {e}")

        # Bouton pour sauvegarder l'étudiant
        Button(add_window, text="Ajouter", command=save_student).grid(row=5, column=0, columnspan=2, pady=20)

        # Center the window
        add_window.update_idletasks()
        width = add_window.winfo_width()
        height = add_window.winfo_height()
        x = (add_window.winfo_screenwidth() // 2) - (width // 2)
        y = (add_window.winfo_screenheight() // 2) - (height // 2)
        add_window.geometry(f"{width}x{height}+{x}+{y}")


    def modify_student(self):
        """Ouvrir une fenêtre pour modifier les informations d'un étudiant."""
        selected_item = self.treeview_students.selection()

        if not selected_item:
            messagebox.showwarning("Aucun Étudiant Sélectionné", "Veuillez sélectionner un étudiant à modifier.")
            return

        # Obtenir l'ID de l'étudiant depuis l'élément sélectionné dans le Treeview
        student_id = self.treeview_students.item(selected_item[0], "values")[0]

        # Rechercher l'étudiant dans la base de données
        student_to_modify = session.query(Student).filter_by(id=student_id).first()

        if not student_to_modify:
            messagebox.showerror("Erreur", "L'étudiant sélectionné n'existe pas.")
            return

        # Créer une fenêtre Toplevel pour la modification
        modify_window = Toplevel(self.content_frame)
        modify_window.title("Modifier Étudiant")
        modify_window.geometry("400x400")
        modify_window.grab_set()  # Bloquer les interactions avec la fenêtre principale

        # Widgets pour modifier les informations de l'étudiant
        Label(modify_window, text="Code Massar :", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky=W)
        entry_code = Entry(modify_window, width=30)
        entry_code.insert(0, student_to_modify.code)
        entry_code.grid(row=0, column=1, padx=10, pady=10)

        Label(modify_window, text="Nom :", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky=W)
        entry_name = Entry(modify_window, width=30)
        entry_name.insert(0, student_to_modify.name)
        entry_name.grid(row=1, column=1, padx=10, pady=10)

        Label(modify_window, text="Email :", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky=W)
        entry_email = Entry(modify_window, width=30)
        entry_email.insert(0, student_to_modify.email)
        entry_email.grid(row=2, column=1, padx=10, pady=10)

        Label(modify_window, text="Téléphone :", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10, sticky=W)
        entry_phone = Entry(modify_window, width=30)
        entry_phone.insert(0, student_to_modify.phone)
        entry_phone.grid(row=3, column=1, padx=10, pady=10)

        Label(modify_window, text="Date de Naissance (AAAA-MM-JJ) :", font=("Arial", 12)).grid(row=4, column=0, padx=10,
                                                                                               pady=10, sticky=W)
        entry_birthdate = Entry(modify_window, width=30)
        entry_birthdate.insert(0,
                               student_to_modify.birthdate.strftime("%Y-%m-%d") if student_to_modify.birthdate else "")
        entry_birthdate.grid(row=4, column=1, padx=10, pady=10)

        # Fonction pour sauvegarder les modifications
        def save_changes():
            new_code = entry_code.get().strip()
            new_name = entry_name.get().strip()
            new_email = entry_email.get().strip()
            new_phone = entry_phone.get().strip()
            new_birthdate = entry_birthdate.get().strip()

            if not new_code or not new_name or not new_email:
                messagebox.showwarning("Données Incomplètes",
                                       "Veuillez remplir les champs obligatoires (Code, Nom, Email).")
                return

            try:
                # Vérifier si le nouveau code Massar est unique
                if new_code != student_to_modify.code:
                    existing_student = session.query(Student).filter_by(code=new_code).first()
                    if existing_student:
                        messagebox.showerror("Erreur", f"Le code Massar '{new_code}' existe déjà.")
                        return

                # Mettre à jour les informations de l'étudiant
                student_to_modify.code = new_code
                student_to_modify.name = new_name
                student_to_modify.email = new_email
                student_to_modify.phone = new_phone
                student_to_modify.birthdate = date.fromisoformat(new_birthdate) if new_birthdate else None

                session.commit()  # Sauvegarder les modifications dans la base de données

                self.refresh_students()  # Rafraîchir la liste des étudiants dans l'interface utilisateur
                messagebox.showinfo("Succès", "Étudiant modifié avec succès.")
                modify_window.destroy()  # Fermer la fenêtre de modification
            except Exception as e:
                session.rollback()  # Annuler en cas d'erreur
                messagebox.showerror("Erreur", f"Impossible de modifier l'étudiant : {e}")

        # Bouton pour sauvegarder les modifications
        Button(modify_window, text="Sauvegarder", command=save_changes).grid(row=5, column=0, columnspan=2, pady=20)

        # Centrer la fenêtre
        modify_window.update_idletasks()
        width = modify_window.winfo_width()
        height = modify_window.winfo_height()
        x = (modify_window.winfo_screenwidth() // 2) - (width // 2)
        y = (modify_window.winfo_screenheight() // 2) - (height // 2)
        modify_window.geometry(f"{width}x{height}+{x}+{y}")



    def delete_student(self):
        """Delete a student after confirmation."""
        selected_item = self.treeview_students.selection()

        if not selected_item:
            messagebox.showwarning("No Student Selected", "Please select a student to delete.")
            return

        # Get the student ID from the selected item in the Treeview
        student_id = self.treeview_students.item(selected_item[0], "values")[0]

        # Query the database to find the student
        student_to_delete = session.query(Student).filter_by(id=student_id).first()

        if not student_to_delete:
            messagebox.showerror("Error", "The selected student does not exist.")
            return

        # Ask for confirmation
        confirm = messagebox.askyesno(
            "Delete Confirmation",
            f"Are you sure you want to delete the student '{student_to_delete.name}'?"
        )

        if confirm:
            try:
                # Delete the student from the database
                student_to_delete.delete()

                # Refresh the student list in the UI
                self.refresh_students()

                messagebox.showinfo("Success", "Student deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete the student: {e}")


    def show_students(self):
        """Mettre à jour la liste des étudiants dans le Treeview."""
        if self.selected_class:
            # Vider le Treeview avant de le remplir
            for item in self.treeview_students.get_children():
                self.treeview_students.delete(item)

            for student in self.selected_class.students:
                self.treeview_students.insert("", "end",
                                              values=(student.code, student.name,student.email))

    def saving_studant_from_df(self, df ,selected_class):
        # Les colonnes spécifiques
        start_row = 17  # Les données commencent à la ligne 18 (index 17)
        code_column = 2  # Colonne C (index 2)
        name_column = 3  # Colonne D (index 3)
        birthdate_column = 5  # Colonne F (index 5)

        # Vérifier que les colonnes sont bien présentes
        if len(df.columns) < max(code_column, name_column, birthdate_column) + 1:
            messagebox.showerror("Erreur de Format", "Le fichier Excel semble incomplet ou mal formaté.")
            return

        # Parcourir les lignes à partir de la ligne 18
        for index, row in df.iterrows():
            if index < start_row:
                continue  # Ignorer les lignes avant la ligne 18

            student_code = str(row.iloc[code_column]).strip() if not pd.isna(row.iloc[code_column]) else None
            name = str(row.iloc[name_column]).strip() if not pd.isna(row.iloc[name_column]) else None

            if not pd.isna(row.iloc[birthdate_column]):
                try:
                    birthdate = datetime.strptime(str(row.iloc[birthdate_column]), "%d-%m-%Y").date()
                except ValueError:
                    birthdate = None  # Si la date est mal formatée, elle sera ignorée

            # Vérifier si le code et le nom sont valides
            if not student_code or not name:
                continue  # Ignorer les entrées incomplètes

            # Vérifier si le code est unique
            existing_student = session.query(Student).filter_by(code=student_code).first()
            if existing_student:
                messagebox.showwarning(
                    "Code Massar Dupliqué",
                    f"L'étudiant avec le code '{student_code}' existe déjà. Ignoré."
                )
                continue

            # Créer et sauvegarder le nouvel étudiant
            new_student = Student(
                code=student_code,
                name=name,
                birthdate=birthdate,
                mclass_id=selected_class.id
            )

            try:
                new_student.save()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ajouter l'étudiant '{name}' : {e}")

        # Rafraîchir la liste des étudiants dans l'interface
        self.show_students()
        messagebox.showinfo("Succès", "Importation terminée avec succès.")

    def import_students(self):
        """Importer des informations d'élèves à partir d'un fichier Excel à partir des colonnes spécifiques."""
        if not self.selected_class:
            messagebox.showwarning("Aucune Classe", "Veuillez sélectionner une classe pour importer des élèves.")
            return

        # Demander à l'utilisateur de sélectionner un fichier Excel
        file_path = filedialog.askopenfilename(
            title="Sélectionner un fichier Excel",
            filetypes=[("Fichiers Excel", "*.xlsx *.xls")]
        )

        if not file_path:
            return  # L'utilisateur a annulé

        try:
            # Charger le fichier Excel
            df = pd.read_excel(file_path, header=None)  # Pas d'en-tête car les données commencent à C18
            self.saving_studant_from_df(df, self.selected_class)

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire le fichier Excel : {e}")

    def create_class_from_excel(self):
        """Créer une classe à partir d'un fichier Excel et ajouter les élèves à cette classe."""
        # Demander à l'utilisateur de sélectionner un fichier Excel
        file_path = filedialog.askopenfilename(
            title="Sélectionner un fichier Excel",
            filetypes=[("Fichiers Excel", "*.xlsx")]
        )

        if not file_path:
            return  # Si aucun fichier n'est sélectionné, on quitte la fonction

        try:
            # Charger le fichier Excel avec pandas (ici sheet_name=None pour charger toutes les feuilles)
            df_dict = pd.read_excel(file_path, sheet_name=None)

            # On suppose que le nom de la classe est dans la première feuille
            # Obtenez le nom de la première feuille
            sheet_name = list(df_dict.keys())[0]

            # Obtenez le DataFrame de cette première feuille
            df = df_dict[sheet_name]

            # Récupérer le nom de la classe à partir de la cellule I9 (ligne 9, colonne 9)
            class_name = str(df.iloc[7, 8]).strip()

            # Vérification si le nom de la classe est valide
            if not class_name or class_name.lower() == 'nan':
                messagebox.showerror("Erreur", "Le nom de la classe est invalide ou vide dans la cellule I9.")
                return

            print(f"Nom de la classe: {class_name}")

            # Créer la classe dans la base de données
            new_class = MClass(name=class_name, year=2025)
            new_class.save()  # Sauvegarder la classe dans la base de données

            # Ajouter la classe à la liste des classes locales
            self.classes.append(new_class)

            # Enregistrer les élèves depuis le fichier Excel
            self.saving_studant_from_df(df, new_class.get_by_name(class_name))

            self.refresh_classes()

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du traitement du fichier Excel: {e}")

    def manage_notes(self):
        self.clear_content_frame()
        Label(self.content_frame, text="Gestion des Notes", bg="#f4e1e0", font=("Arial", 16)).pack(pady=10)

        # Example: Add functionality to update student notes
        # Logic here depends on your requirements

    def show_groups(self):
        """Afficher le contenu pour 'Groupes'."""
        self.clear_content_frame()

        # Titre principal
        Label(self.content_frame, text="Gestion des Groupes", bg="#f4e1e0", font=("Arial", 16)).pack(pady=10)

        # Cadre des boutons d'action
        button_frame = Frame(self.content_frame, bg="#f4e1e0")
        button_frame.pack(pady=10)

        # Boutons pour ajouter, modifier, et supprimer un groupe
        Button(button_frame, text="Ajouter", command=self.add_group).grid(row=0, column=0, padx=5)
        Button(button_frame, text="Modifier", command=self.modify_group).grid(row=0, column=1, padx=5)
        Button(button_frame, text="Supprimer", command=self.delete_group).grid(row=0, column=2, padx=5)

        # Liste des groupes
        Label(self.content_frame, text="Liste des groupes :", bg="#f4e1e0", font=("Arial", 12)).pack(pady=5)

        self.group_listbox = Listbox(self.content_frame, width=50, height=10)
        self.group_listbox.pack(pady=5, padx=10)

        # Charger et afficher les noms des groupes de la classe actuelle
        try:
            for group in self.groups:
                self.group_listbox.insert(END, group.name)

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les groupes : {e}")

    def add_group(self):
        """Ajouter un groupe à la classe actuelle."""
        new_name = simpledialog.askstring("Nouveau Groupe", "Nom du groupe :")
        if new_name:
            # Check if the group name already exists
            existing_group = session.query(Group).filter_by(name=new_name).first()
            if existing_group:
                messagebox.showwarning("Groupe existant", f"Le groupe '{new_name}' existe déjà.")
                return

            # If the group does not exist, proceed to add it
            try:
                new_group = Group(name=new_name)
                session.add(new_group)  # Add to the database session
                session.commit()  # Commit the transaction
                self.groups.append(new_group)  # Update local list
                self.refresh_groups()  # Refresh the listbox
                messagebox.showinfo("Succès", f"Le groupe '{new_name}' a été ajouté avec succès.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ajouter le groupe : {e}")
        else:
            messagebox.showwarning("Nom manquant", "Veuillez entrer un nom pour le nouveau groupe.")



    def modify_group(self):
        """Modifier un groupe dans la classe actuelle."""
        selected_group_index = self.group_listbox.curselection()
        if selected_group_index:
            selected_group_index = selected_group_index[0]
            selected_group = self.groups[selected_group_index]  # Get the group object from the list

            # Prompt the user for a new group name
            new_name = simpledialog.askstring("Modifier Groupe", f"Modifier le nom du groupe '{selected_group.name}' :")
            if new_name:
                try:
                    selected_group.name = new_name  # Update the group name
                    session.commit()  # Commit the changes to the database
                    self.refresh_groups()  # Refresh the listbox to reflect the updated name
                except Exception as e:
                    messagebox.showerror("Erreur", f"Impossible de modifier le groupe : {e}")
        else:
            messagebox.showwarning("Aucun groupe sélectionné", "Veuillez sélectionner un groupe à modifier.")

    def delete_group(self):
        """Supprimer un groupe de la classe actuelle."""
        selected_group_index = self.group_listbox.curselection()
        if selected_group_index:
            selected_group_index = selected_group_index[0]
            selected_group = self.groups[selected_group_index]  # Get the group object from the list

            # Confirm deletion with the user
            confirm = messagebox.askyesno("Confirmer la suppression",
                                          f"Êtes-vous sûr de vouloir supprimer le groupe '{selected_group.name}' ?")
            if confirm:
                try:
                    session.delete(selected_group)  # Delete the group from the database
                    session.commit()  # Commit the transaction
                    self.groups.remove(selected_group)  # Remove the group from the local list
                    self.refresh_groups()  # Refresh the listbox to reflect the removal
                except Exception as e:
                    messagebox.showerror("Erreur", f"Impossible de supprimer le groupe : {e}")
        else:
            messagebox.showwarning("Aucun groupe sélectionné", "Veuillez sélectionner un groupe à supprimer.")

    def refresh_groups(self):
        """Recharger la liste des groupes de la classe actuelle."""
        self.group_listbox.delete(0, END)
        for group in self.groups:
            self.group_listbox.insert(END, group.name)



    def show_evalutions(self):
        """Afficher le contenu pour 'Évaluations'."""
        self.clear_content_frame()

        Label(self.content_frame, text="Gestion des Évaluations", bg="#f4e1e0", font=("Arial", 16)).pack(pady=10)

        # Treeview for displaying evaluations
        self.evalution_tree = ttk.Treeview(self.content_frame, columns=("ID", "Date", "Description"), show="headings")
        self.evalution_tree.heading("ID", text="ID")
        self.evalution_tree.heading("Date", text="Date")
        self.evalution_tree.heading("Description", text="Description")
        self.evalution_tree.column("ID", width=50, anchor=CENTER)
        self.evalution_tree.column("Date", width=150, anchor=CENTER)
        self.evalution_tree.column("Description", width=300, anchor=W)
        self.evalution_tree.pack(pady=10, padx=10, fill=BOTH, expand=True)

        # Buttons for Add/Edit/Delete actions
        button_frame = Frame(self.content_frame)
        button_frame.pack(pady=10)

        Button(button_frame, text="Ajouter", command=self.add_evalution).grid(row=0, column=0, padx=5)
        Button(button_frame, text="Modifier", command=self.modify_evalution).grid(row=0, column=1, padx=5)
        Button(button_frame, text="Supprimer", command=self.delete_evalution).grid(row=0, column=2, padx=5)

        # Populate the Treeview with evaluation data
        self.refresh_evalutions()


    def refresh_evalutions(self):
        """Rafraîchir la Treeview avec les évaluations de la base de données."""
        for row in self.evalution_tree.get_children():
            self.evalution_tree.delete(row)  # Clear the Treeview

        evalutions = session.query(Evalution).all()  # Fetch all evaluations
        self.evalutions = evalutions  # Save evaluations locally
        for evalution in evalutions:
            self.evalution_tree.insert("", "end", values=(evalution.id, evalution.date, evalution.desc))


    def add_evalution(self):
        """Ajouter une nouvelle évaluation."""
        self._open_evalution_form()


    def modify_evalution(self):
        """Modifier une évaluation existante."""
        selected_item = self.evalution_tree.selection()
        if not selected_item:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une évaluation à modifier.")
            return

        eval_id = self.evalution_tree.item(selected_item[0], "values")[0]
        eval_to_edit = session.query(Evalution).filter_by(id=eval_id).first()
        self._open_evalution_form(eval_to_edit)

    def _open_evalution_form(self, eval_to_edit=None):
        """Afficher une fenêtre pour ajouter ou modifier une évaluation."""
        # Créer une fenêtre pour ajouter/modifier une évaluation
        edit_window = Toplevel(self.root)
        edit_window.title("Ajouter / Modifier une Évaluation")
        edit_window.geometry("400x300")

        # Champ pour la date
        Label(edit_window, text="Date (AAAA-MM-JJ):").pack(pady=5)
        date_entry = Entry(edit_window)
        date_entry.pack(pady=5)
        if eval_to_edit:
            date_entry.insert(0, str(eval_to_edit.date))  # Pré-remplir la date si modification

        # Champ pour la description
        Label(edit_window, text="Description:").pack(pady=5)
        desc_entry = Text(edit_window, height=5, width=40)  # Utilisation d'un widget Text pour plusieurs lignes
        desc_entry.pack(pady=5)
        if eval_to_edit:
            desc_entry.insert("1.0", eval_to_edit.desc)  # Pré-remplir la description si modification

        # Fonction pour enregistrer les données
        def save_evalution():
            """Enregistrer l'évaluation (ajout ou modification)."""
            date_str = date_entry.get().strip()
            desc = desc_entry.get("1.0", "end").strip()  # Récupérer tout le texte de la description
            if not date_str or not desc:
                messagebox.showwarning("Données manquantes", "Veuillez remplir tous les champs.", parent=edit_window)
                return

            try:
                eval_date = datetime.strptime(date_str, "%Y-%m-%d").date()

                if eval_to_edit:  # Modification d'une évaluation existante
                    eval_to_edit.date = eval_date
                    eval_to_edit.desc = desc
                    session.commit()
                    messagebox.showinfo("Succès", "L'évaluation a été modifiée avec succès.", parent=edit_window)
                else:  # Ajout d'une nouvelle évaluation
                    new_eval = Evalution(date=eval_date, desc=desc)
                    session.add(new_eval)
                    session.commit()
                    messagebox.showinfo("Succès", "L'évaluation a été ajoutée avec succès.", parent=edit_window)

                self.refresh_evalutions()
                edit_window.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}", parent=edit_window)

        # Boutons pour enregistrer ou annuler
        Button(edit_window, text="Enregistrer", command=save_evalution).pack(pady=10)
        Button(edit_window, text="Annuler", command=edit_window.destroy).pack(pady=5)

    def delete_evalution(self):
        """Supprimer une évaluation sélectionnée."""
        selected_item = self.evalution_tree.selection()
        if not selected_item:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une évaluation à supprimer.")
            return

        eval_id = self.evalution_tree.item(selected_item[0], "values")[0]
        eval_to_delete = session.query(Evalution).filter_by(id=eval_id).first()

        if eval_to_delete:
            confirm = messagebox.askyesno("Confirmer la suppression", f"Êtes-vous sûr de vouloir supprimer l'évaluation '{eval_to_delete.desc}' ?")
            if confirm:
                try:
                    session.delete(eval_to_delete)
                    session.commit()
                    self.refresh_evalutions()
                    messagebox.showinfo("Succès", "L'évaluation a été supprimée avec succès.")
                except Exception as e:
                    messagebox.showerror("Erreur", f"Impossible de supprimer l'évaluation : {e}")

    def create_widgets(self):
        self.clear_content_frame()

        Label(self.content_frame, text="Affectation des Groupes aux Étudiants", bg="#f4e1e0", font=("Arial", 16)).pack(
            pady=10)

        # Create frames for evaluations, classes, and students
        frame_eval_classes = Frame(self.content_frame, bg="#f4e1e0", bd=2, relief="groove", padx=10, pady=10)
        frame_students = Frame(self.content_frame, bg="#f4e1e0", bd=2, relief="groove", padx=10, pady=10)

        frame_eval_classes.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        frame_students.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        # Evaluation and class management frame
        Label(frame_eval_classes, text="Sélectionnez une Évaluation :", bg="#f4e1e0", font=("Arial", 12)).grid(row=0,
                                                                                                               column=0,
                                                                                                               pady=5)
        self.listbox_evaluations = Listbox(frame_eval_classes, height=8, width=30)
        self.listbox_evaluations.grid(row=1, column=0, pady=5)
        self.listbox_evaluations.bind("<<ListboxSelect>>", self.on_evaluation_select)
        self.refresh_evaluations()

        Label(frame_eval_classes, text="Sélectionnez une Classe :", bg="#f4e1e0", font=("Arial", 12)).grid(row=2,
                                                                                                           column=0,
                                                                                                           pady=5)
        self.listbox_classes = Listbox(frame_eval_classes, height=8, width=30)
        self.listbox_classes.grid(row=3, column=0, pady=5)
        self.listbox_classes.bind("<<ListboxSelect>>", self.on_class_select)
        self.refresh_classes()

        # Student management frame
        Label(frame_students, text="Liste des Étudiants :", bg="#f4e1e0", font=("Arial", 12)).grid(row=0, column=0,
                                                                                                   columnspan=4, pady=5)

        # Student Treeview
        self.treeview_students2 = ttk.Treeview(frame_students, columns=("Code", "Name", "Group"), show="headings")
        self.treeview_students2.heading("Code", text="Code Massar")
        self.treeview_students2.heading("Name", text="Nom")
        self.treeview_students2.heading("Group", text="Groupe")
        self.treeview_students2.column("Code", width=100)
        self.treeview_students2.column("Name", width=150)
        self.treeview_students2.column("Group", width=100)
        self.treeview_students2.grid(row=0, column=0, pady=5, padx=5, sticky="nsew")

        # Scrollbar for the Treeview
        scrollbar = Scrollbar(frame_students, orient=VERTICAL, command=self.treeview_students2.yview)
        self.treeview_students2.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Bind cell selection to open a Combobox for group selection
        self.treeview_students2.bind("<Double-1>", self.on_cell_double_click)

        # Student buttons
        Button(frame_students, text="Enregistrer", command=self.save_group_assignments).grid(row=2, column=0, padx=5, pady=5)


        # Example data
        self.refresh_students_per_groupes()


    def on_cell_double_click(self, event):
        # Get selected row and column
        region = self.treeview_students2.identify("region", event.x, event.y)
        if region == "cell":
            row_id = self.treeview_students2.identify_row(event.y)
            column_id = self.treeview_students2.identify_column(event.x)

            if column_id == "#3":  # If the "Group" column is clicked
                # Get the bounding box of the selected cell
                bbox = self.treeview_students2.bbox(row_id, column_id)

                if bbox:
                    # Create a Combobox for group selection
                    x, y, width, height = bbox
                    self.combobox = ttk.Combobox(self.treeview_students2, values=[group.name for group in self.groups], state="readonly")
                    self.combobox.place(x=x, y=y, width=width, height=height)
                    self.combobox.bind("<<ComboboxSelected>>", lambda e: self.update_group(row_id))
                    # Set the current value
                    current_value = self.treeview_students2.item(row_id, "values")[2]
                    self.combobox.set(current_value)

    def update_group(self, row_id):
        # Update the Treeview with the selected group
        selected_group = self.combobox.get()
        if selected_group:
            values = list(self.treeview_students2.item(row_id, "values"))
            values[2] = selected_group  # Update the group column
            self.treeview_students2.item(row_id, values=values)

        # Remove the Combobox after selection
        self.combobox.destroy()




    def on_evaluation_select(self, event):
        selected_index = self.listbox_evaluations.curselection()
        if selected_index:
            self.selected_evaluation = self.listbox_evaluations.get(selected_index)

    def on_class_select(self, event):
        selected_index = self.listbox_classes.curselection()
        if selected_index:
            self.selected_class = self.listbox_classes.get(selected_index)
            self.refresh_students_per_groupes()

    def refresh_evaluations(self):
        self.listbox_evaluations.delete(0, END)
        evaluations = session.query(Evalution).all()
        for evaluation in evaluations:
            self.listbox_evaluations.insert(END, evaluation.desc)

    def refresh_classes(self):
        self.listbox_classes.delete(0, END)
        classes = session.query(MClass).all()
        for mclass in classes:
            self.listbox_classes.insert(END, mclass.name)

    def refresh_students_per_groupes(self):
        if self.selected_class:
            self.treeview_students2.delete(*self.treeview_students2.get_children())
            selected_class = session.query(MClass).filter_by(name=self.selected_class).first()
            if selected_class:
                for student in selected_class.students:
                    group_name = student.notes[0].group.name if student.notes else "Aucun"
                    self.treeview_students2.insert("", "end", values=(student.code, student.name, group_name))

    def assign_group(self):
        selected_item = self.treeview_students2.selection()
        if selected_item:
            student_data = self.treeview_students2.item(selected_item)['values']
            student_code = student_data[0]  # Get the student's code
            student = session.query(Student).filter_by(code=student_code).first()
            if student:
                # Logic to assign a group (to be implemented)
                pass

    def load_evaluations(self):
        """Charger les évaluations dans la Listbox."""
        for eval in self.evaluations:
            self.eval_listbox.insert(END, f"{eval.id} - {eval.desc}")

    def load_classes(self):
        """Charger les classes dans la Listbox."""
        for cls in self.classes:
            self.class_listbox.insert(END, f"{cls.id} - {cls.name}")

    def select_evaluation(self, event):
        """Sélectionner une évaluation."""
        index = self.eval_listbox.curselection()
        if index:
            self.selected_evaluation = self.evaluations[index[0]]

    def select_class(self, event):
        """Sélectionner une classe et charger ses élèves."""
        index = self.class_listbox.curselection()
        if index:
            self.selected_class = self.classes[index[0]]
            self.load_students()

    def load_students(self):
        """Charger les élèves de la classe sélectionnée."""
        if not self.selected_class:
            return
        self.student_tree.delete(*self.student_tree.get_children())
        for student in self.selected_class.students:
            group_name = student.notes[0].group.name if student.notes else "Aucun"
            self.student_tree.insert("", "end", values=(student.id, student.name, group_name))

    def assign_group(self):
        """Affecter un groupe à l'élève sélectionné."""
        selected_item = self.student_tree.selection()
        if not selected_item:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un élève.")
            return

        selected_student_id = self.student_tree.item(selected_item[0], "values")[0]
        student = session.query(Student).get(selected_student_id)

        group_names = [group.name for group in self.groups]
        group_name = simpledialog.askstring("Affectation de Groupe", f"Groupes disponibles : {', '.join(group_names)}")
        if not group_name:
            return

        group = session.query(Group).filter_by(name=group_name).first()
        if not group:
            messagebox.showerror("Erreur", "Groupe introuvable.")
            return

        # Mettre à jour ou créer une NoteGoupe
        note_group = session.query(NoteGoupe).filter_by(student_id=student.id,
                                                        evalution_id=self.selected_evaluation.id).first()
        if not note_group:
            note_group = NoteGoupe(student_id=student.id, evalution_id=self.selected_evaluation.id, group_id=group.id)
        else:
            note_group.group_id = group.id

        note_group.save()
        messagebox.showinfo("Succès", f"Groupe {group.name} affecté à {student.name}.")
        self.load_students()

    def save_group_assignments(self):
        # Récupérer tous les éléments du Treeview
        for item in self.treeview_students2.get_children():
            # Récupérer les données de l'étudiant (Code, Nom, Groupe)
            student_data = self.treeview_students2.item(item)['values']
            student_code = student_data[0]  # Code de l'étudiant
            student_name = student_data[1]  # Nom de l'étudiant
            group_name = student_data[2]  # Nom du groupe

            # Récupérer l'étudiant à partir du code
            student = session.query(Student).filter_by(code=student_code).first()

            if student:
                # Rechercher le groupe dans la base de données
                group = session.query(Group).filter_by(name=group_name).first()

                if group:
                    # Rechercher l'évaluation sélectionnée
                    evaluation = session.query(Evalution).filter_by(desc=self.selected_evaluation).first()

                    if evaluation:
                        # Vérifier si une note existe déjà pour cet étudiant et ce groupe
                        existing_note_group = session.query(NoteGoupe).filter_by(student_id=student.id,
                                                                                 group_id=group.id).first()
                        if not existing_note_group:
                            # Si aucun enregistrement n'existe, créer une nouvelle note
                            note_groupe = NoteGoupe(
                                note=None,  # La valeur de la note peut être définie si nécessaire
                                student_id=student.id,
                                group_id=group.id,
                                evalution_id=evaluation.id  # Utiliser l'évaluation récupérée
                            )
                            note_groupe.save()  # Enregistrer dans la base de données

        # Vous pouvez appeler la méthode refresh_students pour actualiser l'affichage après la sauvegarde
        self.refresh_students_per_groupes()


# Main application
if __name__ == "__main__":
    root = Tk()
    app = StudentManagementApp(root)
    root.mainloop()
