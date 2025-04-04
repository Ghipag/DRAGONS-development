def lists_overlap(a, b):
    set1 = set(a)

    set2 = set(b)

    intersected_set = set1.intersection(set2)

    intersected_list = list(intersected_set)

    return intersected_list

#{'label':'Comparison','check_classifier':False}
# DO NOT INCLUDE Design_Element_FDomain or
explored_types = ['Comparison',
                    'Difference',
                    'Difference_Value',
                    'Difference_PARENT',
                    'Difference_DATA_INTERFACE',
                    'Difference_FLUID_INTERFACE',
                    'Difference_MECHANICAL_INTERFACE',
                    'Difference_Multiplicity',
                    'Difference_POWER_INTERFACE',
                    'Comparison_DATA_INTERFACE',
                    'Comparison_FLUID_INTERFACE',
                    'Comparison_MECHANICAL_INTERFACE',
                    'Comparison_Multiplicity',
                    'Comparison_PARENT',
                    'Comparison_POWER_INTERFACE',
                    'Comparison_THERMAL_INTERFACE',
                    'Comparison_Value',
                    'Requirement',
                    'AOCS_Domain',
                    'AOP_Domain',
                    'Along_Track_Distance_Domain',
                    'Altitude_Domain',
                    'Angular_Error_Domain',
                    'Antenna_Domain',
                    'Apogee_Radius_Domain',
                    'Availability_Domain',
                    'Comms_Domain',
                    'Communications_Domain',
                    'Data_Bus_Domain',
                    'Data_Transfer_Rate_Domain',
                    'Decommissioning_Domain',
                    'Eccentricity_Domain',
                    'End_Of_Life_Domain',
                    'Formation_Distance_Accuracy_Domain',
                    'Formation_Domain',
                    'Function_Domain',
                    'GNSS_Receiver_Domain',
                    'Geo_Location_accuracy_Domain',
                    'Ground_Resolution_Domain',
                    'Ground_Segment_Domain',
                    'Ground_Station_Domain',
                    'Heat_Pipe_Domain',
                    'Imaging_Domain',
                    'Inclination_Domain',
                    'LEOP_Domain',
                    'LTDN_Domain',
                    'Latency_Domain',
                    'Launcher_Domain',
                    'Lifetime_Domain',
                    'Manoeuvre_Domain',
                    'Nominal_Domain',
                    'Number_of_Launchers_Domain',
                    'OBDH_Domain',
                    'Observation_Local_Time_Domain',
                    'Observation_Zentih_Angle_Domain',
                    'Onboard_Computer_Domain',
                    'Operational_Domain',
                    'Orbital_Domain',
                    'Payload_Actuator_Domain',
                    'Payload_Domain',
                    'Payload_Unit_Domain',
                    'Perigee_Radius_Domain',
                    'Period_Domain',
                    'Pointing_Accuracy_Domain',
                    'Pointing_Domain',
                    'Pointing_Knowledge_Domain',
                    'Position_Latitude_Domain',
                    'Power_Domain',
                    'Power_Subsystem_Domain',
                    'Propulsion_Domain',
                    'Propulsion_Subsystem_Domain',
                    'RAAN_Domain',
                    'Reciever_Domain',
                    'Revisit_Domain',
                    'SMA_Domain',
                    'Safe_Domain',
                    'Separation_Time_Domain',
                    'Solid_State_Recorder_Domain',
                    'Spacecraft_Domain',
                    'Standby_Domain',
                    'System_Components_Domain',
                    'System_Domain',
                    'Temperature_Estimation_Accuracy_Domain',
                    'Thermal_Domain',
                    'Thermal_Subsystem_Domain',
                    'Three_Axis_stab_status_Domain',
                    'Transmitter_Domain',
                    'True_Anomaly_Domain',
                    'Variation_of_Local_Time_of_Observation_Domain'
                    'Design_Element',
                    'Function',
                    'AOCS_FDomain',
                    'AOP_FDomain',
                    'Ammonia',
                    'Angular_Error_FDomain',
                    'Antenna_FDomain',
                    'Apogee_Radius_FDomain',
                    'CAN',
                    'Cartidge',
                    'Cartridge',
                    'Coarse',
                    'Comms_FDomain',
                    'Communications_FDomain',
                    'Control',
                    'Control_Moment_Gyro'
                    'Daylight',
                    'Decommissioning_FDomain',
                    'Deployable',
                    'Drain',
                    'Dry',
                    'Eccentricity_FDomain',
                    'Eclipse',
                    'End_Of_Life_FDomain',
                    'Fill_and_Drain',
                    'Fill_and_Drain__1',
                    'Fine',
                    'Formation_Distance_Accuracy_FDomain',
                    'Formation_FDomain',
                    'Fuel',
                    'Fuel_Tank_FillDrain',
                    'Function_FDomain',
                    'GNSS_Receiver_FDomain',
                    'Geo_Location_accuracy_FDomain',
                    'Ground_Segment_FDomain',
                    'Ground_Station_FDomain',
                    'Helix',
                    'High_Gain',
                    'High_Gain_TX',
                    'High_Gian',
                    'Horn',
                    'Hydrazine',
                    'Hydrazine_s',
                    'ION',
                    'Inclination_FDomain',
                    'K_Band',
                    'Ka_Band',
                    'LEOP_FDomain',
                    'Latch',
                    'Lion',
                    'Low_Gain',
                    'Low_Gain_TX',
                    'Low_Noise',
                    'MIL_STD_1553',
                    'Manoeuvre_FDomain',
                    'Mode_FDomain',
                    'Nitrogen',
                    'OBDH_FDomain',
                    'Observation_Local_Time_FDomain',
                    'Observation_Zentih_Angle_FDomain',
                    'Onboard_Computer_FDomain',
                    'Operational_FDomain',
                    'Orbital_FDomain',
                    'Parabolic',
                    'Patch',
                    'Patch_FDomain',
                    'Payload_FDomain',
                    'Payload_Unit_FDomain',
                    'Payload_Diplexer',
                    'Payload_Antenna',
                    'Payload_Reflector',
                    'Perigee_Radius_FDomain',
                    'Pointing_Accuracy_FDomain',
                    'Pointing_FDomain',
                    'Position_Latitude_FDomain',
                    'Power_FDomain',
                    'Power_Subsystem_FDomain',
                    'Pressurant',
                    'Pressurant_FillDrain',
                    'Pressurant_Isolation',
                    'Pressurant_Tank_FillDrain',
                    'Propellant',
                    'Propellant_FillDrain',
                    'Propellant_Tank_Latch',
                    'Propulsion_FDomain',
                    'Propulsion_Subsystem_FDomain',
                    'Reciever_FDomain',
                    'Revisit_FDomain',
                    'SAR',
                    'SMA_FDomain',
                    'S_Band',
                    'S_Band_FDomain',
                    'Safe_FDomain',
                    'Separation_Time_FDomain',
                    'SpaceWire',
                    'Subsystem_FDomain',
                    'System_Components_FDomain',
                    'Temperature_Estimation_Accuracy_FDomain',
                    'Thermal_FDomain',
                    'Thermal_Subsystem_FDomain',
                    'Thermo_Electric',
                    'Three_Axis_stab_status_FDomain',
                    'Thruster_Isolation',
                    'Total_Dry',
                    'Total_Wet',
                    'Transmitter_FDomain',
                    'Triple_Junction',
                    'Unit_FDomain',
                    'Variation_of_Local_Time_of_Observation_FDomain',
                    'Wet',
                    'X_Band',
                    'Xenon',
                    'Parameter',
                    'Component',
                    'Mode',
                    'Condition',
                    'Spacecraft',
                    'Subsystem',
                    'Unit',
                    'Payload',
                    'AOCS',
                    'Power_Subsystem',
                    'Thermal_Subsystem',
                    'Communications',
                    'Propulsion_Subsystem',
                    'OBDH',
                    'Solar_Array',
                    'Solar_Array_Actuator',
                    'Battery',
                    'PCDU',
                    'Power_Bus',
                    'Harness',
                    'Switch_Mode_Regulator',
                    'Regulated_Peak_Power_Tracker',
                    'Reaction_Wheel',
                    'Magnetorquer',
                    'GNSS_Receiver',
                    'Earth_Sensor',
                    'Sun_Sensor',
                    'IMU',
                    'Star_Tracker',
                    'IO_remote_data_processing_and_power_distribution_board',
                    'Deployable_Boom',
                    'Thruster',
                    'Tank',
                    'Valve',
                    'Pressure_Regulator',
                    'Filter',
                    'Pressure_Transducer',
                    'Manifold_Control_System',
                    'Manifold_Heat_Sensor',
                    'Propellant_Tank_Thermal_Control',
                    'Radiator',
                    'Heater',
                    'Thermostats',
                    'Heat_Pipe',
                    'Thermal_Control_Unit',
                    'Louvre_Control_Mechanism',
                    'Multi_Layer_Insulation',
                    'Antenna',
                    'Transmitter',
                    'Transciever',
                    'Reciever',
                    'Transponder',
                    'EDRS_Terminal',
                    'Antenna_Pointing_Mechanism',
                    'Modem',
                    'Security_Module',
                    'Amplifier',
                    'RF_Distrubution_Unit',
                    'Onboard_Computer',
                    'Solid_State_Recorder',
                    'Remote_Interface_Unit',
                    'Data_Bus',
                    'Actuator_Drive_Electronics',
                    'Payload_Actuator',
                    'Payload_Electronics',
                    'Payload_Unit',
                    'Magnetometer',
                    'Ground_Station',
                    'Standby',
                    'Imaging',
                    'Comms',
                    'Manoeuvre',
                    'Safe',
                    'Nominal',
                    'LEOP',
                    'Decommissioning',
                    'Lifetime',
                    'Cost',
                    'Altitude',
                    'Perigee_Radius',
                    'Apogee_Radius',
                    'SMA',
                    'Inclination',
                    'AOP',
                    'Eccentricity',
                    'LTAN',
                    'LTDN',
                    'True_Anomaly',
                    'RAAN',
                    'Period',
                    'Revisit',
                    'Mass',
                    'Power',
                    'Data_Generation',
                    'Focal_Length',
                    'Single_Pixel_Size',
                    'Ground_Resolution',
                    'Delta_V',
                    'Volume',
                    'Thrust',
                    'Momentum',
                    'Magnetic_Dipole',
                    'Angular_Error',
                    'Pointing_Accuracy',
                    'Area',
                    'Yaw',
                    'Voltage',
                    'Capacity',
                    'Frequency',
                    'Data_Transfer_Rate',
                    'Diameter',
                    'Gain',
                    'Data_Storage',
                    'Number_of_pixels_Per_Detector_Side',
                    'Depth_of_Discharge',
                    'Position_Knowledge',
                    'Pointing_Knowledge',
                    'Temeprature_Limit',
                    'Position_Latitude',
                    'Position_Longitude',
                    'Length',
                    'Field_of_View',
                    'Rotation_Speed',
                    'Temperature_Estimation_Accuracy',
                    'Observation_Local_Time',
                    'Observation_Zentih_Angle',
                    'Variation_of_Local_Time_of_Observation',
                    'Geo_Location_accuracy',
                    'Availability',
                    'Number_of_Launchers',
                    'Three_Axis_stab_status',
                    'Along_Track_Distance',
                    'Formation_Distance_Accuracy',
                    'Separation_Time',
                    'Latency']

