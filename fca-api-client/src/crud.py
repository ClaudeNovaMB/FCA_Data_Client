from fca_models import FirmData, FirmNames, FirmAddress, FirmControlledFunction, FirmRequirement 
from fca_models import FirmRegulator, FirmWaiver, FirmExclusion, FirmDisciplinaryHistory
from fca_models import IndividualData, FirmAppointedRepresentative, IndividualDisciplinaryHistory, IndividualControlFunction
from fca_models import FirmActivitiesAndPermissions
from sqlalchemy.orm import sessionmaker
from config import engine  # Correctly imports engine
from db_models import FirmTable, FirmExceptionalInfoDetailTable, FirmNamesTable, FirmAddressTable
from db_models import FirmControlledFunctionTable, FirmActivitiesAndPermissionsTable, FirmRequirementTable
from db_models import FirmRegulatorTable, FirmWaiverTable, FirmExclusionTable, FirmDisciplinaryHistoryTable
from db_models import IndividualDataTable, FirmAppointedRepresentativeTable, FirmInvestmentTypeTable, Base
from db_models import IndividualControlFunctionTable, IndividualDisciplinaryHistoryTable
import logging
from typing import Dict, Any, List
from psycopg2.errors import UniqueViolation

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

Session = sessionmaker(bind=engine)

def initialize_database():
    """
    Initialize the database by creating all tables.

    This function uses the SQLAlchemy `create_all` method to create all tables
    defined in the SQLAlchemy models. It imports the engine from the config module
    and the Base class from db_models, which contains the metadata for all models.

    The function is called at the module level to ensure the database is initialized
    when the module is loaded.
    """
    from config import engine  # Import the engine from the config module
    Base.metadata.create_all(engine)

# Call the function to initialize the database
initialize_database()

