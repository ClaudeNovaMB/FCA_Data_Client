CREATE SCHEMA IF NOT EXISTS fcadata;

CREATE TABLE IF NOT EXISTS fcadata.individual_data (
    frn INTEGER NOT NULL REFERENCES fcadata.firms(frn),
    irn VARCHAR PRIMARY KEY UNIQUE,
    full_name VARCHAR,
    commonly_used_name VARCHAR,
    individual_status VARCHAR,
    UNIQUE (frn, full_name, commonly_used_name, individual_status, status)
);

CREATE TABLE IF NOT EXISTS fcadata.individual_control_function (
    id SERIAL PRIMARY KEY,
    irn VARCHAR NOT NULL REFERENCES fcadata.individual_data(irn),
    firm_name VARCHAR,
    control_status VARCHAR,
    effective_date VARCHAR,
    end_date VARCHAR,
    customer_engagement_method VARCHAR,
    suspension_restriction_end_date VARCHAR,
    suspension_restriction_start_date VARCHAR,
    restriction VARCHAR,
    UNIQUE (irn, person_name, firm_name, effective_date, end_date, customer_engagement_method, suspension_restriction_end_date, suspension_restriction_start_date, restriction)
);

CREATE TABLE IF NOT EXISTS fcadata.individual_disciplinary_history (
    id SERIAL PRIMARY KEY,
    irn VARCHAR NOT NULL REFERENCES fcadata.individual_data(irn),
    action_effective_from VARCHAR,
    enforcement_type VARCHAR,
    typeof_action VARCHAR,
    typeof_description VARCHAR,
    UNIQUE (irn, action_effective_from, enforcement_type, typeof_action, typeof_description)
);

