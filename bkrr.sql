--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

-- Started on 2025-01-06 16:46:20

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
-- TOC entry 876 (class 1247 OID 16602)
-- Name: userbackground; Type: TYPE; Schema: public; Owner: myuser
--

CREATE TYPE public.userbackground AS ENUM (
    'RESEARCHER',
    'FISHERMAN',
    'NGO',
    'BYCATCH_ACTIVIST',
    'OBSERVER'
);


ALTER TYPE public.userbackground OWNER TO myuser;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 217 (class 1259 OID 16390)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO myuser;

--
-- TOC entry 223 (class 1259 OID 16410)
-- Name: bycatch; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.bycatch (
    bycatch_id character varying NOT NULL,
    port_id character varying NOT NULL,
    species_id character varying NOT NULL,
    date_caught timestamp without time zone NOT NULL,
    quantity integer NOT NULL,
    bpue double precision NOT NULL,
    total_catch integer,
    gear_type character varying NOT NULL
);


ALTER TABLE public.bycatch OWNER TO myuser;

--
-- TOC entry 222 (class 1259 OID 16409)
-- Name: bycatch_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.bycatch_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bycatch_id_seq OWNER TO myuser;

--
-- TOC entry 4866 (class 0 OID 0)
-- Dependencies: 222
-- Name: bycatch_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.bycatch_id_seq OWNED BY public.bycatch.bycatch_id;


--
-- TOC entry 219 (class 1259 OID 16396)
-- Name: ports; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.ports (
    port_id character varying NOT NULL,
    name character varying(100) NOT NULL,
    location character varying(255),
    size character varying(50) NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    authority_name character varying(100),
    phone character varying(50),
    email character varying(100),
    region character varying(100)
);


ALTER TABLE public.ports OWNER TO myuser;

--
-- TOC entry 218 (class 1259 OID 16395)
-- Name: ports_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.ports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ports_id_seq OWNER TO myuser;

--
-- TOC entry 4867 (class 0 OID 0)
-- Dependencies: 218
-- Name: ports_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.ports_id_seq OWNED BY public.ports.port_id;


--
-- TOC entry 229 (class 1259 OID 16614)
-- Name: recommendations; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.recommendations (
    id integer NOT NULL,
    user_id integer NOT NULL,
    content text NOT NULL
);


ALTER TABLE public.recommendations OWNER TO myuser;

--
-- TOC entry 228 (class 1259 OID 16613)
-- Name: recommendations_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.recommendations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.recommendations_id_seq OWNER TO myuser;

--
-- TOC entry 4868 (class 0 OID 0)
-- Dependencies: 228
-- Name: recommendations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.recommendations_id_seq OWNED BY public.recommendations.id;


--
-- TOC entry 225 (class 1259 OID 16427)
-- Name: reports; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.reports (
    report_id character varying NOT NULL,
    bycatch_id character varying NOT NULL,
    reporter_name character varying(100) NOT NULL,
    contact_info character varying(255) NOT NULL,
    remarks text,
    created_at timestamp without time zone,
    gear_type character varying(100) NOT NULL,
    species_id character varying NOT NULL,
    quantity integer,
    date date NOT NULL
);


ALTER TABLE public.reports OWNER TO myuser;

--
-- TOC entry 224 (class 1259 OID 16426)
-- Name: reports_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.reports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reports_id_seq OWNER TO myuser;

--
-- TOC entry 4869 (class 0 OID 0)
-- Dependencies: 224
-- Name: reports_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.reports_id_seq OWNED BY public.reports.report_id;


--
-- TOC entry 221 (class 1259 OID 16403)
-- Name: species; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.species (
    species_id character varying NOT NULL,
    iucn_status character varying(50) NOT NULL,
    estimated_catch integer NOT NULL,
    mortality_rate double precision NOT NULL,
    scientific_name character varying(100) NOT NULL,
    common_name character varying(100),
    origin character varying(50)
);


ALTER TABLE public.species OWNER TO myuser;

--
-- TOC entry 220 (class 1259 OID 16402)
-- Name: species_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.species_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.species_id_seq OWNER TO myuser;

--
-- TOC entry 4870 (class 0 OID 0)
-- Dependencies: 220
-- Name: species_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.species_id_seq OWNED BY public.species.species_id;


--
-- TOC entry 227 (class 1259 OID 16591)
-- Name: users; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(255) NOT NULL,
    background public.userbackground NOT NULL
);


ALTER TABLE public.users OWNER TO myuser;

--
-- TOC entry 226 (class 1259 OID 16590)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO myuser;

