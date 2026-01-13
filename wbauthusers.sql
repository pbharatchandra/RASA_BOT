CREATE TABLE IF NOT EXISTS public.wbauthusers
(
    userid integer NOT NULL,
    loginname character varying(30) COLLATE pg_catalog."default",
    hashpwd character varying(50) COLLATE pg_catalog."default",
    fullname character varying(50) COLLATE pg_catalog."default",
    usercatid integer,
    pwdexpirydate timestamp with time zone,
    isactive boolean,
    intramailid character varying(50) COLLATE pg_catalog."default",
    internetmailid character varying COLLATE pg_catalog."default",
    isdeleted boolean DEFAULT false,
    email_otp character varying(10) COLLATE pg_catalog."default",
    otp_expiry timestamp with time zone,
    password_reset_token character varying(100) COLLATE pg_catalog."default",
    token_expiry timestamp with time zone,
    last_pwd_reset_at timestamp without time zone,
    CONSTRAINT wbauthusers_pkey PRIMARY KEY (userid),
    CONSTRAINT wbauthusers_userid_key UNIQUE (userid)
)
