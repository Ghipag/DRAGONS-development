import pandas as pd
import database_interaction.database_tools as database_tools
import plotly.graph_objects as go
import plotly.express as px
import urllib, json
import graph_export.graph_plotting as graph_plotting
from tqdm import tqdm

class difference_record:
    """
    Represents a difference record between two design elements.

    This class defines a difference record object that encapsulates information about a difference
    between two design elements from different designs. It includes attributes for the names and elements
    of the two designs, a key to identify the difference, and specifics about the difference.

    @param design_A_name: The name of the first design.
    @type design_A_name: str

    @param design_A_element: The element in the first design.
    @type design_A_element: str

    @param design_B_name: The name of the second design.
    @type design_B_name: str

    @param design_B_element: The element in the second design.
    @type design_B_element: str

    @param key: The key to identify the difference.
    @type key: str

    @param difference_specifics: Specific details about the difference.
    @type difference_specifics: str

    @pre 'design_A_name', 'design_A_element', 'design_B_name', 'key', and 'difference_specifics' should be valid strings.
         'design_B_element' can be a dictionary with the 'n' key containing the 'uid' value.

    @see: This class is used to represent and store difference records.
    """
    def __init__(self,design_A_name,design_A_element,design_B_name,design_B_element,key,difference_specifics):
        self.design_A_name = design_A_name
        self.design_A_element = design_A_element
        self.design_B_name = design_B_name
        self.design_B_element = design_B_element[0]['n']['uid']
        self.key = key
        if type(difference_specifics) is dict:
            self.difference_specifics = f'{difference_specifics["target"]} {difference_specifics["target_classifier"]}'
        else:
            self.difference_specifics = difference_specifics

class comparison_record:
    """
    Represents a comparison record between multiple design elements.

    This class defines a comparison record object that encapsulates information about a comparison
    between multiple design elements from different designs. It includes attributes for the names of the
    designs and elements involved in the comparison, a key to identify the comparison, and a list to store
    discovered differences.

    @param design_names: The names of the designs involved in the comparison.
    @type design_names: list of str

    @param design_elements: The elements in the designs to be compared.
    @type design_elements: list of dictionaries

    @param key: The key to identify the comparison.
    @type key: str

    @pre 'design_names' should be a valid list of strings, 'design_elements' should be a list of dictionaries
         where each dictionary contains an 'n' key with a 'uid' value, and 'key' should be a valid string.

    @see: This class is used to represent and store comparison records.
    """
    def __init__(self,design_names,design_elements,key):
        # generate name by alphabetically sorting design names and elements and using the following template
        sorted_design_names = sorted(design_names)
        # sorting design_element names
        design_element_names = []
        for element in design_elements:
            design_element_names.append(element[0]['n']['uid'])
        sorted_design_elements = sorted(design_element_names)
        self.name = (f"{sorted_design_names}->{sorted_design_elements}>>{key}").replace("'",'')
        self.design_names = sorted_design_names
        self.design_elements = sorted_design_elements
        self.key = key
        self.discovered_differences = []      

class object_location_pair:
    """
    Represents a pair of an object and its associated location.

    This class defines an object-location pair, where 'element' represents the object and 'location' represents its associated location.

    @param element: The object to be paired.
    @type element: any

    @param location: The location associated with the object.
    @type location: any

    @pre 'element' and 'location' can be of any type, as this class provides a general-purpose object-location pairing.

    @see: This class can be used to represent and store pairs of objects and their corresponding locations.
    """
    def __init__(self,element,location):
        self.element = element
        self.location = location

def identify_pairwise_design_union(names,graphs):
    """
    Identify and mark elements that are shared classifiers between two designs.

    This function takes two design names and their corresponding Neo4j graph database connections.
    It identifies elements that are shared classifiers between the two designs and marks them by adding a
    common comparison name as a label to these elements. The comparison name is generated based on the input design names.

    @param names: A list containing the names of the two designs to be compared.
    @type names: list of str

    @param graphs: A list containing Neo4j graph database connections for the two designs.
    @type graphs: list of neo4j.Graph

    @pre 'names' should be a list containing exactly two design names as strings, and 'graphs' should be a list containing
         the corresponding Neo4j graph database connections.

    @see: This function is used to identify and mark shared classifiers between two designs in Neo4j.
    """
    comparison_name = names[0]+'_vs_'+names[1]+'_SHARED_Classifier'

    query = """
            MATCH (n1:"""+names[0]+"""_Design_Instance_Element),(classifier),(n2:"""+names[1]+"""_Design_Instance_Element)
            WHERE (n1)-[:CLASSIFIER]->(classifier) AND (n2)-[:CLASSIFIER]->(classifier)
            SET n1:"""+comparison_name+""", n2:"""+comparison_name+"""
            """
    database_tools.run_neo_query(['nil'],query,graphs)

