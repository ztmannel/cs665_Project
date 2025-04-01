CREATE TABLE IF NOT EXISTS employee_personal_info(
    employee_id     INTEGER,
    first_name      TEXT            NOT NULL, 
    last_name       TEXT            NOT NULL,
    position        TEXT            NOT NULL,
    phone           INTEGER         CHECK (phone GLOB '???-???-????')   NOT NULL,
    address         TEXT            NOT NULL,
    city            TEXT            NOT NULL,
    state           TEXT            NOT NULL,
    country         TEXT            NOT NULL,
    personal_email  TEXT    UNIQUE  NOT NULL,
    PRIMARY KEY (employee_id) --REFERENCES badge_info, compensation_table, employee_company_info, employee_time_off(employee_id) ON DELETE CASCADE
);

--date is in DDMMYYYY format; employee_id relates to the employee_personal_info.employee_id (functional dependency)
CREATE TABLE IF NOT EXISTS badge_info(
    badge_id            INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    employee_id         INTEGER NOT NULL,
    activation_date     INTEGER NOT NULL,
    deactivation_date   INTEGER NOT NULL,
    FOREIGN KEY(employee_id) REFERENCES employee_personal_info(employee_id)
);

--employee_id relates to the employee_personal_info.employee_id
CREATE TABLE IF NOT EXISTS compensation_table(
    employee_id			INTEGER	NOT NULL,
	salary              INTEGER NOT NULL,
    bonus               INTEGER NOT NULL,
    salary_set_date     INTEGER NOT NULL,
    FOREIGN KEY(employee_id) REFERENCES employee_personal_info(employee_id)
);

/*Date is in DDMMYYYY. time is in HHmm format. badge_id relates to the badge_info.badge_id*/
CREATE TABLE IF NOT EXISTS badge_sign_in_times(
    badge_id		INTEGER	NOT NULL,
	date_scanned    INTEGER,
    time_scanned    INTEGER,
    FOREIGN KEY (badge_id) REFERENCES badge_info(badge_id)
);

--employee_id relates to the employee_personal_info.employee_id
CREATE TABLE IF NOT EXISTS employee_company_info(
    employee_id			INTEGER	        NOT NULL,
	company_email       TEXT    UNIQUE  NOT NULL,
    department          TEXT            NOT NULL,
    manager_emp_id      INTEGER         NOT NULL,
    hire_date           INTEGER         NOT NULL,
    termination_date    INTEGER,
    FOREIGN KEY (employee_id) REFERENCES employee_personal_info(employee_id)
);

--employee_id relates to the employee_personal_info.employee_id
CREATE TABLE IF NOT EXISTS employee_time_off(
    employee_id			INTEGER	NOT NULL,
	hours_remaining     INTEGER,
    hours_consumed      INTEGER,
    total_annual_hours  INTEGER,
    FOREIGN KEY(employee_id) REFERENCES employee_personal_info(employee_id)
);