import requests
import json
import time


def new_post(titulo, texto, id):

    url = 'https://jsonplaceholder.typicode.com/posts/'
    body = {
        'title': titulo,
        'body': texto,
        'userId' : id
    }

    try:
        response = requests.post(url, body)
        print(response.status_code)

        if response.status_code == 201:
            data = response.json()
            return data
    
    except requests.exceptions.RequestException as e:
        print('Erro em new post', e)
    
    
def get_post(url, id):
    url = f'https://jsonplaceholder.typicode.com/posts/{id}'
    response = requests.get(url)
    print(response.status_code)

    if response.status_code == 200:
        data = response.json()
        print(data)

def new_user(usuarios):

    email = input('Digite seu email: ')

    for u in usuarios:
        if u['email'] == email:
            print('Email ja cadastrado')
            return None
        
    senha = input('Digite sua senha: ')

    user = {
            'id': len(usuarios)+1,
            'email' : email,
            'senha': senha,
            'posts': [],
            'interacoes': []
            }
    
    usuarios.append(user)
    print('Usuário cadastrado com sucesso!')

def login(usuarios):
    email = input('Digiete seu email: ')
    senha = input('Digite sua senha: ')
    for u in usuarios:
        if u['email'] == email and u['senha'] == senha:
            return u
        
    else:
        print('Email ou Senha incorretos')

def menu_login():
    
        print('1 - Cadastrar\n' \
              '2 - Logar\n' \
              '3 - Sair')
        opcao = input('Digite a opção que deseja: ')

        return opcao

def menu(todos_posts, user):
    print('1 - Visualizar Posts\n' \
          '2 - Visualizar meus Posts\n' \
          '3 - Filtrar posts por User\n' \
          '4 - Fazer novo post\n' \
          '5 - Sair')
    while True:
        try:
            opcao = int(input('Digite a opção que deseja: '))
            if opcao not in range(1,6):
                print('Digite um numero valido [1-5]')
                continue

            if opcao == 1:
                print(todos_posts)
            elif opcao == 2:
                if user['posts']:
                    print('\n---- Meus Posts ----')
                    for post in user['post']:
                        print(post)
                user['interacoes'].append("Visualizou todos os posts")
            
            elif opcao == 3:
                while True:
                    try:
                        id = int(input('Digite o numero de Id do user que deseja ver [1-100]: '))
                        if id in range(1,101):
                            get_post(id)
                            user['interacoes'].append("Visualizou posts por user")
                            break
                        else:
                            print('Digite um valor valido [1-100]')
                            continue

                    except ValueError:
                        print('Digite um valor valido [1-100]')

            elif opcao == 4:
                print('\n--- Novo Post ---')
                titulo = input('Digite um Titulo para seu post: ')
                texto = input('Digite seu texto: ')
                id_user = user['id']
                new_post(titulo, texto, id_user)

                user['interacoes'].append("Fez um novo post")
            
            elif opcao == 5:
                print('Saindo...')
                time.sleep(2)


        except ValueError:
            print('Digite um numero valido [1-5]')
        
        except KeyboardInterrupt:
            print('Programa finalizado pelo usuário')
            exit()
        
def main():
    usuarios = []
    todos_posts = []
    while True:
        opcao = menu_login()
        try:
            if opcao == '1':
                new_user(usuarios)

            elif opcao == '2':
                novo_login = login(usuarios)
                if novo_login:
                    menu(todos_posts, novo_login)

            elif opcao == '3':
                print()
                print('Saindo...')
                time.sleep(2)
                print('Até mais!!')
                exit()

            else:
                print('A opção escolhida não é valida')
                continue

        except ValueError:
                print('A opção escolhida não é valida')
        except KeyboardInterrupt:
            print('Programa finalizado pelo usuário')
            exit()



main()
