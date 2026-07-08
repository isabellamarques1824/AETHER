package br.com.fiap.bean;

public class Ambiente implements Monitoravel {

    private double temperatura;
    private double umidade;
    private double nivelAgua;

    public Ambiente() {
    }

    public Ambiente(double temperatura, double umidade, double nivelAgua) {
        this.temperatura = temperatura;
        this.umidade = umidade;
        this.nivelAgua = nivelAgua;
    }

    public double getTemperatura() {
        return temperatura;
    }

    public void setTemperatura(double temperatura) {
        this.temperatura = temperatura;
    }

    public double getUmidade() {
        return umidade;
    }

    public void setUmidade(double umidade) {
        this.umidade = umidade;
    }

    public double getNivelAgua() {
        return nivelAgua;
    }

    public void setNivelAgua(double nivelAgua) {
        this.nivelAgua = nivelAgua;
    }

    @Override
    public String monitorar() {
        return "Monitoramento Ambiental\n"
                + "Temperatura: " + temperatura + " graus\n"
                + "Umidade: " + umidade + "%\n"
                + "Nível de água: " + nivelAgua + "%\n";
    }
}