package br.com.fiap.bean;

public class AetherSistema {

    private String nomeSistema;
    private String localMonitorado;

    public AetherSistema() {
    }

    public AetherSistema(String nomeSistema, String localMonitorado) {
        this.nomeSistema = nomeSistema;
        this.localMonitorado = localMonitorado;
    }

    public String getNomeSistema() {
        return nomeSistema;
    }

    public void setNomeSistema(String nomeSistema) {
        this.nomeSistema = nomeSistema;
    }

    public String getLocalMonitorado() {
        return localMonitorado;
    }

    public void setLocalMonitorado(String localMonitorado) {
        this.localMonitorado = localMonitorado;
    }

    public String classificarRisco(Recurso recurso, Comunicacao comunicacao) {
        if (recurso.getAgua() < 30 || recurso.getEnergia() < 30 || !comunicacao.verificarConexao()) {
            return "CRÍTICO";
        } else if (recurso.getAgua() < 50 || recurso.getEnergia() < 50 || recurso.getAlimentos() < 50) {
            return "ALTO";
        } else if (recurso.getAgua() < 70 || recurso.getEnergia() < 70 || recurso.getAlimentos() < 70) {
            return "MODERADO";
        } else {
            return "BAIXO";
        }
    }

    public String ativarAquaSave(Recurso recurso) {
        if (recurso.getAgua() < 30) {
            Protocolo protocolo = new Protocolo("AquaSave");
            return protocolo.ativar() + "Economia de água iniciada.\n";
        } else {
            return "AquaSave não foi necessário.\n";
        }
    }

    public String ativarSignalLock(Comunicacao comunicacao) {
        if (!comunicacao.verificarConexao()) {
            Protocolo protocolo = new Protocolo("SignalLock");
            return protocolo.ativar() + "Comunicação alternativa priorizada.\n";
        } else {
            return "SignalLock não foi necessário.\n";
        }
    }

    public String ativarResourceLock(Recurso recurso) {
        if (recurso.calcularAutonomia() < 40) {
            Protocolo protocolo = new Protocolo("ResourceLock");
            return protocolo.ativar() + "Preservação de recursos essenciais iniciada.\n";
        } else {
            return "ResourceLock não foi necessário.\n";
        }
    }

    public String ativarEmergencyMode(String risco) {
        if (risco.equals("CRÍTICO")) {
            Protocolo protocolo = new Protocolo("Emergency Mode");
            return protocolo.ativar() + "Alerta crítico enviado para a Defesa Civil.\n";
        } else {
            return "Emergency Mode não foi necessário.\n";
        }
    }

    public String gerarRelatorio(String risco, Recurso recurso, Comunicacao comunicacao) {
        String relatorio = " RELATÓRIO AETHER \n";
        relatorio += "Sistema: " + nomeSistema + "\n";
        relatorio += "Local: " + localMonitorado + "\n";
        relatorio += "Nível de risco: " + risco + "\n";
        relatorio += "Água: " + recurso.getAgua() + "%\n";
        relatorio += "Energia: " + recurso.getEnergia() + "%\n";
        relatorio += "Alimentos: " + recurso.getAlimentos() + "%\n";
        relatorio += "Comunicação ativa: " + comunicacao.verificarConexao() + "\n";
        relatorio += "Autonomia media: " + recurso.calcularAutonomia() + "%\n";
        return relatorio;
    }
}
