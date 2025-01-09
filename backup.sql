PGDMP               	         }         	   bycatchdb    17.2    17.2 :    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false                        0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false                       1262    16387 	   bycatchdb    DATABASE     |   CREATE DATABASE bycatchdb WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'French_France.1252';
    DROP DATABASE bycatchdb;
                     postgres    false            l           1247    16602    userbackground    TYPE     �   CREATE TYPE public.userbackground AS ENUM (
    'RESEARCHER',
    'FISHERMAN',
    'NGO',
    'BYCATCH_ACTIVIST',
    'OBSERVER'
);
 !   DROP TYPE public.userbackground;
       public               myuser    false            �            1259    16390    alembic_version    TABLE     X   CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);
 #   DROP TABLE public.alembic_version;
       public         heap r       myuser    false            �            1259    16410    bycatch    TABLE     Z  CREATE TABLE public.bycatch (
    bycatch_id character varying NOT NULL,
    port_id character varying NOT NULL,
    species_id character varying NOT NULL,
    date_caught timestamp without time zone NOT NULL,
    quantity integer NOT NULL,
    bpue double precision NOT NULL,
    total_catch integer,
    gear_type character varying NOT NULL
);
    DROP TABLE public.bycatch;
       public         heap r       myuser    false            �            1259    16409    bycatch_id_seq    SEQUENCE     �   CREATE SEQUENCE public.bycatch_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.bycatch_id_seq;
       public               myuser    false    223                       0    0    bycatch_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.bycatch_id_seq OWNED BY public.bycatch.bycatch_id;
          public               myuser    false    222            �            1259    16396    ports    TABLE     �  CREATE TABLE public.ports (
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
    DROP TABLE public.ports;
       public         heap r       myuser    false            �            1259    16395    ports_id_seq    SEQUENCE     �   CREATE SEQUENCE public.ports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.ports_id_seq;
       public               myuser    false    219                       0    0    ports_id_seq    SEQUENCE OWNED BY     B   ALTER SEQUENCE public.ports_id_seq OWNED BY public.ports.port_id;
          public               myuser    false    218            �            1259    16614    recommendations    TABLE     z   CREATE TABLE public.recommendations (
    id integer NOT NULL,
    user_id integer NOT NULL,
    content text NOT NULL
);
 #   DROP TABLE public.recommendations;
       public         heap r       myuser    false            �            1259    16613    recommendations_id_seq    SEQUENCE     �   CREATE SEQUENCE public.recommendations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.recommendations_id_seq;
       public               myuser    false    229                       0    0    recommendations_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.recommendations_id_seq OWNED BY public.recommendations.id;
          public               myuser    false    228            �            1259    16427    reports    TABLE     �  CREATE TABLE public.reports (
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
    DROP TABLE public.reports;
       public         heap r       myuser    false            �            1259    16426    reports_id_seq    SEQUENCE     �   CREATE SEQUENCE public.reports_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.reports_id_seq;
       public               myuser    false    225                       0    0    reports_id_seq    SEQUENCE OWNED BY     H   ALTER SEQUENCE public.reports_id_seq OWNED BY public.reports.report_id;
          public               myuser    false    224            �            1259    16403    species    TABLE     N  CREATE TABLE public.species (
    species_id character varying NOT NULL,
    iucn_status character varying(50) NOT NULL,
    estimated_catch integer NOT NULL,
    mortality_rate double precision NOT NULL,
    scientific_name character varying(100) NOT NULL,
    common_name character varying(100),
    origin character varying(50)
);
    DROP TABLE public.species;
       public         heap r       myuser    false            �            1259    16402    species_id_seq    SEQUENCE     �   CREATE SEQUENCE public.species_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.species_id_seq;
       public               myuser    false    221                       0    0    species_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.species_id_seq OWNED BY public.species.species_id;
          public               myuser    false    220            �            1259    16591    users    TABLE     �   CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(255) NOT NULL,
    background public.userbackground NOT NULL
);
    DROP TABLE public.users;
       public         heap r       myuser    false    876            �            1259    16590    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public               myuser    false    227                       0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public               myuser    false    226            D           2604    16511    bycatch bycatch_id    DEFAULT     p   ALTER TABLE ONLY public.bycatch ALTER COLUMN bycatch_id SET DEFAULT nextval('public.bycatch_id_seq'::regclass);
 A   ALTER TABLE public.bycatch ALTER COLUMN bycatch_id DROP DEFAULT;
       public               myuser    false    223    222    223            B           2604    16457    ports port_id    DEFAULT     i   ALTER TABLE ONLY public.ports ALTER COLUMN port_id SET DEFAULT nextval('public.ports_id_seq'::regclass);
 <   ALTER TABLE public.ports ALTER COLUMN port_id DROP DEFAULT;
       public               myuser    false    218    219    219            G           2604    16617    recommendations id    DEFAULT     x   ALTER TABLE ONLY public.recommendations ALTER COLUMN id SET DEFAULT nextval('public.recommendations_id_seq'::regclass);
 A   ALTER TABLE public.recommendations ALTER COLUMN id DROP DEFAULT;
       public               myuser    false    228    229    229            E           2604    16526    reports report_id    DEFAULT     o   ALTER TABLE ONLY public.reports ALTER COLUMN report_id SET DEFAULT nextval('public.reports_id_seq'::regclass);
 @   ALTER TABLE public.reports ALTER COLUMN report_id DROP DEFAULT;
       public               myuser    false    225    224    225            C           2604    16482    species species_id    DEFAULT     p   ALTER TABLE ONLY public.species ALTER COLUMN species_id SET DEFAULT nextval('public.species_id_seq'::regclass);
 A   ALTER TABLE public.species ALTER COLUMN species_id DROP DEFAULT;
       public               myuser    false    221    220    221            F           2604    16594    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public               myuser    false    227    226    227            �          0    16390    alembic_version 
   TABLE DATA           6   COPY public.alembic_version (version_num) FROM stdin;
    public               myuser    false    217   �D       �          0    16410    bycatch 
   TABLE DATA           w   COPY public.bycatch (bycatch_id, port_id, species_id, date_caught, quantity, bpue, total_catch, gear_type) FROM stdin;
    public               myuser    false    223   E       �          0    16396    ports 
   TABLE DATA           y   COPY public.ports (port_id, name, location, size, latitude, longitude, authority_name, phone, email, region) FROM stdin;
    public               myuser    false    219   F       �          0    16614    recommendations 
   TABLE DATA           ?   COPY public.recommendations (id, user_id, content) FROM stdin;
    public               myuser    false    229   G       �          0    16427    reports 
   TABLE DATA           �   COPY public.reports (report_id, bycatch_id, reporter_name, contact_info, remarks, created_at, gear_type, species_id, quantity, date) FROM stdin;
    public               myuser    false    225   �G       �          0    16403    species 
   TABLE DATA           �   COPY public.species (species_id, iucn_status, estimated_catch, mortality_rate, scientific_name, common_name, origin) FROM stdin;
    public               myuser    false    221   YI       �          0    16591    users 
   TABLE DATA           J   COPY public.users (id, username, email, password, background) FROM stdin;
    public               myuser    false    227   cJ       	           0    0    bycatch_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.bycatch_id_seq', 1, false);
          public               myuser    false    222            
           0    0    ports_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.ports_id_seq', 1, false);
          public               myuser    false    218                       0    0    recommendations_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.recommendations_id_seq', 45, true);
          public               myuser    false    228                       0    0    reports_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.reports_id_seq', 1, false);
          public               myuser    false    224                       0    0    species_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.species_id_seq', 1, false);
          public               myuser    false    220                       0    0    users_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.users_id_seq', 4, true);
          public               myuser    false    226            I           2606    16394 #   alembic_version alembic_version_pkc 
   CONSTRAINT     j   ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
 M   ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
       public                 myuser    false    217            O           2606    16513    bycatch bycatch_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.bycatch
    ADD CONSTRAINT bycatch_pkey PRIMARY KEY (bycatch_id);
 >   ALTER TABLE ONLY public.bycatch DROP CONSTRAINT bycatch_pkey;
       public                 myuser    false    223            K           2606    16459    ports ports_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.ports
    ADD CONSTRAINT ports_pkey PRIMARY KEY (port_id);
 :   ALTER TABLE ONLY public.ports DROP CONSTRAINT ports_pkey;
       public                 myuser    false    219            Y           2606    16621 $   recommendations recommendations_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.recommendations
    ADD CONSTRAINT recommendations_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.recommendations DROP CONSTRAINT recommendations_pkey;
       public                 myuser    false    229            Q           2606    16528    reports reports_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_pkey PRIMARY KEY (report_id);
 >   ALTER TABLE ONLY public.reports DROP CONSTRAINT reports_pkey;
       public                 myuser    false    225            M           2606    16484    species species_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.species
    ADD CONSTRAINT species_pkey PRIMARY KEY (species_id);
 >   ALTER TABLE ONLY public.species DROP CONSTRAINT species_pkey;
       public                 myuser    false    221            S           2606    16600    users users_email_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);
 ?   ALTER TABLE ONLY public.users DROP CONSTRAINT users_email_key;
       public                 myuser    false    227            U           2606    16596    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public                 myuser    false    227            W           2606    16598    users users_username_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_username_key;
       public                 myuser    false    227            Z           2606    16474    bycatch bycatch_port_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.bycatch
    ADD CONSTRAINT bycatch_port_id_fkey FOREIGN KEY (port_id) REFERENCES public.ports(port_id);
 F   ALTER TABLE ONLY public.bycatch DROP CONSTRAINT bycatch_port_id_fkey;
       public               myuser    false    219    4683    223            [           2606    16500    bycatch bycatch_species_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.bycatch
    ADD CONSTRAINT bycatch_species_id_fkey FOREIGN KEY (species_id) REFERENCES public.species(species_id);
 I   ALTER TABLE ONLY public.bycatch DROP CONSTRAINT bycatch_species_id_fkey;
       public               myuser    false    221    4685    223            ^           2606    16622 ,   recommendations recommendations_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.recommendations
    ADD CONSTRAINT recommendations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
 V   ALTER TABLE ONLY public.recommendations DROP CONSTRAINT recommendations_user_id_fkey;
       public               myuser    false    229    227    4693            \           2606    16580    reports reports_bycatch_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_bycatch_id_fkey FOREIGN KEY (bycatch_id) REFERENCES public.bycatch(bycatch_id);
 I   ALTER TABLE ONLY public.reports DROP CONSTRAINT reports_bycatch_id_fkey;
       public               myuser    false    225    223    4687            ]           2606    16585    reports reports_species_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_species_id_fkey FOREIGN KEY (species_id) REFERENCES public.species(species_id);
 I   ALTER TABLE ONLY public.reports DROP CONSTRAINT reports_species_id_fkey;
       public               myuser    false    225    221    4685                       826    16389    DEFAULT PRIVILEGES FOR TABLES    DEFAULT ACL     J   ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TABLES TO myuser;
                        postgres    false            �      x�3424N��445K6����� %��      �   �   x����
