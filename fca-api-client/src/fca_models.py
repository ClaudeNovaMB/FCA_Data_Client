from pydantic import BaseModel, Field, HttpUrl
from typing import Dict, List, Optional
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FirmAppointedRepresentativeDetail(BaseModel):
    url: HttpUrl = Field(..., alias="URL")
    termination_date: Optional[str] = Field(None, alias="Termination Date")
    record_subtype: str = Field(..., alias="Record SubType")
    principal_frn: str = Field(..., alias="Principal FRN")
    principal_firm_name: str = Field(..., alias="Principal Firm Name")
    effective_date: str = Field(..., alias="Effective Date")
    eea_tied_agent: bool = Field(..., alias="EEA Tied Agent")
    tied_agent: bool = Field(..., alias="Tied Agent")
    insurance_distribution: bool = Field(..., alias="Insurance Distribution")
    frn: str = Field(..., alias="FRN")
    name: str = Field(..., alias="Name")

class FirmAppointedRepresentative(BaseModel):
    previous_appointed_representatives: List[FirmAppointedRepresentativeDetail] = Field(default_factory=list, alias="PreviousAppointedRepresentatives")
    current_appointed_representatives: List[FirmAppointedRepresentativeDetail] = Field(default_factory=list, alias="CurrentAppointedRepresentatives")

class FirmDisciplinaryHistory(BaseModel):
    typeof_description: str = Field(..., alias="TypeofDescription")
    typeof_action: str = Field(..., alias="TypeofAction")
    enforcement_type: str = Field(..., alias="EnforcementType")
    action_effective_from: str = Field(..., alias="ActionEffectiveFrom")

class FirmExclusion(BaseModel):
    psd2_exclusion_type: str = Field(..., alias="PSD2_Exclusion_Type")
    particular_exclusion_relied_upon: str = Field(..., alias="Particular_Exclusion_relied_upon")
    description_of_services: str = Field(..., alias="Description_of_services")

class FirmWaiver(BaseModel):
    #convert waivers_discretions property to 'Null' if it is None

    waivers_discretions: Optional[str] = Field(..., alias="Waivers_Discretions")
    rule_article_no: List[str] = Field(default_factory=list, alias="Rule_ArticleNo")

class FirmPermissionDetail(BaseModel):
    name: str = Field(..., alias="Name")
    investment_types: List[str] = Field(default_factory=list, alias="InvestmentTypes")

class FirmPassportPermission(BaseModel):
    permissions: List[FirmPermissionDetail] = Field(default_factory=list, alias="Permissions")
    passport_type: str = Field(..., alias="PassportType")
    passport_direction: str = Field(..., alias="PassportDirection")
    directive: str = Field(..., alias="Directive")
    country: str = Field(..., alias="Country")

class FirmPassportDetail(BaseModel):
    passport_direction: str = Field(..., alias="PassportDirection")
    country: str = Field(..., alias="Country")

class FirmPassport(BaseModel):
    passports: List[FirmPassportDetail] = Field(default_factory=list, alias="Passports")

class FirmRegulator(BaseModel):
    termination_date: Optional[str] = Field(None, alias="Termination Date")
    effective_date: str = Field(..., alias="Effective Date")
    regulator_name: str = Field(..., alias="Regulator Name")

class FirmInvestmentType(BaseModel):
    investment_type_name: str = Field(..., alias="Investment Type Name")

class FirmRequirement(BaseModel):
    effective_date: Optional[str] = Field(None, alias="Effective Date")
    derivatives_as_incidental_services_only: Optional[str] = Field('Null', alias="Derivatives as incidental services only.")
    requirement_reference: Optional[str] = Field(None, alias="Requirement Reference")
    financial_promotions_requirement: Optional[bool] = Field(None, alias="Financial Promotions Requirement")
    financial_promotions_investment_types: Optional[str] = Field('Null', alias="Financial Promotions Investment Types")

class FirmActivityDetail(BaseModel):
    participation: Optional[str] = Field(None, alias="participation")
    participation_option: Optional[List[str]] = Field(default_factory=list, alias="participation_option")

class FirmActivitiesAndPermissions(BaseModel):
    activity_name: Optional[str] = Field(None, alias="activity_name")
    participation: Optional[List[FirmActivityDetail]] = Field(default_factory=list, alias="participation")

class FirmControlledFunctionDetail(BaseModel):
    suspension_restriction_end_date: Optional[str] = Field(None, alias="Suspension / Restriction End Date")
    suspension_restriction_start_date: Optional[str] = Field(None, alias="Suspension / Restriction Start Date")
    restriction: Optional[str] = Field(None, alias="Restriction")
    effective_date: Optional[str] = Field(None, alias="Effective Date")
    individual_name: Optional[str] = Field(None, alias="Individual Name")
    name: Optional[str] = Field(None, alias="Name")
    url: Optional[str] = Field(None, alias="URL")
    end_date: Optional[str] = Field(None, alias="End Date")

class FirmControlledFunction(BaseModel):
    current: Optional[Dict[str, FirmControlledFunctionDetail]] = Field(default_factory=dict, alias="Current")
    previous: Optional[Dict[str, FirmControlledFunctionDetail]] = Field(default_factory=dict, alias="Previous")

class FirmAddress(BaseModel):
    website_address: Optional[str] = Field(None, alias="Website Address")
    phone_number: Optional[str] = Field(None, alias="Phone Number")
    country: Optional[str] = Field(None, alias="Country")
    postcode: Optional[str] = Field(None, alias="Postcode")
    county: Optional[str] = Field(None, alias="County")
    town: Optional[str] = Field(None, alias="Town")
    address_line_4: Optional[str] = Field(None, alias="Address Line 4")
    address_line_3: Optional[str] = Field(None, alias="Address Line 3")
    address_line_2: Optional[str] = Field(None, alias="Address Line 2")
    address_line_1: Optional[str] = Field(None, alias="Address Line 1")
    address_type: Optional[str] = Field(None, alias="Address Type")

