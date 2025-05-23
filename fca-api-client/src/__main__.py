import argparse
from client import FCAApiClient
from crud import database_operations

def main():
    """
    Main function to handle command-line arguments and interact with the FCA API client.

    This function uses the `argparse` library to parse command-line arguments for
    searching firms or retrieving firm data. It creates an instance of `FCAApiClient`
    to perform the API requests. The function depends on:
    - The `argparse` library for command-line argument parsing.
    - The `FCAApiClient` class for interacting with the FCA API.

    Returns:
        None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--frn", type=int, help="Firm Reference Number")
    parser.add_argument("--out", type=str, help="Output file")
    args = parser.parse_args()

    client = FCAApiClient()
    crud = database_operations()
    frn = 451236
    
    firm_data = client.get_firm_data(frn)
    
    if firm_data is not None:
        firm_data_status = crud.save_firmdata_to_database(firm_data)
        if firm_data_status:
            print(f"Firm data update in database for FRN: {firm_data.frn}\n")
        else:
            print(f"Failed to update firm data for FRN: {firm_data.frn}\n")

    firm_names = client.get_firm_names(frn)
    
    if firm_names is not None:
        all_saved = True
        for firm_name in firm_names:
            firm_name_status = crud.save_firm_names_to_database(firm_name, frn=frn)
            if not firm_name_status:
                all_saved = False
                print(f"Failed to save firm name for FRN: {frn}")
        if all_saved:
            print(f"Firm names updated in database for FRN: {frn}\n")
        else:
            print(f"Failed to update all firm names for FRN: {frn}\n")
    
    firm_address = client.get_firm_addresses(frn)
    
    if firm_address is not None:
        all_saved = True
        for address in firm_address:
            firm_address_status = crud.save_firm_address_to_database(firm_address=address, frn=frn)
            if not firm_address_status:
                print(f"Failed to save firm address for FRN: {frn}")
                all_saved = False
        if all_saved:
            print(f"Firm addresses updated in database for FRN: {frn}\n")
        else:
            print(f"Failed to update firm addresses for FRN: {frn}\n")


    firm_controlled_functions = client.get_firm_controlled_functions(frn)

    if firm_controlled_functions is not None:
        controlled_functions_status = crud.save_firm_controlled_functions_to_database(firm_controlled_functions, frn=frn)
        if controlled_functions_status:
            print(f"Controlled functions updated in database for FRN: {frn}\n")
        else:
            print(f"Failed to update controlled functions for FRN: {frn}\n")

    firm_activities_permissions = client.get_firm_activities_and_permissions(frn)

    if firm_activities_permissions is not None:
        activities_permissions_status = crud.save_firm_activities_and_permissions_to_database(firm_activities_permissions, frn=frn)
        if activities_permissions_status:
            print(f"Activities and permissions saved to database for FRN: {frn}\n")
        else:
            print(f"Failed to save activities and permissions for FRN: {frn}\n")

    firm_requirements = client.get_firm_requirements(frn)

    if firm_requirements is not None:
        requirements_status = crud.save_firm_requirements_to_database(firm_requirements, frn=frn)
        if requirements_status:
            print(f"Firm requirements saved to database for FRN: {frn}\n")
        else:
            print(f"Failed to save firm requirements for FRN: {frn}\n")

    firm_requirement_references = crud.read_firm_requirement_references(frn)
    if firm_requirement_references is not None:
        for reference in firm_requirement_references:
            
            firm_investment_type = client.get_firm_investment_types(frn, reference)

            if firm_investment_type is not None:
                investment_type_status = crud.save_firm_investment_types_to_database(firm_investment_type, frn=frn)
                if investment_type_status:
                    print(f"Firm investment types updated in database for FRN: {frn}\n")
                else:
                    print(f"Failed to update firm investment types for FRN: {frn}\n")

    firm_regulators = client.get_firm_regulators(frn)

    if firm_regulators is not None:
        regulators_status = crud.save_firm_regulators_to_database(firm_regulators, frn=frn)
        if regulators_status:
            print(f"Firm regulators saved to database for FRN: {frn}\n")
        else:
            print(f"Failed to save firm regulators for FRN: {frn}\n")

    firm_waivers = client.get_firm_waiver(frn)

    if firm_waivers is not None:
        waivers_status = crud.save_firm_waivers_to_database(firm_waivers, frn=frn)
        if waivers_status:
            print(f"Firm waivers saved to database for FRN: {frn}\n")
        else:
            print(f"Failed to save firm waivers for FRN: {frn}\n")

    firm_exclusions = client.get_firm_exclusions(frn)

    if firm_exclusions is not None:
        exclusions_status = crud.save_firm_exclusions_to_database(firm_exclusions, frn=frn)
        if exclusions_status:
            print(f"Firm exclusions saved to database for FRN: {frn}\n")
        else:
            print(f"Failed to save firm exclusions for FRN: {frn}\n")

    firm_disciplinary_history = client.get_firm_disciplinary_history(frn)

    if firm_disciplinary_history is not None:
        disciplinary_history_status = crud.save_firm_disciplinary_history_to_database(firm_disciplinary_history, frn=frn)
        if disciplinary_history_status:
            print(f"Firm disciplinary history saved to database for FRN: {frn}\n")
        else:
            print(f"Failed to save firm disciplinary history for FRN: {frn}\n")

    firm_individuals = client.get_firm_individuals(frn)

    if firm_individuals is not None:
        for individual in firm_individuals:
            firm_individual = client.get_individual_data(str(individual))
            

            if firm_individual is not None:
                for individual_data in firm_individual:
                    individual_status = crud.save_firm_individuals_to_database(individual_data, frn=frn)
                    if individual_status:
                        print(f"Individual data saved to database for FRN: {frn}\n")
                    else:
                        print(f"Failed to save individual data for FRN: {frn}\n")
                    
            individual_CF = client.get_individual_control_function(str(individual))
            if individual_CF is not None:
                individual_CF_status = crud.save_individual_control_function_to_database(individual_CF, irn=str(individual))
                if individual_CF_status:
                    print(f"Individual control function saved to database for FRN: {frn}\n")
                else:
                    print(f"Failed to save individual control function for FRN: {frn}\n")

            individual_DH = client.get_individual_disciplinary_history(str(individual))
            if individual_DH is not None:
                for individual_disciplinary_history in individual_DH:
                    individual_DH_status = crud.save_individual_disciplinary_history_to_database(individual_disciplinary_history, irn=str(individual))
                    if individual_DH_status:
                        print(f"Individual disciplinary history saved to database for FRN: {frn}\n")
                    else:
                        print(f"Failed to save individual disciplinary history for FRN: {frn}\n")


    # firm_appointed_representatives = client.get_firm_appointed_representatives(frn)

    # if firm_appointed_representatives is not None:
    #     representatives_status = crud.save_firm_appointed_representatives_to_database(firm_appointed_representatives, frn=frn)
    #     if representatives_status:
    #         print(f"Firm appointed representatives saved to database for FRN: {frn}")
    #     else:
    #         print(f"Failed to save firm appointed representatives for FRN: {frn}")

if __name__ == "__main__":
    main()