def identify_dissimilar_node_classifiers(names,graphs):
    """
    Identify and return dissimilar node classifiers between two designs.

    This function takes two design names and their corresponding Neo4j graph database connections.
    It identifies node classifiers that are dissimilar between the two designs and returns them.

    @param names: A list containing the names of the two designs to be compared.
    @type names: list of str

    @param graphs: A list containing Neo4j graph database connections for the two designs.
    @type graphs: list of neo4j.Graph

    @return: A result set containing dissimilar node classifiers between the two designs.
    @rtype: neo4j.Result

    @pre 'names' should be a list containing exactly two design names as strings, and 'graphs' should be a list containing
         the corresponding Neo4j graph database connections.

    @see: This function is used to identify and return dissimilar node classifiers between two designs in Neo4j.
    """
    joint_label_name = names[0]+'_vs_'+names[1]+'_SHARED'
    query = """
            MATCH (n1:"""+names[0]+"""_Design_Instance_Element),(n2:"""+names[1]+"""_Design_Instance_Element)
            WHERE NOT n1:"""+joint_label_name+""" AND NOT n2:"""+joint_label_name+"""
            RETURN n1, n2
            """
    database_tools.run_neo_query(['nil'],query,graphs)

def identify_value_differences(names,graphs):
    """
    Identify and mark parameter value differences between two designs.

    This function takes two design names and their corresponding Neo4j graph database connections.
    It identifies parameter value differences between the two designs and marks the parameters by adding a
    common comparison name as a label to these parameters. The comparison name is generated based on the input design names.

    @param names: A list containing the names of the two designs to be compared.
    @type names: list of str

    @param graphs: A list containing Neo4j graph database connections for the two designs.
    @type graphs: list of neo4j.Graph

    @pre 'names' should be a list containing exactly two design names as strings, and 'graphs' should be a list containing
         the corresponding Neo4j graph database connections.

    @see: This function is used to identify and mark parameter value differences between two designs in Neo4j.
    """
    # need to consider both shared classifier and owner
    comparison_name = names[0]+'_vs_'+names[1]+'_SHARED_Parameter'
    query = """
            MATCH (n1:"""+names[0]+"""_Design_Instance_Element)-[r1:PARENT]-(ownern1:"""+names[0]+"""_Design_Instance_Element),(n2:"""+names[1]+"""_Design_Instance_Element)-[r2:PARENT]-(ownern2:"""+names[1]+"""_Design_Instance_Element),(classifier:Classifier),(owner_classifier:Classifier)
            WITH n1,r1,ownern1,n2,r2,ownern2
            WHERE (n1)-[:CLASSIFIER]->(classifier) AND (n2)-[:CLASSIFIER]->(classifier) AND (ownern1)-[:CLASSIFIER]->(owner_classifier) AND (ownern2)-[:CLASSIFIER]->(owner_classifier) AND n1:Parameter AND n2:Parameter
            SET n1:"""+comparison_name+""", n2:"""+comparison_name+"""
            """
    database_tools.run_neo_query(['nil'],query,graphs)

def identify_child_classifier(value1,des1_element,name,graph):
    """
    Identify the classifier of a child element in a specific design.

    This function takes the unique identifier 'value1' of a child element, the parent element 'des1_element', and the design name 'name'.
    It matches the child element in the specified design and returns its classifier.

    @param value1: The unique identifier of the child element.
    @type value1: str

    @param des1_element: The parent element in the design hierarchy.
    @type des1_element: list of neo4j.Node

    @param name: The name of the design in which to search for the child element.
    @type name: str

    @param graph: The Neo4j graph database connection for the specified design.
    @type graph: neo4j.Graph

    @return: The classifier of the identified child element.
    @rtype: list of dict

    @pre 'value1' should be a valid unique identifier, 'des1_element' should be a list of Neo4j nodes representing the parent element,
         'name' should be a valid design name, and 'graph' should be a Neo4j graph database connection.

    @see: This function is used to identify the classifier of a child element in a specific design.
    """
    query = """
            MATCH (n1:"""+name+"""_Design_Instance_Element {uid:'"""+value1+"""'})-[r1:PARENT]->(ownern1:"""+name+"""_Design_Instance_Element {uid:'"""+des1_element[0]['n']['uid']+"""'})
            RETURN n1.Classifier
            """
    return database_tools.run_neo_query(['nil'],query,graph)