class FirmNameDetail(BaseModel):
    effective_from: Optional[str] = Field(None, alias="Effective From")
    effective_to: Optional[str] = Field(None, alias="Effective To")
    name_status: Optional[str] = Field(None, alias="Status")
    firm_name: Optional[str] = Field(None, alias="Name")

class FirmNames(BaseModel):
    current_names: Optional[List[FirmNameDetail]] = Field(default_factory=list, alias="Current Names")
    previous_names: Optional[List[FirmNameDetail]] = Field(default_factory=list, alias="Previous Names")

class FirmExceptionalInfoDetail(BaseModel):
    exceptional_info_title: str = Field(..., alias="Exceptional Info Title")
    exceptional_info_body: str = Field(..., alias="Exceptional Info Body")

class FirmData(BaseModel):
    exceptional_info_details: Optional[List[FirmExceptionalInfoDetail]] = Field(default_factory=list, alias="Exceptional Info Details")
    status_effective_date: Optional[str] = Field(None, alias="Status Effective Date")
    e_money_agent_status: Optional[str] = Field(None, alias="E-Money Agent Status")
    psd_emd_effective_date: Optional[str] = Field(None, alias="PSD / EMD Effective Date")
    client_money_permission: Optional[str] = Field(None, alias="Client Money Permission")
    sub_status_effective_from: Optional[str] = Field(None, alias="Sub Status Effective from")
    sub_status: Optional[str] = Field(None, alias="Sub-Status")
    mutual_society_number: Optional[str] = Field(None, alias="Mutual Society Number")
    companies_house_number: Optional[str] = Field(None, alias="Companies House Number")
    mlrs_status_effective_date: Optional[str] = Field(None, alias="MLRs Status Effective Date")
    mlrs_status: Optional[str] = Field(None, alias="MLRs Status")
    e_money_agent_effective_date: Optional[str] = Field(None, alias="E-Money Agent Effective Date")
    psd_agent_effective_date: Optional[str] = Field(None, alias="PSD Agent Effective date")
    psd_agent_status: Optional[str] = Field(None, alias="PSD Agent Status")
    psd_emd_status: Optional[str] = Field(None, alias="PSD / EMD Status")
    status: Optional[str] = Field(None, alias="Status")
    business_type: Optional[str] = Field(None, alias="Business Type")
    organisation_name: Optional[str] = Field(None, alias="Organisation Name")
    frn: int = Field(alias="FRN")

class FirmQuery(BaseModel):
    #convert frn from string to integer
    reference: Optional[str] = Field(..., alias="Reference Number")
    status: Optional[str] = Field(..., alias="Status")
    type_of_business_or_individual: Optional[str] = Field(..., alias="Type of business or Individual")
    name: Optional[str] = Field(..., alias="Name")

class IndividualDetails(BaseModel):
    irn: Optional[str] = Field(..., alias="IRN")
    full_name: Optional[str] = Field(..., alias="Full Name")
    commonly_used_name: Optional[str] = Field(..., alias="Commonly Used Name")
    individual_status: Optional[str] = Field(..., alias="Status")
    disciplinary_history: Optional[str] = Field(None, alias="Disciplinary History")
    current_roles_activities: Optional[str] = Field(None, alias="Current roles & activities")

class IndividualData(BaseModel):
    #convert irn from string to integer
    individual_data: Optional[IndividualDetails] = Field(..., alias="Details")

class IndividualControlFunctionDetail(BaseModel):
    customer_engagement_method: Optional[str] = Field(None, alias="Customer Engagement Method")
    end_date: Optional[str] = Field(None, alias="End Date")
    suspension_restriction_end_date: Optional[str] = Field(None, alias="Suspension / Restriction End Date")
    suspension_restriction_start_date: Optional[str] = Field(None, alias="Suspension / Restriction Start Date")
    restriction: Optional[str] = Field(None, alias="Restriction")
    effective_date: Optional[str] = Field(None, alias="Effective Date")
    firm_name: Optional[str] = Field(None, alias="Firm Name")
    role_name: Optional[str] = Field(None, alias="Name")

class IndividualControlFunction(BaseModel):
    current: Optional[Dict[str, IndividualControlFunctionDetail]] = Field(default_factory=dict, alias="Current")
    previous: Optional[Dict[str, IndividualControlFunctionDetail]] = Field(default_factory=dict, alias="Previous")

class IndividualDisciplinaryHistoryDetail(BaseModel):
    typeof_description: str = Field(..., alias="TypeofDescription")
    typeof_action: str = Field(..., alias="TypeofAction")
    enforcement_type: str = Field(..., alias="EnforcementType")
    action_effective_from: str = Field(..., alias="ActionEffectiveFrom")

class IndividualDisciplinaryHistory(BaseModel):
    typeof_description: str = Field(..., alias="TypeofDescription")
    typeof_action: str = Field(..., alias="TypeofAction")
    enforcement_type: str = Field(..., alias="EnforcementType")
    action_effective_from: str = Field(..., alias="ActionEffectiveFrom")   

class ResultInfo(BaseModel):
    next: Optional[str] = Field(None, alias="Next")
    page: str = Field(..., alias="page")
    per_page: str = Field(..., alias="per_page")
    total_count: str = Field(..., alias="total_count")

class ApiResponse(BaseModel):
    status: str = Field(..., alias="Status")
    result_info: Optional[ResultInfo] = Field(..., alias="ResultInfo")
    message: str = Field(..., alias="Message")