�@�������3gf�i9mB]E�AKP���LEZ�q�}�`�QRE��h ?�'�%�J���)�&�Pt壩>�Y�q�S��J�6���5eU_���W��������Bɨ$�hHl;�-~vP����U;+˽W�WL�2D�(�����\ח͌�����Q��3�k�t� 3�_�O���ن���+�1�6��A\6B�'�fv�      �     x�}нn�0���p�+��[��Rh$�P�X�@�O�����C�*�B��s>�yRq	I��q��0�3��9�r�۩u���ƃ��X4޳� /��D3��"�q�G�o��Ӱ��c3|���1�ʼ�)!�K��N���"����1.�T1t���Gh<��r�ܸ��+��+.��@HԒ�++�1A����e�م҄JH]������]. #�U���{I��j\�������4=�>��+�-zgѴEv�#FQ����      �   �   x�͐��@Ek��[bb���Jag��6��D܍����jb�(�;ս'G-�T�x���6��ML��^.�`%�;���j-�6����l���VC�G�lpr|�l��@K��p�m7���>��ږ`��I<����.O�r�fmz�������HA���ER�Q�r�f�"*)���j�f�"�<M�'��!�      �   p  x�m��n�0E�㯘� �%J�:E��-`8�.���H,$�I�חq��M�`8�����B*�ޖe�i6=�O�)W�+x<�Κ��G����h�N����:��H�!`%7��V��T[V��~x7L�x�eȋ��~�R�Q|�,n��;
�8���M^�>c�w]Z�:�P�kKQ�F�J����g��e�p�2�׸z�J��3�~�w}�����0�w�ޘ#�Q4K���-+.���9_Є�*�t�
]�+��ov��[���:�����0�K�YпbG�͕�.�.�Rp���P_�nV�ʭ���ԏ���k���u?�R�x9�����>��`\W����h�݇��$��f�����      �   �   x�}�AO�0����/�ҕ���˘�2q��^�M�I�����LS��d�}�ټj]��w�{b��Z�^�kh�)%T�2az9;e�!s	^\ϘFP�[��e�;�Q}���s�WK��"�
�g��k���G���	v�������艱�b�����JFT�&g�(�O#���y��]B>�8,�԰#du�0��>e������0M��=l	cRM��CuiXB3�	��{L"��֥3d~�}U�a��      �     x�M�K��0��u�.\3\v�0\�hfS��U?1�(��w�N�͓c���d�)(LJNJ 1&��IA�".z��Z��iM����1�_��-�l��ԋ+����3��oX�^�~{T�����q��<�R�F%��<�ھ���z1I鵻}r�z`OvOW� -�C�q�l{�����c���ն��~u�s��GyP^������II8yk�ոݍ��}Z{Z�&
!�����;'__r�ޗt,z�5�~�ج�s��J�L��5M��j�     