def identify_target_classifier(des_element,target_uid,relationship_type,name,graph):
    """
    Identify the classifier of a target element related to a specified design element.

    This function takes a design element 'des_element' (parent), a target element unique identifier 'target_uid', a relationship type 'relationship_type',
    the design name 'name', and the Neo4j graph database connection 'graph'. It matches the target element related to the specified design element
    using the given relationship type and returns its classifier.

    @param des_element: The design element (parent) in the relationship.
    @type des_element: list of neo4j.Node

    @param target_uid: The unique identifier of the target element.
    @type target_uid: str

    @param relationship_type: The type of relationship connecting the design element and the target element.
    @type relationship_type: str

    @param name: The name of the design in which to search for the target element.
    @type name: str

    @param graph: The Neo4j graph database connection for the specified design.
    @type graph: neo4j.Graph

    @return: The classifier of the identified target element.
    @rtype: list of dict

    @pre 'des_element' should be a list of Neo4j nodes representing the design element (parent), 'target_uid' should be a valid unique identifier,
         'relationship_type' should be a valid relationship type, 'name' should be a valid design name, and 'graph' should be a Neo4j graph database connection.

    @see: This function is used to identify the classifier of a target element related to a specified design element in Neo4j.
    """
    query = """
            MATCH (n1:"""+name+"""_Design_Instance_Element {uid:'"""+des_element[0]['n']['uid']+"""'})-[r1:"""+relationship_type+"""]-(target:"""+name+"""_Design_Instance_Element {uid:'"""+target_uid+"""'})
            RETURN target.Classifier
            """
    return database_tools.run_neo_query(['nil'],query,graph)

def identify_element_children(des_element,name,graph):
    """
    Identify the children of a specified design element.

    This function takes a design element 'des_element', the design name 'name', and the Neo4j graph database connection 'graph'.
    It matches the children of the specified design element and returns their unique identifiers.

    @param des_element: The design element for which to identify children.
    @type des_element: list of neo4j.Node

    @param name: The name of the design in which to search for children.
    @type name: str

    @param graph: The Neo4j graph database connection for the specified design.
    @type graph: neo4j.Graph

    @return: A list of unique identifiers for the identified children.
    @rtype: list of dict

    @pre 'des_element' should be a list of Neo4j nodes representing the design element, 'name' should be a valid design name,
         and 'graph' should be a Neo4j graph database connection.

    @see: This function is used to identify the children of a specified design element in Neo4j.
    """
    query = """
            MATCH (n1:"""+name+"""_Design_Instance_Element {uid:'"""+des_element[0]['n']['uid']+"""'})<-[r1:PARENT]-(child:"""+name+"""_Design_Instance_Element)
            RETURN child.uid
            """
    return database_tools.run_neo_query(['nil'],query,graph)

def numerical_value_comparison(comparisons,key,des_elements,des_names):
    """
    Compare numerical property values of design elements.

    This function compares numerical property values of design elements across different designs.
    It takes a list of comparison records 'comparisons', a 'key' object specifying the property to compare,
    a list of design elements 'des_elements', and a list of design names 'des_names'.

    @param comparisons: The list of comparison records to which differences will be appended.
    @type comparisons: list of comparison_record

    @param key: The key object specifying the property to compare.
    @type key: object_location_pair

    @param des_elements: A list of design elements from different designs to compare.
    @type des_elements: list of list of neo4j.Node

    @param des_names: A list of design names corresponding to the design elements.
    @type des_names: list of str

    @return: The updated list of comparison records with differences appended.
    @rtype: list of comparison_record

    @pre 'comparisons' should be a list of comparison_record objects, 'key' should specify a valid property to compare,
         'des_elements' should be a list of lists of Neo4j nodes representing design elements, and 'des_names' should be a list
         of valid design names corresponding to the design elements.

    @see: This function is used to compare numerical property values of design elements across different designs.
    """
    # compare node property numerical values
    #print('comparing numerical values')
    difference_list = []
    design_index = 1
    while design_index < len(des_elements):
        current_element = des_elements[design_index]
        current_des_name = des_names[design_index]
        value_difference = current_element[0]['n'][key.element]- des_elements[0][0]['n'][key.element]
        if value_difference != 0:
            comparisons[-1].discovered_differences.append(difference_record(des_names[0],des_elements[0][0]['n']['uid'],current_des_name,current_element,key.element,value_difference))
        design_index += 1
        return comparisons

def value_set_comparison(comparisons,value,key,des_elements,des_names):
    """
    Compare sets of values for a specific property of design elements.

    This function compares sets of values for a specific property of design elements across different designs.
    It takes a list of comparison records 'comparisons', a 'value' to compare, a 'key' object specifying the property to compare,
    a list of design elements 'des_elements', and a list of design names 'des_names'.

    @param comparisons: The list of comparison records to which differences will be appended.
    @type comparisons: list of comparison_record

    @param value: The value to compare within the property set.
    @type value: str

    @param key: The key object specifying the property to compare.
    @type key: object_location_pair

    @param des_elements: A list of design elements from different designs to compare.
    @type des_elements: list of list of neo4j.Node

    @param des_names: A list of design names corresponding to the design elements.
    @type des_names: list of str

    @return: The updated list of comparison records with differences appended.
    @rtype: list of comparison_record

    @pre 'comparisons' should be a list of comparison_record objects, 'value' should be a valid value to compare,
         'key' should specify a valid property to compare, 'des_elements' should be a list of lists of Neo4j nodes representing
         design elements, and 'des_names' should be a list of valid design names corresponding to the design elements.

    @see: This function is used to compare sets of values for a specific property of design elements across different designs.
    """
    # compare node value set by split key entry by each semi-colon
    #print('comparing value sets')
    #print(f'value is {value}')
    
    design_index = 1
    while design_index < len(des_elements):
        # select different design to compare against
        current_element = des_elements[design_index]
        current_des_name = des_names[design_index]
        value_B_list = []
        for value in current_element[0]['n'][key.element].split(';'):
            value_B_list.append(value)
        if value not in value_B_list:
            #print(f'dissimilar value:{value}')
            comparisons[-1].discovered_differences.append(difference_record(des_names[0],des_elements[0][0]['n']['uid'],current_des_name,current_element,key.element,value))
        design_index += 1
    return comparisons

