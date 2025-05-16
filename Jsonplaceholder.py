import requests
import json
import time

all_posts = []

def get_post(id):
    """
    Obtém os posts públicos de um usuário pelo ID usando a API JSONPlaceholder.
    
    Parâmetros:
        id (int): ID do usuário (1 a 100).
    
    Retorna:
        list: Lista de posts do usuário, se encontrados.
    """
    url = 'https://jsonplaceholder.typicode.com/posts'
    params = {'userId': id}
    response = requests.get(url, params=params)
    response.raise_for_status()

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f'Erro de requisição! Status code: {response.status_code}')


def new_post(id, title, text):
    """
    Cria um novo post para o usuário na API JSONPlaceholder.
    
    Parâmetros:
        id (int): ID do usuário.
        title (str): Título do post.
        text (str): Conteúdo do post.
    
    Retorna:
        dict: Dados do post criado.
    """
    url = 'https://jsonplaceholder.typicode.com/posts'
    body = {
        "userId": id,
        "title": title,
        "body": text
    }

    response = requests.post(url, json=body)

    if response.status_code == 201:
        data = response.json()
        return data
    else:
        print(f'Erro de requisição! Status code: {response.status_code}')


def menu_login():
    """
    Exibe o menu de login e retorna a opção escolhida pelo usuário.
    
    Retorna:
        str: Opção escolhida.
    """
    print('-=' * 25)
    print("1 - Cadastrar\n"
          "2 - Entrar\n"
          "3 - Sair\n")
    opcao = input('Digite a opção: ')
    return opcao


def menu(all_posts, user):
    """
    Exibe o menu principal após login e gerencia as ações do usuário.
    
    Parâmetros:
        all_posts (list): Lista com todos os posts criados.
        user (dict): Dados do usuário logado.
    """
    while True:
        print('-=' * 25)
        print("1 - Visualizar posts\n"
              "2 - Fazer post\n"
              "3 - Visualizar meus posts\n"
              "4 - Sair\n")

        try:
            opcao = input('Digite a opção: ')

            if opcao == '1':
                while True:
                    try:
                        id = int(input('Digite o número do ID do usuário que deseja ver os posts [1-100]: '))
                        if 1 <= id <= 100:
                            data = get_post(id)

                            for p in data:
                                print(f"UserId: {p['userId']}")
                                print(f"Título: {p['title']}")
                                print(f"Texto: {p['body']}")
                                print('~-' * 25)

                            for post in all_posts:
                                if post['userId'] == id:
                                    print(f"UserId: {post['userId']}")
                                    print(f"Título: {post['title']}")
                                    print(f"Texto: {post['body']}")
                                    print('~-' * 25)

                            user['interacoes'].append('Visualizou todos os posts')
                            break
                        else:
                            print('Número inválido, digite um número entre 1 e 100.')
                    except ValueError:
                        print('Número inválido, digite um número inteiro.')
                
            elif opcao == '2':
                new_title = input('Digite um título para seu post: ')
                new_text = input('Digite o texto: ')
                userid = user['userId']

                user_post = new_post(userid, new_title, new_text)
                all_posts.append(user_post)
                user['posts'].append(user_post)
                user['interacoes'].append('Fez um post')
                print('Publicando...')
                time.sleep(1)
                print('Seu post foi publicado com sucesso!')

            elif opcao == '3':
                if not user['posts']:
                    print('Nenhum post encontrado.')
                    continue

                print("Meus posts".center(50, '-'))
                for p in user['posts']:
                    print()
                    print(f"UserId: {p['userId']}")
                    print(f"Título: {p['title']}")
                    print(f"Texto: {p['body']}")
                    print('~-' * 25)

                user['interacoes'].append('Visualizou seus posts')

            elif opcao == '4':
                if user['interacoes']:
                    print("Interações no Sistema".center(50, '-'))
                    for i in user['interacoes']:
                        print(i)
                print('-~' * 25)
                print('Saindo...')
                time.sleep(2)
                break

            else:
                print('Opção inválida!')

        except ValueError:
            print('Valor inválido!')
        except KeyboardInterrupt:
            print('\nPrograma finalizado pelo usuário.')
            exit()


def cadastro(user_list):
    """
    Cadastra um novo usuário, garantindo que o e-mail não esteja repetido.
    
    Parâmetros:
        user_list (list): Lista de usuários cadastrados.
    """
    print('~-' * 25)
    email = input('Digite seu e-mail: ')

    for user in user_list:
        if user['email'] == email:
            print('E-mail já cadastrado!')
            return None

    senha = input('Digite sua senha: ')
    print('~-' * 25)

    new_user = {
        'userId': len(user_list) + 1,
        'email': email,
        'senha': senha,
        'posts': [],
        'interacoes': []
    }
    user_list.append(new_user)
    print('Usuário cadastrado com sucesso!')


def login(user_list):
    """
    Realiza o login do usuário com base no e-mail e senha.
    
    Parâmetros:
        user_list (list): Lista de usuários cadastrados.
    
    Retorna:
        dict or None: Usuário autenticado ou None.
    """
    print('-=' * 25)
    email = input('Digite seu e-mail: ')
    senha = input('Digite sua senha: ')
    print('-=' * 25)

    for user in user_list:
        if user['email'] == email and user['senha'] == senha:
            print(f'Bem-vindo, {email}!')
            return user

    print('E-mail ou senha inválidos!')
    return None


def main():
    """
    Função principal do sistema. Gerencia o fluxo de cadastro, login e menu principal.
    """
    user_list = []

    while True:
        opcao = menu_login()

        try:
            if opcao == '1':
                cadastro(user_list)

            elif opcao == '2':
                new_user = login(user_list)
                if new_user:
                    menu(all_posts, new_user)

            elif opcao == '3':
                print('Saindo...')
                time.sleep(1.5)
                print('Até mais!')
                exit()

            else:
                print('Opção inválida!')

        except KeyboardInterrupt:
            print('\nPrograma finalizado pelo usuário.')
            exit()


if __name__ == "__main__":
    main()
