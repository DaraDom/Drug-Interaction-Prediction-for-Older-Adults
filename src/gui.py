import traitlets
import ipywidgets as widgets
from IPython.display import display

from .model import Model

class AnalysisGUI:
    def __init__(self, serious_model: Model, reaction_model: Model, age_range: tuple, weight_range: tuple, medications: list) -> None:
        self.serious_model = serious_model
        self.reaction_model = reaction_model

        self.medications_list = medications

        self.gender = widgets.Dropdown(
            options=[("Male", 0), ("Female", 1), ("Other", 2)],
            description="Gender:",
            layout=widgets.Layout(margin="10px 0")
        )

        self.age = widgets.IntSlider(
            min=age_range[0], 
            max=age_range[1], 
            default_value=age_range[0], 
            description="Age (YRs): ",
            layout=widgets.Layout(margin="10px 0")
        )

        self.weight = widgets.FloatSlider(
            min=weight_range[0], 
            max=weight_range[1], 
            default_value=weight_range[0], 
            description="Weight (KGs): ",
            layout=widgets.Layout(margin="10px 0") 
        )
        
        self.medication = MultiSelectWithSearch(
            options=self.medications_list,
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
            width=400,
            height=500,
            layout=widgets.Layout(padding='10px', overflow="hidden")
        )

        self.output = widgets.Label(
            layout=widgets.Layout(padding='10px', border="1px solid", height="120px", width="300px", overflow="auto")
        )

        bottom_left_box = widgets.VBox([self.predict, self.output], layout=widgets.Layout(padding='10px', flex='1', height="auto"))
        left_box = widgets.VBox([self.gender, self.age, self.weight, self.medication, bottom_left_box], layout=widgets.Layout(width="auto"))
        right_box = widgets.VBox([self.body_image])
        
        # Main layout
        main_layout = widgets.VBox([widgets.HBox([left_box, right_box])], layout=widgets.Layout(height="550px", align_self='center'))

        # Display the layout
        display(main_layout)
    
    def on_predict_button_click(self, b) -> None:
        gender = self.gender.value
        age = self.age.value
        weight = self.weight.value
        selected_medications = [True if med in [self.medication.selected_box.value] else False for med in self.medications_list]
        criteria = [gender, age, weight] + selected_medications

        self.output.value = self.serious_model.make_prediction(criteria).upper() + self.reaction_model.make_prediction(criteria).capitalize()


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
            rows=5,
            layout=widgets.Layout(margin="10px 0")
        )
        self.options_box.observe(self._on_select_change, names='value')
        
        self.selected_box = widgets.SelectMultiple(
            options=self.selected_options,
            rows=3
        )
        self.selected_box.observe(self._on_selected_box_change, names='value')
        
        self.label = widgets.Label(value=title)
        
        self.children = [self.label, widgets.VBox([self.search_box, self.options_box, self.selected_box])]
    
    def _on_search_change(self, change):
        search_value = change['new']
        filtered_options = [opt for opt in self.options if search_value.lower() in opt.lower()]
        currently_selected = set(self.options_box.value)
        valid_selected = currently_selected.intersection(filtered_options)
        self.options_box.options = filtered_options
        self.options_box.value = tuple(valid_selected)

    def _on_select_change(self, change):
        selected = list(change['new'])
        selected_options = list(self.selected_box.options)
        for option in selected:
            if option not in selected_options:
                selected_options.append(option)

        self.selected_box.options = selected_options
    
    
    def _on_selected_box_change(self, change):
        selected_items = list(change['new'])
        updated_options = [item for item in self.selected_box.options if item not in selected_items]
        self.selected_box.options = updated_options