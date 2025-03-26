import traitlets
import ipywidgets as widgets
from IPython.display import display

from .model import Model

class AnalysisGUI:
    def __init__(self, serious_model: Model, reaction_model: Model, medications: list) -> None:
        self.serious_model = serious_model
        self.reaction_model = reaction_model

        self.gender = widgets.Dropdown(
            options=[("Male", 0), ("Female", 1), ("Other", 2)],
            description="Gender:",
            layout=widgets.Layout(padding='10px')
        )
        
        self.medication = MultiSelectWithSearch(
            options=medications,
            title="Medications:"
        )

        self.predict = widgets.Button(
            description="Predict",
            layout=widgets.Layout(align_self='center')
        )
        self.predict.on_click(self.on_predict_button_click)

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
        left_box = widgets.VBox([self.gender, self.medication, bottom_left_box])
        right_box = widgets.VBox([self.body_image])
        
        # Main layout
        main_layout = widgets.VBox([widgets.HBox([left_box, right_box])])

        # Display the layout
        display(main_layout)
    
    def on_predict_button_click(self, b) -> None:
        # Make prediction
        self.output.value = self.serious_model#self.serious_model.make_prediction([]) + self.reaction_model.make_prediction([])
        pass



class MultiSelectWithSearch(widgets.VBox):
    def __init__(self, options, title):
        super().__init__()
        self.options = options
        self.selected_options = []
        self.layout = widgets.Layout(margin='10px')
        
        self.search_box = widgets.Text(
            placeholder='Search...'
        )
        self.search_box.observe(self._on_search_change, names='value')
        
        self.options_box = widgets.SelectMultiple(
            options=self.options,
            rows=5,  # Set rows to 5 for options box
            description='Options'
        )
        self.options_box.observe(self._on_select_change, names='value')
        
        self.selected_box = widgets.SelectMultiple(
            options=self.selected_options,
            rows=3,  # Set rows to 3 for selected box
            description='Selected'
        )
        
        self.label = widgets.Label(value=title)
        
        self.children = [self.label, widgets.VBox([self.search_box, self.options_box, self.selected_box])]
    
    def _on_search_change(self, change):
        search_value = change['new']
        filtered_options = [opt for opt in self.options if search_value.lower() in opt.lower()]
        self.options_box.options = filtered_options
    
    def _on_select_change(self, change):
        self.selected_options = list(change['new'])
        self.selected_box.options = self.selected_options