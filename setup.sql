CREATE TABLE devices (
    id serial PRIMARY KEY,
    hostname text,
    location text
);

CREATE TABLE moisture_logs (
    id serial PRIMARY KEY,
    datetime timestamp without time zone,
    moisture_data jsonb
);

CREATE TABLE plant_types (
    id serial PRIMARY KEY,
    scientific_name text
);

CREATE TABLE plants (
    id serial PRIMARY KEY,
    name text,
    scientific_name integer REFERENCES plant_types(id)
);

CREATE TABLE plant_device_registration (
    id serial PRIMARY KEY,
    plant_id integer NOT NULL REFERENCES plants(id),
    device_id integer NOT NULL REFERENCES devices(id),
    registered_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    unregistered_at timestamp without time zone,
    is_active boolean DEFAULT true
);
