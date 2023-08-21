-- Table: soe.transactions

-- DROP TABLE IF EXISTS soe.transactions;

CREATE TABLE IF NOT EXISTS soe.transactions
(
    sortcode text COLLATE pg_catalog."default",
    account_number text COLLATE pg_catalog."default",
    "transactionId" text COLLATE pg_catalog."default",
    amount double precision,
    transaction_type text COLLATE pg_catalog."default",
    merchant_name text COLLATE pg_catalog."default",
    merchant_city text COLLATE pg_catalog."default",
    transaction_date date,
    type text COLLATE pg_catalog."default",
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    CONSTRAINT id PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS soe.transactions
    OWNER to arnabsaha;

-- Table: soe.declinedtransactions

-- DROP TABLE IF EXISTS soe.declinedtransactions;

CREATE TABLE IF NOT EXISTS soe.declinedtransactions
(
    id bigint NOT NULL,
    sortcode text COLLATE pg_catalog."default",
    account_number text COLLATE pg_catalog."default",
    amount double precision,
    merchant_name text COLLATE pg_catalog."default",
    merchant_city text COLLATE pg_catalog."default",
    reason_code text COLLATE pg_catalog."default",
    reason_text text COLLATE pg_catalog."default",
    transaction_date date,
    CONSTRAINT declinedtransactions_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS soe.declinedtransactions
    OWNER to arnabsaha;    