mapped_types = ['Classifier',
                    'Comparison',
                    'Difference',
                    'Difference_Value',
                    'Difference_PARENT',
                    'Difference_DATA_INTERFACE',
                    'Difference_FLUID_INTERFACE',
                    'Difference_MECHANICAL_INTERFACE',
                    'Difference_Multiplicity',
                    'Difference_POWER_INTERFACE',
                    'Comparison_DATA_INTERFACE',
                    'Comparison_FLUID_INTERFACE',
                    'Comparison_MECHANICAL_INTERFACE',
                    'Comparison_Multiplicity',
                    'Comparison_PARENT',
                    'Comparison_POWER_INTERFACE',
                    'Comparison_THERMAL_INTERFACE',
                    'Comparison_Value',
                    'Requirement',
                    'AOCS_Domain',
                    'AOP_Domain',
                    'Along_Track_Distance_Domain',
                    'Altitude_Domain',
                    'Angular_Error_Domain',
                    'Antenna_Domain',
                    'Apogee_Radius_Domain',
                    'Availability_Domain',
                    'Comms_Domain',
                    'Communications_Domain',
                    'Data_Bus_Domain',
                    'Data_Transfer_Rate_Domain',
                    'Decommissioning_Domain',
                    'Eccentricity_Domain',
                    'End_Of_Life_Domain',
                    'Formation_Distance_Accuracy_Domain',
                    'Formation_Domain',
                    'Function_Domain',
                    'GNSS_Receiver_Domain',
                    'Geo_Location_accuracy_Domain',
                    'Ground_Resolution_Domain',
                    'Ground_Segment_Domain',
                    'Ground_Station_Domain',
                    'Heat_Pipe_Domain',
                    'Imaging_Domain',
                    'Inclination_Domain',
                    'LEOP_Domain',
                    'LTDN_Domain',
                    'Latency_Domain',
                    'Launcher_Domain',
                    'Lifetime_Domain',
                    'Manoeuvre_Domain',
                    'Nominal_Domain',
                    'Number_of_Launchers_Domain',
                    'OBDH_Domain',
                    'Observation_Local_Time_Domain',
                    'Observation_Zentih_Angle_Domain',
                    'Onboard_Computer_Domain',
                    'Operational_Domain',
                    'Orbital_Domain',
                    'Payload_Actuator_Domain',
                    'Payload_Domain',
                    'Payload_Unit_Domain',
                    'Payload_Diplexer',
                    'Payload_Antenna',
                    'Payload_Reflector',
                    'Perigee_Radius_Domain',
                    'Period_Domain',
                    'Pointing_Accuracy_Domain',
                    'Pointing_Domain',
                    'Pointing_Knowledge_Domain',
                    'Position_Latitude_Domain',
                    'Power_Domain',
                    'Power_Subsystem_Domain',
                    'Propulsion_Domain',
                    'Propulsion_Subsystem_Domain',
                    'RAAN_Domain',
                    'Reciever_Domain',
                    'Revisit_Domain',
                    'SMA_Domain',
                    'Safe_Domain',
                    'Separation_Time_Domain',
                    'Solid_State_Recorder_Domain',
                    'Spacecraft_Domain',
                    'Standby_Domain',
                    'System_Components_Domain',
                    'System_Domain',
                    'Temperature_Estimation_Accuracy_Domain',
                    'Thermal_Domain',
                    'Thermal_Subsystem_Domain',
                    'Three_Axis_stab_status_Domain',
                    'Transmitter_Domain',
                    'True_Anomaly_Domain',
                    'Variation_of_Local_Time_of_Observation_Domain'
                    'Design_Element',
                    'Function',
                    'AOCS_FDomain',
                    'AOP_FDomain',
                    'Ammonia',
                    'Angular_Error_FDomain',
                    'Antenna_FDomain',
                    'Apogee_Radius_FDomain',
                    'CAN',
                    'Cartidge',
                    'Cartridge',
                    'Coarse',
                    'Comms_FDomain',
                    'Communications_FDomain',
                    'Control',
                    'Control_Moment_Gyro'
                    'Daylight',
                    'Decommissioning_FDomain',
                    'Deployable',
                    'Drain',
                    'Dry',
                    'Eccentricity_FDomain',
                    'Eclipse',
                    'End_Of_Life_FDomain',
                    'Fill_and_Drain',
                    'Fill_and_Drain__1',
                    'Fine',
                    'Formation_Distance_Accuracy_FDomain',
                    'Formation_FDomain',
                    'Fuel',
                    'Fuel_Tank_FillDrain',
                    'Function_FDomain',
                    'GNSS_Receiver_FDomain',
                    'Geo_Location_accuracy_FDomain',
                    'Ground_Segment_FDomain',
                    'Ground_Station_FDomain',
                    'Helix',
                    'High_Gain',
                    'High_Gain_TX',
                    'High_Gian',
                    'Horn',
                    'Hydrazine',
                    'Hydrazine_s',
                    'ION',
                    'Inclination_FDomain',
                    'K_Band',
                    'Ka_Band',
                    'LEOP_FDomain',
                    'Latch',
                    'Lion',
                    'Low_Gain',
                    'Low_Gain_TX',
                    'Low_Noise',
                    'MIL_STD_1553',
                    'Manoeuvre_FDomain',
                    'Mode_FDomain',
                    'Nitrogen',
                    'OBDH_FDomain',
                    'Observation_Local_Time_FDomain',
                    'Observation_Zentih_Angle_FDomain',
                    'Onboard_Computer_FDomain',
                    'Operational_FDomain',
                    'Orbital_FDomain',
                    'Parabolic',
                    'Patch',
                    'Patch_FDomain',
                    'Payload_FDomain',
                    'Payload_Unit_FDomain',
                    'Perigee_Radius_FDomain',
                    'Pointing_Accuracy_FDomain',
                    'Pointing_FDomain',
                    'Position_Latitude_FDomain',
                    'Power_FDomain',
                    'Power_Subsystem_FDomain',
                    'Pressurant',
                    'Pressurant_FillDrain',
                    'Pressurant_Isolation',
                    'Pressurant_Tank_FillDrain',
                    'Propellant',
                    'Propellant_FillDrain',
                    'Propellant_Tank_Latch',
                    'Propulsion_FDomain',
                    'Propulsion_Subsystem_FDomain',
                    'Reciever_FDomain',
                    'Revisit_FDomain',
                    'SAR',
                    'SMA_FDomain',
                    'S_Band',
                    'S_Band_FDomain',
                    'Safe_FDomain',
                    'Separation_Time_FDomain',
                    'SpaceWire',
                    'Subsystem_FDomain',
                    'System_Components_FDomain',
                    'Temperature_Estimation_Accuracy_FDomain',
                    'Thermal_FDomain',
                    'Thermal_Subsystem_FDomain',
                    'Thermo_Electric',
                    'Three_Axis_stab_status_FDomain',
                    'Thruster_Isolation',
                    'Total_Dry',
                    'Total_Wet',
                    'Transmitter_FDomain',
                    'Triple_Junction',
                    'Unit_FDomain',
                    'Variation_of_Local_Time_of_Observation_FDomain',
                    'Wet',
                    'X_Band',
                    'Xenon',
                    'Parameter',
                    'Component',
                    'Mode',
                    'Condition',
                    'Spacecraft',
                    'Subsystem',
                    'Unit',
                    'Payload',
                    'AOCS',
                    'Power_Subsystem',
                    'Thermal_Subsystem',
                    'Communications',
                    'Propulsion_Subsystem',
                    'OBDH',
                    'Solar_Array',
                    'Solar_Array_Actuator',
                    'Battery',
                    'PCDU',
                    'Power_Bus',
                    'Harness',
                    'Switch_Mode_Regulator',
                    'Regulated_Peak_Power_Tracker',
                    'Reaction_Wheel',
                    'Magnetorquer',
                    'GNSS_Receiver',
                    'Earth_Sensor',
                    'Sun_Sensor',
                    'IMU',
                    'Star_Tracker',
                    'IO_remote_data_processing_and_power_distribution_board',
                    'Deployable_Boom',
                    'Thruster',
                    'Tank',
                    'Valve',
                    'Pressure_Regulator',
                    'Filter',
                    'Pressure_Transducer',
                    'Manifold_Control_System',
                    'Manifold_Heat_Sensor',
                    'Propellant_Tank_Thermal_Control',
                    'Radiator',
                    'Heater',
                    'Thermostats',
                    'Heat_Pipe',
                    'Thermal_Control_Unit',
                    'Louvre_Control_Mechanism',
                    'Multi_Layer_Insulation',
                    'Antenna',
                    'Transmitter',
                    'Transciever',
                    'Reciever',
                    'Transponder',
                    'EDRS_Terminal',
                    'Antenna_Pointing_Mechanism',
                    'Modem',
                    'Security_Module',
                    'Amplifier',
                    'RF_Distrubution_Unit',
                    'Onboard_Computer',
                    'Solid_State_Recorder',
                    'Remote_Interface_Unit',
                    'Data_Bus',
                    'Actuator_Drive_Electronics',
                    'Payload_Actuator',
                    'Payload_Electronics',
                    'Payload_Unit',
                    'Magnetometer',
                    'Ground_Station',
                    'Standby',
                    'Imaging',
                    'Comms',
                    'Manoeuvre',
                    'Safe',
                    'Nominal',
                    'LEOP',
                    'Decommissioning',
                    'Lifetime',
                    'Cost',
                    'Altitude',
                    'Perigee_Radius',
                    'Apogee_Radius',
                    'SMA',
                    'Inclination',
                    'AOP',
                    'Eccentricity',
                    'LTAN',
                    'LTDN',
                    'True_Anomaly',
                    'RAAN',
                    'Period',
                    'Revisit',
                    'Mass',
                    'Power',
                    'Data_Generation',
                    'Focal_Length',
                    'Single_Pixel_Size',
                    'Ground_Resolution',
                    'Delta_V',
                    'Volume',
                    'Thrust',
                    'Momentum',
                    'Magnetic_Dipole',
                    'Angular_Error',
                    'Pointing_Accuracy',
                    'Area',
                    'Yaw',
                    'Voltage',
                    'Capacity',
                    'Frequency',
                    'Data_Transfer_Rate',
                    'Diameter',
                    'Gain',
                    'Data_Storage',
                    'Number_of_pixels_Per_Detector_Side',
                    'Depth_of_Discharge',
                    'Position_Knowledge',
                    'Pointing_Knowledge',
                    'Temeprature_Limit',
                    'Position_Latitude',
                    'Position_Longitude',
                    'Length',
                    'Field_of_View',
                    'Rotation_Speed',
                    'Temperature_Estimation_Accuracy',
                    'Observation_Local_Time',
                    'Observation_Zentih_Angle',
                    'Variation_of_Local_Time_of_Observation',
                    'Geo_Location_accuracy',
                    'Availability',
                    'Number_of_Launchers',
                    'Three_Axis_stab_status',
                    'Along_Track_Distance',
                    'Formation_Distance_Accuracy',
                    'Separation_Time',
                    'Latency']