--
-- TOC entry 4871 (class 0 OID 0)
-- Dependencies: 226
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4676 (class 2604 OID 16511)
-- Name: bycatch bycatch_id; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.bycatch ALTER COLUMN bycatch_id SET DEFAULT nextval('public.bycatch_id_seq'::regclass);


--
-- TOC entry 4674 (class 2604 OID 16457)
-- Name: ports port_id; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.ports ALTER COLUMN port_id SET DEFAULT nextval('public.ports_id_seq'::regclass);


--
-- TOC entry 4679 (class 2604 OID 16617)
-- Name: recommendations id; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.recommendations ALTER COLUMN id SET DEFAULT nextval('public.recommendations_id_seq'::regclass);


--
-- TOC entry 4677 (class 2604 OID 16526)
-- Name: reports report_id; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.reports ALTER COLUMN report_id SET DEFAULT nextval('public.reports_id_seq'::regclass);


--
-- TOC entry 4675 (class 2604 OID 16482)
-- Name: species species_id; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.species ALTER COLUMN species_id SET DEFAULT nextval('public.species_id_seq'::regclass);


--
-- TOC entry 4678 (class 2604 OID 16594)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 4848 (class 0 OID 16390)
-- Dependencies: 217
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.alembic_version (version_num) FROM stdin;
1213f99156c5
\.


--
-- TOC entry 4854 (class 0 OID 16410)
-- Dependencies: 223
-- Data for Name: bycatch; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.bycatch (bycatch_id, port_id, species_id, date_caught, quantity, bpue, total_catch, gear_type) FROM stdin;
BC00128	TNSS05	SP001	2024-12-31 00:00:00	9	0.7	30	Trawling
BC00130	TNTN01	SP004	2024-12-31 00:00:00	12	0.6	130	Pelagic longlines
BC00124	TNSS05	SP002	2024-12-28 00:00:00	8	0.4	80	Bottom trawling
BC00126	TNTN01	SP004	2024-12-27 00:00:00	12	0.6	130	Pelagic longlines
BC00125	TNGB04	SP003	2025-01-02 00:00:00	15	0.3	120	Demersal longlines
BC00127	TNGB04	SP005	2025-01-03 00:00:00	15	0.3	120	Demersal longlines
BC00123	TNBZ24	SP001	2024-12-29 00:00:00	10	0.5	100	Longline
BC00129	TNGB04	SP005	2024-12-30 00:00:00	34	0.2	45	Net
\.


--
-- TOC entry 4850 (class 0 OID 16396)
-- Dependencies: 219
-- Data for Name: ports; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.ports (port_id, name, location, size, latitude, longitude, authority_name, phone, email, region) FROM stdin;
TNBZ24	Bizerte Port	North Tunisia	Large	37.28	9.87	OMMP	+216 71 735 812	br.bizerte@douane.gov.tn	\N
TNTN01	La Goulette Port	North Tunisia	Large	36.8189	10.1658	OMMP	+216 71 123 456	lagoulette.port@douane.gov.tn	\N
TNZZ02	Zarzis Port	South Tunisia	Small	34.7405	10.6894	OMMP	+216 73 789 012	zarzis.port@douane.gov.tn	\N
TNGB04	Gabès Port	South Tunisia	Medium	33.8833	10.0999	OMMP	+216 75 123 456	gabes.port@douane.gov.tn	\N
TNSS05	Sousse Port	North Tunisia	Large	35.8251	10.6374	OMMP	+216 73 789 012	sousse.port@douane.gov.tn	\N
\.


--
-- TOC entry 4860 (class 0 OID 16614)
-- Dependencies: 229
-- Data for Name: recommendations; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.recommendations (id, user_id, content) FROM stdin;
\.


--
-- TOC entry 4856 (class 0 OID 16427)
-- Dependencies: 225
-- Data for Name: reports; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.reports (report_id, bycatch_id, reporter_name, contact_info, remarks, created_at, gear_type, species_id, quantity, date) FROM stdin;
RPT123456	BC00123	Mohamed Tajouri	54636336	Species not typically found in this area	2024-12-31 15:16:01.449252	Longline	SP001	5	2024-12-31
RPT123457	BC00124	Ali Ben Hassen	56789012	Rare occurrence	2024-12-31 18:12:04.694764	Bottom trawling	SP002	3	2024-12-31
RPT123458	BC00125	Imen Jaziri	58923456	Caught in deep waters	2024-12-31 18:13:20.344648	Demersal longlines	SP003	6	2024-12-31
RPT123460	BC00127	Firas Boudhina	56123456	High number of catches	2024-12-31 18:13:37.280566	Trawling	SP005	7	2024-12-31
RPT123459	BC00126	Rami Khadhraoui	57863412	Unusual bycatch in this season	2024-12-31 18:13:55.238189	Pelagic longlines	SP004	4	2024-12-31
\.