class database_operations:
    
    def save_firmdata_to_database(self, firm_data: FirmData):
        """
        Save firm data to the database.

        This function creates a new `FirmTable` SQLAlchemy object and saves it to the database.
        It depends on:
        - The `Session` object from SQLAlchemy for database transactions.
        - The `FirmTable` SQLAlchemy model to represent the database table.

        Args:
            firm_data (FirmData): The firm data to be saved.
        """
        session = Session()
        try:
            firm_data_status = True
            firm = FirmTable(
                frn=firm_data.frn,
                organisation_name=firm_data.organisation_name,
                companies_house_number=firm_data.companies_house_number,
                business_type=firm_data.business_type,
                mutual_society_number=firm_data.mutual_society_number,
                firm_status=firm_data.status,
                status_effective_date=firm_data.status_effective_date,
                sub_status=firm_data.sub_status,
                sub_status_effective_from=firm_data.sub_status_effective_from,
                e_money_agent_status=firm_data.e_money_agent_status,
                e_money_agent_effective_date=firm_data.e_money_agent_effective_date,
                mlrs_status=firm_data.mlrs_status,
                mlrs_status_effective_date=firm_data.mlrs_status_effective_date,
                psd_agent_status=firm_data.psd_agent_status,
                psd_agent_effective_date=firm_data.psd_agent_effective_date,
                psd_emd_status=firm_data.psd_emd_status,
                psd_emd_effective_date=firm_data.psd_emd_effective_date,
                client_money_permission=firm_data.client_money_permission
            )
            if firm_data.exceptional_info_details is not None:
                for info in firm_data.exceptional_info_details:
                    try:
                        exceptional_info_detail = FirmExceptionalInfoDetailTable(
                            firm_frn=firm_data.frn,
                            exceptional_info_title=info.exceptional_info_title,
                            exceptional_info_body=info.exceptional_info_body
                        )
                        session.merge(exceptional_info_detail)
                        session.commit()
                        logger.info(f"Exceptional info detail added for FRN: {firm_data.frn}")
                    except UniqueViolation:
                        session.rollback()
            session.merge(firm)
            session.commit()
            logger.info(f"Firm data updated in database for FRN: {firm_data.frn}")
            return firm_data_status
        except UniqueViolation:
            session.rollback()
        except Exception as e:
            session.rollback()
            firm_data_status = False
            logger.error(f"Error updating firm data to database for FRN {firm_data.frn}: {e}")
            return firm_data_status
        finally:
            session.close()
            logger.info(f"Session closed for FRN: {firm_data.frn}")

    def save_firm_names_to_database(self, firm_names: FirmNames, frn: int):
        """
        Save firm names to the database.

        This function creates a new `FirmNamesTable` SQLAlchemy object and saves it to the database.
        It depends on:
        - The `Session` object from SQLAlchemy for database transactions.
        - The `FirmNamesTable` SQLAlchemy model to represent the database table.

        Args:
            firm_data (FirmData): The firm data to be saved.
        """
        session = Session()
        try:
            if firm_names.current_names is not None:
                firm_name_status = True
                for name in firm_names.current_names:
                    try:
                        firm_name = FirmNamesTable(
                            firm_frn=frn,
                            firm_name=name.firm_name,
                            name_status=name.name_status,
                            effective_from=name.effective_from,
                            effective_to=name.effective_to,
                        )
                        session.add(firm_name)
                        session.commit()
                        logger.info(f"FRN: {frn} - Current name added: {name.firm_name}")
                    except UniqueViolation:
                        session.rollback()
            if firm_names.previous_names is not None:
                for name in firm_names.previous_names:
                    try:
                        firm_name = FirmNamesTable(
                            firm_frn=frn,
                            firm_name=name.firm_name,
                            name_status=name.name_status,
                            effective_from=name.effective_from,
                            effective_to=name.effective_to
                        )
                        session.add(firm_name)
                        session.commit()
                        logger.info(f"FRN: {frn} - Previous name added: {name.firm_name}")
                    except UniqueViolation:
                        session.rollback()
                logger.info(f"Firm names updated in database for FRN: {frn}")
                return True
        except Exception as e:
            session.rollback()
            firm_name_status = False
            logger.error(f"Error updating firm names to database for FRN {frn}: {e}")
            return firm_name_status
        finally:
            session.close()
            logger.info(f"Session closed for Firm_Names (FRN: {frn})")

    def save_firm_address_to_database(self, firm_address: FirmAddress, frn: int):
        """
        Save firm address to the database.

        This function creates a new `FirmAddressTable` SQLAlchemy object and saves it to the database.
        It depends on:
        - The `Session` object from SQLAlchemy for database transactions.
        - The `FirmAddressTable` SQLAlchemy model to represent the database table.

        Args:
            firm_data (FirmData): The firm data to be saved.
        """
        session = Session()
        try:
            if firm_address is not None:
                firm_address_status = True
                firm_address = FirmAddressTable(

                    firm_frn=frn,
                    address_type=firm_address.address_type,
                    address_line_1=firm_address.address_line_1,
                    address_line_2=firm_address.address_line_2,
                    address_line_3=firm_address.address_line_3,
                    address_line_4=firm_address.address_line_4,
                    town=firm_address.town,
                    county=firm_address.county,
                    postcode=firm_address.postcode,
                    country=firm_address.country,
                    phone_number=firm_address.phone_number,
                    website_address=firm_address.website_address
                )
                session.merge(firm_address)
            session.commit()
            logger.info(f"FRM: {frn} - New address added")
            return firm_address_status
        except UniqueViolation:
            session.rollback()
        except Exception as e:
            session.rollback()
            firm_address_status = False
            logger.error(f"Error saving firm address to database for FRN {frn}: {e}")
            return firm_address_status
        finally:
            session.close()
            logger.info(f"Session closed for FRN: {frn}")

    def save_firm_controlled_functions_to_database(self, controlled_function: FirmControlledFunction, frn: int):
        """
        Save firm controlled functions to the database.

        This function creates new `FirmControlledFunctionTable` SQLAlchemy objects and saves them to the database.
        It depends on:
        - The `Session` object from SQLAlchemy for database transactions.
        - The `FirmControlledFunctionTable` SQLAlchemy model to represent the database table.

        Args:
            controlled_function (FirmControlledFunction): The controlled function data to be saved.
            frn (int): The Firm Reference Number.
        """
        session = Session()
        try:
            controlled_functions_status = True
            # Save current controlled functions if available
            if controlled_function.current:
                for key, detail in controlled_function.current.items():
                    try:
                        controlled_function_entry = FirmControlledFunctionTable(
                            firm_frn=frn,
                            control_status='current',
                            individual_name=detail.individual_name,
                            controller_name=detail.name,
                            url=detail.url,
                            effective_date=detail.effective_date,
                            end_date=detail.end_date,
                            suspension_restriction_start_date=detail.suspension_restriction_start_date,
                            suspension_restriction_end_date=detail.suspension_restriction_end_date,
                            restriction=detail.restriction
                        )
                        session.merge(controlled_function_entry)
                        session.commit()
                    except UniqueViolation:
                        session.rollback()
            # Save previous controlled functions if available
            if controlled_function.previous:
                for key, detail in controlled_function.previous.items():
                    try:
                        controlled_function_entry = FirmControlledFunctionTable(
                            firm_frn=frn,
                            control_status='previous',
                            individual_name=detail.individual_name,
                            controller_name=detail.name,
                            url=detail.url,
                            effective_date=detail.effective_date,
                            end_date=detail.end_date,
                            suspension_restriction_start_date=detail.suspension_restriction_start_date,
                            suspension_restriction_end_date=detail.suspension_restriction_end_date,
                            restriction=detail.restriction
                        )
                        session.merge(controlled_function_entry)
                        session.commit()
                    except UniqueViolation:
                        session.rollback()
            
            logger.info(f"Controlled functions updated in database for FRN: {frn}")
            return controlled_functions_status
        except Exception as e:
            session.rollback()
            controlled_functions_status = False
            logger.error(f"Error saving controlled functions to database for FRN {frn}: {e}")
            return controlled_functions_status
        finally:
            session.close()
            logger.info(f"Session closed for FRN: {frn}")

    def save_firm_activities_and_permissions_to_database(self, activities_permissions: List[FirmActivitiesAndPermissions], frn: int):
        """
        Save firm activities and permissions to the database.

        This function creates new `FirmActivitiesAndPermissionsTable` SQLAlchemy objects and saves them to the database.
        It depends on:
        - The `Session` object from SQLAlchemy for database transactions.
        - The `FirmActivitiesAndPermissionsTable` SQLAlchemy model to represent the database table.

        Args:
            activities_permissions (List[FirmActivitiesAndPermissions]): The parsed activities and permissions data to be saved.
            frn (int): The Firm Reference Number.
        """
        session = Session()
        try:
            activities_permissions_status = True
            for activity_permission in activities_permissions:
                if activity_permission.participation:
                    for participation_detail in activity_permission.participation:
                        if participation_detail.participation_option:
                            for participation_option in participation_detail.participation_option:
                                try:
                                    entry = FirmActivitiesAndPermissionsTable(
                                        firm_frn=frn,
                                        activity_name=activity_permission.activity_name,
                                        participation=participation_detail.participation,
                                        participation_option=participation_option
                                    )
                                    session.merge(entry)
                                    session.commit()
                                except UniqueViolation:
                                    session.rollback()
                
            logger.info(f"Activities and permissions updated in database for FRN: {frn}")
            return activities_permissions_status
        except Exception as e:
            session.rollback()
            activities_permissions_status = False
            logger.error(f"Error updating activities and permissions to database for FRN {frn}: {e}")
            return activities_permissions_status
        finally:
            session.close()
            logger.info(f"Session closed for FRN: {frn}")

    def save_firm_requirements_to_database(self, firm_requirements: List[FirmRequirement], frn: int):
        """
        Save firm requirements to the database.

        This function creates new `FirmRequirementTable` SQLAlchemy objects and saves them to the database.
        It depends on:
        - The `Session` object from SQLAlchemy for database transactions.
        - The `FirmRequirementTable` SQLAlchemy model to represent the database table.

        Args:
            firm_requirements (List[FirmRequirement]): The list of firm requirements to be saved.
            frn (int): The Firm Reference Number.
        """
        session = Session()
        try:
            requirements_status = True
            for requirement in firm_requirements:
                try:
                    requirement_entry = FirmRequirementTable(
                        firm_frn=frn,
                        effective_date=requirement.effective_date,
                        derivatives_as_incidental_services_only=requirement.derivatives_as_incidental_services_only,
                        requirement_reference=requirement.requirement_reference,
                        financial_promotions_requirement=requirement.financial_promotions_requirement,
                        financial_promotions_investment_types=requirement.financial_promotions_investment_types
                    )
                    session.merge(requirement_entry)
                    session.commit()
                except UniqueViolation:
                    session.rollback()
            logger.info(f"Firm requirements updated in database for FRN: {frn}")
            return requirements_status
        except Exception as e:
            session.rollback()
            requirements_status = False
            logger.error(f"Error updating firm requirements to database for FRN {frn}: {e}")
            return requirements_status
        finally:
            session.close()
            logger.info(f"Session closed for FRN: {frn}")

    def read_firm_requirement_references(self, frn: int) -> List[str]:
        """
        Read firm requirement references from the database.

        This function queries the `FirmRequirementTable` to retrieve all requirement references for a given FRN.
        It depends on:
        - The `Session` object from SQLAlchemy for database transactions.
        - The `FirmRequirementTable` SQLAlchemy model to represent the database table.

        Args:
            frn (int): The Firm Reference Number.

        Returns:
            List[str]: A list of requirement references for the specified FRN.
        """
        session = Session()
        try:
            requirement_references = session.query(FirmRequirementTable).filter_by(firm_frn=frn).all()
            return [str(reference.requirement_reference) for reference in requirement_references]
        except Exception as e:
            logger.error(f"Error reading firm requirement references from database for FRN {frn}: {e}")
            return []
        finally:
            session.close()
            logger.info(f"Session closed for FRN: {frn}")

    def save_firm_investment_types_to_database(self, firm_investment_types: List[str], frn: int):
        """
        Save firm investment types to the database.

        This function creates new `FirmInvestmentTypeTable` SQLAlchemy objects and saves them to the database.
        It depends on:
        - The `Session` object from SQLAlchemy for database transactions.
        - The `FirmInvestmentTypeTable` SQLAlchemy model to represent the database table.

        Args:
            firm_investment_types (List[str]): The list of firm investment types to be saved.
            frn (int): The Firm Reference Number.
        """
        session = Session()
        try:
            investment_type_status = True
            for investment_type in firm_investment_types:
                try:
                    investment_type_entry = FirmInvestmentTypeTable(
                        firm_frn=frn,
                        investment_type=investment_type
                    )
                    session.add(investment_type_entry)
                    session.commit()
                except UniqueViolation:
                    session.rollback()
            logger.info(f"Firm investment types saved to database for FRN: {frn}")
            return investment_type_status
        except Exception as e:
            session.rollback()
            investment_type_status = False
            logger.error(f"Error saving firm investment types to database for FRN {frn}: {e}")
            return investment_type_status
        finally:
            session.close()
            logger.info(f"Session closed for FRN: {frn}")

    def save_firm_regulators_to_database(self, firm_regulators: List[FirmRegulator], frn: int):
        """
        Save firm regulators to the database.

        This function creates new `FirmRegulatorTable` SQLAlchemy objects and saves them to the database.
        It depends on:
        - The `Session` object from SQLAlchemy for database transactions.
        - The `FirmRegulatorTable` SQLAlchemy model to represent the database table.

        Args:
            firm_regulators (List[FirmRegulator]): The list of firm regulators to be saved.
            frn (int): The Firm Reference Number.
        """
        session = Session()
        try:
            regulators_status = True
            for regulator in firm_regulators:
                try:
                    regulator_entry = FirmRegulatorTable(
                        termination_date=regulator.termination_date,
                        effective_date=regulator.effective_date,
                        regulator_name=regulator.regulator_name,
                        firm_frn=frn
                    )
                    session.merge(regulator_entry)
                    session.commit()
                    logger.info(f"Firm regulators saved to database for FRN: {frn}")
                except UniqueViolation:
                    session.rollback()
                    logger.warning(f"Duplicate entry for regulator {regulator.regulator_name} for FRN {frn}")
            return regulators_status
        except Exception as e:
            session.rollback()
            regulators_status = False
            logger.error(f"Error saving firm regulators to database for FRN {frn}: {e}")
            return regulators_status
        finally:
            session.close()
            logger.info(f"Session closed for FRN: {frn}")

    def save_firm_waivers_to_database(self, firm_waivers: List[FirmWaiver], frn: int):
        """
        Save firm waivers to the database.

        This function creates new `FirmWaiverTable` SQLAlchemy objects and saves them to the database.
        It depends on:
        - The `Session` object from SQLAlchemy for database transactions.
        - The `FirmWaiverTable` SQLAlchemy model to represent the database table.

        Args:
            firm_waivers (List[FirmWaiver]): The list of firm waivers to be saved.
            frn (int): The Firm Reference Number.
        """
        session = Session()
        try:
            for waiver in firm_waivers:
                waiver_entry = FirmWaiverTable(
                    waivers_discretions_url=waiver.waivers_discretions_url,
                    waivers_discretions=waiver.waivers_discretions,
                    rule_article_no=waiver.rule_article_no,
                    firm_frn=frn
                )
                session.add(waiver_entry)
            session.commit()
            logger.info(f"Firm waivers saved to database for FRN: {frn}")
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving firm waivers to database for FRN {frn}: {e}")
            return False
        finally:
            session.close()
            logger.info(f"Session closed for FRN: {frn}")

    def save_firm_exclusions_to_database(self, firm_exclusions: List[FirmExclusion], frn: int):
        """
        Save firm exclusions to the database.

        This function creates new `FirmExclusionTable` SQLAlchemy objects and saves them to the database.
        It depends on:
        - The `Session` object from SQLAlchemy for database transactions.
        - The `FirmExclusionTable` SQLAlchemy model to represent the database table.

        Args:
            firm_exclusions (List[FirmExclusion]): The list of firm exclusions to be saved.
            frn (int): The Firm Reference Number.
        """
        session = Session()
        try:
            for exclusion in firm_exclusions:
                exclusion_entry = FirmExclusionTable(
                    psd2_exclusion_type=exclusion.psd2_exclusion_type,
                    particular_exclusion_relied_upon=exclusion.particular_exclusion_relied_upon,
                    description_of_services=exclusion.description_of_services,
                    firm_frn=frn
                )
                session.add(exclusion_entry)
            session.commit()
            logger.info(f"Firm exclusions saved to database for FRN: {frn}")
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving firm exclusions to database for FRN {frn}: {e}")
            return False
        finally:
            session.close()
            logger.info(f"Session closed for FRN: {frn}")

    def save_firm_disciplinary_history_to_database(self, disciplinary_history: List[FirmDisciplinaryHistory], frn: int):
        """
        Save firm disciplinary history to the database.

        This function creates new `FirmDisciplinaryHistoryTable` SQLAlchemy objects and saves them to the database.
        It depends on:
        - The `Session` object from SQLAlchemy for database transactions.
        - The `FirmDisciplinaryHistoryTable` SQLAlchemy model to represent the database table.

        Args:
            disciplinary_history (List[FirmDisciplinaryHistory]): The list of firm disciplinary history to be saved.
            frn (int): The Firm Reference Number.
        """
        session = Session()
        try:
            for history in disciplinary_history:
                history_entry = FirmDisciplinaryHistoryTable(
                    typeof_description=history.typeof_description,
                    typeof_action=history.typeof_action,
                    enforcement_type=history.enforcement_type,
                    action_effective_from=history.action_effective_from,
                    firm_frn=frn
                )
                session.add(history_entry)
            session.commit()
            logger.info(f"Firm disciplinary history saved to database for FRN: {frn}")
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving firm disciplinary history to database for FRN {frn}: {e}")
            return False
        finally:
            session.close()
            logger.info(f"Session closed for FRN: {frn}")

    def save_firm_individuals_to_database(self, individual_data: IndividualData, frn: int):
        """
        Save firm individuals to the database.

        This function creates new `IndividualDataTable` SQLAlchemy objects and saves them to the database.
        It depends on:
        - The `Session` object from SQLAlchemy for database transactions.
        - The `IndividualDataTable` SQLAlchemy model to represent the database table.

        Args:
            firm_individuals (List[IndividualData]): The list of firm individuals to be saved.
            frn (int): The Firm Reference Number.
        """
        session = Session()
        irn = individual_data.individual_data.irn if individual_data.individual_data else None
        try:
            try:

                if individual_data.individual_data is not None:
                    individual_entry = IndividualDataTable(
                        frn=frn,
                        irn=individual_data.individual_data.irn,
                        full_name=individual_data.individual_data.full_name,
                        commonly_used_name=individual_data.individual_data.commonly_used_name,
                        individual_status=individual_data.individual_data.individual_status
                    )
                    session.merge(individual_entry)
                    session.commit()
                    logger.info(f"Firm individuals saved to database for FRN: {frn} - IRN {irn}")
                return True
            except UniqueViolation:
                session.rollback()
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving firm individuals to database for FRN {frn} - IRN: {irn} : {e}")
            return False
        finally:
            session.close()
            logger.info(f"Session closed for FRN: {frn}")
        
    def save_individual_control_function_to_database(self, individual_control_function: IndividualControlFunction, irn: str):
        """
        Save individual control functions to the database.

        This function creates new `IndividualControlFunctionTable` SQLAlchemy objects and saves them to the database.
        It depends on:
        - The `Session` object from SQLAlchemy for database transactions.
        - The `IndividualControlFunctionTable` SQLAlchemy model to represent the database table.

        Args:
            individual_control_function (List[FirmControlledFunction]): The list of individual control functions to be saved.
            frn (int): The Firm Reference Number.
        """
        session = Session()
        try:
            individual_CF_status = True
            # Save current controlled functions if available
            if individual_control_function.current:
                for key, detail in individual_control_function.current.items():
                    try:
                        control_function_entry = IndividualControlFunctionTable(
                            irn=irn,
                            role_name=detail.role_name,
                            firm_name=detail.firm_name,
                            control_status='current',
                            effective_date=detail.effective_date,
                            end_date=detail.end_date,
                            customer_engagement_method=detail.customer_engagement_method,
                            suspension_restriction_start_date=detail.suspension_restriction_start_date,
                            suspension_restriction_end_date=detail.suspension_restriction_end_date,
                            restriction=detail.restriction
                        )
                        session.merge(control_function_entry)
                        session.commit()
                    except UniqueViolation:
                        session.rollback()
            # Save previous controlled functions if available
            if individual_control_function.previous:
                for key, detail in individual_control_function.previous.items():
                    try:
                        control_function_entry = IndividualControlFunctionTable(
                            irn=irn,
                            role_name=detail.role_name,
                            firm_name=detail.firm_name,
                            control_status='previous',
                            effective_date=detail.effective_date,
                            end_date=detail.end_date,
                            customer_engagement_method=detail.customer_engagement_method,
                            suspension_restriction_start_date=detail.suspension_restriction_start_date,
                            suspension_restriction_end_date=detail.suspension_restriction_end_date,
                            restriction=detail.restriction
                        )
                        session.merge(control_function_entry)
                        session.commit()
                    except UniqueViolation:
                        session.rollback()
            
                    logger.info(f"Controlled functions updated in database for FRN: {irn}")
                return individual_CF_status
        except Exception as e:
            session.rollback()
            individual_CF_status = False
            logger.error(f"Error saving controlled functions to database for FRN {irn}: {e}")
            return individual_CF_status
        finally:
            session.close()
            logger.info(f"Session closed for FRN: {irn}")

    def save_individual_disciplinary_history_to_database(self, disciplinary_history: IndividualDisciplinaryHistory, irn: str):
        """
        Save individual disciplinary history to the database.

        This function creates new `IndividualDisciplinaryHistoryTable` SQLAlchemy objects and saves them to the database.
        It depends on:
        - The `Session` object from SQLAlchemy for database transactions.
        - The `IndividualDisciplinaryHistoryTable` SQLAlchemy model to represent the database table.

        Args:
            disciplinary_history (List[IndividualDisciplinaryHistory]): The list of individual disciplinary history to be saved.
            irn (str): The Individual Reference Number.
        """
        session = Session()
        try:
            disciplinary_history_status = True
            if disciplinary_history is not None:
                history_entry = IndividualDisciplinaryHistoryTable(
                    irn=irn,
                    typeof_description=disciplinary_history.typeof_description,
                    typeof_action=disciplinary_history.typeof_action,
                    enforcement_type=disciplinary_history.enforcement_type,
                    action_effective_from=disciplinary_history.action_effective_from
                )
                session.merge(history_entry)
                session.commit()
                logger.info(f"Individual disciplinary history saved to database for IRN: {irn}")
                return disciplinary_history_status
        except UniqueViolation:
            session.rollback()
        except Exception as e:
            session.rollback()
            disciplinary_history_status = False
            logger.error(f"Error saving individual disciplinary history to database for IRN {irn}: {e}")
            return disciplinary_history_status
        finally:
            session.close()
            logger.info(f"Session closed for IRN: {irn}")        

    def save_firm_appointed_representatives_to_database(self, appointed_representatives: FirmAppointedRepresentative, frn: int):
        """
        Save firm appointed representatives to the database.

        This function creates new `FirmAppointedRepresentativeTable` SQLAlchemy objects and saves them to the database.
        It depends on:
        - The `Session` object from SQLAlchemy for database transactions.
        - The `FirmAppointedRepresentativeTable` SQLAlchemy model to represent the database table.

        Args:
            appointed_representatives (FirmAppointedRepresentative): The appointed representatives data to be saved.
            frn (int): The Firm Reference Number.
        """
        session = Session()
        try:
            for representative in appointed_representatives.current_appointed_representatives:
                current_entry = FirmAppointedRepresentativeTable(
                    current_appointed_representatives=representative.name,
                    firm_frn=frn
                )
                session.add(current_entry)

            for representative in appointed_representatives.previous_appointed_representatives:
                previous_entry = FirmAppointedRepresentativeTable(
                    previous_appointed_representatives=representative.name,
                    firm_frn=frn
                )
                session.add(previous_entry)

            session.commit()
            logger.info(f"Firm appointed representatives saved to database for FRN: {frn}")
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving firm appointed representatives to database for FRN {frn}: {e}")
            return False
        finally:
            session.close()
            logger.info(f"Session closed for FRN: {frn}")