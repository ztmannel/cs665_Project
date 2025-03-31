
INSERT INTO employee_personal_info (first_name, last_name, position, phone, address, city, state, country, personal_email, employee_id) VALUES
('Jason', 'Jones', 'CEO', '555-555-5000', '8762 E Kansas St', 'Wichita', 'KS', 'USA', 'moneyspender@email.com', '3052'),
('Jim', 'Dean', 'Manager', '555-555-5001', '3750 N Main', 'Wichita', 'KS', 'USA', 'partyboy76@email.com', '1125'),
('Francis', 'Penn', 'Senior Analyst', '555-555-5002', '1168 E Thompson St', 'Wichita', 'KS', 'USA', 'write4fun@email.com', '7590'),
('John', 'Little', 'Analyst', '555-555-5003', '506 S Atlanta Ave', 'Wichita', 'KS', 'USA', 'loudmusiclover07@email.com', '3690'),
('Georgia', 'Robins', 'Developer', '555-555-5004', '735 W Hickory', 'Wichita', 'KS', 'USA', 'grobins@email.com', '9358');

INSERT INTO badge_info (activation_date, deactivation_date, employee_id, badge_id) VALUES
('05032025', 'NULL', '3052', '1'),
('05032025', 'NULL', '1125', '2'),
('10032025', 'NULL', '7590', '3'),
('27032025', 'NULL', '3690', '4'),
('05032025', 'NULL', '9358', '5');

INSERT INTO compensation_table (salary, bonus, salary_set_date, employee_id) VALUES
('120000', '6000', '10032025', '3052'),
('85000', '5000', '10032025', '1125'),
('85000', '3000', '15032025', '7590'),
('70000', '5000', '27032025', '3690'),
('80000', '5000', '10032025', '9358');

INSERT INTO badge_sign_in_times (date_scanned, time_scanned, badge_id) VALUES
('10032025', '0800', '3052'),
('10032025', '0755', '1125'),
('15032025', '0750', '7590'),
('15032025', '0750', '7590'),
('27032025', '0900', '3690');

INSERT INTO employee_company_info (company_email, department, manager_emp_id, hire_date, termination_date, employee_id) VALUES
('j.jones@company.com', 'CEO', 'NULL', '05032025', 'NULL', '3052'),
('j.dean@company.com', 'Software', '3052', '05032025', 'NULL', '1125'),
('f.penn@company.com', 'Software', '1125', '10032025', 'NULL', '7590'),
('j.little@company.com', 'Software', '1125', '27032025', 'NULL', '3690'),
('g.robins@company.com', 'Development', '1125', '05032025', 'NULL', '9358');

INSERT INTO employee_time_off (hours_remaining, hours_consumed, total_annual_hours, employee_id) VALUES
('104', '16', '120', '3052'),
('96', '16', '112', '1125'),
('64', '16', '80', '7590'),
('72', '8', '80', '3690'),
('80', '0', '80', '9358');