--
-- TOC entry 4852 (class 0 OID 16403)
-- Dependencies: 221
-- Data for Name: species; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.species (species_id, iucn_status, estimated_catch, mortality_rate, scientific_name, common_name, origin) FROM stdin;
SP001	Endangered	5000	0.25	Caretta caretta	Loggerhead Sea Turtle	Migratory
SP002	Endangered	7000	0.25	Sardina pilchardus	Sardine	Migratory
SP003	Endangered	500	0.3	Squatina squatina	Angel Shark	Native
SP004	Vulnerable	1000	0.2	Rhinobatos cemiculus	Blackfin Guitarfish	Migratory
SP005	Near Threatened	1500	0.25	Rhinobatos rhinobatos	Common Guitarfish	Migratory
SP006	Least Concern	3000	0.1	Chimaera monstrosa	Rabbitfish	Native
\.


--
-- TOC entry 4858 (class 0 OID 16591)
-- Dependencies: 227
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.users (id, username, email, password, background) FROM stdin;
2	Isra Mariem Thabti	isrameryemth@gmail.com	$2b$12$Mcea5580gkHnuypIG3i9ueAIUr/9aOCH6gttC02x.UHuWftYTsZ.i	FISHERMAN
\.


--
-- TOC entry 4872 (class 0 OID 0)
-- Dependencies: 222
-- Name: bycatch_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.bycatch_id_seq', 1, false);


--
-- TOC entry 4873 (class 0 OID 0)
-- Dependencies: 218
-- Name: ports_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.ports_id_seq', 1, false);


--
-- TOC entry 4874 (class 0 OID 0)
-- Dependencies: 228
-- Name: recommendations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.recommendations_id_seq', 1, false);


--
-- TOC entry 4875 (class 0 OID 0)
-- Dependencies: 224
-- Name: reports_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.reports_id_seq', 1, false);


--
-- TOC entry 4876 (class 0 OID 0)
-- Dependencies: 220
-- Name: species_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.species_id_seq', 1, false);


--
-- TOC entry 4877 (class 0 OID 0)
-- Dependencies: 226
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- TOC entry 4681 (class 2606 OID 16394)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 4687 (class 2606 OID 16513)
-- Name: bycatch bycatch_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.bycatch
    ADD CONSTRAINT bycatch_pkey PRIMARY KEY (bycatch_id);


--
-- TOC entry 4683 (class 2606 OID 16459)
-- Name: ports ports_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.ports
    ADD CONSTRAINT ports_pkey PRIMARY KEY (port_id);


--
-- TOC entry 4697 (class 2606 OID 16621)
-- Name: recommendations recommendations_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.recommendations
    ADD CONSTRAINT recommendations_pkey PRIMARY KEY (id);


--
-- TOC entry 4689 (class 2606 OID 16528)
-- Name: reports reports_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_pkey PRIMARY KEY (report_id);


--
-- TOC entry 4685 (class 2606 OID 16484)
-- Name: species species_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.species
    ADD CONSTRAINT species_pkey PRIMARY KEY (species_id);


--
-- TOC entry 4691 (class 2606 OID 16600)
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- TOC entry 4693 (class 2606 OID 16596)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4695 (class 2606 OID 16598)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 4698 (class 2606 OID 16474)
-- Name: bycatch bycatch_port_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.bycatch
    ADD CONSTRAINT bycatch_port_id_fkey FOREIGN KEY (port_id) REFERENCES public.ports(port_id);


--
-- TOC entry 4699 (class 2606 OID 16500)
-- Name: bycatch bycatch_species_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.bycatch
    ADD CONSTRAINT bycatch_species_id_fkey FOREIGN KEY (species_id) REFERENCES public.species(species_id);


--
-- TOC entry 4702 (class 2606 OID 16622)
-- Name: recommendations recommendations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.recommendations
    ADD CONSTRAINT recommendations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 4700 (class 2606 OID 16580)
-- Name: reports reports_bycatch_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_bycatch_id_fkey FOREIGN KEY (bycatch_id) REFERENCES public.bycatch(bycatch_id);


--
-- TOC entry 4701 (class 2606 OID 16585)
-- Name: reports reports_species_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_species_id_fkey FOREIGN KEY (species_id) REFERENCES public.species(species_id);


--
-- TOC entry 2076 (class 826 OID 16389)
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TABLES TO myuser;


-- Completed on 2025-01-06 16:46:20

--
-- PostgreSQL database dump complete
--

