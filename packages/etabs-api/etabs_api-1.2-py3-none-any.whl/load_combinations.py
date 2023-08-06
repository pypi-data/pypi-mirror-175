
from typing import Union


class LoadCombination:
    def __init__(
                self,
                etabs=None,
                ):
        self.etabs = etabs
        self.SapModel = etabs.SapModel

    def add_load_combination(
        self,
        combo_name: str,
        load_case_names: list = [],
        scale_factor: float = 1,
        type_: int = 0, # envelop: 1
        ):
        '''
        Add Envelop Load combination
        '''
        self.etabs.SapModel.RespCombo.add(combo_name, type_)
        for case_name in load_case_names:
            self.etabs.SapModel.RespCombo.SetCaseList(
                combo_name,
                type_, # loadcase=0, loadcombo=1
                case_name,    # cname
                scale_factor,    # sf
                )

    def get_load_combinations_of_type(
        self,
        type_: str = 'ALL', # 'GRAVITY' , 'SEISMIC
        all_load_combos: Union[list, bool] = None,
        ):
        '''
        return load combinations with respect to type_
        '''
        if all_load_combos is None:
            all_load_combos = self.SapModel.RespCombo.GetNameList()[1]
        if type_ == 'ALL':
            return all_load_combos
        seismic_load_cases = self.etabs.load_cases.get_seismic_load_cases()
        seismic_load_combos = []
        for combo in all_load_combos:
            if self.is_seismic(
                        combo,
                        seismic_load_cases=seismic_load_cases,
                        ):
                seismic_load_combos.append(combo)
        if type_ == 'SEISMIC':
            return seismic_load_combos
        elif type_ == "GRAVITY":
            return set(all_load_combos).difference(seismic_load_combos)
        
    def is_seismic(
        self,
        combo: str,
        seismic_load_cases: Union[list, bool] = None,
        ):
        if seismic_load_cases is None:
            seismic_load_cases = self.etabs.load_cases.get_seismic_load_cases()
        load_cases = self.SapModel.RespCombo.GetCaseList(combo)[2]
        for lc in load_cases:
            if lc in seismic_load_cases:
                return True
        return False


