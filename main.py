import html
import sqlite3

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="CineHub - Laboratorio de Seguranca")


def obter_banco():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            is_admin BOOLEAN NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS filmes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            genero TEXT NOT NULL,
            ano INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comentarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filme_id INTEGER NOT NULL,
            autor TEXT NOT NULL,
            conteudo TEXT NOT NULL,
            FOREIGN KEY (filme_id) REFERENCES filmes (id)
        )
    """)

    cursor.execute("""
        INSERT INTO usuarios (nome, email, senha, is_admin)
        VALUES
            ('Administrador', 'admin@cinehub.org', 'segredo_admin_123', 1),
            ('Critico Lucas', 'lucas@cinehub.org', 'senha_lucas_456', 0)
    """)

    cursor.execute("""
        INSERT INTO filmes (titulo, genero, ano)
        VALUES
            ('Cidade de Deus', 'Drama', 2002),
            ('O Auto da Compadecida', 'Comedia', 2000),
            ('Bacurau', 'Ficcao', 2019)
    """)

    conn.commit()
    return conn


db = obter_banco()


class RequisicaoLogin(BaseModel):
    email: str
    senha: str


class RequisicaoComentario(BaseModel):
    autor: str
    conteudo: str


@app.post("/vulneravel/login")
def login_vulneravel(dados: RequisicaoLogin):
    cursor = db.cursor()
    query = f"SELECT id, nome, email, is_admin FROM usuarios WHERE email = '{dados.email}' AND senha = '{dados.senha}'"
    cursor.execute(query)
    usuario = cursor.fetchone()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais invalidas"
        )

    return {
        "id": usuario[0],
        "nome": usuario[1],
        "email": usuario[2],
        "is_admin": bool(usuario[3]),
        "status": "Autenticado com sucesso"
    }


@app.post("/vulneravel/filmes/{filme_id}/comentarios")
def comentar_vulneravel(filme_id: int, dados: RequisicaoComentario):
    cursor = db.cursor()
    cursor.execute("SELECT id FROM filmes WHERE id = ?", (filme_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Filme nao encontrado")

    cursor.execute(
        "INSERT INTO comentarios (filme_id, autor, conteudo) VALUES (?, ?, ?)",
        (filme_id, dados.autor, dados.conteudo)
    )
    db.commit()

    return {
        "filme_id": filme_id,
        "autor": dados.autor,
        "conteudo": dados.conteudo,
        "aviso": "Comentario registrado sem higienizacao"
    }


@app.post("/seguro/login")
def login_seguro(dados: RequisicaoLogin):
    cursor = db.cursor()
    query = "SELECT id, nome, email, is_admin FROM usuarios WHERE email = ? AND senha = ?"
    cursor.execute(query, (dados.email, dados.senha))
    usuario = cursor.fetchone()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais invalidas"
        )

    return {
        "id": usuario[0],
        "nome": usuario[1],
        "email": usuario[2],
        "is_admin": bool(usuario[3]),
        "status": "Autenticado com sucesso"
    }


@app.post("/seguro/filmes/{filme_id}/comentarios")
def comentar_seguro(filme_id: int, dados: RequisicaoComentario):
    cursor = db.cursor()
    cursor.execute("SELECT id FROM filmes WHERE id = ?", (filme_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Filme nao encontrado")

    autor_seguro = html.escape(dados.autor.strip())
    conteudo_seguro = html.escape(dados.conteudo.strip())

    cursor.execute(
        "INSERT INTO comentarios (filme_id, autor, conteudo) VALUES (?, ?, ?)",
        (filme_id, autor_seguro, conteudo_seguro)
    )
    db.commit()

    return {
        "filme_id": filme_id,
        "autor": autor_seguro,
        "conteudo": conteudo_seguro,
        "aviso": "Comentario higienizado com sucesso"
    }