def single_value_comparison(comparisons,value,key,des_elements,des_names):
    """
    Compare a single value for a specific property of design elements.

    This function compares a single value for a specific property of design elements across different designs.
    It takes a list of comparison records 'comparisons', a 'value' to compare, a 'key' object specifying the property to compare,
    a list of design elements 'des_elements', and a list of design names 'des_names'.

    @param comparisons: The list of comparison records to which differences will be appended.
    @type comparisons: list of comparison_record

    @param value: The value to compare within the property.
    @type value: str

    @param key: The key object specifying the property to compare.
    @type key: object_location_pair

    @param des_elements: A list of design elements from different designs to compare.
    @type des_elements: list of list of neo4j.Node

    @param des_names: A list of design names corresponding to the design elements.
    @type des_names: list of str

    @return: The updated list of comparison records with differences appended.
    @rtype: list of comparison_record

    @pre 'comparisons' should be a list of comparison_record objects, 'value' should be a valid value to compare,
         'key' should specify a valid property to compare, 'des_elements' should be a list of lists of Neo4j nodes representing
         design elements, and 'des_names' should be a list of valid design names corresponding to the design elements.

    @see: This function is used to compare a single value for a specific property of design elements across different designs.
    """
    # compare node property value
    #print('comparing single values')
    #print(f'value is {value}')
    design_index = 1
    while design_index < len(des_elements):
        # select different design to compare against
        current_element = des_elements[design_index]
        current_des_name = des_names[design_index]
        value_B = current_element[0]['n'][key.element]
        if value != value_B:
            comparisons[-1].discovered_differences.append(difference_record(des_names[0],des_elements[0][0]['n']['uid'],current_des_name,current_element,key.element,value))
        design_index += 1
    return comparisons

def property_comparison(comparisons,key):
    """
    Compare a property across different design elements and designs.

    This function compares a property across different design elements and designs.
    It constructs a comparison object and then iterates over each design element, changing the base design being compared to.

    @param comparisons: The list of comparison records to which differences will be appended.
    @type comparisons: list of comparison_record

    @param key: The key object specifying the property to compare.
    @type key: object_location_pair

    @return: The updated list of comparison records with differences appended.
    @rtype: list of comparison_record

    @pre 'comparisons' should be a list of comparison_record objects, and 'key' should specify a valid property to compare.

    @see: This function is used to compare a property across different design elements and designs.
    """
    # constructing comparison object
    des_names = []
    des_elements = []
    for element in key.location:
        des_names.append(element.location)
        des_elements.append(element.element)
    comparisons.append(comparison_record(des_names,des_elements,key.element))

    # need to loop over each design element to change the base design being compared to
    # this is achieved by moving the base design element to the start of the list
    # and allowing the comparison functions to compare to this
    design_element_index = 0
    while design_element_index < len(des_elements) :
        # do the re order
        des_elements.insert(0,des_elements.pop(design_element_index))
        des_names.insert(0,des_names.pop(design_element_index))
        # now looping through each value for this key
        # handling case where values are a int's
        if str(des_elements[0][0]['n'][key.element]).isdigit():
            comparisons = numerical_value_comparison(comparisons,key,des_elements,des_names)
        elif ';' in str(des_elements[0][0]['n'][key]):
            for value in str(des_elements[0][0]['n'][key.element]).split(';'):
                comparisons = value_set_comparison(comparisons,value,key,des_elements,des_names)
        else:
            value = des_elements[0][0]['n'][key.element]
            comparisons = single_value_comparison(comparisons,value,key,des_elements,des_names)
        design_element_index += 1
    return comparisons
    

