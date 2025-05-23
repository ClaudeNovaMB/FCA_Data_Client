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