labels = ['Ammonia',
                    'CAN',
                    'Cartidge',
                    'Cartridge',
                    'Coarse',
                    'Control',
                    'Control_Moment_Gyro'
                    'Daylight',
                    'Deployable',
                    'Drain',
                    'Dry',
                    'Eclipse',
                    'Fill_and_Drain',
                    'Fill_and_Drain__1',
                    'Fine',
                    'Fuel',
                    'Fuel_Tank_FillDrain',
                    'Helix',
                    'High_Gain',
                    'High_Gain_TX',
                    'High_Gian',
                    'Horn',
                    'Hydrazine',
                    'Hydrazine_s',
                    'ION',
                    'K_Band',
                    'Ka_Band',
                    'Latch',
                    'Lion',
                    'Low_Gain',
                    'Low_Gain_TX',
                    'Low_Noise',
                    'MIL_STD_1553',
                    'Nitrogen',
                    'Parabolic',
                    'Patch',
                    'Payload_Diplexer',
                    'Payload_Antenna',
                    'Payload_Reflector',
                    'Pressurant',
                    'Pressurant_FillDrain',
                    'Pressurant_Isolation',
                    'Pressurant_Tank_FillDrain',
                    'Propellant',
                    'Propellant_FillDrain',
                    'Propellant_Tank_Latch',
                    'SAR',
                    'S_Band',
                    'SpaceWire',
                    'Thermo_Electric',
                    'Thruster_Isolation',
                    'Total_Dry',
                    'Total_Wet',
                    'Triple_Junction',
                    'Wet',
                    'X_Band',
                    'Xenon']

def identify_target_types(target_lables):
    # these are mappings for possible neighbour types
    # need better control than this....
    shared_labels = lists_overlap(mapped_types, target_lables)

    # CAREFUL FOR nondeterministic behavior here!
    # if no shared label identified, label as 'untraked'
    if shared_labels:
        return shared_labels
    else:
        print(f'UNTRACKED: {target_lables}')
        return 'UNTRACKED'


def define_labelled_types():
    # these are the types whose neighbours will be considered
    return explored_types

def define_mapped_types():
    # these are the types whose neighbours will be considered
    return mapped_types

def define_pure_labels():
    # these are the types whose neighbours will be considered
    return labels