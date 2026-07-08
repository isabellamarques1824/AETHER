package br.com.fiap.bean;

import java.time.LocalDateTime;

public class HistoricoEvento {

    private String descricao;
    private LocalDateTime dataHora;

    public HistoricoEvento() {
    }

    public HistoricoEvento(String descricao) {
        this.descricao = descricao;
        this.dataHora = LocalDateTime.now();
    }

    public String getDescricao() {
        return descricao;
    }

    public void setDescricao(String descricao) {
        this.descricao = descricao;
    }


    public LocalDateTime getDataHora() {
        return dataHora;
    }

    public void setDataHora(LocalDateTime dataHora) {
        this.dataHora = dataHora;
    }

    public String registrarEvento() {
        return "Evento registrado: " + descricao + "\nData e hora: " + dataHora;
    }
}