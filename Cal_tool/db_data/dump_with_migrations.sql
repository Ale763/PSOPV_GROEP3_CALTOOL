--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Drop databases
--

DROP DATABASE a;




--
-- Drop roles
--

DROP ROLE a;
DROP ROLE postgres;


--
-- Roles
--

CREATE ROLE a;
ALTER ROLE a WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB LOGIN NOREPLICATION NOBYPASSRLS PASSWORD 'md54124bc0a9335c27f086f24ba207a4912';
CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS;






--
-- Database creation
--

CREATE DATABASE a WITH TEMPLATE = template0 OWNER = a;
REVOKE CONNECT,TEMPORARY ON DATABASE template1 FROM PUBLIC;
GRANT CONNECT ON DATABASE template1 TO PUBLIC;


\connect a

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 10.3 (Debian 10.3-1.pgdg90+1)
-- Dumped by pg_dump version 10.3 (Debian 10.3-1.pgdg90+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: a
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO a;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: a
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO a;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: a
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: a
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO a;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: a
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO a;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: a
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: a
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO a;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: a
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO a;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: a
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: a
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO a;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: a
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO a;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: a
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO a;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: a
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: a
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO a;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: a
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: a
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO a;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: a
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO a;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: a
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: cal_tool_calendar_sources; Type: TABLE; Schema: public; Owner: a
--

CREATE TABLE public.cal_tool_calendar_sources (
    cal_source_id character varying(200) NOT NULL,
    source_location character varying(200) NOT NULL,
    filtered_source_location character varying(200) NOT NULL,
    type character varying(200) NOT NULL,
    cal_id_id character varying(200) NOT NULL
);


ALTER TABLE public.cal_tool_calendar_sources OWNER TO a;

--
-- Name: cal_tool_calendars; Type: TABLE; Schema: public; Owner: a
--

CREATE TABLE public.cal_tool_calendars (
    cal_id character varying(200) NOT NULL,
    cal_alias character varying(30),
    cal_color character varying(20) NOT NULL,
    last_checked timestamp with time zone NOT NULL,
    unique_id_id character varying(200) NOT NULL
);


ALTER TABLE public.cal_tool_calendars OWNER TO a;

--
-- Name: cal_tool_filter_attributes; Type: TABLE; Schema: public; Owner: a
--

CREATE TABLE public.cal_tool_filter_attributes (
    id integer NOT NULL,
    attribute character varying(200) NOT NULL,
    value character varying(200) NOT NULL,
    filter_id_id character varying(200) NOT NULL
);


ALTER TABLE public.cal_tool_filter_attributes OWNER TO a;

--
-- Name: cal_tool_filter_attributes_id_seq; Type: SEQUENCE; Schema: public; Owner: a
--

CREATE SEQUENCE public.cal_tool_filter_attributes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cal_tool_filter_attributes_id_seq OWNER TO a;

--
-- Name: cal_tool_filter_attributes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: a
--

ALTER SEQUENCE public.cal_tool_filter_attributes_id_seq OWNED BY public.cal_tool_filter_attributes.id;


--
-- Name: cal_tool_filters; Type: TABLE; Schema: public; Owner: a
--

CREATE TABLE public.cal_tool_filters (
    filter_id character varying(200) NOT NULL,
    last_modified timestamp with time zone NOT NULL,
    cal_id_id character varying(200) NOT NULL
);


ALTER TABLE public.cal_tool_filters OWNER TO a;

--
-- Name: cal_tool_password_tokens; Type: TABLE; Schema: public; Owner: a
--

CREATE TABLE public.cal_tool_password_tokens (
    unique_id_id character varying(200) NOT NULL,
    password_token character varying(200) NOT NULL,
    "timestamp" timestamp with time zone NOT NULL
);


ALTER TABLE public.cal_tool_password_tokens OWNER TO a;

--
-- Name: cal_tool_shared_calendars; Type: TABLE; Schema: public; Owner: a
--

CREATE TABLE public.cal_tool_shared_calendars (
    id integer NOT NULL,
    mail character varying(50),
    url character varying(200) NOT NULL,
    password character varying(200) NOT NULL,
    cal_id_id character varying(200) NOT NULL
);


ALTER TABLE public.cal_tool_shared_calendars OWNER TO a;

--
-- Name: cal_tool_shared_calendars_id_seq; Type: SEQUENCE; Schema: public; Owner: a
--

CREATE SEQUENCE public.cal_tool_shared_calendars_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cal_tool_shared_calendars_id_seq OWNER TO a;

--
-- Name: cal_tool_shared_calendars_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: a
--

ALTER SEQUENCE public.cal_tool_shared_calendars_id_seq OWNED BY public.cal_tool_shared_calendars.id;


--
-- Name: cal_tool_users; Type: TABLE; Schema: public; Owner: a
--

CREATE TABLE public.cal_tool_users (
    unique_id character varying(200) NOT NULL,
    nickname character varying(30),
    password character varying(200) NOT NULL,
    mail character varying(50),
    role character varying(20) NOT NULL,
    last_login timestamp with time zone NOT NULL
);


ALTER TABLE public.cal_tool_users OWNER TO a;

--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: a
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO a;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: a
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO a;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: a
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: a
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO a;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: a
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO a;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: a
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: a
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO a;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: a
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO a;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: a
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: a
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO a;

--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: cal_tool_filter_attributes id; Type: DEFAULT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.cal_tool_filter_attributes ALTER COLUMN id SET DEFAULT nextval('public.cal_tool_filter_attributes_id_seq'::regclass);


--
-- Name: cal_tool_shared_calendars id; Type: DEFAULT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.cal_tool_shared_calendars ALTER COLUMN id SET DEFAULT nextval('public.cal_tool_shared_calendars_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: a
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: a
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: a
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add permission	2	add_permission
5	Can change permission	2	change_permission
6	Can delete permission	2	delete_permission
7	Can add group	3	add_group
8	Can change group	3	change_group
9	Can delete group	3	delete_group
10	Can add user	4	add_user
11	Can change user	4	change_user
12	Can delete user	4	delete_user
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add users	7	add_users
20	Can change users	7	change_users
21	Can delete users	7	delete_users
22	Can add calendar_sources	8	add_calendar_sources
23	Can change calendar_sources	8	change_calendar_sources
24	Can delete calendar_sources	8	delete_calendar_sources
25	Can add calendars	9	add_calendars
26	Can change calendars	9	change_calendars
27	Can delete calendars	9	delete_calendars
28	Can add filter_attributes	10	add_filter_attributes
29	Can change filter_attributes	10	change_filter_attributes
30	Can delete filter_attributes	10	delete_filter_attributes
31	Can add filters	11	add_filters
32	Can change filters	11	change_filters
33	Can delete filters	11	delete_filters
34	Can add password_tokens	12	add_password_tokens
35	Can change password_tokens	12	change_password_tokens
36	Can delete password_tokens	12	delete_password_tokens
37	Can add shared_calendars	13	add_shared_calendars
38	Can change shared_calendars	13	change_shared_calendars
39	Can delete shared_calendars	13	delete_shared_calendars
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: a
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$100000$K8ATS7HnmlXP$Jf8JHiW0SJ8yngy/ktMCwQ/kLzPn9mQDAN3Mt2n91mM=	2018-04-13 19:07:15.271438+00	t	admin				t	t	2018-04-13 19:07:07.114867+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: a
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: a
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: cal_tool_calendar_sources; Type: TABLE DATA; Schema: public; Owner: a
--

COPY public.cal_tool_calendar_sources (cal_source_id, source_location, filtered_source_location, type, cal_id_id) FROM stdin;
\.


--
-- Data for Name: cal_tool_calendars; Type: TABLE DATA; Schema: public; Owner: a
--

COPY public.cal_tool_calendars (cal_id, cal_alias, cal_color, last_checked, unique_id_id) FROM stdin;
\.


--
-- Data for Name: cal_tool_filter_attributes; Type: TABLE DATA; Schema: public; Owner: a
--

COPY public.cal_tool_filter_attributes (id, attribute, value, filter_id_id) FROM stdin;
\.


--
-- Data for Name: cal_tool_filters; Type: TABLE DATA; Schema: public; Owner: a
--

COPY public.cal_tool_filters (filter_id, last_modified, cal_id_id) FROM stdin;
\.


--
-- Data for Name: cal_tool_password_tokens; Type: TABLE DATA; Schema: public; Owner: a
--

COPY public.cal_tool_password_tokens (unique_id_id, password_token, "timestamp") FROM stdin;
\.


--
-- Data for Name: cal_tool_shared_calendars; Type: TABLE DATA; Schema: public; Owner: a
--

COPY public.cal_tool_shared_calendars (id, mail, url, password, cal_id_id) FROM stdin;
\.


--
-- Data for Name: cal_tool_users; Type: TABLE DATA; Schema: public; Owner: a
--

COPY public.cal_tool_users (unique_id, nickname, password, mail, role, last_login) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: a
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: a
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	cal_tool	users
8	cal_tool	calendar_sources
9	cal_tool	calendars
10	cal_tool	filter_attributes
11	cal_tool	filters
12	cal_tool	password_tokens
13	cal_tool	shared_calendars
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: a
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	cal_tool	0001_initial	2018-04-13 19:06:51.100603+00
2	cal_tool	0002_auto_20180403_2219	2018-04-13 19:06:51.139611+00
3	cal_tool	0003_auto_20180413_1835	2018-04-13 19:06:52.037044+00
4	contenttypes	0001_initial	2018-04-13 19:06:54.859883+00
5	auth	0001_initial	2018-04-13 19:06:55.481154+00
6	admin	0001_initial	2018-04-13 19:06:55.672671+00
7	admin	0002_logentry_remove_auto_add	2018-04-13 19:06:55.711821+00
8	contenttypes	0002_remove_content_type_name	2018-04-13 19:06:55.836139+00
9	auth	0002_alter_permission_name_max_length	2018-04-13 19:06:55.857411+00
10	auth	0003_alter_user_email_max_length	2018-04-13 19:06:55.961841+00
11	auth	0004_alter_user_username_opts	2018-04-13 19:06:56.001616+00
12	auth	0005_alter_user_last_login_null	2018-04-13 19:06:56.074024+00
13	auth	0006_require_contenttypes_0002	2018-04-13 19:06:56.092567+00
14	auth	0007_alter_validators_add_error_messages	2018-04-13 19:06:56.147065+00
15	auth	0008_alter_user_username_max_length	2018-04-13 19:06:56.492427+00
16	auth	0009_alter_user_last_name_max_length	2018-04-13 19:06:56.545254+00
17	sessions	0001_initial	2018-04-13 19:06:56.646892+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: a
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: a
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: a
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: a
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 39, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: a
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: a
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: a
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: cal_tool_filter_attributes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: a
--

SELECT pg_catalog.setval('public.cal_tool_filter_attributes_id_seq', 1, false);


--
-- Name: cal_tool_shared_calendars_id_seq; Type: SEQUENCE SET; Schema: public; Owner: a
--

SELECT pg_catalog.setval('public.cal_tool_shared_calendars_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: a
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: a
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 13, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: a
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 17, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: cal_tool_calendar_sources cal_tool_calendar_sources_pkey; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.cal_tool_calendar_sources
    ADD CONSTRAINT cal_tool_calendar_sources_pkey PRIMARY KEY (cal_source_id);


--
-- Name: cal_tool_calendars cal_tool_calendars_pkey; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.cal_tool_calendars
    ADD CONSTRAINT cal_tool_calendars_pkey PRIMARY KEY (cal_id);


--
-- Name: cal_tool_filter_attributes cal_tool_filter_attributes_pkey; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.cal_tool_filter_attributes
    ADD CONSTRAINT cal_tool_filter_attributes_pkey PRIMARY KEY (id);


--
-- Name: cal_tool_filters cal_tool_filters_pkey; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.cal_tool_filters
    ADD CONSTRAINT cal_tool_filters_pkey PRIMARY KEY (filter_id);


--
-- Name: cal_tool_password_tokens cal_tool_password_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.cal_tool_password_tokens
    ADD CONSTRAINT cal_tool_password_tokens_pkey PRIMARY KEY (unique_id_id);


--
-- Name: cal_tool_shared_calendars cal_tool_shared_calendars_mail_key; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.cal_tool_shared_calendars
    ADD CONSTRAINT cal_tool_shared_calendars_mail_key UNIQUE (mail);


--
-- Name: cal_tool_shared_calendars cal_tool_shared_calendars_pkey; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.cal_tool_shared_calendars
    ADD CONSTRAINT cal_tool_shared_calendars_pkey PRIMARY KEY (id);


--
-- Name: cal_tool_shared_calendars cal_tool_shared_calendars_url_key; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.cal_tool_shared_calendars
    ADD CONSTRAINT cal_tool_shared_calendars_url_key UNIQUE (url);


--
-- Name: cal_tool_users cal_tool_users_mail_key; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.cal_tool_users
    ADD CONSTRAINT cal_tool_users_mail_key UNIQUE (mail);


--
-- Name: cal_tool_users cal_tool_users_nickname_c9f71b80_uniq; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.cal_tool_users
    ADD CONSTRAINT cal_tool_users_nickname_c9f71b80_uniq UNIQUE (nickname);


--
-- Name: cal_tool_users cal_tool_users_pkey; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.cal_tool_users
    ADD CONSTRAINT cal_tool_users_pkey PRIMARY KEY (unique_id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: cal_tool_calendar_sources_cal_id_id_71c904f5; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX cal_tool_calendar_sources_cal_id_id_71c904f5 ON public.cal_tool_calendar_sources USING btree (cal_id_id);


--
-- Name: cal_tool_calendar_sources_cal_id_id_71c904f5_like; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX cal_tool_calendar_sources_cal_id_id_71c904f5_like ON public.cal_tool_calendar_sources USING btree (cal_id_id varchar_pattern_ops);


--
-- Name: cal_tool_calendar_sources_cal_source_id_9baae2fa_like; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX cal_tool_calendar_sources_cal_source_id_9baae2fa_like ON public.cal_tool_calendar_sources USING btree (cal_source_id varchar_pattern_ops);


--
-- Name: cal_tool_calendars_cal_id_abf15b93_like; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX cal_tool_calendars_cal_id_abf15b93_like ON public.cal_tool_calendars USING btree (cal_id varchar_pattern_ops);


--
-- Name: cal_tool_calendars_unique_id_id_324460b9; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX cal_tool_calendars_unique_id_id_324460b9 ON public.cal_tool_calendars USING btree (unique_id_id);


--
-- Name: cal_tool_calendars_unique_id_id_324460b9_like; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX cal_tool_calendars_unique_id_id_324460b9_like ON public.cal_tool_calendars USING btree (unique_id_id varchar_pattern_ops);


--
-- Name: cal_tool_filter_attributes_filter_id_id_b77a34f8; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX cal_tool_filter_attributes_filter_id_id_b77a34f8 ON public.cal_tool_filter_attributes USING btree (filter_id_id);


--
-- Name: cal_tool_filter_attributes_filter_id_id_b77a34f8_like; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX cal_tool_filter_attributes_filter_id_id_b77a34f8_like ON public.cal_tool_filter_attributes USING btree (filter_id_id varchar_pattern_ops);


--
-- Name: cal_tool_filters_cal_id_id_cb623fd6; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX cal_tool_filters_cal_id_id_cb623fd6 ON public.cal_tool_filters USING btree (cal_id_id);


--
-- Name: cal_tool_filters_cal_id_id_cb623fd6_like; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX cal_tool_filters_cal_id_id_cb623fd6_like ON public.cal_tool_filters USING btree (cal_id_id varchar_pattern_ops);


--
-- Name: cal_tool_filters_filter_id_bb0225c7_like; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX cal_tool_filters_filter_id_bb0225c7_like ON public.cal_tool_filters USING btree (filter_id varchar_pattern_ops);


--
-- Name: cal_tool_password_tokens_unique_id_id_deaac209_like; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX cal_tool_password_tokens_unique_id_id_deaac209_like ON public.cal_tool_password_tokens USING btree (unique_id_id varchar_pattern_ops);


--
-- Name: cal_tool_shared_calendars_cal_id_id_048983eb; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX cal_tool_shared_calendars_cal_id_id_048983eb ON public.cal_tool_shared_calendars USING btree (cal_id_id);


--
-- Name: cal_tool_shared_calendars_cal_id_id_048983eb_like; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX cal_tool_shared_calendars_cal_id_id_048983eb_like ON public.cal_tool_shared_calendars USING btree (cal_id_id varchar_pattern_ops);


--
-- Name: cal_tool_shared_calendars_mail_1bc8b44d_like; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX cal_tool_shared_calendars_mail_1bc8b44d_like ON public.cal_tool_shared_calendars USING btree (mail varchar_pattern_ops);


--
-- Name: cal_tool_shared_calendars_url_182e3d23_like; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX cal_tool_shared_calendars_url_182e3d23_like ON public.cal_tool_shared_calendars USING btree (url varchar_pattern_ops);


--
-- Name: cal_tool_users_mail_0ef2c8e2_like; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX cal_tool_users_mail_0ef2c8e2_like ON public.cal_tool_users USING btree (mail varchar_pattern_ops);


--
-- Name: cal_tool_users_nickname_c9f71b80_like; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX cal_tool_users_nickname_c9f71b80_like ON public.cal_tool_users USING btree (nickname varchar_pattern_ops);


--
-- Name: cal_tool_users_unique_id_45831a12_like; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX cal_tool_users_unique_id_45831a12_like ON public.cal_tool_users USING btree (unique_id varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: a
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cal_tool_calendar_sources cal_tool_calendar_so_cal_id_id_71c904f5_fk_cal_tool_; Type: FK CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.cal_tool_calendar_sources
    ADD CONSTRAINT cal_tool_calendar_so_cal_id_id_71c904f5_fk_cal_tool_ FOREIGN KEY (cal_id_id) REFERENCES public.cal_tool_calendars(cal_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cal_tool_calendars cal_tool_calendars_unique_id_id_324460b9_fk_cal_tool_; Type: FK CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.cal_tool_calendars
    ADD CONSTRAINT cal_tool_calendars_unique_id_id_324460b9_fk_cal_tool_ FOREIGN KEY (unique_id_id) REFERENCES public.cal_tool_users(unique_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cal_tool_filter_attributes cal_tool_filter_attr_filter_id_id_b77a34f8_fk_cal_tool_; Type: FK CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.cal_tool_filter_attributes
    ADD CONSTRAINT cal_tool_filter_attr_filter_id_id_b77a34f8_fk_cal_tool_ FOREIGN KEY (filter_id_id) REFERENCES public.cal_tool_filters(filter_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cal_tool_filters cal_tool_filters_cal_id_id_cb623fd6_fk_cal_tool_; Type: FK CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.cal_tool_filters
    ADD CONSTRAINT cal_tool_filters_cal_id_id_cb623fd6_fk_cal_tool_ FOREIGN KEY (cal_id_id) REFERENCES public.cal_tool_calendars(cal_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cal_tool_password_tokens cal_tool_password_to_unique_id_id_deaac209_fk_cal_tool_; Type: FK CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.cal_tool_password_tokens
    ADD CONSTRAINT cal_tool_password_to_unique_id_id_deaac209_fk_cal_tool_ FOREIGN KEY (unique_id_id) REFERENCES public.cal_tool_users(unique_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cal_tool_shared_calendars cal_tool_shared_cale_cal_id_id_048983eb_fk_cal_tool_; Type: FK CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.cal_tool_shared_calendars
    ADD CONSTRAINT cal_tool_shared_cale_cal_id_id_048983eb_fk_cal_tool_ FOREIGN KEY (cal_id_id) REFERENCES public.cal_tool_calendars(cal_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk; Type: FK CONSTRAINT; Schema: public; Owner: a
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

\connect postgres

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 10.3 (Debian 10.3-1.pgdg90+1)
-- Dumped by pg_dump version 10.3 (Debian 10.3-1.pgdg90+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: DATABASE postgres; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- PostgreSQL database dump complete
--

\connect template1

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 10.3 (Debian 10.3-1.pgdg90+1)
-- Dumped by pg_dump version 10.3 (Debian 10.3-1.pgdg90+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: DATABASE template1; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE template1 IS 'default template for new databases';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--

