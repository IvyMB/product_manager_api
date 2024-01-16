API de Gerenciamento de Produtos com Flask e MongoDB
Este projeto consiste em uma API desenvolvida em Flask para gerenciamento eficiente de produtos, utilizando MongoDB como banco de dados. A API oferece operações CRUD para produtos e categorias, proporcionando uma solução flexível e escalável.

Funcionalidades Principais:
Produtos:

Cadastro de novos produtos com informações detalhadas.
Atualização de dados de produtos existentes.
Consulta de todos os produtos ou produtos específicos por ID.
Exclusão de produtos.
Categorias:

Adição de novas categorias para organizar os produtos.
Atualização de informações de categorias existentes.
Consulta de todas as categorias ou categorias específicas por ID.
Exclusão de categorias.
Tecnologias Utilizadas:
Flask: Framework web em Python, escolhido pela sua simplicidade e extensibilidade.
MongoDB: Banco de dados NoSQL, proporcionando flexibilidade no esquema de dados.
Flask-MongoEngine: Facilita a integração entre Flask e MongoDB.
Estrutura do Projeto:
O projeto segue uma estrutura organizada para facilitar a manutenção e escalabilidade:

app/blueprints: Módulos Flask (blueprints) para separar funcionalidades.
app/services: Lógica de negócios para manipulação de dados.
app/schemas: Esquemas Marshmallow para validação de dados.
app/exceptions: Exceções personalizadas para melhor controle de erros.
Como Contribuir:
Sua contribuição é bem-vinda! Se deseja contribuir, siga os passos abaixo:

Faça um Fork: Crie uma cópia do projeto no seu perfil.
Clone o Repositório: git clone https://github.com/seu-usuario/nome-do-repo.git
Crie uma Branch: git checkout -b nome-da-sua-branch
Faça as Modificações: Implemente as melhorias ou correções desejadas.
Envie um Pull Request: Compartilhe suas alterações para revisão.
