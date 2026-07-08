package br.com.fiap.bean;

public class Recurso {

    private double agua;
    private double energia;
    private double alimentos;

    public Recurso() {
    }

    public Recurso(double agua, double energia, double alimentos) {
        this.agua = agua;
        this.energia = energia;
        this.alimentos = alimentos;
    }

    public double getAgua() {
        return agua;
    }

    public void setAgua(double agua) {
        this.agua = agua;
    }

    public double getEnergia() {
        return energia;
    }

    public void setEnergia(double energia) {
        this.energia = energia;
    }

    public double getAlimentos() {
        return alimentos;
    }

    public void setAlimentos(double alimentos) {
        this.alimentos = alimentos;
    }

    public double calcularAutonomia() {
        return (agua + energia + alimentos) / 3;
    }
}