CREATE TABLE IF NOT EXISTS fcadata.firms
(
    frn integer NOT NULL DEFAULT nextval('fcadata.firms_frn_seq'::regclass),
    organisation_name character varying COLLATE pg_catalog."default" NOT NULL,
    companies_house_number character varying COLLATE pg_catalog."default",
    business_type character varying COLLATE pg_catalog."default",
    mutual_society_number character varying COLLATE pg_catalog."default",
    firm_status character varying COLLATE pg_catalog."default",
    status_effective_date character varying COLLATE pg_catalog."default",
    sub_status character varying COLLATE pg_catalog."default",
    sub_status_effective_from character varying COLLATE pg_catalog."default",
    e_money_agent_status character varying COLLATE pg_catalog."default",
    e_money_agent_effective_date character varying COLLATE pg_catalog."default",
    mlrs_status character varying COLLATE pg_catalog."default",
    mlrs_status_effective_date character varying COLLATE pg_catalog."default",
    psd_agent_status character varying COLLATE pg_catalog."default",
    psd_agent_effective_date character varying COLLATE pg_catalog."default",
    psd_emd_status character varying COLLATE pg_catalog."default",
    psd_emd_effective_date character varying COLLATE pg_catalog."default",
    exceptional_info character varying COLLATE pg_catalog."default",
    client_money_permission character varying COLLATE pg_catalog."default",
    CONSTRAINT firms_pkey PRIMARY KEY (frn)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS fcadata.firms
    OWNER to admin_user;

CREATE TABLE IF NOT EXISTS fcadata.firm_activities_and_permissions
(
    id integer NOT NULL DEFAULT nextval('fcadata.firm_activities_and_permissions_id_seq'::regclass),
    firm_frn integer NOT NULL,
    activity_name character varying COLLATE pg_catalog."default" NOT NULL,
    participation character varying COLLATE pg_catalog."default" NOT NULL,
    participation_option character varying COLLATE pg_catalog."default",
    CONSTRAINT firm_activities_and_permissions_pkey PRIMARY KEY (id),
    CONSTRAINT unique_activities_and_permissions UNIQUE (firm_frn, activity_name, participation, participation_option),
    CONSTRAINT firm_activities_and_permissions_firm_frn_fkey FOREIGN KEY (firm_frn)
        REFERENCES fcadata.firms (frn) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS fcadata.firm_activities_and_permissions
    OWNER to admin_user;

CREATE TABLE IF NOT EXISTS fcadata.firm_addresses
(
    id integer NOT NULL DEFAULT nextval('fcadata.firm_addresses_id_seq'::regclass),
    firm_frn integer NOT NULL,
    address_type character varying COLLATE pg_catalog."default",
    address_line_1 character varying COLLATE pg_catalog."default",
    address_line_2 character varying COLLATE pg_catalog."default",
    address_line_3 character varying COLLATE pg_catalog."default",
    address_line_4 character varying COLLATE pg_catalog."default",
    town character varying COLLATE pg_catalog."default",
    county character varying COLLATE pg_catalog."default",
    postcode character varying COLLATE pg_catalog."default",
    country character varying COLLATE pg_catalog."default",
    phone_number character varying COLLATE pg_catalog."default",
    website_address character varying COLLATE pg_catalog."default",
    CONSTRAINT firm_addresses_pkey PRIMARY KEY (id),
    CONSTRAINT unique_addresses UNIQUE (firm_frn, address_type, address_line_1, address_line_2, address_line_3, address_line_4, town, county, postcode, country, phone_number, website_address),
    CONSTRAINT firm_addresses_firm_frn_fkey FOREIGN KEY (firm_frn)
        REFERENCES fcadata.firms (frn) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS fcadata.firm_addresses
    OWNER to admin_user;

CREATE TABLE IF NOT EXISTS fcadata.firm_appointed_representatives
(
    id integer NOT NULL DEFAULT nextval('fcadata.firm_appointed_representatives_id_seq'::regclass),
    previous_appointed_representatives character varying COLLATE pg_catalog."default",
    current_appointed_representatives character varying COLLATE pg_catalog."default",
    firm_frn integer NOT NULL,
    CONSTRAINT firm_appointed_representatives_pkey PRIMARY KEY (id),
    CONSTRAINT unique_far UNIQUE (firm_frn, current_appointed_representatives, previous_appointed_representatives),
    CONSTRAINT firm_appointed_representatives_firm_frn_fkey FOREIGN KEY (firm_frn)
        REFERENCES fcadata.firms (frn) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS fcadata.firm_appointed_representatives
    OWNER to admin_user;

CREATE TABLE IF NOT EXISTS fcadata.firm_controlled_functions
(
    id integer NOT NULL DEFAULT nextval('fcadata.firm_controlled_functions_id_seq'::regclass),
    firm_frn integer NOT NULL,
    control_status character varying(50) COLLATE pg_catalog."default" NOT NULL,
    individual_name character varying(255) COLLATE pg_catalog."default",
    controller_name character varying(255) COLLATE pg_catalog."default",
    url character varying(255) COLLATE pg_catalog."default",
    effective_date character varying(50) COLLATE pg_catalog."default",
    end_date character varying(50) COLLATE pg_catalog."default",
    suspension_restriction_start_date character varying(50) COLLATE pg_catalog."default",
    suspension_restriction_end_date character varying(50) COLLATE pg_catalog."default",
    restriction character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT firm_controlled_functions_pkey PRIMARY KEY (id),
    CONSTRAINT unique_controlled_function UNIQUE (firm_frn, control_status, individual_name, controller_name),
    CONSTRAINT firm_controlled_functions_firm_frn_fkey FOREIGN KEY (firm_frn)
        REFERENCES fcadata.firms (frn) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS fcadata.firm_controlled_functions
    OWNER to admin_user;

CREATE TABLE IF NOT EXISTS fcadata.firm_disciplinary_histories
(
    id integer NOT NULL DEFAULT nextval('fcadata.firm_disciplinary_histories_id_seq'::regclass),
    firm_frn integer NOT NULL,
    action_effective_from character varying COLLATE pg_catalog."default" NOT NULL,
    enforcement_type character varying COLLATE pg_catalog."default" NOT NULL,
    typeof_action character varying COLLATE pg_catalog."default" NOT NULL,
    typeof_description character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT firm_disciplinary_histories_pkey PRIMARY KEY (id),
    CONSTRAINT unique_fdh UNIQUE (firm_frn, typeof_description, typeof_action, enforcement_type, action_effective_from),
    CONSTRAINT firm_disciplinary_histories_firm_frn_fkey FOREIGN KEY (firm_frn)
        REFERENCES fcadata.firms (frn) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS fcadata.firm_disciplinary_histories
    OWNER to admin_user;

CREATE TABLE IF NOT EXISTS fcadata.firm_exclusions
(
    id integer NOT NULL DEFAULT nextval('fcadata.firm_exclusions_id_seq'::regclass),
    firm_frn integer NOT NULL,
    psd2_exclusion_type character varying COLLATE pg_catalog."default" NOT NULL,
    particular_exclusion_relied_upon character varying COLLATE pg_catalog."default" NOT NULL,
    description_of_services character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT firm_exclusions_pkey PRIMARY KEY (id),
    CONSTRAINT unique_fe UNIQUE (firm_frn, description_of_services, particular_exclusion_relied_upon, psd2_exclusion_type),
    CONSTRAINT firm_exclusions_firm_frn_fkey FOREIGN KEY (firm_frn)
        REFERENCES fcadata.firms (frn) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS fcadata.firm_exclusions
    OWNER to admin_user;

CREATE TABLE IF NOT EXISTS fcadata.firm_investment_types
(
    id integer NOT NULL DEFAULT nextval('fcadata.firm_investment_types_id_seq'::regclass),
    firm_frn integer NOT NULL,
    investment_type_name character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT firm_investment_types_pkey PRIMARY KEY (id),
    CONSTRAINT unique_fit UNIQUE (firm_frn, investment_type_name),
    CONSTRAINT firm_investment_types_firm_frn_fkey FOREIGN KEY (firm_frn)
        REFERENCES fcadata.firms (frn) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS fcadata.firm_investment_types
    OWNER to admin_user;

CREATE TABLE IF NOT EXISTS fcadata.firm_names
(
    id integer NOT NULL DEFAULT nextval('fcadata.firm_names_id_seq'::regclass),
    firm_frn integer NOT NULL,
    firm_name character varying COLLATE pg_catalog."default" NOT NULL,
    name_status character varying COLLATE pg_catalog."default",
    effective_from character varying COLLATE pg_catalog."default",
    effective_to character varying COLLATE pg_catalog."default",
    CONSTRAINT firm_names_pkey PRIMARY KEY (id),
    CONSTRAINT unique_fn UNIQUE (firm_frn, firm_name, name_status, effective_from, effective_to),
    CONSTRAINT firm_names_firm_frn_fkey FOREIGN KEY (firm_frn)
        REFERENCES fcadata.firms (frn) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS fcadata.firm_names
    OWNER to admin_user;
CREATE TABLE IF NOT EXISTS fcadata.firm_passports
(
    id integer NOT NULL DEFAULT nextval('fcadata.firm_passports_id_seq'::regclass),
    firm_frn integer NOT NULL,
    firm_name character varying COLLATE pg_catalog."default" NOT NULL,
	country character varying COLLATE pg_catalog."default" NOT NULL,
	directive character varying COLLATE pg_catalog."default" NOT NULL,
	investment_type character varying COLLATE pg_catalog."default" NOT NULL,
	passport_type character varying COLLATE pg_catalog."default" NOT NULL,
	passport_direction character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT firm_passports_pkey PRIMARY KEY (id),
    CONSTRAINT unique_fp UNIQUE (firm_frn, firm_name, country, investment_type, directive, passport_direction, passport_type),
    CONSTRAINT firm_passports_firm_frn_fkey FOREIGN KEY (firm_frn)
        REFERENCES fcadata.firms (frn) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS fcadata.firm_passports
    OWNER to admin_user;

CREATE TABLE IF NOT EXISTS fcadata.firm_regulators
(
    id integer NOT NULL DEFAULT nextval('fcadata.firm_regulators_id_seq'::regclass),
    firm_frn integer NOT NULL,
    regulator_name character varying COLLATE pg_catalog."default" NOT NULL,
    effective_date character varying COLLATE pg_catalog."default" NOT NULL,
    termination_date character varying COLLATE pg_catalog."default",
    CONSTRAINT firm_regulators_pkey PRIMARY KEY (id),
    CONSTRAINT unique_firm_regulators UNIQUE (firm_frn, termination_date, effective_date, regulator_name),
    CONSTRAINT firm_regulators_firm_frn_fkey FOREIGN KEY (firm_frn)
        REFERENCES fcadata.firms (frn) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS fcadata.firm_regulators
    OWNER to admin_user;

CREATE TABLE IF NOT EXISTS fcadata.firm_requirements
(
    id integer NOT NULL DEFAULT nextval('fcadata.firm_requirements_id_seq'::regclass),
    firm_frn integer NOT NULL,
    effective_date character varying COLLATE pg_catalog."default",
    derivatives_as_incidental_services_only character varying COLLATE pg_catalog."default",
    requirement_reference character varying COLLATE pg_catalog."default",
    financial_promotions_requirement character varying COLLATE pg_catalog."default",
    financial_promotions_investment_types character varying COLLATE pg_catalog."default",
    CONSTRAINT firm_requirements_pkey PRIMARY KEY (id),
    CONSTRAINT unique_firm_requirements UNIQUE (firm_frn, effective_date, derivatives_as_incidental_services_only, requirement_reference, financial_promotions_requirement, financial_promotions_investment_types),
    CONSTRAINT firm_requirements_firm_frn_fkey FOREIGN KEY (firm_frn)
        REFERENCES fcadata.firms (frn) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS fcadata.firm_requirements
    OWNER to admin_user;

CREATE TABLE IF NOT EXISTS fcadata.firm_waivers
(
    id integer NOT NULL DEFAULT nextval('fcadata.firm_waivers_id_seq'::regclass),
    firm_frn integer NOT NULL,
    rule_article_no character varying COLLATE pg_catalog."default",
    waivers_discretions character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT firm_waivers_pkey PRIMARY KEY (id),
    CONSTRAINT unique_fw UNIQUE (firm_frn, waivers_discretions_url, waivers_discretions, rule_article_no),
    CONSTRAINT firm_waivers_firm_frn_fkey FOREIGN KEY (firm_frn)
        REFERENCES fcadata.firms (frn) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS fcadata.firm_waivers
    OWNER to admin_user;

-- Updated log table definitions to leverage TimescaleDB hypertable optimization
CREATE TABLE IF NOT EXISTS fcadata.client_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    log_level VARCHAR NOT NULL,
    log_message VARCHAR NOT NULL
);

SELECT create_hypertable('fcadata.client_logs', 'timestamp');

CREATE TABLE IF NOT EXISTS fcadata.crud_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    log_level VARCHAR NOT NULL,
    log_message VARCHAR NOT NULL
);

SELECT create_hypertable('fcadata.crud_logs', 'timestamp');

