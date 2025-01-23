-- File: config/postgres/init-users.sql
-- Create roles table
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INTEGER REFERENCES roles(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create permissions table
CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    role_id INTEGER REFERENCES roles(id),
    resource VARCHAR(100) NOT NULL,
    access_level VARCHAR(50) NOT NULL
);

-- Insert default roles
INSERT INTO roles (name, description) VALUES 
('admin', 'Full system access'),
('user', 'Standard user access');

-- Insert sample permissions
INSERT INTO permissions (role_id, resource, access_level)
SELECT id, 
       CASE 
           WHEN name = 'admin' THEN 'all_resources'
           ELSE 'limited_resources'
       END,
       CASE 
           WHEN name = 'admin' THEN 'full_access'
           ELSE 'read_only'
       END
FROM roles;
