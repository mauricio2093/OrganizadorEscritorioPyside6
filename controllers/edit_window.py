import os
import  shutil

from PySide6.QtWidgets import QWidget, QFileDialog
from PySide6.QtCore import Qt

from views.add_edit_window import AddEditWindow
from views.general_custom_ui import GeneralCustomUi

from database import recipes


class EditWindowForm(QWidget, AddEditWindow):

    def __int__(self, parent = None, recipe_id = None):
        self.recipe_id = recipe_id

        super().__init__(parent)
        self.setupGui(self)
        self.ui = GeneralCustomUi(self)
        self.setWindowFlag(Qt.Window)

        self.fill_inputs()
        self.ui.fill_category_cb()
        self.add_edit_button.setText("Editar")
        self.add_edit_button.clicked.connect(self.update_recipe)
        self.select_img_button.clicked.connect(self.select_img)

    def mousePressEvent(self, event) :
        self.ui.mouse_press_event(event)

    def update_recipe(self):
        title =  self.title_line_edit.text()
        category = self.category_comboBox.currentText()
        url = self.url_line_edit.text()
        budget = self.budget_line_edit.text() 
        img_path  = f"images\{self.image_path_line_edit.text()}"
        ingredients = self.ingredients_text_edit.toPlainText()
        directions = self.direction_text_edit.toPlainText()

        data = (title, category, url, budget, img_path, ingredients, directions)

        if recipes.update(self.recipe_id, data):
            self.replace_img()
            print("Recipe Edited")
            self.close()

    def fill_inputs(self):
        data = recipes.select_by_id(self.recipe_id)

        self.title_line_edit.setText(data[1])
        self.category_comboBox.setCurrentText(data[2])
        self.url_line_edit.setText(data[3])
        self.budget_line_edit.setText(str(data[4]))

        img_name = data[5].split("\\")[-1]

        self.old_image = img_name
        self.new_img = img_name

        self.image_path_line_edit.setText(img_name)
        self.ingredients_text_edit.setPlainText(data[7])

    def select_img(self):
        self.img_path_from = QFileDialog.getOpenFileName()[0]

        if self.img_path_from:
            self.new_img = self.img_path_from.split("/")[-1]
            self.image_path_line_edit.setText(self.new_img)

    def replace_img(self):
        if self.old_image != self.new_img:
            os.remove("images\\" + self.old_image)
            shutil.copy(self.img_path_from, "images")
