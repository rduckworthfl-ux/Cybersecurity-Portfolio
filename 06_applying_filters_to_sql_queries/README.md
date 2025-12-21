# SQL Data Filtering for Security Analysis

## Project Description

In this project, I acted as a security analyst for an organization requiring specific data extraction to investigate potential security issues and audit employee system access. The objective was to utilize Structured Query Language (SQL) filters to isolate relevant information from a MariaDB database.

This exercise simulates real-world SOC tasks, such as identifying suspicious login activity, auditing user accounts based on department, and investigating access anomalies based on geolocation.

## Scenario & Strategy

The organization required data on two fronts: **Security Incident Investigation** (analyzing login attempts) and **System Administration** (auditing employee records). To achieve this, I applied various SQL filters (`WHERE`, `AND`, `OR`, `NOT`) to precise datasets.

The scope of the investigation included:

1. Identifying failed login attempts occurring after business hours.
2. Isolating login activity on specific dates associated with a security event.
3. Filtering login attempts originating from outside specific authorized regions (Mexico).
4. Auditing employee records for specific departments (Marketing, Finance, Sales) to verify access privileges.

## Technical Walkthrough

### 1. Investigating After-Hours Failed Logins

**Objective:** Detect potential unauthorized access attempts occurring outside of standard business hours.
**Logic:** I queried the `log_in_attempts` table. The criteria for "after-hours" was defined as any time after 18:00 (6:00 PM). I also filtered for failed attempts (`success = 0`) to focus on potential brute-force or unauthorized access anomalies.

```sql
SELECT * FROM log_in_attempts
WHERE login_time > '18:00:00' AND success = 0;

```

### 2. Time-Window Analysis (Specific Dates)

**Objective:** Isolate traffic during a specific 48-hour window to correlate with a known security alert.
**Logic:** I needed to broaden the search to include all login attempts (successful or failed) on two specific dates: May 8th and May 9th, 2022. I used the `OR` operator to ensure records from either date were retrieved.

```sql
SELECT * FROM log_in_attempts
WHERE login_date = '2022-05-09' OR login_date = '2022-05-08';

```

### 3. Geolocation Filtering

**Objective:** Identify login attempts originating from outside the organization's primary operational region.
**Logic:** The organization expects traffic from Mexico. I used the `NOT` operator combined with `LIKE` to exclude any log entries where the country was "MEX" or "MEXICO". This query isolates "anomalous" traffic sources.

```sql
SELECT * FROM log_in_attempts
WHERE NOT country LIKE 'MEX%';

```

### 4. Departmental Access Audits

**Objective:** Retrieve employee records for specific departments to validate Role-Based Access Control (RBAC) policies.
**Logic:**

- **Marketing:** Simple equality filter.
- **Finance or Sales:** Used `OR` to group these high-value targets.
- **Non-IT Personnel:** Used `NOT` to exclude the Information Technology team, useful for identifying users who may need different patch schedules or security training.

```sql
-- Marketing Audit
SELECT * FROM employees WHERE department = 'Marketing';

-- Finance & Sales Audit
SELECT * FROM employees WHERE department = 'Finance' OR department = 'Sales';

-- Non-IT Audit
SELECT * FROM employees WHERE NOT department = 'Information Technology';

```

## Summary

This project demonstrates the critical role of SQL in cybersecurity. By mastering filtering commands (`AND`, `OR`, `NOT`, `LIKE`), a security analyst can effectively sift through massive datasets to find indicators of compromise (IOCs), validate user permissions, and support incident response investigations.
