# 🧑‍💼 EmpregaSenac

Sistema web desenvolvido com Django para gestão de **vagas de emprego**. Conecta **empresas** que desejam divulgar oportunidades a **candidatos** em busca de colocação no mercado.

---

## 🏗️ Funcionalidades Principais

### 👤 Autenticação
- Login e logout de usuários.
- Cadastro de dois tipos de usuários:
  - **Candidato**: pode visualizar vagas e se candidatar.
  - **Empresa**: pode criar, editar, excluir e listar vagas.

### 📋 Gestão de Vagas
- Empresas podem:
  - Criar vagas (título, nível, localidade, salário, descrição).
  - Editar ou excluir suas próprias vagas.
- Candidatos podem:
  - Visualizar todas as vagas disponíveis.
  - Enviar candidatura com nome, e-mail e currículo.

### 📎 Upload de Currículo
- O arquivo de currículo é enviado e armazenado no **Cloudinary**.

### 📧 Confirmação por E-mail
- Após candidatura, o candidato recebe uma confirmação automática via **e-mail SMTP (Gmail)**.

---

## 🗃️ Modelos

### `User` (do Django)

### `Candidato`
| Campo       | Tipo      |
|-------------|-----------|
| nome        | CharField |
| telefone    | CharField |
| cidade      | CharField |

### `Empresa`
| Campo         | Tipo      |
|---------------|-----------|
| nome_empresa  | CharField |
| cnpj          | CharField |

### `Vaga`
| Campo       | Tipo      |
|-------------|-----------|
| titulo      | CharField |
| descricao   | TextField |
| nivel       | Choices   |
| localidade  | CharField |
| salario     | Decimal   |
| empresa     | FK → Empresa |

### `Candidatura`
| Campo     | Tipo      |
|-----------|-----------|
| vaga      | FK → Vaga |
| nome      | CharField |
| email     | Email     |
| curriculo | FileField |
| data_envio| DateTime  |

---

## 🔐 Regras de Acesso

- Apenas usuários **autenticados** podem criar/editar/excluir vagas.
- Apenas usuários com perfil de **empresa** têm acesso às views de vagas.
- **Mixins** garantem as permissões específicas.

---

## 🌐 Tecnologias Usadas

- Django 5.2
- Bootstrap 5 (via CDN)
- PostgreSQL (hospedado no Supabase)
- Cloudinary (armazenamento de currículos)
- SMTP Gmail (envio de e-mails)
- `widget_tweaks` (melhorias em formulários HTML)

---

## ⚙️ Variáveis de Ambiente (.env)

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=<user>
DB_PASSWORD=<senha>
DB_HOST=<host>
DB_PORT=5432

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=<email>
EMAIL_HOST_PASSWORD=<senha_app>
EMAIL_USE_TLS=True

CLOUDINARY_URL=cloudinary://<api_key>:<api_secret>@<cloud_name>
DEFAULT_FILE_STORAGE=cloudinary_storage.storage.MediaCloudinaryStorage

DEBUG=True
ALLOWED_HOSTS=*.onrender.com,localhost,127.0.0.1
SECRET_KEY=your-secret-key
````

---

## ▶️ Como Executar Localmente

1. Clone o projeto:

   ```bash
   git clone https://github.com/lpjunior/python_2025_1_6_on.git empregasenac
   cd empregasenac
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   venv\Scripts\activate # no Windows 
   source venv/bin/activate  # bi Linux
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure o `.env` com suas credenciais.

5. Rode as migrações:

   ```bash
   python manage.py migrate
   ```

6. Inicie o servidor:

   ```bash
   python manage.py runserver
   ```

7. Acesse: [http://localhost:8000](http://localhost:8000)

---

## ✅ Melhorias Futuras

* Empresas visualizarem candidaturas recebidas.
* Paginação e busca de vagas.
* Painel administrativo personalizado.
* Testes automatizados (`tests.py`).

---

## 📄 Licença

Este projeto é de uso educacional para o curso de **Programação em Python no SENAC**.

---

