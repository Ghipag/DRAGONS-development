import rdflib
import py2neo
import database_interaction.database_tools as database_tools
import database_interaction.data_extraction as data_extraction
from colorama import init as colorama_init
import design_problem_formulation.design_problem_query_tools as design_problem_query_tools
import design_problem_formulation.product_line_engineering as product_line_engineering
import design_problem_formulation.llm_prompt_generation as llm_prompt_generation
import graph_export.graph_export as graph_export
import interface.interface as interface
import sys  

colorama_init()

def run_process_identification_tool(process_elements):
    sys.path.append("C:/Users/lt17550/University of Bristol/grp-Louis-Timperley-PhD - General/MBSE Design Space Problem Space/MBSE_Design_Space_Problem_Space")

    import process_identification
    import os
    os.chdir("C:/Users/lt17550/University of Bristol/grp-Louis-Timperley-PhD - General/MBSE Design Space Problem Space/MBSE_Design_Space_Problem_Space")

    # now find a candidate process for each possible solution endpoint
    candidate_path_total_cost_list = []
    process_query_list = []
    print('here')
    print(process_elements['solution_ends'])
    for endpoint in process_elements['solution_ends']:
        candidate_path_total_cost,process_query = process_identification.identify_process(MBSE_environment = {'language':'SysML V1',
                                'tool':'Cameo',
                                'method':'SEAM',
                                'simulation_tool':'Cameo_Simulation_Toolkit'},
            solution_end = endpoint,
            suggest_techniques = True,
            varaibility_types = process_elements['variability_type'])
        
        print(f"retrieved candidate solution issue cost: {candidate_path_total_cost}")
        print(f"retrieved path query is:\n {process_query}")
        candidate_path_total_cost_list.append(candidate_path_total_cost)
        process_query_list.append(process_query)

    return candidate_path_total_cost_list, process_query_list

def identify_process_elements(design_query):
    process_elements = {'solution_ends':[],'variability_type':[]}

    # running through possible cases    
    if design_query['query type'] == 'Requirement_to_Function_SA':
        process_elements['solution_ends'].append('Optimum_set_of_system_element_types')
        process_elements['solution_ends'].append('System_Architecture')
        process_elements['variability_type'].append('Element_Type')
        pass

    if design_query['query type'] == 'Function_to_Component_SA':
        process_elements['solution_ends'].append('Optimum_set_of_system_element_types')
        process_elements['solution_ends'].append('System_Architecture')
        process_elements['variability_type'].append('Element_Type')
        pass

    if design_query['query type'] == 'Function_to_Mode_SA':
        process_elements['solution_ends'].append('Optimum_set_of_system_element_types')
        process_elements['solution_ends'].append('System_Architecture')
        process_elements['variability_type'].append('Element_Type')
        pass

    if design_query['query type'] == 'Functional_decomposition_SA':
        process_elements['solution_ends'].append('Optimum_set_of_system_element_types')
        process_elements['solution_ends'].append('System_Architecture')
        process_elements['variability_type'].append('Element_Type')
        pass

    if design_query['query type'] == 'Internal_Interfaces_Analysis':
        process_elements['solution_ends'].append('System_Architecture')
        process_elements['variability_type'].append('Topology')
        pass

    if design_query['query type'] == 'Parametric_Analysis':
        process_elements['solution_ends'].append('Globally_Optimal_Design_Parameters')
        process_elements['solution_ends'].append('Local_Minimum')
        process_elements['variability_type'].append('Parameter')
    return process_elements

