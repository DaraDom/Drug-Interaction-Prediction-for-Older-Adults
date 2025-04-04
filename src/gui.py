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
        serious_prediction = self.serious_model.make_prediction(criteria)
        serious_value = int(serious_prediction.item())
        criteria = [serious_value] + criteria
        reaction_prediction = self.reaction_model.make_prediction(criteria)

        if serious_value > 0:
            serious_prediction = "Serious"
        else:
            serious_prediction = "Non-Serious"
        
        serious_output = str(serious_prediction).upper()
        reaction_output = str(reaction_prediction).capitalize()
        self.output.value =  f"{serious_output}: {reaction_output}"


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


thresholds_array = [0.0274903  0.13975503 0.08227772 0.04283334 0.2979197  0.15833676
 0.02170037 0.25333005 0.00773242 0.02584355 0.1640971  0.607358
 0.11414348 0.08427174 0.27883527 0.08739183 0.058432   0.0124686
 0.04094156 0.14285906 0.10399323 0.30011907 0.09689189 0.07832858
 0.0613495  0.03659273 0.06773925 0.15019818 0.14769289 0.12304027
 0.02414288 0.10994828 0.09695306 0.01749285 0.03014488 0.03408354
 0.1487771  0.06720072 0.01743384 0.03853117 0.03718285 0.03190257
 0.03222847 0.16417402 0.05735774 0.05857195 0.08093197 0.36498073
 0.01005055 0.01690817 0.06418414 0.03055441 0.05502418 0.01831038
 0.00413069 0.01146009 0.00319467 0.04612214 0.19553626 0.1372304
 0.14587374 0.07711466 0.02224535 0.1948199  0.16433792 0.14691605
 0.15291944 0.11217678 0.23158002 0.1213881  0.17817363 0.0235533
 0.03357412 0.09614486 0.34249437 0.24532446 0.01266216 0.04909281
 0.01896563 0.03126441 0.02616418 0.16684908 0.11527352 0.1767583
 0.2449283  0.06167574 0.00583166 0.09495452 0.03610953 0.6411653
 0.01556343 0.00793177 0.26648962 0.03451781 0.07561529 0.06063308
 0.3122795  0.04821264 0.06725048 0.1865524  0.14228585 0.07733711
 0.27398044 0.04450991 0.03425689 0.4750477  0.14581965 0.0468738
 0.01566956 0.1478769  0.07657202 0.38997018 0.03988124 0.14122802
 0.02385833 0.04196336 0.12309966 0.01395617 0.04427406 0.9117171
 0.27090123 0.09926766 0.01839353 0.15819764 0.07128081 0.02475004
 0.24707144 0.42473018 0.017515   0.4290627  0.01405096 0.03516298
 0.06185616 0.07700349 0.0658781  0.05237873 0.04582319 0.00845057
 0.02759652 0.02743305 0.01373747 0.03211843 0.00713695 0.02119831
 0.01692987 0.04798335 0.03414918 0.00691756 0.04976577 0.08930193
 0.5938834  0.01801203 0.29278228 0.45479155 0.07092148 0.03670707
 0.03081669 0.03051532 0.11138986 0.03558196 0.49136662 0.07485937
 0.1846213  0.0235216  0.01399601 0.03542549 0.0287015  0.00871856
 0.03022513 0.14553171 0.11253554 0.05944852 0.13766575 0.06084185
 0.20498163 0.06040015 0.11150779 0.1495197  0.03883167 0.01615218
 0.20560116 0.11991285 0.08107027 0.08954743 0.47556904 0.24488991
 0.5397885  0.5254035  0.14805163 0.63235664 0.03471529 0.1021436
 0.09714893 0.01811591 0.0486724  0.08057739 0.01579445 0.01272796
 0.02183337 0.16124636 0.06716927 0.00466019 0.01563043 0.11428384
 0.9999945  0.03977557 0.01204185 0.18634298 0.01999301 0.21999426
 0.05789326 0.09869695 0.24121709 0.03243283 0.06257305 0.12061812
 0.09299278 0.0277959  0.05066868 0.0478061  0.16724543 0.00771242
 0.02787822 0.20566577 0.05346865 0.04108108 0.27488086 0.07949415
 0.17025523 0.01948842 0.02976358 0.08814745 0.00794012 0.14551802
 0.5557915  0.10835022 0.08633371 0.0573112  0.05010774 0.10001227
 0.12697005 0.39694893 0.05412719 0.0145994  0.13894436 0.0742055
 0.08864275 0.08071638 0.18712701 0.08151952 0.07348089 0.19764175
 0.07421436 0.20194092 0.14796843 0.17467284 0.09737141 0.05884223
 0.02899146 0.12964836 0.06546739 0.00561016 0.01276935 0.2020029
 0.15120973 0.24460548 0.02542409 0.09357306 0.02207533 0.00419486
 0.02324264 0.00471873 0.07694098 0.01329413 0.26751468 0.08470616
 0.01883966 0.13780281 0.08479439 0.12143107 0.08962314 0.23677818
 0.04196487 0.28531423 0.04004873 0.04753681 0.1416763  0.01318873
 0.07223789 0.00731885 0.01007321 0.01804912 0.01148198 0.06234243
 0.10553056 0.04595133 0.11187904 0.0442166  0.1236579  0.01121264
 0.9169064  0.06616384 0.29042935 0.06075688 0.0501739  0.00861545
 0.03801812 0.05823302 0.03252592 0.05865234 0.02188843 0.05101855
 0.00784464 0.02947189 0.05425466 0.01708553 0.12443827 0.1614054
 0.02184926 0.01800163 0.03187975 0.16470225 0.04673842 0.08782747
 0.06631626 0.02872275 0.06911842 0.582065   0.13371089 0.0609382
 0.02482737 0.45733216 0.18680859 0.04263834 0.08310306 0.0942639
 0.0459327  0.0499472  0.0721987  0.21023907 0.11083926 0.02123851
 0.2934855  0.04745171 0.10140596 0.01555271 0.15014797 0.01402156
 0.0912765  0.03919244 0.00623469 0.0655871  0.06378233 0.06076755
 0.05769528 0.01079635 0.10141654 0.01643972 0.08126785 0.00853063
 0.03091657 0.00615764 0.16308667 0.04002573 0.10165753 0.21094365
 0.05014674 0.0394659  0.12288646 0.15129109 0.20674638 0.04124479
 0.02755236 0.11659881 0.05128151 0.7374472  0.06623259 0.0465019
 0.10359412 0.00820567 0.41556573 0.09785422 0.04843507 0.04050831
 0.05254212 0.44426706 0.01020936 0.0938003  0.09289219 0.16127418
 0.06872421 0.13880354 0.02627569 0.19527213 0.07548724 0.07834333
 0.01361789 0.2866797  0.01805876 0.32249886 0.1068567  0.05156286
 0.32760793 0.04066464 0.03832148 0.03161303 0.12851657 0.760034
 0.12606482 0.05811122 0.05702012 0.03595426 0.16376004 0.01315872
 0.02929652 0.13337258 0.04336503 0.04979939 0.08439414 0.03863441
 0.35483345 0.03401716 0.23028848 0.02133201 0.2924088  0.6267278
 0.01820709 0.28745013 0.10115039 0.01718555 0.37598944 0.08072064
 0.14416638 0.04630007 0.07280144 0.2938328  0.00649681 0.15349144
 0.00958743 0.0208918  0.00479832 0.26639384 0.0367294  0.11621187
 0.03493073 0.00904816 0.00326959 0.02650616 0.04573274 0.01580653
 0.10383325 0.03371992 0.01136371 0.13440287 0.07185315 0.04761355
 0.18169777 0.05631506 0.08074876 0.02945596 0.03115058 0.2715203
 0.22532111 0.0812908  0.11202987 0.01549125 0.02221817 0.0963918
 0.11639515 0.10920394 0.09279837 0.02241669 0.40588552 0.02239146
 0.03153571 0.03256612 0.0642589  0.21877146 0.0891879  0.07989709
 0.25015047 0.02897482 0.02959569 0.05507597 0.3117524  0.09504059
 0.02721942 0.06173706 0.64040345 0.32804692 0.06008625 0.05252918
 0.69980127 0.09779131 0.05430489 0.34197184 0.11418729 0.06183574
 0.25226563 0.06042855 0.11771405 0.054735   0.04068165 0.20920171
 0.11350874 0.03438887 0.03556013 0.02695324 0.1961562  0.20720004
 0.079441   0.05175635 0.04792799 0.01829943 0.4163711  0.1266147
 0.14577891 0.05893509 0.03028549 0.06100473 0.16004993 0.16175163
 0.02094244 0.0495997  0.10310115 0.05583159 0.08019254 0.08345492
 0.06178379 0.08808021 0.20862252 0.10376033 0.0945804  0.11248534
 0.14501582 0.3047019  0.41848138 0.14776379 0.04394774 0.06196207
 0.02075386 0.11818009 0.01383125 0.0484159  0.23969643 0.05400544
 0.35500148 0.44615158 0.02784009 0.04027839 0.18842171 0.07254374
 0.22352912 0.04863141 0.04447925 0.01556953 0.01711273 0.00379257
 0.02846939 0.17424877 0.00816052 0.0119103  0.01645604 0.16638048
 0.2413069  0.07220677 0.07557704 0.02135066 0.03461238 0.01151288]