--
-- PostgreSQL database dump
--

\restrict aDTute0CREwoF6kSfaUMpIeCBuNFczealbtzg7LeK4O4hfNfo9advnENzMHDk38

-- Dumped from database version 18beta3
-- Dumped by pg_dump version 18beta3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: event_type; Type: TYPE; Schema: public; Owner: avnadmin
--

CREATE TYPE public.event_type AS ENUM (
    'watering',
    'repot',
    'environment change',
    'cuttings'
);


ALTER TYPE public.event_type OWNER TO avnadmin;

--
-- Name: health_check; Type: TYPE; Schema: public; Owner: avnadmin
--

CREATE TYPE public.health_check AS ENUM (
    'dead',
    'worsening',
    'bad',
    'improving',
    'healthy',
    'thriving'
);


ALTER TYPE public.health_check OWNER TO avnadmin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: events; Type: TABLE; Schema: public; Owner: avnadmin
--

CREATE TABLE public.events (
    id integer NOT NULL,
    datetime timestamp without time zone DEFAULT now(),
    event_type public.event_type,
    comments text,
    plant_id integer
);


ALTER TABLE public.events OWNER TO avnadmin;

--
-- Name: events_id_seq; Type: SEQUENCE; Schema: public; Owner: avnadmin
--

CREATE SEQUENCE public.events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.events_id_seq OWNER TO avnadmin;

--
-- Name: events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avnadmin
--

ALTER SEQUENCE public.events_id_seq OWNED BY public.events.id;


--
-- Name: health_checkin; Type: TABLE; Schema: public; Owner: avnadmin
--

CREATE TABLE public.health_checkin (
    id integer NOT NULL,
    datetime timestamp without time zone DEFAULT now(),
    health_status public.health_check,
    comments text,
    plant_id integer
);


ALTER TABLE public.health_checkin OWNER TO avnadmin;

--
-- Name: health_checkin_id_seq; Type: SEQUENCE; Schema: public; Owner: avnadmin
--

CREATE SEQUENCE public.health_checkin_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.health_checkin_id_seq OWNER TO avnadmin;

--
-- Name: health_checkin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avnadmin
--

ALTER SEQUENCE public.health_checkin_id_seq OWNED BY public.health_checkin.id;


--
-- Name: images; Type: TABLE; Schema: public; Owner: avnadmin
--

CREATE TABLE public.images (
    id integer NOT NULL,
    filename character varying(100),
    plant integer,
    caption text,
    datetime timestamp without time zone DEFAULT now(),
    health_check integer,
    event integer
);


ALTER TABLE public.images OWNER TO avnadmin;

--
-- Name: images_id_seq; Type: SEQUENCE; Schema: public; Owner: avnadmin
--

CREATE SEQUENCE public.images_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.images_id_seq OWNER TO avnadmin;

--
-- Name: images_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avnadmin
--

ALTER SEQUENCE public.images_id_seq OWNED BY public.images.id;


--
-- Name: plant_types; Type: TABLE; Schema: public; Owner: avnadmin
--

CREATE TABLE public.plant_types (
    id integer NOT NULL,
    scientific_name text
);


ALTER TABLE public.plant_types OWNER TO avnadmin;

--
-- Name: plant_types_id_seq; Type: SEQUENCE; Schema: public; Owner: avnadmin
--

CREATE SEQUENCE public.plant_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.plant_types_id_seq OWNER TO avnadmin;

--
-- Name: plant_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avnadmin
--

ALTER SEQUENCE public.plant_types_id_seq OWNED BY public.plant_types.id;


--
-- Name: plants; Type: TABLE; Schema: public; Owner: avnadmin
--

CREATE TABLE public.plants (
    id integer NOT NULL,
    name text,
    scientific_name integer,
    notes text
);


ALTER TABLE public.plants OWNER TO avnadmin;

--
-- Name: plants_id_seq; Type: SEQUENCE; Schema: public; Owner: avnadmin
--

CREATE SEQUENCE public.plants_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.plants_id_seq OWNER TO avnadmin;

--
-- Name: plants_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avnadmin
--

ALTER SEQUENCE public.plants_id_seq OWNED BY public.plants.id;


--
-- Name: events id; Type: DEFAULT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.events ALTER COLUMN id SET DEFAULT nextval('public.events_id_seq'::regclass);


--
-- Name: health_checkin id; Type: DEFAULT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.health_checkin ALTER COLUMN id SET DEFAULT nextval('public.health_checkin_id_seq'::regclass);


--
-- Name: images id; Type: DEFAULT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.images ALTER COLUMN id SET DEFAULT nextval('public.images_id_seq'::regclass);


--
-- Name: plant_types id; Type: DEFAULT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.plant_types ALTER COLUMN id SET DEFAULT nextval('public.plant_types_id_seq'::regclass);


--
-- Name: plants id; Type: DEFAULT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.plants ALTER COLUMN id SET DEFAULT nextval('public.plants_id_seq'::regclass);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);


--
-- Name: health_checkin health_checkin_pkey; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.health_checkin
    ADD CONSTRAINT health_checkin_pkey PRIMARY KEY (id);


--
-- Name: images images_pkey; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_pkey PRIMARY KEY (id);


--
-- Name: plant_types plant_types_pkey; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.plant_types
    ADD CONSTRAINT plant_types_pkey PRIMARY KEY (id);


--
-- Name: plants plants_pkey; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.plants
    ADD CONSTRAINT plants_pkey PRIMARY KEY (id);


--
-- Name: events events_plant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_plant_id_fkey FOREIGN KEY (plant_id) REFERENCES public.plants(id);


--
-- Name: health_checkin health_checkin_plant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.health_checkin
    ADD CONSTRAINT health_checkin_plant_id_fkey FOREIGN KEY (plant_id) REFERENCES public.plants(id);


--
-- Name: images images_event_fkey; Type: FK CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_event_fkey FOREIGN KEY (event) REFERENCES public.events(id);


--
-- Name: images images_health_check_fkey; Type: FK CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_health_check_fkey FOREIGN KEY (health_check) REFERENCES public.health_checkin(id);


--
-- Name: images images_plant_fkey; Type: FK CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_plant_fkey FOREIGN KEY (plant) REFERENCES public.plants(id);


--
-- Name: plants plants_scientific_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.plants
    ADD CONSTRAINT plants_scientific_name_fkey FOREIGN KEY (scientific_name) REFERENCES public.plant_types(id);


--
-- PostgreSQL database dump complete
--

\unrestrict aDTute0CREwoF6kSfaUMpIeCBuNFczealbtzg7LeK4O4hfNfo9advnENzMHDk38