def get_mabhas6_load_combinations(
    way='LRFD', # 'ASD'
    separate_direction: bool = False,
    ):
    '''
    separate_direction: For 100-30 earthquake
    '''
    if separate_direction:
        if way == "LRFD":
            return {
                '11'   : {'Dead':1.4},
                '21'   : {'Dead':1.2 , 'L':1.6, 'L_5':1.6, 'RoofLive':0.5},
                '22'   : {'Dead':1.2 , 'L':1.6, 'L_5':1.6, 'Snow':0.5},
                '31'   : {'Dead':1.2, 'L':1, 'L_5':0.5, 'RoofLive':1.6},
                '32'   : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':1.6},
                '41'   : {'Dead':1.2, 'L':1, 'L_5':0.5, 'RoofLive':0.5},
                '42'   : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.5},
                '51'   : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'EPX': 1, 'EV':1},
                '52'   : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'ENX': 1, 'EV':1},
                '53'   : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'EPX':-1, 'EV':1},
                '54'   : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'ENX':-1, 'EV':1},
                '55'   : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'ENY': 1, 'EV':1},
                '56'  : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'EPY': 1, 'EV':1},
                '57'  : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'EPY':-1, 'EV':1},
                '58'  : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'ENY':-1, 'EV':1},
                '71'   : {'Dead':0.9, 'EPX': 1, 'EV':-1},
                '72'   : {'Dead':0.9, 'ENX': 1, 'EV':-1},
                '73'   : {'Dead':0.9, 'EPX':-1, 'EV':-1},
                '74'   : {'Dead':0.9, 'ENX':-1, 'EV':-1},
                '75'  : {'Dead':0.9, 'EPY': 1, 'EV':-1},
                '76'   : {'Dead':0.9, 'ENY': 1, 'EV':-1},
                '77'  : {'Dead':0.9, 'EPY':-1, 'EV':-1},
                '78'  : {'Dead':0.9, 'ENY':-1, 'EV':-1},
            }
        elif way == "ASD":
            return {
                '11'   : {'Dead':1},
                '21'   : {'Dead':1, 'L':1, 'L_5':1},
                '31'   : {'Dead':1, 'Snow':1},
                '32'   : {'Dead':1, 'RoofLive':1},
                '41'   : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75},
                '42'   : {'Dead':1, 'L':0.75, 'L_5':0.75, 'RoofLive':0.75},
                '71'   : {'Dead':1, 'EPX': 0.7, 'EV':1},
                '72'   : {'Dead':1, 'ENX': 0.7, 'EV':1},
                '73'   : {'Dead':1, 'EPX':-0.7, 'EV':1},
                '74'   : {'Dead':1, 'ENX':-0.7, 'EV':1},
                '75'   : {'Dead':1, 'ENY': 0.7, 'EV':1},
                '76'  : {'Dead':1, 'EPY': 0.7, 'EV':1},
                '77'  : {'Dead':1, 'EPY':-0.7, 'EV':1},
                '78'  : {'Dead':1, 'ENY':-0.7, 'EV':1},
                '79'  : {'Dead':1, 'EX': 0.7, 'EV':1},
                '710'  : {'Dead':1, 'EX':-0.7, 'EV':1},
                '711'  : {'Dead':1, 'EY': 0.7, 'EV':1},
                '712'  : {'Dead':1, 'EY':-0.7, 'EV':1},
                '81'   : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EPX': 0.525, 'EV':1},
                '82'   : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'ENX': 0.525, 'EV':1},
                '83'   : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EPX':-0.525, 'EV':1},
                '84'   : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'ENX':-0.525, 'EV':1},
                '85'   : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'ENY': 0.525, 'EV':1},
                '86'  : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EPY': 0.525, 'EV':1},
                '87'  : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EPY':-0.525, 'EV':1},
                '88'  : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'ENY':-0.525, 'EV':1},
                '89'  : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EX' : 0.525, 'EV':1},
                '810'  : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EX' :-0.525, 'EV':1},
                '811'  : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EY' : 0.525, 'EV':1},
                '812'  : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EY' :-0.525, 'EV':1},
                '101'  : {'Dead':0.6, 'EPX': 0.7, 'EV':-1},
                '102'  : {'Dead':0.6, 'ENX': 0.7, 'EV':-1},
                '103'  : {'Dead':0.6, 'EPX':-0.7, 'EV':-1},
                '104'  : {'Dead':0.6, 'ENX':-0.7, 'EV':-1},
                '105'  : {'Dead':0.6, 'ENY': 0.7, 'EV':-1},
                '106' : {'Dead':0.6, 'EPY': 0.7, 'EV':-1},
                '107' : {'Dead':0.6, 'EPY':-0.7, 'EV':-1},
                '108' : {'Dead':0.6, 'ENY':-0.7, 'EV':-1},
                '109' : {'Dead':0.6, 'EX' : 0.7, 'EV':-1},
                '1010' : {'Dead':0.6, 'EX' :-0.7, 'EV':-1},
                '1011' : {'Dead':0.6, 'EY' : 0.7, 'EV':-1},
                '1012' : {'Dead':0.6, 'EY' :-0.7, 'EV':-1},
            }
    else:
        if way == "LRFD":
            return {
                '11'   : {'Dead':1.4},
                '21'   : {'Dead':1.2 , 'L':1.6, 'L_5':1.6, 'RoofLive':0.5},
                '22'   : {'Dead':1.2 , 'L':1.6, 'L_5':1.6, 'Snow':0.5},
                '31'   : {'Dead':1.2, 'L':1, 'L_5':0.5, 'RoofLive':1.6},
                '32'   : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':1.6},
                '41'   : {'Dead':1.2, 'L':1, 'L_5':0.5, 'RoofLive':0.5},
                '42'   : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.5},
                '51'   : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'EPX': 1, 'EY': 0.3, 'EV':1},
                '52'   : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'ENX': 1, 'EY': 0.3, 'EV':1},
                '53'   : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'EPX': 1, 'EY':-0.3, 'EV':1},
                '54'   : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'ENX': 1, 'EY':-0.3, 'EV':1},
                '55'   : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'EPX':-1, 'EY': 0.3, 'EV':1},
                '56'   : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'ENX':-1, 'EY': 0.3, 'EV':1},
                '57'   : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'EPX':-1, 'EY':-0.3, 'EV':1},
                '58'   : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'ENX':-1, 'EY':-0.3, 'EV':1},
                '59'   : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'ENY': 1, 'EX': 0.3, 'EV':1},
                '510'  : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'EPY': 1, 'EX': 0.3, 'EV':1},
                '511'  : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'EPY': 1, 'EX':-0.3, 'EV':1},
                '512'  : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'ENY': 1, 'EX':-0.3, 'EV':1},
                '513'  : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'EPY':-1, 'EX': 0.3, 'EV':1},
                '514'  : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'ENY':-1, 'EX': 0.3, 'EV':1},
                '515'  : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'EPY':-1, 'EX':-0.3, 'EV':1},
                '516'  : {'Dead':1.2, 'L':1, 'L_5':0.5, 'Snow':0.2, 'ENY':-1, 'EX':-0.3, 'EV':1},
                '71'   : {'Dead':0.9, 'EPX': 1, 'EY': 0.3, 'EV':-1},
                '72'   : {'Dead':0.9, 'ENX': 1, 'EY': 0.3, 'EV':-1},
                '73'   : {'Dead':0.9, 'EPX': 1, 'EY':-0.3, 'EV':-1},
                '74'   : {'Dead':0.9, 'ENX': 1, 'EY':-0.3, 'EV':-1},
                '75'   : {'Dead':0.9, 'EPX':-1, 'EY': 0.3, 'EV':-1},
                '76'   : {'Dead':0.9, 'ENX':-1, 'EY': 0.3, 'EV':-1},
                '77'   : {'Dead':0.9, 'EPX':-1, 'EY':-0.3, 'EV':-1},
                '78'   : {'Dead':0.9, 'ENX':-1, 'EY':-0.3, 'EV':-1},
                '79'   : {'Dead':0.9, 'ENY': 1, 'EX': 0.3, 'EV':-1},
                '710'  : {'Dead':0.9, 'EPY': 1, 'EX': 0.3, 'EV':-1},
                '711'  : {'Dead':0.9, 'EPY': 1, 'EX':-0.3, 'EV':-1},
                '712'  : {'Dead':0.9, 'ENY': 1, 'EX':-0.3, 'EV':-1},
                '713'  : {'Dead':0.9, 'EPY':-1, 'EX': 0.3, 'EV':-1},
                '714'  : {'Dead':0.9, 'ENY':-1, 'EX': 0.3, 'EV':-1},
                '715'  : {'Dead':0.9, 'EPY':-1, 'EX':-0.3, 'EV':-1},
                '716'  : {'Dead':0.9, 'ENY':-1, 'EX':-0.3, 'EV':-1},
            }
        elif way == "ASD":
            return {
                '11'   : {'Dead':1},
                '21'   : {'Dead':1, 'L':1, 'L_5':1},
                '31'   : {'Dead':1, 'Snow':1},
                '32'   : {'Dead':1, 'RoofLive':1},
                '41'   : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75},
                '42'   : {'Dead':1, 'L':0.75, 'L_5':0.75, 'RoofLive':0.75},
                '71'   : {'Dead':1, 'EPX': 0.7, 'EY': 0.21, 'EV':1},
                '72'   : {'Dead':1, 'ENX': 0.7, 'EY': 0.21, 'EV':1},
                '73'   : {'Dead':1, 'EPX': 0.7, 'EY':-0.21, 'EV':1},
                '74'   : {'Dead':1, 'ENX': 0.7, 'EY':-0.21, 'EV':1},
                '75'   : {'Dead':1, 'EPX':-0.7, 'EY': 0.21, 'EV':1},
                '76'   : {'Dead':1, 'ENX':-0.7, 'EY': 0.21, 'EV':1},
                '77'   : {'Dead':1, 'EPX':-0.7, 'EY':-0.21, 'EV':1},
                '78'   : {'Dead':1, 'ENX':-0.7, 'EY':-0.21, 'EV':1},
                '79'   : {'Dead':1, 'ENY': 0.7, 'EX': 0.21, 'EV':1},
                '710'  : {'Dead':1, 'EPY': 0.7, 'EX': 0.21, 'EV':1},
                '711'  : {'Dead':1, 'EPY': 0.7, 'EX':-0.21, 'EV':1},
                '712'  : {'Dead':1, 'ENY': 0.7, 'EX':-0.21, 'EV':1},
                '713'  : {'Dead':1, 'EPY':-0.7, 'EX': 0.21, 'EV':1},
                '714'  : {'Dead':1, 'ENY':-0.7, 'EX': 0.21, 'EV':1},
                '715'  : {'Dead':1, 'EPY':-0.7, 'EX':-0.21, 'EV':1},
                '716'  : {'Dead':1, 'ENY':-0.7, 'EX':-0.21, 'EV':1},
                '717'  : {'Dead':1, 'EX': 0.7, 'EY': 0.21, 'EV':1},
                '718'  : {'Dead':1, 'EX':-0.7, 'EY': 0.21, 'EV':1},
                '719'  : {'Dead':1, 'EX': 0.7, 'EY':-0.21, 'EV':1},
                '720'  : {'Dead':1, 'EX':-0.7, 'EY':-0.21, 'EV':1},
                '721'  : {'Dead':1, 'EY': 0.7, 'EX': 0.21, 'EV':1},
                '722'  : {'Dead':1, 'EY':-0.7, 'EX': 0.21, 'EV':1},
                '723'  : {'Dead':1, 'EY': 0.7, 'EX':-0.21, 'EV':1},
                '724'  : {'Dead':1, 'EY':-0.7, 'EX':-0.21, 'EV':1},
                '81'   : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EPX': 0.525, 'EY': 0.1575, 'EV':1},
                '82'   : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'ENX': 0.525, 'EY': 0.1575, 'EV':1},
                '83'   : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EPX': 0.525, 'EY':-0.1575, 'EV':1},
                '84'   : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'ENX': 0.525, 'EY':-0.1575, 'EV':1},
                '85'   : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EPX':-0.525, 'EY': 0.1575, 'EV':1},
                '86'   : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'ENX':-0.525, 'EY': 0.1575, 'EV':1},
                '87'   : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EPX':-0.525, 'EY':-0.1575, 'EV':1},
                '88'   : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'ENX':-0.525, 'EY':-0.1575, 'EV':1},
                '89'   : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'ENY': 0.525, 'EX': 0.1575, 'EV':1},
                '810'  : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EPY': 0.525, 'EX': 0.1575, 'EV':1},
                '811'  : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EPY': 0.525, 'EX':-0.1575, 'EV':1},
                '812'  : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'ENY': 0.525, 'EX':-0.1575, 'EV':1},
                '813'  : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EPY':-0.525, 'EX': 0.1575, 'EV':1},
                '814'  : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'ENY':-0.525, 'EX': 0.1575, 'EV':1},
                '815'  : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EPY':-0.525, 'EX':-0.1575, 'EV':1},
                '816'  : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'ENY':-0.525, 'EX':-0.1575, 'EV':1},
                '817'  : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EX' : 0.525, 'EY': 0.1575, 'EV':1},
                '818'  : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EX' : 0.525, 'EY':-0.1575, 'EV':1},
                '819'  : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EX' :-0.525, 'EY': 0.1575, 'EV':1},
                '820'  : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EX' :-0.525, 'EY':-0.1575, 'EV':1},
                '821'  : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EY' : 0.525, 'EX': 0.1575, 'EV':1},
                '822'  : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EY' : 0.525, 'EX':-0.1575, 'EV':1},
                '823'  : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EY' :-0.525, 'EX': 0.1575, 'EV':1},
                '824'  : {'Dead':1, 'L':0.75, 'L_5':0.75, 'Snow':0.75, 'EY' :-0.525, 'EX':-0.1575, 'EV':1},
                '101'  : {'Dead':0.6, 'EPX': 0.7, 'EY': 0.21, 'EV':-1},
                '102'  : {'Dead':0.6, 'ENX': 0.7, 'EY': 0.21, 'EV':-1},
                '103'  : {'Dead':0.6, 'EPX': 0.7, 'EY':-0.21, 'EV':-1},
                '104'  : {'Dead':0.6, 'ENX': 0.7, 'EY':-0.21, 'EV':-1},
                '105'  : {'Dead':0.6, 'EPX':-0.7, 'EY': 0.21, 'EV':-1},
                '106'  : {'Dead':0.6, 'ENX':-0.7, 'EY': 0.21, 'EV':-1},
                '107'  : {'Dead':0.6, 'EPX':-0.7, 'EY':-0.21, 'EV':-1},
                '108'  : {'Dead':0.6, 'ENX':-0.7, 'EY':-0.21, 'EV':-1},
                '109'  : {'Dead':0.6, 'ENY': 0.7, 'EX': 0.21, 'EV':-1},
                '1010' : {'Dead':0.6, 'EPY': 0.7, 'EX': 0.21, 'EV':-1},
                '1011' : {'Dead':0.6, 'EPY': 0.7, 'EX':-0.21, 'EV':-1},
                '1012' : {'Dead':0.6, 'ENY': 0.7, 'EX':-0.21, 'EV':-1},
                '1013' : {'Dead':0.6, 'EPY':-0.7, 'EX': 0.21, 'EV':-1},
                '1014' : {'Dead':0.6, 'ENY':-0.7, 'EX': 0.21, 'EV':-1},
                '1015' : {'Dead':0.6, 'EPY':-0.7, 'EX':-0.21, 'EV':-1},
                '1016' : {'Dead':0.6, 'ENY':-0.7, 'EX':-0.21, 'EV':-1},
                '1017' : {'Dead':0.6, 'EX' : 0.7, 'EY': 0.21, 'EV':-1},
                '1018' : {'Dead':0.6, 'EX' : 0.7, 'EY':-0.21, 'EV':-1},
                '1019' : {'Dead':0.6, 'EX' :-0.7, 'EY': 0.21, 'EV':-1},
                '1020' : {'Dead':0.6, 'EX' :-0.7, 'EY':-0.21, 'EV':-1},
                '1021' : {'Dead':0.6, 'EY' : 0.7, 'EX': 0.21, 'EV':-1},
                '1022' : {'Dead':0.6, 'EY' : 0.7, 'EX':-0.21, 'EV':-1},
                '1023' : {'Dead':0.6, 'EY' :-0.7, 'EX': 0.21, 'EV':-1},
                '1024' : {'Dead':0.6, 'EY' :-0.7, 'EX':-0.21, 'EV':-1},
            }

def generate_concrete_load_combinations(
    # load_patterns : {Uist,':nio bool] = None,
    equivalent_loads : dict,
    prefix : str = 'COMBO',
    suffix : str = '',
    rho_x : float = 1,
    rho_y : float = 1,
    type_ : str = 'Linear Add',
    design_type: str = 'LRFD',
    separate_direction: bool = False,
    ev_negative: bool = True,
    ):
    data = []
    for number, combos in get_mabhas6_load_combinations(design_type, separate_direction).items():
        for lname, sf in combos.items():
            if lname in ('EX', 'EPX', 'ENX'):
                sf *= rho_x
            elif lname in ('EY', 'EPY', 'ENY'):
                sf *= rho_y
            elif lname == 'EV' and not ev_negative and sf < 0:
                continue
            equal_names = equivalent_loads.get(lname, [])
            for name in equal_names:
                combo_name = f'{prefix}{number}{suffix}'
                data.extend([combo_name, type_, name, sf])
    return data
        







    
    
        
        
        

    