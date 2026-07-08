package br.com.fiap.bean;

public class Comunicacao implements Monitoravel {

    private boolean ativa;
    private String tipoConexao;

    public Comunicacao() {
    }

    public Comunicacao(boolean ativa, String tipoConexao) {
        this.ativa = ativa;
        this.tipoConexao = tipoConexao;
    }

    public boolean isAtiva() {
        return ativa;
    }

    public void setAtiva(boolean ativa) {
        this.ativa = ativa;
    }

    public String getTipoConexao() {
        return tipoConexao;
    }

    public void setTipoConexao(String tipoConexao) {
        this.tipoConexao = tipoConexao;
    }

    public boolean verificarConexao() {
        return ativa;
    }

    @Override
    public String monitorar() {
        if (ativa) {
            return "Comunicação ativa via " + tipoConexao + "\n";
        } else {
            return "Falha de comunicação detectada\n";
        }
    }
}