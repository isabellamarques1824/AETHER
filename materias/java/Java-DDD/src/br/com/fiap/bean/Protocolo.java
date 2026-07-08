package br.com.fiap.bean;

public class Protocolo {

    private String nome;
    private boolean ativo;

    public Protocolo() {
    }

    public Protocolo(String nome) {
        this.nome = nome;
        this.ativo = false;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }


    public boolean isAtivo() {
        return ativo;
    }

    public void setAtivo(boolean ativo) {
        this.ativo = ativo;
    }

    public String ativar() {
        ativo = true;
        return "Protocolo " + nome + " ativado.\n";
    }
}