def relationship_comparison(comparisons,des_elements,graph):
    """
    Compare relationships between different design elements and designs.

    This function compares relationships between different design elements and designs.
    It finds each element's relationship types, switches the base design for comparison,
    and then compares the relationships and classifiers between designs.

    @param comparisons: The list of comparison records to which differences will be appended.
    @type comparisons: list of comparison_record

    @param des_elements: A list of object_location_pair objects representing design elements to compare.
    @type des_elements: list of object_location_pair

    @param graph: The Neo4j graph database connection.
    @type graph: neo4j.Graph

    @return: The updated list of comparison records with differences appended.
    @rtype: list of comparison_record

    @pre 'comparisons' should be a list of comparison_record objects, 'des_elements' should be a list of object_location_pair objects,
    and 'graph' should be a valid Neo4j graph database connection.

    @see: This function is used to compare relationships between different design elements and designs.
    """
    # find each element's relationship types
    relationship_types =[]
    for design in des_elements:
        query = """
            MATCH (n:"""+design.location+"""_Design_Instance_Element{uid:'"""+design.element[0]['n']['uid']+"""'})-[r]-(n2:"""+design.location+"""_Design_Instance_Element) 
            RETURN DISTINCT type(r);
            """
    
        relationship_types.append(database_tools.run_neo_query(['nil'],query,graph))
    # set of relationship types to ignore in comparison
    ignore_relationship_type_list = ['HARD_DEPENDENCY']
    
    # loop for switching base design
    design_element_index = 0
    while design_element_index < len(des_elements) :
        # selecting new design to compare as basis
        des_elements.insert(0,des_elements.pop(design_element_index))
        relationship_types.insert(0,relationship_types.pop(design_element_index))

        relationship_types_A = relationship_types[0]
        des_A_element = des_elements[0].element
        name_A = des_elements[0].location
        # now loop through each of these relationship types and find associated nodes to compare
        # for each relationship node one has, find an a equivalent (according to target classifier) with node 2, if none than record difference
        for relationship_type in relationship_types_A:
            #print(f'relationship type: {relationship_type}')
            #print(f'ignore list: {ignore_relationship_type_list}')
            if relationship_type['type(r)'] not in ignore_relationship_type_list:
                #print('not ignored')
                # find related nodes with this type of relationship to compare to later
                query = """
                        MATCH (n:"""+name_A+"""_Design_Instance_Element{uid:'"""+des_A_element[0]['n']['uid']+"""'})-[r:"""+relationship_type['type(r)']+"""]-(n2:"""+name_A+"""_Design_Instance_Element) 
                        RETURN n2;
                        """
                
                targets_A = database_tools.run_neo_query(['nil'],query,graph)
                # find target classifiers
                target_A_classifiers = []
                for target in targets_A:
                    #print(f'target is: {target}')
                    classifier_data = identify_target_classifier(des_A_element,target['n2']['uid'],relationship_type['type(r)'],name_A,graph)
                    target_A_classifiers.append([target['n2']['name'],classifier_data[0]['target.Classifier']]) # row containing the target name and its classifier

                # now finding the set of connected nodes and their classifiers in each other design
                comparison_design_index = 1
                while comparison_design_index < len(des_elements):
                    name_B = des_elements[comparison_design_index].location
                    des_B_element = des_elements[comparison_design_index].element
                    query = """ 
                            MATCH (n:"""+name_B+"""_Design_Instance_Element{uid:'"""+des_B_element[0]['n']['uid']+"""'})-[r:"""+relationship_type['type(r)']+"""]-(n2:"""+name_B+"""_Design_Instance_Element) 
                            RETURN n2;
                            """
                    
                    targets_B = database_tools.run_neo_query(['nil'],query,graph)
                    # find target classifiers
                    target_B_classifiers = []
                    for target in targets_B:
                        #print(f'target is: {target}')
                        target_B_classifiers.append(identify_target_classifier(des_B_element,target['n2']['uid'],relationship_type['type(r)'],name_B,graph))

                    target_B_classifiers_list = []
                    for entry in target_B_classifiers:
                        target_B_classifiers_list.append(entry[0]['target.Classifier'])

                    # now have a set of the two target classifiers, compare for differences 
                    # constructing comparison object
                    des_names = []
                    des_elements_extracted = []
                    for element in des_elements:
                        des_names.append(element.location)
                        des_elements_extracted.append(element.element)
                    des_names,des_elements_extracted,relationship_type['type(r)']
                    comparisons.append(comparison_record(des_names,des_elements_extracted,relationship_type['type(r)']))
                    for classifier_row in target_A_classifiers:
                        classifier = classifier_row[1]
                        target = classifier_row[0]
                        if classifier  not in target_B_classifiers_list:
                            comparisons[-1].discovered_differences.append(difference_record(name_A,des_A_element[0]['n']['uid'],name_B,des_B_element,relationship_type['type(r)'],{'target':target,'target_classifier':classifier}))
                    comparison_design_index += 1
        design_element_index += 1
    return  comparisons

