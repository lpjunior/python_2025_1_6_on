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

--C.R.U.D
--Create, Retrieve, Update, Delete

-- Inserindo dados
INSERT INTO public.contacts(first_name, last_name, email, phone)
    VALUES ('Raphael', 'Aragao', 'raphael@senac.com', '2121-2121');
INSERT INTO public.contacts(first_name, last_name, email, phone)
    VALUES ('Caius', 'Israel', 'caius@senac.com', '2121-2121');
INSERT INTO public.contacts(first_name, last_name, email, phone)
    VALUES ('Pedro', 'Henrique', 'pedro@senac.com', '2121-2121');
INSERT INTO public.contacts(first_name, last_name, email, phone)
    VALUES ('Caroline', 'Rodrigues', 'caroline@senac.com', '2121-2121');
INSERT INTO public.contacts(first_name, last_name, email, phone)
    VALUES ('Jose', 'Rodrigues', 'jose@senac.com', '2121-2121');

-- Consultando a tabela contacts
SELECT * FROM public.contacts;
SELECT first_name, last_name FROM public.contacts;
SELECT first_name AS firstname, last_name AS lastname FROM public.contacts;
SELECT * FROM public.contacts WHERE first_name ilike '%a%';
SELECT COUNT(*) FROM public.contacts;
SELECT last_name, COUNT(*) AS total FROM public.contacts GROUP BY last_name;
-- consulta como prefixo (valor%)
-- consulta como sufixo (%valor)
-- consulta como encontre o valor (%valor%)

INSERT INTO public.contacts(first_name, last_name, email, phone)
    VALUES ('Aluno', 'a ser excluido', 'aluno@senac.com', '2121-2121');

-- Atualizando um registro da tabela contacts
UPDATE public.contacts
    SET
    last_name = 'A ser atualizado e excluido',
    email = 'aluno.excluido@senac.com'
WHERE email = 'aluno@senac.com';

-- Excluindo um registro na tabela contacts
DELETE FROM public.contacts WHERE contact_id = 'b537bca5-5b05-4e53-a185-ba21d49774ab';
commit;
DELETE FROM public.contacts;
rollback;