def main():
    # tikz queryies
    # MATCH(n:AVDASI_2020_S1_Design_Instance_Element&Subsystem|AVDASI_2020_S1_Design_Instance_Element&Spacecraft)-[r:PARENT]->(n2:AVDASI_2020_S1_Design_Instance_Element&Subsystem|AVDASI_2020_S1_Design_Instance_Element&Spacecraft) RETURN n,n2,r FOR subsystem_diagram
    # MATCH(n:AVDASI_2020_S1_Design_Instance_Element)-[r:POWER_INTERFACE]-(n2:AVDASI_2020_S1_Design_Instance_Element) RETURN n,n2,r FOR power_arch_diagram
    # MATCH(n:AVDASI_2020_S1_Design_Instance_Element:AOCS)<-[r:PARENT]-(n2:AVDASI_2020_S1_Design_Instance_Element)RETURN n,n2,r FOR AOCS_subsystem_diagram
    # MATCH(n:AVDASI_2020_S1_Design_Instance_Element)-[r:PARENT]->(n2:AVDASI_2020_S1_Design_Instance_Element:Power_Subsystem) RETURN n,n2,r FOR power_subsystem_diagram
    # MATCH(n:AVDASI_2020_S1_Design_Instance_Element&Unit|AVDASI_2020_S1_Design_Instance_Element&Subsystem|AVDASI_2020_S1_Design_Instance_Element&Spacecraft)-[r:PARENT]->(n2:AVDASI_2020_S1_Design_Instance_Element&Unit|AVDASI_2020_S1_Design_Instance_Element&Subsystem|AVDASI_2020_S1_Design_Instance_Element&Spacecraft) RETURN n,n2,r for full_breakdown_diagram
    # MATCH(n:AVDASI_2020_S1_Design_Instance_Element&Spacecraft)-[r:PARENT]-(n2:AVDASI_2020_S1_Design_Instance_Element&Function) RETURN n,r,n2

    # graph = py2neo.Graph("bolt://127.0.0.1:7687", auth=('neo4j', 'test'))

    # # # query = """
    # # # MATCH(n:AVDASI_2020_S1_Design_Instance_Element:Spacecraft),(n2:AVDASI_2020_Requirement_Element),(n)-[r]-(n2)  RETURN n,r,n2
    # # # """
    # color_dict = {'Spacecraft': 'blue!20', 'Subsystem': 'red!20', 'Unit': 'green!20','Parameter':'magenta!20','Function':'cyan!20','Requirement':'purple!20'}

    # # # graph_export.export_query_subgraph_to_tikz(graph, query,color_dict,'C:/Users\lt17550/University of Bristol/grp-Louis-Timperley-PhD - General/Thesis and Planning/Latex experimenting/images/var_framework/req_space')
    
    # # query = """
    # # MATCH(n3:AVDASI_2020_alt_Requirement_Element)<-[:SATISFY]-(n:AVDASI_2020_S1_Design_Instance_Element&Function)-[r:PARENT]->(n2:AVDASI_2020_S1_Design_Instance_Element&Subsystem|AVDASI_2020_S1_Design_Instance_Element&Spacecraft) RETURN n,n2,r
    # # """
    # # graph_export.export_query_subgraph_to_tikz(graph, query,color_dict,'C:/Users\lt17550/University of Bristol/grp-Louis-Timperley-PhD - General/Thesis and Planning/Latex experimenting/images/var_framework/sat_comps')
    # query = """MATCH(n:run_2b_Design_Instance_Element)<-[r:PARENT]-(n2:run_2b_Design_Instance_Element)
    # WHERE n2:Unit OR n2:Subsystem OR n2:Spacecraft
    # RETURN n,n2,r"""
    # graph_export.export_query_subgraph_to_tikz(graph, '',color_dict,'C:/Users\lt17550/University of Bristol/grp-Louis-Timperley-PhD - General/Thesis and Planning/Latex experimenting/images/llm/llm_output')
    # exit()
    # connect to neo4j graph
    graph = py2neo.Graph("bolt://127.0.0.1:7687", auth=('neo4j', 'test'))
    database_tools.clear_database(graph)

    # load variability framework
    variability_framework = rdflib.Graph()
    variability_framework.parse("active_framework/rdf_variability_definition_1.ttl")

    # load component classifiers
    component_data = data_extraction.read_data('Components')
    data_extraction.process_component_classifier_data(component_data,graph)
    
    # load Condition classifiers
    condition_data = data_extraction.read_data('Conditions')
    data_extraction.process_condition_classifier_data(condition_data,graph)

    # load mode classifiers
    mode_data = data_extraction.read_data('Modes')
    data_extraction.process_mode_classifier_data(mode_data,graph)

    # load parameter classifiers
    parameter_data = data_extraction.read_data('Parameters')
    data_extraction.process_parameter_classifier_data(parameter_data,graph)
    
    # random generation test
    # generate_random_design(variability_framework,graph)

    # test design problem querying

    #####################################################################
    # Definition of Designs and requirements
    #####################################################################

    # AVDASI 2020
    mission_name = 'AVDASI_2020'
    data_extraction.load_mission_requirements(mission_name,graph)

    # my design
    #my_design_TRUTHS_parameters'
    design_name = 'AVDASI_2020_S1_chapt6'
    design_data = data_extraction.read_data(design_name)
    data_extraction.process_design_data(mission_name,design_name,design_data,graph)

    # querying for design problem formulation
    #'MIS_001','MIS_002','MIS_003','MIS_004','MIS_005','MIS_006','MIS_007','MIS_008','MIS_009','MIS_010','MIS_011','MIS_012','MIS_013','MIS_014','MIS_015','MIS_016'
    #'func-0','func-1','func-2','func-3','func-Day_Standby','func-Eclipse_Standby','func-Eclipse_Safe_Mode'
    #'func-0','func-1','func-2','func-Detumbling','func-Payload_Spinup','func-Safe'
    #'func-0','func-1','func-2','func-3','func-Idle','func-Nominal_Operations','func-Uncontrolled_Orbit_Decay'
    #'DHS-040','DHS-250','GEN-130','GEN-135'
    #'Latency','Data_Storage','observation_downlink_rate'
    #'Data_Storage','observation_downlink_rate','Land_Imaging_Rate','Ocean_Imaging_Rate','Latency'
    #'MIS_010','MIS_011','MIS_014'
    #'TRUTHS_Decontamination','TRUTHS_Deep_Space_Pointing_Manouevre','TRUTHS_HIS_Lunar_Imaging_Manouevre','TRUTHS_Lunar_Spectral_Irradiance_HIS_Obsv','TRUTHS_Lunar_Spectral_Irradiance_OBSC_Obsv','TRUTHS_MMFU_Downlink','TRUTHS_Nadir_Earth_Radiance_Obsv_','TRUTHS_Nadir_Imaging_Manoeuvre','TRUTHS_OBCS_Lunar_Imaging_Manoeuvre','TRUTHS_Off__Nadir_Earth_Radiance_Obsv','TRUTHS_Orbit_Cont_In_Plane','TRUTHS_Orbit_Control_Out_Of_Plane','TRUTHS_S2SC_Manouevre','TRUTHS_SMC_Calibration','TRUTHS_Solar_Calibration_Manouevre','TRUTHS_Solar_Imaging_Manouevre','TRUTHS_Solar_SSI_Obsv','TRUTHS_Solar_TSI_Obsv','TRUTHS_TT&C','Initialisation','DHS_Reconfig'
    #'Power_Supply'
    #['Latency','Data_Storage','observation_downlink_rate']
    #,'GEN-130','GEN-135'
    design_query = {'query type':'Parametric Analysis',
                    'requirement':['MIS_007','MIS_005','MIS_008'],
                    'design variable':[],
                    'dependant variable':['Altitude'],
                    'additional model elements':[]}

    
    
    completed_query,log_record = design_problem_query_tools.design_context_query(variability_framework,design_query,mission_name,design_name,graph)

    # now explain the result abit
    design_problem_query_tools.generate_result_explanation(['AOCS'],True,design_name)
    # identify process related elements
    #process_elements = identify_process_elements(completed_query)

    # now running MBSE process selection tool
    #candidate_path_total_cost, process_query = run_process_identification_tool(process_elements)

    
    interface.show_query_data(completed_query)
    product_line_engineering.present_product_line_info(completed_query,design_name,mission_name,graph,variability_framework)


    #database_tools.relabel_design_relationships('UNCONFIRMED_PARENT','PARENT',design_name,graph)
    # display dict in tkinter window
    #prompt_string,expected_output_types = llm_prompt_generation.generate_prompt(completed_query)

    #print(prompt_string)
    #print(expected_output_types)

if __name__ == "__main__":
    main()