def compare_nodes(comparisons,des_elements,names,graph):
    """
    Compare properties and relationships between nodes in different designs.

    This function compares properties and relationships between nodes in different designs.
    It collects differences between the nodes and records them as "difference" nodes in the comparisons list.

    @param comparisons: The list of comparison records to which differences will be appended.
    @type comparisons: list of comparison_record

    @param des_elements: A list of object_location_pair objects representing design elements to compare.
    @type des_elements: list of object_location_pair

    @param names: A list of design names corresponding to des_elements.
    @type names: list of str

    @param graph: The Neo4j graph database connection.
    @type graph: neo4j.Graph

    @return: The updated list of comparison records with differences appended.
    @rtype: list of comparison_record

    @pre 'comparisons' should be a list of comparison_record objects, 'des_elements' should be a list of object_location_pair objects,
    'names' should be a list of corresponding design names, and 'graph' should be a valid Neo4j graph database connection.

    @see: This function is used to compare properties and relationships between nodes in different designs.
    """
    # collect differences between the nodes and record as "difference" nodes
    # property differences
    key_list = []
    pure_key_list = []
    for design_element in des_elements:
        for key in design_element.element[0]['n'].keys():
            # ignoring uid and name keys
            if key != 'uid' and key != 'name':
                # if new key add entry else add design to existing entry
                if pure_key_list.count(key) == 0:
                    key_list.append(object_location_pair(key,[design_element]))
                    pure_key_list.append(key)
                else:
                    key_list[pure_key_list.index(key)].location.append(design_element)

    # now looping over list of keys to find common ones
    for key in key_list:
        # ignoring singleton keys
        if len(key.location) > 1:
            #print(f'comparing node key: {key.element}')
            comparisons = property_comparison(comparisons,key)

    
    # relationship differences
    comparisons = relationship_comparison(comparisons,des_elements,graph)
    return comparisons

def traverse_tree(brief_name,comparisons,des_elements,names,graphs):
    """
    Recursively traverse a tree structure of nodes to compare them.

    This function recursively traverses a tree structure of nodes to compare them.
    It compares nodes at each level, starting with the root nodes, and continues down to the leaf nodes.

    @param brief_name: A brief name or identifier for the comparison group.
    @type brief_name: str

    @param comparisons: The list of comparison records to which differences will be appended.
    @type comparisons: list of comparison_record

    @param des_elements: A list of object_location_pair objects representing design elements to compare at the current level.
    @type des_elements: list of object_location_pair

    @param names: A list of design names corresponding to des_elements.
    @type names: list of str

    @param graphs: A list of Neo4j graph database connections corresponding to each design.
    @type graphs: list of neo4j.Graph

    @return: The updated list of comparison records with differences appended.
    @rtype: list of comparison_record

    @pre 'brief_name' should be a valid identifier, 'comparisons' should be a list of comparison_record objects,
    'des_elements' should be a list of object_location_pair objects, 'names' should be a list of corresponding design names,
    and 'graphs' should be a list of valid Neo4j graph database connections.

    @see: This function is used to recursively traverse a tree structure of nodes and compare them at each level.
    """
    # compared the nodes
    comparisons = compare_nodes(comparisons,des_elements,names,graphs)

    # decide on next node group
    # these groups should be of same classifier
    # need to consider the children of non similar nodes however, this will be done later
    # first generate group of nodes to be compared with shared classifiers
    similar_node_groups = []
    child_list = []
    classifier_list = []
    # first collect all children and their corresponding classifiers
    for design_element in des_elements:
        for child in identify_element_children(design_element.element,design_element.location,graphs):
            child_list.append(object_location_pair(child,design_element.location))
            classifier_list.append(object_location_pair(identify_child_classifier(child['child.uid'],design_element.element,design_element.location,graphs),design_element.location))

    # now looping over these lists to identify the common children, using an index
    index = 0
    while index < len(child_list):
        classifier = classifier_list[index]
        # finding all occurances of this classifier
        i = 0
        current_group = [child_list[index]]
        while i < len(child_list):
            # match classifiers from different designs
            if classifier.element == classifier_list[i].element and classifier.location != classifier_list[i].location:
                current_group.append(child_list[i])
                # now removing matched children to avoid duplicate groupings
                classifier_list.pop(i)
                child_list.pop(i)   
            i += 1

        # ignore instances of singleton children
        if len(current_group)>1:
            # now constructing the group and adding it to the list of common children 
            #print(f'current group: {current_group}')      
            similar_node_groups.append(current_group)
        index += 1

    # now loop over pairs of nodes to be compared
    for group in similar_node_groups:
        new_des_elements = []
        for element in group:
            query = """
                MATCH (n {uid:'"""+element.element['child.uid']+"""'})
                SET n:"""+brief_name+"""_compared_Element
                RETURN n
            """
            new_des_elements.append(object_location_pair(database_tools.run_neo_query(['nil'],query,graphs),element.location))

        # jump down to next level
        #print(f"next des elements are :{new_des_elements}")
        
        comparisons = traverse_tree(brief_name,comparisons,new_des_elements,names,graphs)
    return comparisons
                    
