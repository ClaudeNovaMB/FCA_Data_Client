from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FirmTable(Base):
    __tablename__ = 'firms'
    __table_args__ = {'schema': 'fcadata'}

    frn = Column(Integer, primary_key=True, nullable=False, unique=True)
    organisation_name = Column(String, nullable=False)
    companies_house_number = Column(String, nullable=True)
    business_type = Column(String, nullable=True)
    mutual_society_number = Column(String, nullable=True)
    firm_status = Column(String, nullable=True)
    status_effective_date = Column(String, nullable=True)
    sub_status = Column(String, nullable=True)
    sub_status_effective_from = Column(String, nullable=True)
    e_money_agent_status = Column(String, nullable=True)
    e_money_agent_effective_date = Column(String, nullable=True)
    mlrs_status = Column(String, nullable=True)
    mlrs_status_effective_date = Column(String, nullable=True)
    psd_agent_status = Column(String, nullable=True)
    psd_agent_effective_date = Column(String, nullable=True)
    psd_emd_status = Column(String, nullable=True)
    psd_emd_effective_date = Column(String, nullable=True)
    exceptional_info = Column(String, nullable=True)
    client_money_permission = Column(String, nullable=True)

class FirmExceptionalInfoDetailTable(Base):
    __tablename__ = 'firm_exceptional_info_details'
    __table_args__ = {'schema': 'fcadata'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    firm_frn = Column(Integer, ForeignKey('fcadata.firms.frn'), nullable=False)
    exceptional_info_title = Column(String, nullable=False)
    exceptional_info_body = Column(String, nullable=False)

class FirmNamesTable(Base):
    __tablename__ = 'firm_names'
    __table_args__ = {'schema': 'fcadata'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    firm_frn = Column(Integer, ForeignKey('fcadata.firms.frn'), nullable=False)
    firm_name = Column(String, nullable=False)
    name_status = Column(String, nullable=True)
    effective_from = Column(String, nullable=True)
    effective_to = Column(String, nullable=True)
    

class FirmAddressTable(Base):
    __tablename__ = 'firm_addresses'
    __table_args__ = {'schema': 'fcadata'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    firm_frn = Column(Integer, ForeignKey('fcadata.firms.frn'), nullable=False)
    address_type = Column(String, nullable=True)
    address_line_1 = Column(String, nullable=True)
    address_line_2 = Column(String, nullable=True)
    address_line_3 = Column(String, nullable=True)    
    address_line_4 = Column(String, nullable=True)
    town = Column(String, nullable=True)
    county = Column(String, nullable=True)
    postcode = Column(String, nullable=True)
    country = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    website_address = Column(String, nullable=True)

class FirmControlledFunctionTable(Base):
    __tablename__ = 'firm_controlled_functions'
    __table_args__ = {'schema': 'fcadata'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    firm_frn = Column(Integer, ForeignKey('fcadata.firms.frn'), nullable=False)
    control_status = Column(String, nullable=False)  # Indicates whether it's 'current' or 'previous'
    individual_name = Column(String, nullable=True)
    controller_name = Column(String, nullable=True)
    url = Column(String, nullable=True)
    effective_date = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    suspension_restriction_start_date = Column(String, nullable=True)
    suspension_restriction_end_date = Column(String, nullable=True)
    restriction = Column(String, nullable=True)

class FirmActivitiesAndPermissionsTable(Base):
    __tablename__ = 'firm_activities_and_permissions'
    __table_args__ = {'schema': 'fcadata'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    firm_frn = Column(Integer, ForeignKey('fcadata.firms.frn'), nullable=False)  # Foreign key to FirmTable
    activity_name = Column(String, nullable=False)  # Activity name is required
    participation = Column(String, nullable=False)  # Participation is required
    participation_option = Column(String, nullable=True)  # Values can be optional

class FirmRequirementTable(Base):
    __tablename__ = 'firm_requirements'
    __table_args__ = {'schema': 'fcadata'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    firm_frn = Column(Integer, ForeignKey('fcadata.firms.frn'), nullable=False)
    effective_date = Column(String, nullable=True)
    derivatives_as_incidental_services_only = Column(String, nullable=True)
    requirement_reference = Column(String, nullable=True)
    financial_promotions_requirement = Column(String, nullable=True)
    financial_promotions_investment_types = Column(String, nullable=True)

class FirmInvestmentTypeTable(Base):
    __tablename__ = 'firm_investment_types'
    __table_args__ = {'schema': 'fcadata'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    firm_frn = Column(Integer, ForeignKey('fcadata.firms.frn'), nullable=False)
    investment_type_name = Column(String, nullable=False)

class FirmRegulatorTable(Base):
    __tablename__ = 'firm_regulators'
    __table_args__ = {'schema': 'fcadata'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    termination_date = Column(String, nullable=True)
    effective_date = Column(String, nullable=False)
    regulator_name = Column(String, nullable=False)
    firm_frn = Column(Integer, ForeignKey('fcadata.firms.frn'), nullable=False)

class FirmPassportTable(Base):
    __tablename__ = 'firm_passports'
    __table_args__ = {'schema': 'fcadata'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    passport_direction = Column(String, nullable=False)
    firm_name = Column(String, nullable=False)
    investment_type = Column(String, nullable=False)
    passport_type = Column(String, nullable=False)
    passport_direction = Column(String, nullable=False)
    directive = Column(String, nullable=False)
    country = Column(String, nullable=False)
    firm_frn = Column(Integer, ForeignKey('fcadata.firms.frn'), nullable=False)

class FirmWaiverTable(Base):
    __tablename__ = 'firm_waivers'
    __table_args__ = {'schema': 'fcadata'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    waivers_discretions_url = Column(String, nullable=False)
    waivers_discretions = Column(String, nullable=False)
    rule_article_no = Column(String, nullable=True)
    firm_frn = Column(Integer, ForeignKey('fcadata.firms.frn'), nullable=False)

class FirmExclusionTable(Base):
    __tablename__ = 'firm_exclusions'
    __table_args__ = {'schema': 'fcadata'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    psd2_exclusion_type = Column(String, nullable=False)
    particular_exclusion_relied_upon = Column(String, nullable=False)
    description_of_services = Column(String, nullable=False)
    firm_frn = Column(Integer, ForeignKey('fcadata.firms.frn'), nullable=False)

class FirmDisciplinaryHistoryTable(Base):
    __tablename__ = 'firm_disciplinary_histories'
    __table_args__ = {'schema': 'fcadata'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    typeof_description = Column(String, nullable=False)
    typeof_action = Column(String, nullable=False)
    enforcement_type = Column(String, nullable=False)
    action_effective_from = Column(String, nullable=False)
    firm_frn = Column(Integer, ForeignKey('fcadata.firms.frn'), nullable=False)

class FirmAppointedRepresentativeTable(Base):
    __tablename__ = 'firm_appointed_representatives'
    __table_args__ = {'schema': 'fcadata'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    previous_appointed_representatives = Column(String, nullable=True)
    current_appointed_representatives = Column(String, nullable=True)
    firm_frn = Column(Integer, ForeignKey('fcadata.firms.frn'), nullable=False)

class IndividualDataTable(Base):
    __tablename__ = 'individual_data'
    __table_args__ = {'schema': 'fcadata'}
    
    frn = Column(Integer, ForeignKey('fcadata.firms.frn'), nullable=False)
    irn = Column(String, primary_key=True, unique=True)
    full_name = Column(String, nullable=True)
    commonly_used_name = Column(String, nullable=True)
    individual_status = Column(String, nullable=True)

    
class IndividualControlFunctionTable(Base):
    __tablename__ = 'individual_control_function'
    __table_args__ = {'schema': 'fcadata'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    irn = Column(String, ForeignKey('fcadata.individual_data.irn'), nullable=False)
    role_name = Column(String, nullable=True)
    firm_name = Column(String, nullable=True)
    control_status = Column(String, nullable=True) 
    effective_date = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    customer_engagement_method = Column(String, nullable=True)
    suspension_restriction_end_date = Column(String, nullable=True)
    suspension_restriction_start_date = Column(String, nullable=True)
    restriction = Column(String, nullable=True)

class IndividualDisciplinaryHistoryTable(Base):
    __tablename__ = 'individual_disciplinary_history'
    __table_args__ = {'schema': 'fcadata'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    irn = Column(String, ForeignKey('fcadata.individual_data.irn'), nullable=False)
    action_effective_from = Column(String, nullable=True)
    enforcement_type = Column(String, nullable=True)
    typeof_action = Column(String, nullable=True)
    typeof_description = Column(String, nullable=True)
    
