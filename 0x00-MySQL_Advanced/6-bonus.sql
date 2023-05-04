-- creates a stored procedure AddBonus that 
-- adds a new correction for a student

DELIMITER |
CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(256), IN score INT)
BEGIN
    IF project_name NOT IN (SELECT name FROM projects) THEN 
        INSERT INTO projects (name) VALUES (project_name);
    END IF;

    INSERT INTO corrections (user_id, project_id, score) 
        VALUES (user_id,
            (SELECT id FROM projects WHERE name = project_name),
            score);
END; |

DELIMITER ;