def diff_algorithm(brief_name,names,repeated_differences,graphs):
    """
    Perform a differential comparison of designs represented in Neo4j graphs.

    This function performs a differential comparison of designs represented in Neo4j graphs.
    It compares nodes at each level of the design hierarchy, identifying differences and storing them as 'Comparison'
    and 'Difference' nodes in the database.

    @param brief_name: A brief name or identifier for the comparison group.
    @type brief_name: str

    @param names: A list of design names corresponding to Neo4j graphs.
    @type names: list of str

    @param graphs: A list of Neo4j graph database connections corresponding to each design.
    @type graphs: list of neo4j.Graph

    @return: None

    @pre 'brief_name' should be a valid identifier, 'names' should be a list of design names,
    and 'graphs' should be a list of valid Neo4j graph database connections.

    @see: This function performs a differential comparison of designs represented in Neo4j graphs
    and stores the results in the database.
    """
    # start at root node (spacecraft) and compare differences at each node recursively
    des_elements = []
    
    for name in names:
        query = """
            MATCH (n:Spacecraft)
            WHERE (n:"""+name+"""_Design_Instance_Element)
            SET n:"""+brief_name+"""_Compared_Element
            RETURN n
        """
        des_elements.append(object_location_pair(database_tools.run_neo_query(['nil'],query,graphs),name))# object_location_pair with design element and design name it belongs to

    comparisons = []
    #print('traversing tree and performing comparisons')
    # count number of design elements (for progress bar)
    query = """
        MATCH (n:Design_Element)
        RETURN count(n) as count
    """
    
    n = database_tools.run_neo_query(['nil'],query,graphs)[0]['count']

    comparisons = traverse_tree(brief_name,comparisons,des_elements,names,graphs)

    # post process the differences dict
    #remove empty comparisons entries
    comparisons_reduced = []
    #print('reducing comparisons')
    for comparison in comparisons:
        if comparison.discovered_differences:
            comparisons_reduced.append(comparison)
    #print(comparisons_reduced[0])
 
    # now loading these differences into database as 'comparison' and 'difference' nodes
    #print('loading comparisons into database')
    for comparison in comparisons_reduced:
        # creating node with selected name
        query = """
             MERGE (comparison:Comparison {uid: '"""+ comparison.name.replace("'",'')  +"""'})
                SET 
                    comparison: """+ comparison.key +""",
                    comparison: Comparison_"""+ comparison.key +""",
                    comparison: """+ brief_name +"""_Comparison,
                    comparison.Locations = '"""+ str(comparison.design_elements).replace("[",'').replace("]",'').replace("'",'') +"""'
        """
        database_tools.run_neo_query(['nil'],query,graphs)
        # add relationships to locations in the compared designs
        for location in comparison.design_elements:
            query = """
                MATCH 
                    (comparison:Comparison {uid: '"""+ comparison.name.replace("'",'')  +"""'}),
                    (location {uid:'"""+location+"""'})
                MERGE (comparison)-[:COMPARISON_LOCATION_IN_DESIGN]->(location)
            """
            database_tools.run_neo_query(['nil'],query,graphs)
            #print(location)
        for difference in comparison.discovered_differences:
            #print(f'comparison name: {comparison.name}')
            #print(f'current difference: {difference.difference_specifics}')
            query = """
                MATCH (comparison:Comparison {uid: '"""+ comparison.name.replace("'",'')  +"""'})
                MERGE (difference:Difference {uid: '"""+ difference.design_A_name+','+difference.design_A_element+','+difference.design_B_name+','+difference.design_B_element+','+str(difference.difference_specifics) +','+difference.key+"""'})-[:DISCOVERED_BY]->(comparison)
                SET 
                    difference: """+ difference.key +""",
                    difference: Difference_"""+ difference.key +""",
                    difference: """+ brief_name +"""_Difference,
                    difference.Different_Detail = '"""+ str(difference.difference_specifics) +"""',
                    difference.Base_Design = '"""+ difference.design_A_name +"""'
            """
            try:
                database_tools.run_neo_query(['nil'],query,graphs)
            except:
                repeated_differences.append(difference)
            # add relationships to difference location in the compared designs
            query = """
                MATCH 
                    (difference:Difference {uid: '"""+ difference.design_A_name+','+difference.design_A_element+','+difference.design_B_name+','+difference.design_B_element+','+str(difference.difference_specifics) +','+difference.key+"""'}),
                    (location {uid:'"""+difference.design_A_element+"""'})
                MERGE (difference)-[:DIFFERENCE_LOCATION_IN_DESIGN]->(location)
            """
            database_tools.run_neo_query(['nil'],query,graphs)
    
    # linking comparisons by equivalent locations in design ownership trees
    #print('link to relevant sections of designs')
    query = """
            MATCH (comparison:Comparison)
            RETURN comparison
              
        """
    responses = database_tools.run_neo_query(['nil'],query,graphs)
    for response in responses:
        uid = response['comparison']['uid']
        locations = response['comparison']['Locations'].replace(" ",'').split(',')
        designs = response['comparison']['uid'].split('->')[0].replace("[",'').replace("]",'').split(',')
        owners =[]
        location_index = 0
        while location_index < len(locations):
            # find the owner of each local in the comparison
            query = """
                    MATCH (location:"""+designs[location_index].replace('-','')+"""_Design_Instance_Element {uid:'"""+locations[location_index]+"""'})-[:PARENT]->(owner)
                    RETURN owner.uid
                """
            #print(query)
            owners.append(database_tools.run_neo_query(['nil'],query,graphs))
            location_index += 1
        # now found owners, search for any comparisons that include that owner in their locations tag
        query = """
            MATCH (comparison:Comparison)
            RETURN comparison
              
        """
        all_comparisons = database_tools.run_neo_query(['nil'],query,graphs)
        for owner in owners:
            for comparison in all_comparisons:
                if owner:# allow for case where looking for owner of root element, where there are no owners
                    # condition is where the owner appears in the list of locations exactly (not just overlap with another element's name)
                    locations_tag = comparison['comparison']['Locations'].replace(' ','') # remove any spaces for clarity
                    locations_list = locations_tag.split(',')
                    #print(locations_list)
                    #print(owner[0]['owner.uid'])
                    if owner[0]['owner.uid'] in locations_list:
                        query = """
                                MATCH(owner_comparison:Comparison {uid:'"""+comparison['comparison']['uid']+"""'}),(comparison:Comparison {uid:'"""+uid+"""'})
                                MERGE (owner_comparison)<-[:PARENT_COMPARISON]-(comparison) 
                                
                            """
                        database_tools.run_neo_query(['nil'],query,graphs)

