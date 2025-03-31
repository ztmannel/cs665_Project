/* 
employee_personal_info(first_name, last_name, position, phone, address, city, state, country, employee_id(PK), personal_email);
badge_info(badge id(FK), employee_id (PK),deactivation_date,activation_date);
compensation_table (employee_id (PK), salary, bonus, timestamp);
badge_sign_in_times (badge id(PK), date scanned, time scanned);
employee_company_info(employee_id (PK), company email, department, manager_emp_id, hire date, termination date);
employee_time_off (employee_id (PK), hours remaining, hours taken, total annual hours); 
*/

CREATE TABLE IF NOT EXISTS employee_personal_info(
    first_name  TEXT    NOT NULL, 
    last_name  TEXT     NOT NULL,
    position  TEXT      NOT NULL,
    phone   INTEGER CHECK (phone GLOB '???-???-????')   NOT NULL,
    address TEXT        NOT NULL,
    city    TEXT        NOT NULL,
    state   TEXT        NOT NULL,
    country TEXT        NOT NULL,
    personal_email  TEXT    NOT NULL,
    PRIMARY KEY (employee_id) REFERENCES (badge_info, compensation_table, employee_company_info, employee_time_off)(employee_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS badge_info(
    activation_date     INTEGER NOT NULL,
    deactivation_date   INTEGER NOT NULL,
    FOREIGN KEY(employee_id),
    PRIMARY KEY(badge_id) REFERENCES (badge_sign_in_times)(badge_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS compensation_table(
    salary              INTEGER NOT NULL,
    bonus               INTEGER NOT NULL,
    salary_set_date     INTEGER, NOT NULL,
    FOREIGN KEY(employee_id)

);

/*make ref to the badge info table*/
CREATE TABLE IF NOT EXISTS badge_sign_in_times(
    date_scanned    INTEGER,
    time_scanned    INTEGER,
    FOREIGN KEY (badge id)
);

CREATE TABLE IF NOT EXISTS employee_company_info(
    company_email       TEXT    NOT NULL,
    department          TEXT    NOT NULL,
    manager_emp_id      INTEGER NOT NULL,
    hire_date           INTEGER NOT NULL,
    termination_date    INTEGER,
    FOREIGN KEY (employee_id)
);

CREATE TABLE IF NOT EXISTS employee_time_off(
    hours_remaining     INTEGER,
    hours_consumed      INTEGER,
    total_annual_hours  INTEGER,
    FOREIGN KEY(employee_id)
);