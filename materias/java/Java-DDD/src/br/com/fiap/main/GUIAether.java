package br.com.fiap.main;

import br.com.fiap.bean.AetherSistema;
import br.com.fiap.bean.Ambiente;
import br.com.fiap.bean.Comunicacao;
import br.com.fiap.bean.HistoricoEvento;
import br.com.fiap.bean.Recurso;

import java.awt.Color;
import java.awt.Font;
import java.awt.Insets;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextArea;
import javax.swing.JTextField;

@SuppressWarnings("serial")
public class GUIAether extends JPanel {

    private JLabel lbTitulo;
    private JLabel lbTemperatura, lbUmidade, lbAgua, lbEnergia, lbAlimentos, lbComunicacao;
    private JTextField tfTemperatura, tfUmidade, tfAgua, tfEnergia, tfAlimentos;
    private JComboBox<String> cbComunicacao;
    private JTextArea taResultado;
    private JButton btAnalisar, btLimpar;

    public GUIAether() {
        inicializarComponentes();
        definirEventos();
    }

    private void inicializarComponentes() {
        setLayout(null);
        setBackground(new Color(2, 18, 38));

        lbTitulo = new JLabel("AETHER - Analise de Ambiente Extremo");
        lbTitulo.setBounds(230, 20, 400, 30);
        lbTitulo.setForeground(Color.WHITE);
        lbTitulo.setFont(new Font("Arial", Font.BOLD, 18));

        lbTemperatura = new JLabel("Temperatura:");
        lbTemperatura.setBounds(80, 80, 120, 25);
        lbTemperatura.setForeground(Color.WHITE);

        tfTemperatura = new JTextField();
        tfTemperatura.setBounds(190, 80, 120, 25);

        lbUmidade = new JLabel("Umidade:");
        lbUmidade.setBounds(80, 120, 120, 25);
        lbUmidade.setForeground(Color.WHITE);

        tfUmidade = new JTextField();
        tfUmidade.setBounds(190, 120, 120, 25);

        lbAgua = new JLabel("Água:");
        lbAgua.setBounds(80, 160, 120, 25);
        lbAgua.setForeground(Color.WHITE);

        tfAgua = new JTextField();
        tfAgua.setBounds(190, 160, 120, 25);

        lbEnergia = new JLabel("Energia:");
        lbEnergia.setBounds(80, 200, 120, 25);
        lbEnergia.setForeground(Color.WHITE);

        tfEnergia = new JTextField();
        tfEnergia.setBounds(190, 200, 120, 25);

        lbAlimentos = new JLabel("Alimentos:");
        lbAlimentos.setBounds(80, 240, 120, 25);
        lbAlimentos.setForeground(Color.WHITE);

        tfAlimentos = new JTextField();
        tfAlimentos.setBounds(190, 240, 120, 25);

        lbComunicacao = new JLabel("Comunicação:");
        lbComunicacao.setBounds(80, 280, 120, 25);
        lbComunicacao.setForeground(Color.WHITE);

        cbComunicacao = new JComboBox<String>();
        cbComunicacao.addItem("Ativa");
        cbComunicacao.addItem("Falha");
        cbComunicacao.setBounds(190, 280, 120, 25);

        btAnalisar = new JButton("Analisar");
        btAnalisar.setBounds(80, 360, 120, 30);

        btLimpar = new JButton("Limpar");
        btLimpar.setBounds(210, 360, 120, 30);

        taResultado = new JTextArea();
        taResultado.setBounds(380, 80, 350, 380);
        taResultado.setEditable(false);
        taResultado.setBackground(new Color(245, 245, 245));
        taResultado.setForeground(new Color(2, 18, 38));
        taResultado.setFont(new Font("Arial", Font.BOLD, 12));
        taResultado.setMargin(new Insets(10, 10, 10, 10));

        add(lbTitulo);
        add(lbTemperatura);
        add(tfTemperatura);
        add(lbUmidade);
        add(tfUmidade);
        add(lbAgua);
        add(tfAgua);
        add(lbEnergia);
        add(tfEnergia);
        add(lbAlimentos);
        add(tfAlimentos);
        add(lbComunicacao);
        add(cbComunicacao);
        add(btAnalisar);
        add(btLimpar);
        add(taResultado);
    }

    private void definirEventos() {
        btAnalisar.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                analisarAmbiente();
            }
        });

        btLimpar.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                limparCampos();
            }
        });
    }

    private void analisarAmbiente() {
        try {
            double temperatura = Double.parseDouble(tfTemperatura.getText());
            double umidade = Double.parseDouble(tfUmidade.getText());
            double agua = Double.parseDouble(tfAgua.getText());
            double energia = Double.parseDouble(tfEnergia.getText());
            double alimentos = Double.parseDouble(tfAlimentos.getText());

            boolean comunicacaoAtiva = (cbComunicacao.getSelectedIndex() == 0);

            Ambiente ambiente = new Ambiente(temperatura, umidade, agua);
            Recurso recurso = new Recurso(agua, energia, alimentos);
            Comunicacao comunicacao = new Comunicacao(comunicacaoAtiva, "Satélite");
            AetherSistema sistema = new AetherSistema("AETHER", "Escola remota na Amazônia");

            String risco = sistema.classificarRisco(recurso, comunicacao);

            String resultado = "";
            resultado += ambiente.monitorar();
            resultado += comunicacao.monitorar();
            resultado += "\n";
            resultado += sistema.gerarRelatorio(risco, recurso, comunicacao);
            resultado += "\nPROTOCOLOS\n";
            resultado += sistema.ativarAquaSave(recurso);
            resultado += sistema.ativarSignalLock(comunicacao);
            resultado += sistema.ativarResourceLock(recurso);
            resultado += sistema.ativarEmergencyMode(risco);
            resultado += "\n";

            HistoricoEvento historico = new HistoricoEvento("Analise realizada pelo sistema AETHER.");
            resultado += historico.registrarEvento();

            taResultado.setText(resultado);

        } catch (Exception erro) {
            JOptionPane.showMessageDialog(null,
                    "Preencha todos os campos corretamente usando apenas números.",
                    "Erro",
                    JOptionPane.ERROR_MESSAGE);
        }
    }

    private void limparCampos() {
        tfTemperatura.setText("");
        tfUmidade.setText("");
        tfAgua.setText("");
        tfEnergia.setText("");
        tfAlimentos.setText("");
        cbComunicacao.setSelectedIndex(0);
        taResultado.setText("");
    }
}