def generate_comparison_stats(brief_name,graph):
    """
    Generate statistics and plots for a comparison group in the Neo4j database.

    This function generates statistics and various plots for a specified comparison group
    stored in the Neo4j database. It retrieves the counts of 'Difference' and 'Comparison' nodes
    for the given comparison group, as well as additional data for plotting.

    @param brief_name: A brief name or identifier for the comparison group.
    @type brief_name: str

    @param graph: A Neo4j graph database connection.
    @type graph: neo4j.Graph

    @return: None

    @pre 'brief_name' should be a valid identifier, and 'graph' should be a valid Neo4j graph database connection.

    @see: This function generates statistics and plots for a specified comparison group in the Neo4j database.
    """
    query = """
                MATCH (n:"""+ brief_name +"""_Difference) RETURN count(*)
            """
    #print(query)
    reponse = database_tools.run_neo_query(['nil'],query,graph)
    number_differences =  reponse[0]['count(*)']
    #print(number_differences)
    query = """
                MATCH (n:"""+ brief_name +"""_Comparison) RETURN count(*)
            """
    #print(query)
    reponse = database_tools.run_neo_query(['nil'],query,graph)
    number_comparisons = reponse[0]['count(*)']
    #print(number_comparisons)

    comparisons_data = graph_plotting.comparison_diff_count_sankey_diagrams(brief_name,graph)

    comparisons_data = graph_plotting.comparison_diff_count_icile_plots(comparisons_data)

    comparisons_data = graph_plotting.comparison_diff_count_pie_charts(comparisons_data)

def population_wide_diff_algorithm(missions_list,graph):
    """
    Perform a population-wide difference analysis for a list of missions.

    This function iterates through a list of missions and their associated designs
    and performs a difference analysis for each mission using the 'diff_algorithm' function.
    It aims to analyze differences across the entire population of missions.

    @param missions_list: A dictionary containing mission names as keys and lists of designs as values.
    @type missions_list: dict

    @param graph: A Neo4j graph database connection.
    @type graph: neo4j.Graph

    @return: None

    @pre 'missions_list' should be a valid dictionary with mission names and associated design lists,
         and 'graph' should be a valid Neo4j graph database connection.

    @see: The 'diff_algorithm' function is used to perform difference analysis for individual missions.
    """
    repeated_differences = []
    process_index = 0
    process_count = len(missions_list.keys())
    with tqdm(total=process_count, colour = 'green') as pbar1:
        for mission, designs in missions_list.items():
            diff_algorithm(mission,missions_list[mission],repeated_differences,graph)
            process_index += 1
            pbar1.n = process_index
            pbar1.refresh()
    #print(repeated_differences)

def population_wide_generate_comparison_stats(missions_list,graph):
    """
    Generate comparison statistics for a population of missions.

    This function iterates through a list of missions and generates comparison statistics for each mission
    using the 'generate_comparison_stats' function. It aims to generate statistics for the entire population
    of missions.

    @param missions_list: A dictionary containing mission names as keys and lists of designs as values.
    @type missions_list: dict

    @param graph: A Neo4j graph database connection.
    @type graph: neo4j.Graph

    @return: None

    @pre 'missions_list' should be a valid dictionary with mission names and associated design lists,
         and 'graph' should be a valid Neo4j graph database connection.

    @see: The 'generate_comparison_stats' function is used to generate comparison statistics for individual missions.
    """
    for mission, designs in missions_list.items():
        generate_comparison_stats(mission,graph)    