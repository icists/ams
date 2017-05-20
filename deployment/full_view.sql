USE application_icists;
CREATE OR REPLACE VIEW `full_view` AS 
	SELECT
		au.id id,
        au.first_name,
        au.last_name,
        au.email,
        a.id app_id,
        p.id part_id,
        a.application_category,
        up.nationality,
        up.gender,
        a.project_topic_id,
        p.project_team_no,
        p.accommodation_id,
        p.breakfast_option,
        p.payment_option,
        p.required_payment_krw,
        p.required_payment_usd

    FROM registration_participant p
		INNER JOIN registration_application a ON a.id = p.application_id
        INNER JOIN session_userprofile up ON a.user_id = up.user_id
        INNER JOIN auth_user au ON au.id = up.user_id
;