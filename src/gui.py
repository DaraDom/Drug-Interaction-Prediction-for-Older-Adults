import ipywidgets as widgets
from IPython.display import display

class AnalysisGUI:
    def __init__(self, model) -> None:
        self.model = model

        self.gender = widgets.Dropdown(
            options=[("Male", 0), ("Female", 1), ("Other", 2)],
            description="Gender:",
            layout=widgets.Layout(padding='10px')
        )
        self.medication = widgets.SelectMultiple(
            options=["Insulin"],
            description="Medications:",
            layout=widgets.Layout(padding='10px')
        )

        self.allergies = widgets.SelectMultiple(
            options=["Hay Fever", "Lactose Intolerant"],
            description="Allergies:",
            layout=widgets.Layout(padding='10px')
        )

        self.predict = widgets.Button(
            description="Predict",
            layout=widgets.Layout(align_self='center')
        )

        self.body_image = widgets.Image(
            value=open("assets/imgs/body.png", "rb").read(),
            format='png',
            width=300,
            height=400,
            layout=widgets.Layout(padding='10px')
        )

        self.output = widgets.Label(
            layout=widgets.Layout(padding='10px', border="1px solid", flex='1')
        )

        bottom_left_box = widgets.VBox([self.predict, self.output], layout=widgets.Layout(padding='10px', flex='1'))
        left_box = widgets.VBox([self.gender, self.medication, self.allergies, bottom_left_box], height=400)
        right_box = widgets.VBox([self.body_image])
        
        # Main layout
        main_layout = widgets.VBox([widgets.HBox([left_box, right_box])])

        # Display the layout
        display(main_layout)
    
    def on_predict_button_click(self) -> None:
        # Change output box
        self.output.value = self.model.make_prediction()

        # Highlight part of image