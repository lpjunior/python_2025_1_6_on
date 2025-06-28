SET search_path TO public;

-- versão antiga
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- versão mais recente
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Deletando a tabela
DROP TABLE IF EXISTS contacts;

-- Criando a tabela contacts
CREATE TABLE IF NOT EXISTS public.contacts (
    contact_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL
);

-- Inserindo dados
INSERT INTO public.contacts(first_name, last_name, email, phone)
    VALUES ('Raphael', 'Aragao', 'raphael@senac.com', '2121-2121');
INSERT INTO public.contacts(first_name, last_name, email, phone)
    VALUES ('Caius', 'Israel', 'caius@senac.com', '2121-2121');
INSERT INTO public.contacts(first_name, last_name, email, phone)
    VALUES ('Pedro', 'Henrique', 'pedro@senac.com', '2121-2121');
INSERT INTO public.contacts(first_name, last_name, email, phone)
    VALUES ('Caroline', 'Rodrigues', 'caroline@senac.com', '2121-2121');

-- Consultando a tabela contacts
SELECT * FROM public.contacts;
SELECT first_name, last_name FROM public.contacts;
SELECT first_name AS firstname, last_name AS lastname FROM public.contacts;
SELECT *
    FROM public.contacts
WHERE first_name = 'Luis'